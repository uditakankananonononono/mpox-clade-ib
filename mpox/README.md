# mpox slice — Project 7

Question: which protein-level differences distinguish clade Ib from the 2022 clade IIb outbreak
strain (B.1), and do they plausibly explain spread-pattern differences?

- GATES_LOCKED.md — gates and thresholds locked before results (own commit, per fleet rule)
- code/ — 01 fixed differences, 02 polarization vs clade Ia, 03 classification, 04 protein builds
- data/ — frozen LAPIS pulls, references, SHA256SUMS.txt, MANIFEST.md (payloads checksummed)
- results/ — fixed_differences*.tsv, figures, ESMFold PDBs, structure_confidence.json
- paper/ — report (in progress)

Reproduce: `python3 code/01_fixed_differences.py && python3 code/02_polarize.py && python3 code/03_classify.py`
from the mpox/ directory; inputs are the frozen files in data/.
