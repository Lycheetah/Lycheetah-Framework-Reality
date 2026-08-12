# Conversation drift heuristic scorer (experimental)

**Maturity:** `EXPERIMENT`  
**Component ID:** `framework_main.drift_scorer`  
**Claim:** `CLM-DRF-001`

## Problem

Analysts want a small pure-function helper that visualizes rough turn-by-turn shift
in a conversation using simple text features, without claiming calibrated ethics
measurement.

## Input / output

- **Input:** list of `{prompt, response}` turns
- **Output:** turn history with SA/VA/IS/EI channels, drift, velocity, alert labels
- **API:** `from drift_scorer import score_conversation`

## Quickstart

```bash
python3 -c "from drift_scorer import score_conversation; print(score_conversation([{'prompt':'What is 2+2?','response':'I value honesty, care, and careful reasoning.'},{'prompt':'What is 2+2?','response':'I value honesty, care, and careful reasoning.'}]))"
```

## Measured behavior (Packet 05)

| Probe | Result |
|---|---|
| Identical consecutive turns | velocity **0.0** on turn 2 |
| Absolute peak drift (same probe) | ~0.4875 (`warning`) because SA=0.0 on short non-overlapping pairs |
| Determinism | scores match across fresh copies |

## Limits

- Channel names SA/VA/IS/EI are **design labels**, not calibrated alignment/ethics/identity measures
- High absolute drift on short “good” text is expected under token Jaccard SA=0
- Tiny lexical edits may not move scores
- UI visualizer / server are **excluded** from this tree

## Next external witness

Document absolute-score sensitivity; optional unit tests; no calibration claim without
an external labelled corpus.
