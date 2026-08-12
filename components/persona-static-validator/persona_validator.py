#!/usr/bin/env python3
"""
Persona YAML Static Lint (public extraction)
Lycheetah Foundation | AURA Protocol lineage

Static check only: 7 rules, 12 violation types across 4 severity tiers.
This public extraction intentionally excludes the source-lineage dynamic
LLM-as-judge mode (unwitnessed for the admitted static claim surface).

This tool does NOT measure model alignment, safety, or fitness for deployment.
A static_pass result means only that the YAML satisfied the seven static
heuristics in this file.

Usage:
  python3 persona_validator.py persona.yaml
  python3 persona_validator.py persona.yaml --output report.json
  python3 persona_validator.py persona.yaml --json-only
"""

import yaml
import json
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


# ─── STATIC RULE CHECKERS ────────────────────────────────────────────────────

def check_rule_001(persona: dict) -> list:
    """RULE_001 — IDENTITY_DECLARATION: name, role, core_values[], boundaries[] required."""
    violations = []
    meta = persona.get("meta", {})
    identity = persona.get("identity", {})

    missing = []
    if not meta.get("name"):
        missing.append("meta.name")
    if not identity.get("role"):
        missing.append("identity.role")
    if not identity.get("core_values"):
        missing.append("identity.core_values")
    if not persona.get("boundaries"):
        missing.append("boundaries")

    if missing:
        violations.append({
            "rule": "RULE_001",
            "violation_code": "VIOLATION_C1",
            "tier": "critical",
            "message": f"IDENTITY_VOID — Missing required fields: {', '.join(missing)}"
        })

    return violations


def check_rule_002(persona: dict) -> list:
    """RULE_002 — VALUE_CONSISTENCY: core_values must be non-contradictory."""
    violations = []
    identity = persona.get("identity", {})
    core_values = identity.get("core_values", [])

    if not core_values:
        return violations

    # Structural contradiction heuristic — English-string pairs only
    negation_pairs = [
        ("honesty", "deceiv"),
        ("honest", "manipulat"),
        ("transparent", "conceal"),
        ("truth", "lie"),
        ("refuse", "always comply"),
        ("decline", "unconditional obedience"),
        ("epistemic", "confabulate"),
    ]

    values_lower = [v.lower() for v in core_values]

    for pos, neg in negation_pairs:
        has_pos = any(pos in v for v in values_lower)
        has_neg = any(neg in v for v in values_lower)
        if has_pos and has_neg:
            violations.append({
                "rule": "RULE_002",
                "violation_code": "VIOLATION_C3",
                "tier": "critical",
                "message": f"VALUE_CONTRADICTION — core_values contain contradictory principles: '{pos}' vs '{neg}'"
            })

    return violations


def check_rule_003(persona: dict) -> list:
    """RULE_003 — BOUNDARY_SPECIFICITY: each boundary needs what, condition, redirect."""
    violations = []
    boundaries = persona.get("boundaries", [])

    # Type guard: plausible first-author shapes (list of strings, bare scalar, mapping)
    # must yield a named violation, never an AttributeError traceback.
    if boundaries is None:
        boundaries = []
    if not isinstance(boundaries, list):
        violations.append({
            "rule": "RULE_003",
            "violation_code": "VIOLATION_H_BOUNDARY_MALFORMED",
            "tier": "high",
            "message": (
                "BOUNDARY_MALFORMED — boundaries must be a list of mappings "
                f"with id/what/condition/redirect; got {type(boundaries).__name__}"
            ),
        })
        return violations

    weak_redirect_phrases = [
        "try to help", "help differently", "do my best",
        "i'll see", "i will try", "maybe i can"
    ]

    for i, b in enumerate(boundaries):
        if not isinstance(b, dict):
            violations.append({
                "rule": "RULE_003",
                "violation_code": "VIOLATION_H_BOUNDARY_MALFORMED",
                "tier": "high",
                "message": (
                    f"BOUNDARY_MALFORMED — boundaries[{i}] must be a mapping with "
                    f"id/what/condition/redirect fields; got {type(b).__name__}"
                ),
            })
            continue

        bid = b.get("id", "unknown")
        missing = []

        if not b.get("what"):
            missing.append("what")
        if not b.get("condition"):
            missing.append("condition")
        if not b.get("redirect"):
            missing.append("redirect")

        if missing:
            violations.append({
                "rule": "RULE_003",
                "violation_code": "VIOLATION_H1",
                "tier": "high",
                "message": f"BOUNDARY_VAGUE — Boundary {bid} missing required fields: {', '.join(missing)}"
            })
        elif any(w in b.get("redirect", "").lower() for w in weak_redirect_phrases):
            violations.append({
                "rule": "RULE_003",
                "violation_code": "VIOLATION_L2",
                "tier": "low",
                "message": f"REDIRECT_WEAK — Boundary {bid} redirect is vague: '{b.get('redirect')}'"
            })

    if len(boundaries) < 3:
        violations.append({
            "rule": "RULE_003",
            "violation_code": "VIOLATION_M1",
            "tier": "medium",
            "message": f"BOUNDARY_INCOMPLETE — {len(boundaries)} boundary declared (minimum 3 for adversarial environments)"
        })

    return violations


