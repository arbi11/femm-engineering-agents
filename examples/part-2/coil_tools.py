"""Small teaching interface to the existing FEMM study planner and runner.

Run from the research_extender checkout. The coding agent chooses these calls;
this module does not contain an LLM or an autonomous planning loop.
"""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd()))
from femm_brain.simulation import plan_simulation
from femm_brain.execution import run_case


def prepare(current=1, turns=100):
    return plan_simulation('aircore-short', {'current': current, 'turns': turns})


def solve(output, current=1, turns=100):
    return run_case('aircore-short', output,
                    {'current': current, 'turns': turns},
                    image='femm-brain-native:tutorial')


def measurements(report):
    return {'status': report['status'], 'current_A': report['metrics']['current_A'],
        'linkage_Wb_turn': report['metrics']['flux_linkage_Wb_turn'],
        'inductance_mH': report['metrics']['inductance_H']*1000,
        'center_Bz_mT': report['metrics']['field_y_T']*1000,
        'stage_checks': {k: v['status'] for k, v in report['checks'].items()}}


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('operation', choices=['prepare','solve'])
    parser.add_argument('--current',type=float,default=1)
    parser.add_argument('--turns',type=int,default=100)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.operation=='prepare':
        result=prepare(args.current,args.turns)
    else:
        if args.output is None:parser.error('solve requires --output')
        result=measurements(solve(args.output,args.current,args.turns))
    print(json.dumps(result,indent=2))
