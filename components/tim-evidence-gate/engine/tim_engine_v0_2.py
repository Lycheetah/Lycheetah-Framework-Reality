from __future__ import annotations

from dataclasses import dataclass, asdict, field
from enum import Enum
import hashlib
import json
import math
from typing import Any, Optional


K_B = 1.380649e-23
HBAR = 1.054571817e-34
LN2 = math.log(2.0)


class Outcome(str, Enum):
    VALID = "VALID"
    PARTIAL = "PARTIAL"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    INCONSISTENT = "INCONSISTENT"
    REJECTED = "REJECTED"


class TURProfile(str, Enum):
    NONE = "NONE"
    CLASSICAL_STEADY_MARKOV_CURRENT = "TUR_CLASSICAL_STEADY_MARKOV_CURRENT"


class LandauerProfile(str, Enum):
    NONE = "NONE"
    ERASURE_REFERENCE = "LANDAUER_ERASURE_REFERENCE"


class EnergyTimeProfile(str, Enum):
    NONE = "NONE"
    LEGACY_CONTEXT_DEPENDENT = "LEGACY_CONTEXT_DEPENDENT_ENERGY_TIME_PROFILE"


@dataclass(frozen=True)
class TIMWindowInput:
    experiment_id: str
    duration_s: float
    window_count: int
    mean_ticks_per_window: float
    variance_ticks_squared: float

    clock_entropy_j_per_k_window: float
    measurement_entropy_j_per_k_window: float
    auxiliary_entropy_j_per_k_window: float = 0.0
    unattributed_entropy_j_per_k_window: float = 0.0
    declared_total_entropy_j_per_k_window: Optional[float] = None

    information_per_tick_bits: Optional[float] = None
    erased_bits_per_window: Optional[float] = None
    measurement_erased_bits_per_window: Optional[float] = None
    erase_all_tick_information_in_window: bool = False

    temperature_k: Optional[float] = None
    energy_spread_j: Optional[float] = None

    clock_boundary: str = ""
    measurement_boundary: str = ""
    total_boundary: str = ""
    tick_definition: str = ""

    tur_profile: TURProfile = TURProfile.NONE
    landauer_profile: LandauerProfile = LandauerProfile.NONE
    energy_time_profile: EnergyTimeProfile = EnergyTimeProfile.NONE

    tur_assumptions: tuple[str, ...] = ()
    energy_time_theorem: str = ()
    assumptions: tuple[str, ...] = ()
    provenance: tuple[str, ...] = ()


def _hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


def _diag(level: Outcome, code: str, message: str) -> dict[str, str]:
    return {"level": level.value, "code": code, "message": message}


