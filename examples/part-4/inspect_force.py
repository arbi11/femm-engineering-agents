import json
from pathlib import Path

r=json.loads((Path(__file__).resolve().parent/'recorded-report.json').read_text())
m=r['metrics'];target=r['frozen_reference']['value']
for name,reference in [('force_magnet_z_N',target),('force_coil_z_N',-target)]:
    value=m[name]
    print(name, 'mN =',1000*value, 'relative error % =',100*abs(value/reference-1))
print('Coil weighted-stress mN =',1000*m['force_coil_wst_z_N'])
print('Body-force imbalance mN =',1000*abs(m['force_magnet_z_N']+m['force_coil_z_N']))
