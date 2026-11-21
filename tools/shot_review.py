"""Plan shot checks and verify a recorded review before continuing its dependency chain."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = 'workflows/methods/shot-checks.json'


def shot_plan(description, tags=(), root=ROOT):
    rules = json.loads((Path(root) / CHECKS).read_text(encoding='utf-8'))
    explicit = set(tags)
    known = {key for row in rules['checks'] for key in (row['id'], row['label'])}
    if explicit - known:
        raise ValueError('未知错题标签：' + ', '.join(sorted(explicit - known)))
    text = ''.join(description.casefold().split())
    dialogue = next(row for row in rules['checks'] if row['id'] == 'dialogue')
    if explicit.intersection(('dialogue', dialogue['label'])) or any(term in text for term in dialogue['terms']):
        explicit.add('voice')
    checks = []
    for row in rules['checks']:
        if ('*' in row['terms'] or explicit.intersection((row['id'], row['label']))
                or any(term in text for term in row['terms'])):
            checks.append({key: value for key, value in row.items() if key != 'terms'})
    fingerprint = hashlib.sha256(json.dumps([description, checks], ensure_ascii=False,
                                           sort_keys=True).encode()).hexdigest()
    return {'checks': checks, 'case_sources': rules['sources'], 'plan_id': fingerprint}


def template(plan, input_revision, selected_version=''):
    """A new sheet starts pending even when all required checks have been identified."""
    rows = {item['id']: {phase: {'status': 'pending', 'version': '', 'evidence': {}, 'observation': ''}
                         for phase in ('preflight', 'review')} for item in plan['checks']}
    sheet = {'plan_id': plan['plan_id'], 'input_revision': input_revision,
            'selected_version': selected_version, 'user_decision': 'unreviewed', 'checks': rows}
    if 'reference' in rows:
        sheet['upstream'] = {'input_revision': '', 'selected_version': '', 'plan_id': ''}
    return sheet


def evaluate(plan, sheet, phase, input_revision, selected_version='', upstream=None):
    if phase not in ('preflight', 'review') or not input_revision.strip():
        raise ValueError('请指定有效阶段与当前镜号/输入版本')
    if phase == 'review' and not selected_version.strip():
        raise ValueError('成片复核需要当前时间线的实际版本标识')
    pending, failed = [], []
    if sheet.get('plan_id') != plan['plan_id'] or sheet.get('input_revision') != input_revision:
        pending.append('回执与当前镜头方案或输入版本不符')
    if phase == 'review' and sheet.get('selected_version') != selected_version:
        pending.append('回执与当前选用版本不符')
    if pending:
        return {'phase': phase, 'status': 'pending', 'allow': False, 'pending': pending, 'failed': []}
    if any(item['id'] == 'reference' for item in plan['checks']):
        expected = sheet.get('upstream')
        keys = ('input_revision', 'selected_version', 'plan_id')
        if (not isinstance(expected, dict) or not isinstance(upstream, dict)
                or any(not isinstance(expected.get(k), str) or not expected[k].strip()
                       or upstream.get(k) != expected[k] for k in keys)
                or upstream.get('phase') != 'review'):
            pending.append('缺同一前镜选片、裁点及方案的复核结果')
        elif upstream.get('status') == 'failed':
            failed.append('前镜复核失败')
        elif (upstream.get('status') != 'passed' or upstream.get('allow') is not True
              or upstream.get('pending') != [] or upstream.get('failed') != []):
            pending.append('前镜复核尚未通过')
    decision = sheet.get('user_decision')
    if decision == 'rejected':
        failed.append('当前版本已被用户判退')
    elif decision not in ('unreviewed', 'accepted'):
        pending.append('缺用户判定状态')
    rows = sheet.get('checks', {})
    if not isinstance(rows, dict):
        raise ValueError('checks 必须按检查项编号记录')
    for item in plan['checks']:
        row = rows.get(item['id'], {})
        for step in (('preflight',) if phase == 'preflight' else ('preflight', 'review')):
            entry = row.get(step, {}) if isinstance(row, dict) else {}
            key = item['id'] + '/' + step
            if not isinstance(entry, dict):
                pending.append(key)
                continue
            if entry.get('status') == 'failed':
                failed.append(key)
                continue
            version = input_revision if step == 'preflight' else selected_version
            necessary = item.get('inputs', ['input']) if step == 'preflight' else item['media']
            evidence = entry.get('evidence')
            observed = entry.get('observation')
            if (entry.get('status') != 'passed' or entry.get('version') != version
                    or not isinstance(observed, str) or not observed.strip()
                    or not isinstance(evidence, dict)
                    or any(not isinstance(evidence.get(kind), str) or not evidence[kind].strip()
                           for kind in necessary)):
                pending.append(key)
    status = 'failed' if failed else 'pending' if pending else 'passed'
    return {'phase': phase, 'plan_id': plan['plan_id'], 'input_revision': input_revision,
            'selected_version': selected_version, 'status': status, 'allow': status == 'passed',
            'pending': pending, 'failed': failed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('description', help='本镜动作、人物关系、台词与相邻接点')
    parser.add_argument('--tag', action='append', default=[], help='人工补充风险标签，可重复')
    action = parser.add_mutually_exclusive_group()
    action.add_argument('--template', action='store_true', help='输出待填回执')
    action.add_argument('--receipt', type=Path, help='检查当前项目中的 JSON 回执')
    parser.add_argument('--upstream-result', type=Path, help='依赖前镜的 review 阶段结果文件')
    parser.add_argument('--phase', choices=('preflight', 'review'))
    parser.add_argument('--input-revision', help='项目/集/镜及剧本、参考绑定和接点的版本')
    parser.add_argument('--selected-version', default='', help='当前所选素材及时间线裁点版本')
    args = parser.parse_args()
    if (args.template or args.receipt) and not (args.input_revision or '').strip():
        parser.error('需要 --input-revision')
    if bool(args.receipt) != bool(args.phase):
        parser.error('--receipt 与 --phase 须一起使用')
    try:
        plan = shot_plan(args.description, args.tag)
        result = plan
        if args.template:
            result = template(plan, args.input_revision, args.selected_version)
        elif args.receipt:
            sheet = json.loads(args.receipt.read_text(encoding='utf-8-sig'))
            if not isinstance(sheet, dict):
                raise ValueError('回执须为 JSON 对象')
            upstream = None
            if args.upstream_result:
                upstream = json.loads(args.upstream_result.read_text(encoding='utf-8-sig'))
            result = evaluate(plan, sheet, args.phase, args.input_revision, args.selected_version, upstream)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result.get('allow') is False else 0


if __name__ == '__main__':
    raise SystemExit(main())
