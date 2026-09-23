# GATES_LOCKED.md — Project 7 (mpox-clade-ib)
Locked 2026-09-23, before any outcome data was examined. Signed-off criteria below are the ones all
results in this slice are judged against.

## Question
Which protein-level differences distinguish mpox clade Ib from the 2022 clade IIb outbreak strain
(lineage B.1), and do they plausibly explain spread-pattern differences?

## Specific contribution (vs closest published work)
Proteome-wide fixed-difference STRUCTURAL ATLAS, clade Ib vs clade IIb B.1: every fixed amino-acid
difference between frozen clade consensus proteomes, polarized with clade Ia outgroup, mapped onto
protein models with per-residue confidence filtering, classified surface/immune/replication/unknown,
plus APOBEC3-signature comparison. Closest works (none do this):
1. bioRxiv 10.1101/2024.09.24.614696 — nucleotide-level clade comparison (CCP deletion, B22R).
2. Molecules 2026, 10.3390/molecules31091466 — single-mutation EFC structural study (G9 M142I).
3. Microbiol Spectrum 2023, 10.1128/spectrum.02315-23 — clade IIb consensus proteome only.

## Data (frozen)
Pathoplexus LAPIS mpox instance, dataVersion 1790097064, pulled 2026-09-23.
Sets (completeness >= 0.95): clade Ib n=377; clade IIb B.1 n=3578; clade Ia outgroup n=511.
References NC_063383.1 (IIb), NC_003310.1 (Ia). 45 raw genomes for independent validation.
Checksums: data/SHA256SUMS.txt; sources and exact query URLs: data/MANIFEST.md.

## Gates
- G1 Reproducibility: fixed-difference list regenerates byte-identically from the frozen manifest;
  two independent runs must match.
- G2 Positive controls BEFORE any novel claim:
  (a) pipeline detects the published complement-control-protein (CCP, OPG032) loss in clade Ib
      raw genomes; (b) pipeline reproduces published APOBEC3 enrichment (TC->TT / GA->AA excess)
      in IIb B.1 substitutions. RESULT: both PASS (25/25 Ib CCP-deleted; 35.3% vs 2.1% null).
- G3 Structural confidence: structural claims only where a residue sits in PDB experimental
  coverage or model pLDDT >= 70; every mapped residue carries its confidence; below-cutoff
  positions are reported as sequence-level only. Structure work limited to selected targets
  (ESMFold, <=400 aa proteins), not hundreds of large structures.
- G4 Classification completeness: 100% of fixed nonsynonymous differences classified
  surface-exposed / immune / replication-assembly / unknown; non-unknown calls require a stated
  rule or citation; unverifiable -> unknown, honestly counted.
- G5 No fishing: gates locked before outcome inspection; negatives preserved as boundaries.
- G6 Honest counts: every report carries verified / thin / missing counts.

## Locked analysis thresholds
- Fixed difference: dominant-residue proportion >= 0.95 in BOTH clade sets; coverage >= 100 (Ib)
  and >= 1500 (IIb B.1) sequences at the position; deletions count as residue differences.
- Polarization vs Ia outgroup requires Ia dominant proportion >= 0.95, coverage >= 100.
- Classification: locked keyword rule order in code/03_classify.py + 3 curated overrides
  (OPG123 NPH-I, OPG125 rif-resistance, OPG098 VP8/L4R -> replication-assembly), criteria recorded.
