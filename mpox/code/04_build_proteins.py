#!/usr/bin/env python3
"""Build reference and clade-Ib-consensus protein sequences for all genes with fixed differences.
Ib consensus = NC_063383 reference translation + all Ib mutations at proportion>=0.95, coverage>=100
(from frozen data/ib_aamuts.json). Deletions ('-') remove the residue."""
import json, csv
from Bio import SeqIO

ref_rec = SeqIO.read('data/NC_063383.gb','genbank')
ref_prot = {}
for f in ref_rec.features:
    if f.type=='CDS':
        g = f.qualifiers.get('gene',[''])[0]
        ref_prot[g] = f.qualifiers.get('translation',[''])[0]

ib_muts = json.load(open('data/ib_aamuts.json'))['data']
fixed = {}
for r in ib_muts:
    if r['proportion'] >= 0.95 and r['coverage'] >= 100:
        fixed.setdefault(r['sequenceName'], {})[r['position']] = r['mutationTo']

ib_prot = {}
for g, seq in ref_prot.items():
    s = list(seq)
    for pos, to in sorted(fixed.get(g, {}).items()):
        if pos-1 < len(s):
            s[pos-1] = '' if to=='-' else to
    ib_prot[g] = ''.join(s)

json.dump(ref_prot, open('results/ref_proteins.json','w'))
json.dump(ib_prot, open('results/ib_consensus_proteins.json','w'))
print('ref proteins:', len(ref_prot), ' Ib consensus built for', len(ib_prot))
for g in ['OPG164','OPG045','OPG019']:
    print(g, 'ref_len', len(ref_prot[g]), 'ib_len', len(ib_prot[g]))
