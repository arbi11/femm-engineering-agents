"""Replay the numerical experiment; this is not an LLM performance evaluation."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
from coil_tools import prepare, solve, measurements

parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
root=args.output.resolve()
root.mkdir(parents=True,exist_ok=False)
cases=[('baseline',1,100,1,1),('double-current',2,100,2,1),('double-turns',1,200,4,4)]
prediction={'relative_ratio_tolerance':.001,
    'assumptions':'Fixed geometry and mesh; linear air-core model; one excited winding',
    'frozen_at':datetime.now(timezone.utc).isoformat(),
    'cases':[{'name':n,'current_A':i,'turns':t,'linkage_ratio':fr,'inductance_ratio':lr}
             for n,i,t,fr,lr in cases]}
(root/'predictions-before-solving.json').write_text(json.dumps(prediction,indent=2)+'\n')
plans={}
for name,current,turns,_,_ in cases:
    plans[name]=prepare(current,turns)
    (root/(name+'-plan.json')).write_text(json.dumps(plans[name],indent=2)+'\n')
reports={};summaries=[]
for name,current,turns,expected_flux,expected_L in cases:
    report=solve(root/name,current,turns)
    reports[name]=report
    assert report['plan_sha256']==plans[name]['plan_sha256']
    m=report['metrics']; b=reports['baseline']['metrics']
    fr=m['flux_linkage_Wb_turn']/b['flux_linkage_Wb_turn']
    lr=m['inductance_H']/b['inductance_H']
    assert abs(fr/expected_flux-1)<=.001 and abs(lr/expected_L-1)<=.001
    summaries.append({'name':name,**measurements(report),
        'linkage_ratio':fr,'inductance_ratio':lr,'ratio_check':'passed'})
    print(name,report['status'],m['inductance_H']*1000,flush=True)
record={'status':'passed','llm_calls_in_replay':0,
    'meaning':'Deterministic numerical replay of the task given to a coding agent',
    'cases':summaries}
(root/'results.json').write_text(json.dumps(record,indent=2)+'\n')