def calculate(
    data: TIMWindowInput,
    closure_relative_tolerance: float = 1e-9,
) -> dict[str, Any]:
    diagnostics: list[dict[str, str]] = []

    # Hard input checks
    if data.duration_s <= 0:
        diagnostics.append(_diag(Outcome.REJECTED, "NONPOSITIVE_WINDOW", "Observation-window duration must be positive."))
    if data.window_count < 2:
        diagnostics.append(_diag(Outcome.REJECTED, "INSUFFICIENT_WINDOWS", "At least two repeated windows are required for sample variance."))
    if data.variance_ticks_squared < 0:
        diagnostics.append(_diag(Outcome.REJECTED, "NEGATIVE_VARIANCE", "Tick-count variance cannot be negative."))
    for name, value in [
        ("clock entropy", data.clock_entropy_j_per_k_window),
        ("measurement entropy", data.measurement_entropy_j_per_k_window),
        ("auxiliary entropy", data.auxiliary_entropy_j_per_k_window),
        ("unattributed entropy", data.unattributed_entropy_j_per_k_window),
    ]:
        if value < 0:
            diagnostics.append(_diag(Outcome.REJECTED, "NEGATIVE_ENTROPY", f"{name} cannot be negative."))
    if data.temperature_k is not None and data.temperature_k <= 0:
        diagnostics.append(_diag(Outcome.REJECTED, "NONPOSITIVE_TEMPERATURE", "Temperature must be positive when supplied."))
    if data.information_per_tick_bits is not None and data.information_per_tick_bits < 0:
        diagnostics.append(_diag(Outcome.REJECTED, "NEGATIVE_INFORMATION", "Information per tick cannot be negative."))
    if data.erased_bits_per_window is not None and data.erased_bits_per_window < 0:
        diagnostics.append(_diag(Outcome.REJECTED, "NEGATIVE_ERASED_BITS", "Erased bits per window cannot be negative."))
    if data.measurement_erased_bits_per_window is not None and data.measurement_erased_bits_per_window < 0:
        diagnostics.append(_diag(Outcome.REJECTED, "NEGATIVE_MEASUREMENT_ERASED_BITS", "Measurement erased bits cannot be negative."))

    if any(d["level"] == Outcome.REJECTED.value for d in diagnostics):
        return _final(data, Outcome.REJECTED, diagnostics, {})

    component_total = (
        data.clock_entropy_j_per_k_window
        + data.measurement_entropy_j_per_k_window
        + data.auxiliary_entropy_j_per_k_window
        + data.unattributed_entropy_j_per_k_window
    )

    declared_total = data.declared_total_entropy_j_per_k_window
    closure = None
    if declared_total is not None:
        denom = max(abs(declared_total), 1e-300)
        closure = abs(declared_total - component_total) / denom
        if closure > closure_relative_tolerance:
            diagnostics.append(_diag(
                Outcome.REJECTED,
                "ENTROPY_CLOSURE_FAILURE",
                f"Declared total {declared_total:.12e} J/K differs from component sum {component_total:.12e} J/K."
            ))
            return _final(data, Outcome.REJECTED, diagnostics, {
                "declared_total_entropy_j_per_k_window": declared_total,
                "component_total_entropy_j_per_k_window": component_total,
                "closure_relative_error": closure,
            })

    total_entropy = component_total if declared_total is None else declared_total

    # Accuracy
    if data.variance_ticks_squared == 0:
        accuracy = math.inf
        diagnostics.append(_diag(
            Outcome.INCONSISTENT,
            "ZERO_VARIANCE",
            "Zero variance produces an unbounded numerical accuracy ratio."
        ))
    else:
        accuracy = data.mean_ticks_per_window ** 2 / data.variance_ticks_squared

    results: dict[str, Any] = {
        "accuracy_A_N": accuracy,
        "component_total_entropy_j_per_k_window": component_total,
        "total_entropy_j_per_k_window": total_entropy,
        "closure_relative_error": closure,
    }

    # TUR
    if data.tur_profile is TURProfile.NONE:
        results["tur"] = {
            "status": Outcome.NOT_APPLICABLE.value,
            "profile": data.tur_profile.value,
            "reason": "No TUR applicability profile declared.",
        }
    else:
        required = {
            "stationary_markov_network",
            "integrated_current",
            "local_detailed_balance",
            "same_boundary_and_window",
        }
        missing = sorted(required - set(data.tur_assumptions))
        if missing:
            results["tur"] = {
                "status": Outcome.NOT_APPLICABLE.value,
                "profile": data.tur_profile.value,
                "missing_assumptions": missing,
            }
            diagnostics.append(_diag(
                Outcome.NOT_APPLICABLE,
                "TUR_ASSUMPTIONS_MISSING",
                "TUR profile declared without all required assumptions."
            ))
        else:
            bound = total_entropy / (2.0 * K_B)
            margin = bound - accuracy
            results["tur"] = {
                "status": Outcome.VALID.value if margin >= 0 else Outcome.INCONSISTENT.value,
                "profile": data.tur_profile.value,
                "bound_dimensionless": bound,
                "margin_dimensionless": margin,
                "condition_satisfied": bool(margin >= 0),
            }
            if margin < 0:
                diagnostics.append(_diag(
                    Outcome.INCONSISTENT,
                    "TUR_PROFILE_FAILURE",
                    "The supplied values fail the selected TUR inequality."
                ))

    # Landauer
    erased_bits = data.erased_bits_per_window
    erasure_source = "explicit"
    if erased_bits is None and data.erase_all_tick_information_in_window:
        if data.information_per_tick_bits is None:
            diagnostics.append(_diag(
                Outcome.REJECTED,
                "ERASURE_ASSUMPTION_MISSING_INFORMATION",
                "Erase-all-tick-information assumption requires information_per_tick_bits."
            ))
            return _final(data, Outcome.REJECTED, diagnostics, results)
        erased_bits = data.mean_ticks_per_window * data.information_per_tick_bits
        erasure_source = "ASSUME_ERASE_ALL_TICK_INFORMATION_IN_WINDOW"

    if data.landauer_profile is LandauerProfile.NONE:
        results["landauer"] = {
            "status": Outcome.NOT_APPLICABLE.value,
            "profile": data.landauer_profile.value,
            "reason": "No Landauer erasure profile declared.",
        }
    elif erased_bits is None:
        results["landauer"] = {
            "status": Outcome.NOT_APPLICABLE.value,
            "profile": data.landauer_profile.value,
            "reason": "Erased bits per observation window are not defined.",
        }
        diagnostics.append(_diag(
            Outcome.NOT_APPLICABLE,
            "ERASED_BITS_UNDEFINED",
            "Information gained per tick is insufficient to infer irreversible erased bits."
        ))
    else:
        landauer_entropy = erased_bits * K_B * LN2
        efficiency = landauer_entropy / total_entropy if total_entropy > 0 else math.inf
        overhead = 1.0 - efficiency
        status = Outcome.VALID
        if efficiency > 1.0 + 1e-12 or overhead < -1e-12:
            status = Outcome.INCONSISTENT
            diagnostics.append(_diag(
                Outcome.INCONSISTENT,
                "LANDAUER_RATIO_OUT_OF_RANGE",
                "Landauer reference exceeds measured total entropy under the declared assumptions."
            ))

        landauer = {
            "status": status.value,
            "profile": data.landauer_profile.value,
            "erased_bits_per_window": erased_bits,
            "erasure_source": erasure_source,
            "landauer_entropy_j_per_k_window": landauer_entropy,
            "landauer_reference_ratio_E_L": efficiency,
            "landauer_reference_overhead_W_L": overhead,
            "landauer_energy_j_window": (
                data.temperature_k * landauer_entropy
                if data.temperature_k is not None else None
            ),
        }

        if data.measurement_erased_bits_per_window is None:
            landauer["measurement_factor_gamma"] = None
            landauer["measurement_factor_status"] = Outcome.NOT_APPLICABLE.value
        else:
            meas_floor = data.measurement_erased_bits_per_window * K_B * LN2
            gamma = (
                data.measurement_entropy_j_per_k_window / meas_floor
                if meas_floor > 0 else math.inf
            )
            landauer["measurement_landauer_entropy_j_per_k_window"] = meas_floor
            landauer["measurement_factor_gamma"] = gamma
            landauer["measurement_factor_status"] = (
                Outcome.VALID.value if gamma >= 1.0 - 1e-12
                else Outcome.INCONSISTENT.value
            )
            if gamma < 1.0 - 1e-12:
                diagnostics.append(_diag(
                    Outcome.INCONSISTENT,
                    "MEASUREMENT_FACTOR_BELOW_ONE",
                    "Measurement entropy falls below the declared Landauer erasure reference."
                ))
        results["landauer"] = landauer

    # eta is diagnostic if denominator exists
    if data.clock_entropy_j_per_k_window > 0:
        results["measurement_clock_ratio_eta"] = (
            data.measurement_entropy_j_per_k_window
            / data.clock_entropy_j_per_k_window
        )
    else:
        results["measurement_clock_ratio_eta"] = None
        diagnostics.append(_diag(
            Outcome.NOT_APPLICABLE,
            "ETA_CLOCK_ENTROPY_ZERO",
            "Measurement-clock ratio is undefined because clock entropy is zero."
        ))

    # Energy-time profile
    if data.energy_time_profile is EnergyTimeProfile.NONE:
        results["energy_time"] = {
            "status": Outcome.NOT_APPLICABLE.value,
            "profile": data.energy_time_profile.value,
            "reason": "No context-dependent energy-time theorem declared.",
        }
    elif data.energy_spread_j is None:
        results["energy_time"] = {
            "status": Outcome.NOT_APPLICABLE.value,
            "profile": data.energy_time_profile.value,
            "reason": "Energy spread is not supplied.",
        }
    elif not data.energy_time_theorem:
        results["energy_time"] = {
            "status": Outcome.NOT_APPLICABLE.value,
            "profile": data.energy_time_profile.value,
            "reason": "Operational theorem/meaning is not declared.",
        }
    else:
        product = data.energy_spread_j * data.duration_s
        results["energy_time"] = {
            "status": Outcome.VALID.value,
            "profile": data.energy_time_profile.value,
            "theorem": data.energy_time_theorem,
            "product_j_s": product,
            "legacy_reference_hbar_over_2_j_s": HBAR / 2.0,
            "legacy_comparison": product >= HBAR / 2.0,
            "warning": "The comparison is context-dependent and not a universal quantum-validity test.",
        }

    # Overall outcome
    levels = {d["level"] for d in diagnostics}
    if Outcome.REJECTED.value in levels:
        overall = Outcome.REJECTED
    elif Outcome.INCONSISTENT.value in levels:
        overall = Outcome.INCONSISTENT
    elif Outcome.PARTIAL.value in levels or Outcome.NOT_APPLICABLE.value in levels:
        overall = Outcome.PARTIAL
    else:
        overall = Outcome.VALID

    return _final(data, overall, diagnostics, results)


