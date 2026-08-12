<!--
Lycheetah-Framework-Reality extraction header
action: COPY_WITH_HEADER_ONLY
owner_component: lamague.public_core_validator
source_repository: github:Lycheetah/Lamague-Public@main
immutable_ref: 56c4a7d25b4d29373bd224211848ae6a02ed59bb
source_path: spec/PUBLIC_CORE_SPECIFICATION_v1.0.md
source_sha256: 3b003aa03483eddbcae4467de7cc1a49780e2cacfdc3f2fe1077f4953bfe776f
maturity: BOUNDED_TOOL
note: Upstream body preserved below this header. Header does not change technical claims.
-->
# LAMAGUE Public Core v1.0

## Status

Bounded public research subset.

This is not the complete LAMAGUE language or symbol registry.

## Grammar

```text
expression  = operation, { arrow, operation } ;
arrow       = "->" | "→" ;
operation   = "O" | "E" | "U" | "I" | "G" | "V" | "F" | "Y" | "Z" ;
```

Typed unknowns may be written:

```text
U<cause>
U<consent>
U<recurrence>
```

## Canonical packet

A public-core expression operates over a semantic packet containing:

```text
purpose
claim
evidence
unknowns
invariants
authority
participants
affected_parties
boundaries
dissent
value_flow
consequences
recovery
provenance
risk
irreversibility
decoder_confidence
```

## Constitutional constraints

### Law One

No compression without recovery.

`Z` must expand rather than compress when a protected field would be lost.

### Law Two

No consequential meaning without visible authority.

A transition affecting another person, resource, right, system, or future state must expose its authority.

### Law Three

No transformation may erase protected uncertainty.

An unknown may:

- remain unresolved;
- be resolved through visible evidence;
- produce a visible fork.

It may not disappear because a decoder, summary, or operator prefers closure.

## Minimal safe sequence

```text
O → E → U → I → G → F → Y
```

Observe.

Attach evidence.

Preserve unknowns.

Declare invariants.

Guard authority and boundaries.

Fold the result into memory.

Yield a bounded output.

## Correction sequence

```text
O → E → U → I → G → V → F → Y
```

The `V` operation generates a new route while preserving legitimate intent and protected constraints.

## Compression sequence

```text
O → E → U → I → G → Z → F → Y
```

`Z` is not automatically compression.

It is a decision point:

```text
safe shared context → compress
uncertain protected meaning → expand
insufficient information → hold
```
