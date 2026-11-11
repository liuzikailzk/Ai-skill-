#!/usr/bin/env python3
"""Route reviewed beats to existing methods; never classify by keywords or generate media."""
import argparse
import hashlib
import json
from pathlib import Path
from knowledge_snapshot import validated_catalog
from query_knowledge import ROOT, eligible, executable, query, validate_taxonomy
from script_workspace import validate_analysis

def route(source,analysis,scene_id,mode='analysis',stage='plan',root=ROOT):
    root=Path(root);taxonomy=json.loads((root/'knowledge/taxonomy.json').read_text())
    validation=validate_analysis(source,analysis,taxonomy)
    scene=next((s for s in analysis['scenes'] if s['id']==scene_id),None)
    if not scene:raise ValueError('Scene is not reviewed: '+scene_id)
    catalog,snapshot=validated_catalog(root);by={e['id']:e for e in catalog['entries']}
    validate_taxonomy(taxonomy,catalog)
    base=query(catalog,'剧本局部制作',mode,['film'],stage=stage)
    routed=[]
    for beat in scene['beats']:
        facets=[beat['primary']]+[f'{f}:{v}' for f,vs in beat['labels'].items() for v in vs if f'{f}:{v}'!=beat['primary']]
        chosen=[];gaps=[];skipped=[]
        for facet in facets:
            ids=taxonomy['method_routes'].get(facet,[])
            if not ids and facet==beat['primary']:gaps.append('No dedicated method for primary facet: '+facet)
            for key in ids:
                e=by.get(key)
                if not e or e.get('kind')!='method' or not eligible(e,mode,['film'],required=True) or not executable(e,mode,base['entry_roots']):raise ValueError('Route target ineligible: '+key)
                if key in [x['id'] for x in chosen]:continue
                if len(chosen)<2:
                    chosen.append({'id':key,'role':'primary' if facet==beat['primary'] and not chosen else 'supporting','reason':facet,'source_refs':beat['source_refs']})
                else:skipped.append({'id':key,'reason':'Keep one main task and at most one support method; reconsider if needed'})
        routed.append({'beat_id':beat['id'],'source_refs':beat['source_refs'],'goal':beat['goal'],'trigger':beat['trigger'],'outcome':beat['outcome'],'methods':chosen,'unselected':skipped,'gaps':gaps,'uncertainties':beat['uncertainties']})
    analysis_hash=hashlib.sha256(json.dumps(analysis,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    return {'snapshot':snapshot,'source_sha256':source['source_sha256'],'extraction_sha256':source['extraction_sha256'],'analysis_revision':analysis['analysis_revision'],'analysis_sha256':analysis_hash,'project_revision':source['source_sha256']+':'+source['extraction_sha256']+':'+analysis_hash,'scene_id':scene_id,'validation':validation,'entry_roots':base['entry_roots'],'required_rules':base['required_rules'],'read_plan_ids':list(dict.fromkeys([x['canonical_id'] for x in base['required_rules']]+[m['id'] for b in routed for m in b['methods']])),'beats':routed,'limits':'Method selection suggestions, not generated-media validation. Confirm source meaning, style and continuity before application.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('analysis',type=Path);p.add_argument('--scene',required=True);p.add_argument('--mode',choices=('analysis','production'),default='analysis');p.add_argument('--stage',choices=('understand','plan','deliver'),default='plan');a=p.parse_args()
    try:result=route(json.loads(a.source.read_text()),json.loads(a.analysis.read_text()),a.scene,a.mode,a.stage)
    except (ValueError,KeyError,AssertionError) as exc:p.error(str(exc))
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
