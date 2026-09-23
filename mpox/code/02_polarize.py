#!/usr/bin/env python3
"""Polarize fixed differences using clade Ia as outgroup.
Categories:
  Ib_derived : Ib != Ia and Ia == IIbB1  (new in clade Ib)
  IIb_derived: IIbB1 != Ia and Ia == Ib  (new in IIb B.1 / since I-II split on II branch)
  cladeI_background: Ib == Ia != IIbB1 ... (same as IIb_derived actually)
  deep_other : all three differ, or Ia == one but ambiguous
Locked threshold: Ia dominant proportion >= 0.95, coverage >= 100.
"""
import json, csv
from collections import Counter

IB = json.load(open('data/ib_aamuts.json'))['data']
IIB = json.load(open('data/iib_aamuts.json'))['data']
IA = json.load(open('data/ia_aamuts.json'))['data']

def dommap(rows):
    out = {}
    for r in rows:
        key = (r['sequenceName'], r['position'])
        out.setdefault(key, {'ref': r['mutationFrom'], 'alts': {}})
        out[key]['alts'][r['mutationTo']] = r
    return out

ib, iib, ia = dommap(IB), dommap(IIB), dommap(IA)

def state(d, key):
    """return (residue, prop, cov) of dominant state; residue None means reference"""
    if key not in d: return (None, None, None)
    best = max(d[key]['alts'].values(), key=lambda r: r['proportion'])
    return (best['mutationTo'], best['proportion'], best['coverage'])

rows = list(csv.DictReader(open('results/fixed_differences.tsv'), delimiter='\t'))
out = []
for r in rows:
    key = (r['gene'], int(r['position']))
    ref = r['ref_IIb2018']
    a_res, a_prop, a_cov = state(ia, key)
    ia_res = ref if a_res is None else a_res
    ia_ok = (a_res is None) or (a_prop >= 0.95 and (a_cov or 9999) >= 100)
    ib_res, w_res = r['Ib_residue'], r['IIbB1_residue']
    if not ia_ok:
        cat = 'outgroup_uncertain'
    elif ia_res == w_res and ib_res != w_res:
        cat = 'Ib_derived'
    elif ia_res == ib_res and w_res != ib_res:
        cat = 'IIb_derived(cladeI_background_in_Ib)'
    elif ia_res != ib_res and ia_res != w_res:
        cat = 'three_way'
    else:
        cat = 'other'
    r['Ia_residue'] = ia_res
    r['Ia_proportion'] = 'ref' if a_res is None else round(a_prop,4)
    r['category'] = cat
    out.append(r)

fields = list(out[0].keys())
with open('results/fixed_differences_polarized.tsv','w',newline='') as fh:
    wr = csv.DictWriter(fh, fieldnames=fields, delimiter='\t'); wr.writeheader(); wr.writerows(out)
print(Counter(r['category'] for r in out))
print('--- Ib_derived ---')
for r in out:
    if r['category']=='Ib_derived':
        print(f"{r['gene']}:{r['ref_IIb2018']}{r['position']}{r['Ib_residue']}  {r['product'][:60]}")