def _final(
    data: TIMWindowInput,
    outcome: Outcome,
    diagnostics: list[dict[str, str]],
    results: dict[str, Any],
) -> dict[str, Any]:
    packet = {
        "specification": "TIM v1.1",
        "engine": "TIM Engine v0.2",
        "outcome": outcome.value,
        "input": asdict(data),
        "results": results,
        "diagnostics": diagnostics,
    }
    packet["semantic_hash"] = _hash(packet)
    return packet


if __name__ == "__main__":
    sample = TIMWindowInput(
        experiment_id="TIM-V1.1-DEMO",
        duration_s=10e-6,
        window_count=50,
        mean_ticks_per_window=1000,
        variance_ticks_squared=25,
        clock_entropy_j_per_k_window=2e-21,
        measurement_entropy_j_per_k_window=8e-21,
        declared_total_entropy_j_per_k_window=1e-20,
        information_per_tick_bits=1.0,
        erased_bits_per_window=500.0,
        measurement_erased_bits_per_window=400.0,
        temperature_k=0.015,
        clock_boundary="clock mechanism",
        measurement_boundary="readout chain",
        total_boundary="clock + readout",
        tick_definition="one counted timing event",
        landauer_profile=LandauerProfile.ERASURE_REFERENCE,
        assumptions=("explicit erased-bit count supplied",),
        provenance=("synthetic demonstration",),
    )
    print(json.dumps(calculate(sample), indent=2, default=str))
