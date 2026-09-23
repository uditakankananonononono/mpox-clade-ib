# Data byte-lock manifest - Project 7 (mpox-clade-ib), frozen 2026-09-23

## Primary source: Pathoplexus LAPIS (open data, INSDC ingest)
- Instance: https://lapis.pathoplexus.org/mpox  dataVersion: 1790097064 (queried 2026-09-23 ~08:02 UTC)
- Frozen pulls (exact queries):
  1. data/ib_aamuts.json   <- /sample/aminoAcidMutations?clade=Ib&completenessFrom=0.95&limit=100000        (set n=377 genomes)
  2. data/iib_aamuts.json  <- /sample/aminoAcidMutations?clade=IIb&lineage=B.1&completenessFrom=0.95&limit=100000 (set n=3578)
  3. data/ia_aamuts.json   <- /sample/aminoAcidMutations?clade=Ia&completenessFrom=0.95&limit=100000        (set n=511)
  4. data/iib_ntmuts.json  <- /sample/nucleotideMutations?clade=IIb&lineage=B.1&completenessFrom=0.95&limit=100000
  5. data/ib_ntmuts.json   <- /sample/nucleotideMutations?clade=Ib&completenessFrom=0.95&limit=100000
- LAPIS alignment reference: NC_063383.1 (MPXV clade IIb, 2018); mutations are aggregated counts/proportions vs that reference.
- QC-set accession lists (documentation): data/qc_sets.json (Ib n=319 with INSDC accessions, IIbB1 n=3577, Ia n=430).

## Reference sequences (NCBI efetch, 2026-09-23)
- data/NC_063383.fasta / NC_063383.gb  (clade IIb reference, gene table parsed to data/gene_table_iib_ref.json)
- data/NC_003310.fasta / NC_003310.gb  (clade Ia reference Zaire-96-I-16; CCP = OPG032, 651 nt)
- data/CCP_cladeIa_gene.fasta (extracted CCP gene used as positive-control probe)

## Raw-genome validation subset (NCBI efetch, 2026-09-23)
- 45 complete genomes: 25 clade Ib, 10 clade Ia, 10 clade IIb B.1 (accessions in results/raw_subset45_accessions.txt)

Checksums of every frozen payload: data/SHA256SUMS.txt (covers payloads, not inventories).
