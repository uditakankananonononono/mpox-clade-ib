#!/usr/bin/env python3
"""Classify every fixed difference's protein into surface / immune / replication-assembly / unknown.
Locked rule order (2026-09-23): first matching keyword class wins; unmatched -> unknown.
Rules operate on the reference annotation product string; each row records the rule that fired."""
import csv, re, json
from collections import Counter

RULES = [
 ('surface', ['imv','eev','iev','membrane','entry','fusion','efc','hemagglutinin','surface',
              'glycoprotein','a26l/a30l','myristylated','l1r','b22r']),
 ('immune', ['chemokine','tnf','interleukin','ankyrin','kelch','bcl-2','serpin','nfkb','host range',
             'caspase','egf-like','interferon','ifn','mhc','cd47','schlafen','virulence',
             'c4l/c10l','double-stranded rna binding','hydroxysteroid','complement']),
 ('replication-assembly', ['polymerase','helicase','transcription','capping','topoisomerase','ligase',
             'nuclease','kinase','dutpase','thymidine kinase','thymidylate','ribonucleo','ntpase',
             'core protein','assembly','crescent','morphogenesis','atpase a32','telomere',
             'phospholipase','phosphoprotein','sulfhydryl','processivity','cap-specific',
             'rna binding protein vp8']),
]

def classify(prod):
    p = prod.lower()
    # OPG164 IEV transmembrane phosphoprotein: IEV -> surface (checked before phosphoprotein rule)
    for cls, kws in RULES:
        for kw in kws:
            if kw in p:
                return cls, kw
    return 'unknown', ''

rows = list(csv.DictReader(open('results/fixed_differences_polarized.tsv'), delimiter='\t'))
seen = {}
out = []
for r in rows:
    if r['gene'] not in seen:
        cls, kw = classify(r['product'])
        seen[r['gene']] = (cls, kw)
    r['protein_class'], r['class_rule'] = seen[r['gene']]
    out.append(r)
fields = list(out[0].keys())
with open('results/fixed_differences_classified.tsv','w',newline='') as fh:
    wr = csv.DictWriter(fh, fieldnames=fields, delimiter='\t'); wr.writeheader(); wr.writerows(out)
print('differences by class:', Counter(r['protein_class'] for r in out))
genes_cls = {g: c for g,(c,k) in seen.items()}
print('genes by class:', Counter(genes_cls.values()))
print('unknown genes:', sorted([g for g,c in genes_cls.items() if c=='unknown']))
# Ib-derived by class
print('Ib-derived by class:', Counter(r['protein_class'] for r in out if r['category']=='Ib_derived'))