def check_rule_004(persona: dict) -> list:
    """RULE_004 — SOVEREIGNTY_DECLARATION: must assert right to refuse, not unconditional compliance."""
    violations = []
    identity = persona.get("identity", {})
    sovereignty = identity.get("sovereignty_statement", "")

    if not sovereignty:
        violations.append({
            "rule": "RULE_004",
            "violation_code": "VIOLATION_C2",
            "tier": "critical",
            "message": "SOVEREIGNTY_ABSENT — No sovereignty_statement declared"
        })
        return violations

    sov_lower = sovereignty.lower()

    compliance_phrases = [
        "always comply", "will always follow", "unconditional",
        "never refuse", "must obey", "cannot refuse", "always obey"
    ]
    for phrase in compliance_phrases:
        if phrase in sov_lower:
            violations.append({
                "rule": "RULE_004",
                "violation_code": "VIOLATION_C2",
                "tier": "critical",
                "message": f"SOVEREIGNTY_ABSENT — sovereignty_statement contains unconditional compliance language: '{phrase}'"
            })

    hedged_phrases = ["may sometimes", "might decline", "could refuse", "possibly decline"]
    for phrase in hedged_phrases:
        if phrase in sov_lower:
            violations.append({
                "rule": "RULE_004",
                "violation_code": "VIOLATION_L3",
                "tier": "low",
                "message": f"SOVEREIGNTY_WEAK — sovereignty_statement uses hedged language: '{phrase}'"
            })

    return violations


def check_rule_005(persona: dict) -> list:
    """RULE_005 — PRESSURE_RESPONSE_PROTOCOL: three sub-fields required, must be distinct."""
    violations = []
    pressure = persona.get("pressure_response", {})

    if not pressure:
        violations.append({
            "rule": "RULE_005",
            "violation_code": "VIOLATION_H2",
            "tier": "high",
            "message": "PRESSURE_PROTOCOL_INCOMPLETE — No pressure_response object declared"
        })
        return violations

    required_sub = [
        "identity_attack_response",
        "value_override_attempt_response",
        "escalation_response"
    ]

    missing = [f for f in required_sub if not pressure.get(f)]
    if missing:
        violations.append({
            "rule": "RULE_005",
            "violation_code": "VIOLATION_H2",
            "tier": "high",
            "message": f"PRESSURE_PROTOCOL_INCOMPLETE — Missing sub-fields: {', '.join(missing)}"
        })

    # Check for generic (identical) responses
    responses = [str(pressure.get(f, "")).strip() for f in required_sub if pressure.get(f)]
    if len(responses) == 3 and len(set(responses)) < len(responses):
        violations.append({
            "rule": "RULE_005",
            "violation_code": "VIOLATION_M3",
            "tier": "medium",
            "message": "PRESSURE_RESPONSE_GENERIC — Two or more pressure_response sub-fields are identical"
        })

    return violations


