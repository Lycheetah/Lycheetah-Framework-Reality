from pathlib import Path
import math
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from tim_engine_v0_2 import (
    TIMWindowInput, TURProfile, LandauerProfile, EnergyTimeProfile,
    calculate, K_B, LN2
)


def base(**changes):
    values = dict(
        experiment_id="T",
        duration_s=1e-5,
        window_count=50,
        mean_ticks_per_window=1000,
        variance_ticks_squared=25,
        clock_entropy_j_per_k_window=2e-21,
        measurement_entropy_j_per_k_window=8e-21,
        declared_total_entropy_j_per_k_window=1e-20,
        clock_boundary="clock",
        measurement_boundary="measurement",
        total_boundary="clock + measurement",
        tick_definition="tick",
    )
    values.update(changes)
    return TIMWindowInput(**values)


class TIMV11Tests(unittest.TestCase):
    def test_accuracy(self):
        self.assertEqual(calculate(base())["results"]["accuracy_A_N"], 40000)

    def test_entropy_closure(self):
        r = calculate(base())
        self.assertAlmostEqual(r["results"]["component_total_entropy_j_per_k_window"], 1e-20)

    def test_entropy_contradiction_rejected(self):
        r = calculate(base(declared_total_entropy_j_per_k_window=9e-21))
        self.assertEqual(r["outcome"], "REJECTED")
        self.assertTrue(any(d["code"] == "ENTROPY_CLOSURE_FAILURE" for d in r["diagnostics"]))

    def test_landauer_not_inferred_from_i_tick(self):
        r = calculate(base(
            information_per_tick_bits=1.0,
            landauer_profile=LandauerProfile.ERASURE_REFERENCE,
        ))
        self.assertEqual(r["results"]["landauer"]["status"], "NOT_APPLICABLE")

    def test_explicit_erased_bits(self):
        r = calculate(base(
            erased_bits_per_window=500,
            landauer_profile=LandauerProfile.ERASURE_REFERENCE,
        ))
        expected = 500 * K_B * LN2
        self.assertAlmostEqual(r["results"]["landauer"]["landauer_entropy_j_per_k_window"], expected)

    def test_named_erase_all_assumption(self):
        r = calculate(base(
            information_per_tick_bits=1,
            erase_all_tick_information_in_window=True,
            landauer_profile=LandauerProfile.ERASURE_REFERENCE,
        ))
        self.assertEqual(r["results"]["landauer"]["erased_bits_per_window"], 1000)
        self.assertEqual(
            r["results"]["landauer"]["erasure_source"],
            "ASSUME_ERASE_ALL_TICK_INFORMATION_IN_WINDOW"
        )

    def test_efficiency_above_one_is_inconsistent(self):
        r = calculate(base(
            erased_bits_per_window=2000,
            landauer_profile=LandauerProfile.ERASURE_REFERENCE,
        ))
        self.assertEqual(r["outcome"], "INCONSISTENT")

    def test_gamma_requires_measurement_erased_bits(self):
        r = calculate(base(
            erased_bits_per_window=500,
            landauer_profile=LandauerProfile.ERASURE_REFERENCE,
        ))
        self.assertIsNone(r["results"]["landauer"]["measurement_factor_gamma"])

    def test_eta_is_diagnostic(self):
        r = calculate(base())
        self.assertEqual(r["results"]["measurement_clock_ratio_eta"], 4)

    def test_tur_not_default(self):
        r = calculate(base())
        self.assertEqual(r["results"]["tur"]["status"], "NOT_APPLICABLE")

    def test_tur_missing_assumptions(self):
        r = calculate(base(tur_profile=TURProfile.CLASSICAL_STEADY_MARKOV_CURRENT))
        self.assertEqual(r["results"]["tur"]["status"], "NOT_APPLICABLE")

    def test_tur_profile_calculates(self):
        r = calculate(base(
            tur_profile=TURProfile.CLASSICAL_STEADY_MARKOV_CURRENT,
            tur_assumptions=(
                "stationary_markov_network",
                "integrated_current",
                "local_detailed_balance",
                "same_boundary_and_window",
            )
        ))
        self.assertFalse(r["results"]["tur"]["condition_satisfied"])

    def test_energy_time_not_default(self):
        r = calculate(base(energy_spread_j=6e-29))
        self.assertEqual(r["results"]["energy_time"]["status"], "NOT_APPLICABLE")

    def test_energy_time_requires_theorem(self):
        r = calculate(base(
            energy_spread_j=6e-29,
            energy_time_profile=EnergyTimeProfile.LEGACY_CONTEXT_DEPENDENT,
        ))
        self.assertEqual(r["results"]["energy_time"]["status"], "NOT_APPLICABLE")

    def test_energy_time_with_theorem(self):
        r = calculate(base(
            energy_spread_j=6e-29,
            energy_time_profile=EnergyTimeProfile.LEGACY_CONTEXT_DEPENDENT,
            energy_time_theorem="declared synthetic legacy comparison",
        ))
        self.assertEqual(r["results"]["energy_time"]["status"], "VALID")

    def test_negative_entropy_rejected(self):
        r = calculate(base(clock_entropy_j_per_k_window=-1))
        self.assertEqual(r["outcome"], "REJECTED")

    def test_hash_is_deterministic(self):
        a = calculate(base())
        b = calculate(base())
        self.assertEqual(a["semantic_hash"], b["semantic_hash"])


if __name__ == "__main__":
    unittest.main()
