import json
from pathlib import Path

root=Path(__file__).resolve().parent
case=json.loads((root/'case.json').read_text())
report=json.loads((root/'recorded-report.json').read_text())
for t in report['levels']['article']['targets']:
    if t.get('acceptance') and t.get('metric') in ['inductance_H@ind','flux_A_Wb:fundamental_rms']:
        print(t['metric'],t['status'],'observed =',t['observed'],'expected =',t['expected'])
print('Native position solves:',sum(s['label'].startswith('p') for s in case['steps']))
print('Half-wave symmetry:',case['assessors'][0]['half_wave_symmetry'])
print('Baseline magnet relative permeability:',case['article']['parameters']['magnet_mu_r']['value'])
