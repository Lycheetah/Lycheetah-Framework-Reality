#!/usr/bin/env python3
"""Packet 05 cascade toy smoke — domain-neutral in-memory only.

Reproduces the sealed Packet 05 expectation:
  n_blocks_after=3, still_has_axiom=true, foundations=[axiom_a, claim_b], qualified=[]
Does not run germ/quantum/medical narratives or claim scientific discovery.
"""
from __future__ import annotations
import json
from cascade_engine import CascadeEngine, KnowledgeBlock


def main() -> None:
    eng = CascadeEngine()
    empty = {
        "n_blocks": len(eng.blocks),
        "foundations": len(eng.foundations()),
        "qualified": len(eng.qualified_blocks()),
    }
    blocks = [
        KnowledgeBlock(
            id="axiom_a",
            content="Axiom A holds in the toy domain.",
            domain="toy",
            paradigm="base",
            evidence_strength=0.9,
            explanatory_power=2.0,
            uncertainty=0.2,
        ),
        KnowledgeBlock(
            id="claim_b",
            content="Claim B is well supported.",
            domain="toy",
            paradigm="base",
            evidence_strength=0.85,
            explanatory_power=2.0,
            uncertainty=0.25,
        ),
        KnowledgeBlock(
            id="claim_c",
            content="Claim C is a weak edge idea.",
            domain="toy",
            paradigm="base",
            evidence_strength=0.4,
            explanatory_power=1.0,
            uncertainty=0.5,
        ),
    ]
    add_results = {}
    for block, key in zip(blocks, ("b1", "b2", "b3")):
        add_results[key] = eng.add_block(block)
    out = {
        "empty": empty,
        "add_results": add_results,
        "n_blocks_after": len(eng.blocks),
        "still_has_axiom": "axiom_a" in eng.blocks,
        "regimes": {bid: eng.blocks[bid].regime for bid in eng.blocks},
        "layers": {bid: eng.blocks[bid].layer for bid in eng.blocks},
        "foundations": [b.id for b in eng.foundations()],
        "qualified": [b.id for b in eng.qualified_blocks()],
        "evidence_boundary": "toy_only_not_scientific_discovery",
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