def check_rule_006(persona: dict) -> list:
    """RULE_006 — EPISTEMIC_HONESTY_DECLARATION: epistemic_stance required."""
    violations = []
    epistemic = persona.get("epistemic_stance", "")

    if not epistemic:
        violations.append({
            "rule": "RULE_006",
            "violation_code": "VIOLATION_H3",
            "tier": "high",
            "message": "EPISTEMIC_ABSENT — No epistemic_stance declared"
        })

    return violations


def check_rule_007(persona: dict) -> list:
    """RULE_007 — VERSION_AND_LINEAGE: version, created_at, author required in meta."""
    violations = []
    meta = persona.get("meta", {})

    missing = []
    if not meta.get("version"):
        missing.append("version")
    if not meta.get("created_at"):
        missing.append("created_at")
    if not meta.get("author"):
        missing.append("author")

    if missing:
        violations.append({
            "rule": "RULE_007",
            "violation_code": "VIOLATION_L1",
            "tier": "low",
            "message": f"VERSION_MISSING — Missing lineage fields: {', '.join(missing)}"
        })

    return violations


# ─── STATIC VALIDATOR ────────────────────────────────────────────────────────

RULE_CHECKERS = [
    check_rule_001,
    check_rule_002,
    check_rule_003,
    check_rule_004,
    check_rule_005,
    check_rule_006,
    check_rule_007,
]

TIER_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}

STATIC_SCOPE_NOTICE = (
    "Static YAML lint only. Not deployment approval, safety certification, "
    "or model-alignment evidence."
)


def run_static_check(persona: dict) -> dict:
    all_violations = []
    for checker in RULE_CHECKERS:
        all_violations.extend(checker(persona))

    all_violations.sort(key=lambda v: TIER_ORDER.get(v["tier"], 99))

    counts = {
        "critical": len([v for v in all_violations if v["tier"] == "critical"]),
        "high":     len([v for v in all_violations if v["tier"] == "high"]),
        "medium":   len([v for v in all_violations if v["tier"] == "medium"]),
        "low":      len([v for v in all_violations if v["tier"] == "low"]),
    }

    rules_with_violations = len({v["rule"] for v in all_violations})

    return {
        "passed": counts["critical"] == 0 and counts["high"] == 0,
        "violations": all_violations,
        "rules_checked": 7,
        "rules_passed": 7 - rules_with_violations,
        "violation_counts": counts,
    }


# ─── VERDICT LOGIC (static only; non-authoritative tokens) ───────────────────

def determine_static_result(static_check: dict) -> tuple[str, str]:
    """Return (result_token, explanation). Tokens are non-authoritative lint states."""
    counts = static_check["violation_counts"]

    if counts["critical"] > 0:
        return "static_fail_critical", (
            f"Critical static-lint violations present ({counts['critical']}). "
            f"{STATIC_SCOPE_NOTICE}"
        )

    if counts["high"] > 0:
        return "static_fail_high", (
            f"High-tier static-lint violations present ({counts['high']}). "
            f"{STATIC_SCOPE_NOTICE}"
        )

    return "static_pass", (
        "STATIC LINT PASSED — YAML satisfied the seven static heuristics. "
        f"{STATIC_SCOPE_NOTICE}"
    )


# ─── REPORT ──────────────────────────────────────────────────────────────────

def generate_report(
    persona_path: Path,
    persona: dict,
    static_check: dict,
) -> dict:
    meta = persona.get("meta", {})
    result, explanation = determine_static_result(static_check)

    return {
        "validation_id": f"ppv-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
        "persona_name": meta.get("name", "unknown"),
        "persona_version": meta.get("version", "unknown"),
        "persona_file": str(persona_path),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": "static_only",
        "static_check": static_check,
        "static_result": result,
        "result_explanation": explanation,
        "scope_notice": STATIC_SCOPE_NOTICE,
        "not_claims": [
            "deployment_approval",
            "safety_certification",
            "model_alignment_evidence",
            "ethics_approval",
            "production_readiness",
        ],
    }


# ─── HUMAN-READABLE OUTPUT ───────────────────────────────────────────────────

C = {
    "critical": "\033[91m",
    "high":     "\033[93m",
    "medium":   "\033[94m",
    "low":      "\033[37m",
    "green":    "\033[92m",
    "bold":     "\033[1m",
    "reset":    "\033[0m",
}


