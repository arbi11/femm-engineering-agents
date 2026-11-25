"""Read the exact hierarchy records used in the article, without a server."""
import json
from pathlib import Path

root=Path(__file__).resolve().parent
graph=json.loads((root/'graph.json').read_text())
nodes={n['id']:n for n in graph['nodes']}
identifiers=['workflow:aircore','method:methods_axisymmetric_coil_section',
 'method:methods_linear_flux_inductance','method:methods_biased_incremental_inductance',
 'primitive:mo_getcircuitproperties']
for identifier in identifiers:
    n=nodes[identifier]
    print('\n'+identifier+'\n'+n['title'])
    for constraint in n.get('constraints',[]):print('  Condition:',constraint)
    for edge in graph['edges']:
        if edge['source']==identifier and edge['target'] in nodes:
            print(' ',edge['relation'],'->',edge['target'])
