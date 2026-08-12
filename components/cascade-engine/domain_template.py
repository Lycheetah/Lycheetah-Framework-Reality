"""
Domain Dataset Template
========================

Copy this file, rename it domain_YOUR_DOMAIN.py, and fill in the blocks
and fidelity checks for your paradigm shift.

Steps:
  1. Define knowledge blocks (old paradigm first, then new paradigm, chronological)
  2. Assign evidence scores honestly (see scoring guide below)
  3. Write fidelity checks (what should the final structure look like?)
  4. Import in run_experiments.py

Evidence Scoring Guide:
  evidence_strength (E ∈ [0,1]):
    0.3-0.5  = Observational/anecdotal, limited replication
    0.5-0.7  = Systematic observation, some controlled studies
    0.7-0.85 = Well-replicated experiments, multiple independent confirmations
    0.85-0.95 = Gold-standard experiments, Nobel-caliber work
    0.95-0.99 = Near-universal replication, textbook-level certainty
    
  explanatory_power (P ∈ [1,3]):
    1.0-1.5 = Explains one narrow phenomenon
    1.5-2.0 = Explains a class of related phenomena
    2.0-2.5 = Explains phenomena across multiple subdomains
    2.5-3.0 = Unifying framework for an entire field
    
  uncertainty (S ∈ (0,1]):
    0.05-0.15 = Very low uncertainty (strong consensus)
    0.15-0.30 = Low uncertainty (well-established, minor open questions)
    0.30-0.50 = Moderate uncertainty (evidence accumulating, debate ongoing)
    0.50-0.70 = High uncertainty (limited evidence, significant debate)
    0.70-0.90 = Very high uncertainty (preliminary, speculative)

IMPORTANT: State your scoring rationale in the 'note' field.
These are judgment calls, not measurements. Honesty about that
is what separates real science from hype.
"""

from cascade_engine import KnowledgeBlock, DomainExperiment, CascadeEngine
from typing import List, Tuple


def build_blocks() -> List[KnowledgeBlock]:
    blocks = []
    
    # ── OLD PARADIGM ──
    
    blocks.append(KnowledgeBlock(
        id="OLD_1_example",
        content="Description of old paradigm claim",
        domain="your_domain_label",       # Used for contradiction matching
        paradigm="old_paradigm_name",
        year=1800,
        evidence_strength=0.65,
        explanatory_power=1.8,
        uncertainty=0.50,
        key_figure="Who established this",
        note="Why you scored it this way",
    ))
    
    # ── NEW PARADIGM ──
    
    blocks.append(KnowledgeBlock(
        id="NEW_1_example",
        content="Description of new paradigm claim",
        domain="your_domain_label",       # Same domain as the old claim it challenges
        paradigm="new_paradigm_name",
        year=1900,
        evidence_strength=0.90,
        explanatory_power=2.5,
        uncertainty=0.12,
        key_figure="Who established this",
        note="Why you scored it this way",
    ))
    
    return blocks


def build_fidelity_checks():
    """
    What should the final structure look like?
    Each check is a function (engine) -> (bool, description_string)
    """
    
    def check_example(engine: CascadeEngine) -> Tuple[bool, str]:
        # Example: check that old paradigm is contextualized
        old = engine.blocks.get("OLD_1_example")
        if not old:
            return False, "Old block not found"
        ok = old.regime == "qualified"
        return ok, f"Old paradigm contextualized: {ok}"
    
    return [check_example]


def create_experiment() -> DomainExperiment:
    return DomainExperiment(
        domain_name="Your Domain Name (dates)",
        blocks=build_blocks(),
        old_paradigm="old_paradigm_name",
        new_paradigm="new_paradigm_name",
        fidelity_checks=build_fidelity_checks(),
    )
