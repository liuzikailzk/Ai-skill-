#!/usr/bin/env python3
"""Extract source structure and validate human/agent annotations; never infer story meaning."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from knowledge_snapshot import atomic_json
from query_knowledge import ROOT

NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
EPISODE=re.compile(r'^第\s*([0-9]+)\s*集\s*$')
SCENE=re.compile(r'^(\d+)\s*[-－—–]\s*(\d+)(?:\s+|(?=[日夜晨晚内外]))(.+)$')

def extraction_digest(source):
    keys=('schema','source_sha256','paragraphs','front_matter_refs','episodes','scenes','warnings')
    return hashlib.sha256(json.dumps({k:source[k] for k in keys},sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def extract_source(path):
    path=Path(path);data=path.read_bytes();warnings=[]
    if path.suffix.lower()=='.docx':
        with zipfile.ZipFile(path) as z:
            tree=ET.fromstring(z.read('word/document.xml'))
            paragraphs=[]
            for i,p in enumerate(tree.findall('.//w:body//w:p',NS),1):
                text=''.join(x.text or '' for x in p.findall('.//w:t',NS))
                if text.strip(): paragraphs.append({'id':f'P{i:04d}','text':text})
            if tree.findall('.//w:ins',NS) or tree.findall('.//w:del',NS):warnings.append('Tracked changes exist; accepted-text extraction requires editorial confirmation')
            if tree.findall('.//w:drawing',NS):warnings.append('Images exist; text extraction does not read visual evidence')
    else:
        paragraphs=[{'id':f'P{i:04d}','text':line} for i,line in enumerate(data.decode('utf-8').splitlines(),1) if line.strip()]
    episodes=[];scenes=[];front=[];current_episode=None;current_scene=None;seen={}
    for p in paragraphs:
        text=unicodedata.normalize('NFKC',p['text']).strip();ep=EPISODE.fullmatch(text);scene=SCENE.fullmatch(text)
        if ep:
            current_episode={'id':ep[1],'source_refs':[p['id']],'scene_ids':[]};episodes.append(current_episode);current_scene=None
        elif scene:
            base=f'{scene[1]}-{scene[2]}';seen[base]=seen.get(base,0)+1
            sid=base if seen[base]==1 else base+f'~{seen[base]}'
            if seen[base]>1:warnings.append('Duplicate scene heading: '+base)
            if current_episode and current_episode['id']!=scene[1]:warnings.append('Scene/episode mismatch: '+sid)
            current_scene={'id':sid,'episode_id':current_episode['id'] if current_episode else scene[1],'heading':p['text'],'source_refs':[p['id']],'semantic_status':'unreviewed'}
            scenes.append(current_scene)
            if current_episode:current_episode['scene_ids'].append(sid)
        elif current_scene:current_scene['source_refs'].append(p['id'])
        elif current_episode:current_episode['source_refs'].append(p['id'])
        else:front.append(p['id'])
    assigned=front+[x for e in episodes for x in e['source_refs']]+[x for s in scenes for x in s['source_refs']]
    if len(assigned)!=len(set(assigned)) or set(assigned)!={p['id'] for p in paragraphs}:raise ValueError('Source coverage is not exact')
    result={'schema':1,'source_sha256':hashlib.sha256(data).hexdigest(),'source_name':path.name,'paragraphs':paragraphs,'front_matter_refs':front,'episodes':episodes,'scenes':scenes,'warnings':warnings,'coverage':{'nonempty_paragraphs':len(paragraphs),'assigned_exactly_once':len(assigned),'semantic_review':'not_performed_by_extractor'}}
    result['extraction_sha256']=extraction_digest(result)
    return result

def validate_analysis(source,analysis,taxonomy=None,require_complete=False):
    taxonomy=taxonomy or json.loads((ROOT/'knowledge/taxonomy.json').read_text())
    fingerprint=extraction_digest(source)
    if source.get('extraction_sha256')!=fingerprint:raise ValueError('Extracted source content changed; regenerate and review affected analysis')
    if analysis.get('extraction_sha256')!=fingerprint:raise ValueError('Analysis belongs to a different extraction revision')
    if analysis.get('source_sha256')!=source['source_sha256']:raise ValueError('Analysis belongs to a different source revision')
    if not analysis.get('analysis_revision'):raise ValueError('Missing analysis revision')
    paragraphs={p['id']:p['text'] for p in source['paragraphs']};scenes={s['id']:s for s in source['scenes']};seen=set();beats_seen=set()
    if not scenes or not analysis.get('scenes'):raise ValueError('No reviewed scene annotations')
    def refs(values,allowed):
        if not values or not set(values)<=set(allowed):raise ValueError('Missing or out-of-scope source references')
    for record in analysis.get('scenes',[]):
        sid=record['id']
        if sid not in scenes or sid in seen:raise ValueError('Unknown or duplicate scene '+sid)
        seen.add(sid);scene=scenes[sid];allowed=scene['source_refs']
        if record.get('review_status')!='reviewed':raise ValueError('Scene not semantically reviewed: '+sid)
        if record.get('reviewed_source_refs')!=allowed:raise ValueError('Scene reading coverage mismatch: '+sid)
        if not record.get('summary'):raise ValueError('Missing scene summary')
        previous=-1;beat_coverage=[]
        for beat in record.get('beats',[]):
            bid=beat.get('id')
            if not bid or bid in beats_seen:raise ValueError('Missing or duplicate beat ID')
            beats_seen.add(bid);refs(beat.get('source_refs'),allowed)
            indexes=[allowed.index(x) for x in beat['source_refs']]
            if indexes!=sorted(set(indexes)) or min(indexes)<=previous:raise ValueError('Overlapping or out-of-order beats')
            previous=max(indexes);beat_coverage+=beat['source_refs']
            for field in ('goal','trigger','outcome','facts','interpretation','entry_state','exit_state','uncertainties'):
                if field not in beat:raise ValueError('Missing beat field '+field)
            for field in ('goal','trigger','outcome'):
                if not isinstance(beat[field],str) or not beat[field].strip():raise ValueError('Nonempty text required: '+field)
            if not isinstance(beat['facts'],list) or not beat['facts'] or any(not isinstance(x,(str,dict)) or not x for x in beat['facts']):raise ValueError('Nonempty factual observations required')
            if not isinstance(beat['interpretation'],(str,list)):raise ValueError('Interpretation must be text or a list')
            if not isinstance(beat['entry_state'],dict) or not isinstance(beat['exit_state'],dict):raise ValueError('States must be objects; unknown values must be explicit')
            if not isinstance(beat['uncertainties'],list):raise ValueError('Uncertainties must be a list')
            labels=beat.get('labels',{})
            if set(labels)!=set(taxonomy['facets']):raise ValueError('Missing/unknown classification dimensions')
            for facet,values in labels.items():
                if not isinstance(values,list) or not values or not all(isinstance(v,str) for v in values) or not set(values)<=set(taxonomy['facets'][facet]):raise ValueError('Unknown labels in '+facet)
            primary=beat.get('primary')
            if not isinstance(primary,str) or ':' not in primary:raise ValueError('Missing primary expression problem')
            facet,value=primary.split(':',1)
            if value not in labels.get(facet,[]):raise ValueError('Primary facet not present in annotation')
            for quote in beat.get('quotes',[]):
                if quote.get('ref') not in beat['source_refs'] or not quote.get('text') or quote['text'] not in paragraphs[quote['ref']]:raise ValueError('Quote differs from source')
        if not record.get('beats'):raise ValueError('Reviewed scene has no beat annotations')
        excluded=record.get('nonbeat_refs',[])
        if len(excluded)!=len(set(excluded)):raise ValueError('Duplicate nonbeat reference')
        if not set(excluded)<=set(allowed) or set(excluded)&set(beat_coverage) or set(excluded)|set(beat_coverage)!=set(allowed):raise ValueError('Beat coverage gap or overlap: '+sid)
        # Nonbeat exclusions are structural headings/cast/end markers only, never narrative action.
        for ref in excluded:
            t=unicodedata.normalize('NFKC',paragraphs[ref]).strip()
            if not (SCENE.fullmatch(t) or t.startswith(('出场人物','人物:','人物：')) or re.fullmatch(r'[（(]?本集完[）)]?',t)):
                raise ValueError('Narrative paragraph excluded from beats: '+ref)
    if require_complete and seen!=set(scenes):raise ValueError('Whole-script semantic coverage incomplete')
    return {'result':'PASS','reviewed_scenes':len(seen),'total_scenes':len(scenes),'beats':len(beats_seen),'complete_scene_coverage':seen==set(scenes),'scope':'Structural coverage, taxonomy and source-reference integrity only; semantic fidelity requires reading review'}

def main():
    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='command',required=True)
    a=s.add_parser('extract');a.add_argument('source',type=Path);a.add_argument('--output',type=Path,required=True)
    a=s.add_parser('validate');a.add_argument('source',type=Path);a.add_argument('analysis',type=Path);a.add_argument('--complete',action='store_true')
    a=p.parse_args()
    try:
        if a.command=='extract':
            result=extract_source(a.source);atomic_json(a.output,result);print(json.dumps({'episodes':len(result['episodes']),'scenes':len(result['scenes']),'coverage':result['coverage'],'warnings':result['warnings']},ensure_ascii=False))
        else:print(json.dumps(validate_analysis(json.loads(a.source.read_text()),json.loads(a.analysis.read_text()),require_complete=a.complete),ensure_ascii=False))
    except (ValueError,KeyError) as exc:p.error(str(exc))
if __name__=='__main__':main()
