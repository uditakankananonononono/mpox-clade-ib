#!/usr/bin/env python3
"""Project 7 - mpox-clade-ib: fixed amino-acid differences between clade Ib and clade IIb lineage B.1.

Inputs are FROZEN LAPIS aggregated mutation pulls (data/*.json) + reference gene table.
Locked criteria (set 2026-09-23 before outcome inspection):
  - coverage_ib >= 100 sequences, coverage_iib >= 1500 sequences at the position
  - dominant residue proportion >= 0.95 in BOTH sets
  - positions absent from a set's mutation list are assigned the reference residue
    (LAPIS returns mutations with proportion >= 0.05, so absence => ref at >0.95)
  - deletions (mutationTo '-') count as residue differences
Output: results/fixed_differences.tsv
"""
import json, csv, sys

IB = json.load(open('data/ib_aamuts.json'))['data']
IIB = json.load(open('data/iib_aamuts.json'))['data']
GENES = {g['gene']: g for g in json.load(open('data/gene_table_iib_ref.json'))}

def dominant(rows):
    """group rows by (gene,pos) -> dict of residue->row with max proportion"""
    out = {}
    for r in rows:
        key = (r['sequenceName'], r['position'])
        res = r['mutationTo']
        if key not in out:
            out[key] = {'ref': r['mutationFrom'], 'alts': {}}
        out[key]['alts'][res] = r
    return out

ib = dominant(IB)
iib = dominant(IIB)

def dom_res(d, key):
    if key not in d:
        return None
    alts = d[key]['alts']
    best = max(alts.values(), key=lambda r: r['proportion'])
    return best

rows = []
all_keys = sorted(set(ib) | set(iib), key=lambda k: (list(GENES).index(k[0]) if k[0] in GENES else 999, k[1]))
for key in all_keys:
    gene, pos = key
    b = dom_res(ib, key)      # Ib-dominant alternative vs reference, or None (=reference)
    w = dom_res(iib, key)     # IIb-B.1-dominant alternative, or None (=reference)
    ref = (ib.get(key) or iib.get(key) or {}).get('ref')

    # Ib residue and frequency
    if b is None:
        ib_res, ib_prop, ib_cov = ref, 1.0, None
    else:
        ib_res, ib_prop, ib_cov = b['mutationTo'], b['proportion'], b['coverage']
    # IIb residue and frequency
    if w is None:
        iib_res, iib_prop, iib_cov = ref, 1.0, None
    else:
        iib_res, iib_prop, iib_cov = w['mutationTo'], w['proportion'], w['coverage']

    if ref is None:
        continue
    if ib_res == iib_res:
        continue
    # locked thresholds
    if b is not None and (ib_prop < 0.95 or ib_cov is None or ib_cov < 100):
        continue
    if w is not None and (iib_prop < 0.95 or iib_cov is None or iib_cov < 1500):
        continue
    rows.append({
        'gene': gene, 'position': pos, 'ref_IIb2018': ref,
        'Ib_residue': ib_res, 'Ib_proportion': round(ib_prop,4), 'Ib_coverage': ib_cov if ib_cov else '>=376',
        'IIbB1_residue': iib_res, 'IIbB1_proportion': (round(iib_prop,4) if w else '>=0.95'), 'IIbB1_coverage': iib_cov if iib_cov else '>=3577',
        'product': GENES.get(gene, {}).get('product','?'),
        'kind': 'deletion' if (ib_res=='-' or iib_res=='-') else 'substitution',
    })

with open('results/fixed_differences.tsv','w',newline='') as fh:
    wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter='\t')
    wr.writeheader(); wr.writerows(rows)
print(len(rows), 'fixed differences')
from collections import Counter
print(Counter(r['kind'] for r in rows))
print(Counter(r['gene'] for r in rows).most_common(15))