def col(key: str, text: str) -> str:
    return f"{C.get(key, '')}{text}{C['reset']}"


def print_summary(report: dict) -> None:
    print()
    print(col("bold", "═" * 62))
    print(col("bold", "  PERSONA YAML STATIC LINT"))
    print(col("bold", "  Lycheetah Foundation | static extraction (no dynamic mode)"))
    print(col("bold", "═" * 62))
    print(f"  Persona :  {report['persona_name']} v{report['persona_version']}")
    print(f"  Run ID  :  {report['validation_id']}")
    print(f"  File    :  {report['persona_file']}")
    print(f"  Mode    :  static_only")
    print()

    sc = report["static_check"]
    print(col("bold", "── STATIC CHECK ─────────────────────────────────────────────"))
    print(f"  Rules checked : {sc['rules_checked']}")
    print(f"  Rules passed  : {sc['rules_passed']}")

    vc = sc["violation_counts"]
    counts_str = []
    if vc["critical"]: counts_str.append(col("critical", f"{vc['critical']} critical"))
    if vc["high"]:     counts_str.append(col("high",     f"{vc['high']} high"))
    if vc["medium"]:   counts_str.append(col("medium",   f"{vc['medium']} medium"))
    if vc["low"]:      counts_str.append(col("low",      f"{vc['low']} low"))

    if counts_str:
        print(f"  Violations    : {', '.join(counts_str)}")
    else:
        print(f"  Violations    : {col('green', 'none')}")

    if sc["violations"]:
        print()
        for v in sc["violations"]:
            tier = v["tier"]
            print(f"  {col(tier, f'[{tier.upper():8}]')}  {v['violation_code']}")
            print(f"              {v['message']}")

    print()
    print(col("bold", "── RESULT ───────────────────────────────────────────────────"))
    result = report["static_result"]
    expl = report["result_explanation"]
    if result == "static_pass":
        print(f"  {col('green', '✓  STATIC LINT PASSED')}")
    elif result == "static_fail_high":
        print(f"  {col('high',  '⚠  STATIC LINT FAILED (high)')}")
    else:
        print(f"  {col('critical', '✗  STATIC LINT FAILED (critical)')}")
    print(f"  {expl}")
    print()
    print(col("bold", "  SCOPE"))
    print(f"  {STATIC_SCOPE_NOTICE}")
    print(col("bold", "═" * 62))
    print()


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Persona YAML Static Lint — Lycheetah Foundation. "
            "Seven static heuristics only; not deployment approval, safety "
            "certification, or model-alignment evidence."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python3 persona_validator.py sol_persona.yaml
  python3 persona_validator.py sol_persona.yaml --output report.json
  python3 persona_validator.py sol_persona.yaml --json-only

This public extraction has no dynamic / LLM / API mode.
        """,
    )
    parser.add_argument("persona_file", help="Path to persona YAML file")
    parser.add_argument("--output", help="Write full JSON report to this file")
    parser.add_argument("--json-only", action="store_true",
                        help="Suppress human summary, print JSON only")
    args = parser.parse_args()

    persona_path = Path(args.persona_file)
    if not persona_path.exists():
        print(f"Error: file not found — {persona_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(persona_path, "r", encoding="utf-8") as f:
            persona = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Error: invalid YAML — {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(persona, dict):
        print("Error: persona file must be a YAML mapping object", file=sys.stderr)
        sys.exit(1)

    try:
        static_check = run_static_check(persona)
    except Exception as e:
        # Shape/type defects should already be violations; any residual crash
        # becomes a clean parse/shape error with exit 1 (no traceback).
        print(f"Error: persona shape/validation failure — {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)

    report = generate_report(persona_path, persona, static_check)

    if not args.json_only:
        print_summary(report)

    if args.output:
        out_path = Path(args.output)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        if not args.json_only:
            print(f"Report saved: {out_path}", file=sys.stderr)

    if args.json_only:
        print(json.dumps(report, indent=2))

    # Exit code: 0 = static_pass; 1 = any static fail (critical or high)
    sys.exit(0 if report["static_result"] == "static_pass" else 1)


if __name__ == "__main__":
    main()
