#!/usr/bin/env python3
"""Check published Skill versions, release metadata, and proposed commit/PR titles."""
import argparse
import json
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)')

def parse_version(value):
    assert isinstance(value, str) and SEMVER.fullmatch(value), f'Invalid semantic version: {value!r}'
    return tuple(map(int, value.split('.')))

def check_title(title, versions):
    labels = re.match(r'^(?:【V[0-9]+\.[0-9]+\.[0-9]+】)+', title)
    assert labels and title[labels.end():].strip(), f'Missing version prefix or description: {title!r}'
    values = re.findall(r'【V([^】]+)】', labels.group())
    for value in values:
        parse_version(value)
        assert value in versions, f'Title version {value} is absent from the current Skill versions {sorted(versions)}'

def check_transition(before, after, kind, locked_major):
    a, b = parse_version(before), parse_version(after)
    assert a[0] == b[0] == locked_major, 'Major upgrade is forbidden'
    if kind == 'patch':
        assert b == (a[0], a[1], a[2] + 1), 'A daily adjustment must increment only patch'
    elif kind == 'minor':
        assert b == (a[0], a[1] + 1, 0), 'A minor release must reset patch to zero'
    elif kind == 'record_only':
        assert a == b, 'Record-only maintenance must not invent a version increment'
    else:
        raise AssertionError(f'Unknown change kind: {kind}')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--commit-title')
    parser.add_argument('--pr-title')
    parser.add_argument('--policy-cases', action='store_true')
    args = parser.parse_args()
    policy = json.loads((ROOT/'registry/version-policy.json').read_text())
    manifest = json.loads((ROOT/'registry/latest.json').read_text())
    readme = (ROOT/'README.md').read_text()
    assert policy['major_upgrade_allowed'] is False and policy['locked_major'] == 1
    assert '展示版本 1.01' not in readme and '展示版本仍为1.01' not in readme
    assert '## 版本更新日志（Changelog）' in readme
    versions = set()
    for name in policy['skills']:
        folder = ROOT/'skills'/name
        metadata = json.loads((folder/'version.json').read_text())
        value = metadata['version']
        assert parse_version(value)[0] == policy['locked_major']
        assert metadata['skill'] == name and metadata['version_format'] == 'semver'
        assert metadata['display_version'] == f"{metadata['category']}-{name} V{value}"
        text = (folder/'SKILL.md').read_text()
        front = yaml.safe_load(text.split('---', 2)[1])
        assert front['name'] == name and isinstance(front['description'], str) and front['description'].strip()
        assert len(re.findall(r'当前发布版本：\*\*'+re.escape(value)+r'\*\*', text)) == 1
        assert not re.search(r'当前发布版本：\*\*1\.01\*\*|V1\.01|字符串`1\.01`', text)
        assert manifest['skills'][name]['version'] == value
        assert re.search(r'\|[^\n]+\| V'+re.escape(value)+r' \| \['+re.escape(name)+r'\]', readme), name
        audit = json.loads((folder/'references/audit/registry.json').read_text())
        assert audit['skill_release_version'] == value
        release_path = (folder/metadata['release_record']).resolve()
        assert release_path.is_relative_to(ROOT) and release_path.is_file()
        assert json.loads(release_path.read_text())['version'] == value
        versions.add(value)
    changelog = readme.split('## 版本更新日志（Changelog）', 1)[1]
    for version in re.findall(r'^### V([^\s]+)', changelog, flags=re.M):
        assert parse_version(version)[2] == 0, 'README Changelog must omit patch releases'
    for title in [args.commit_title, args.pr_title]:
        if title is not None:
            check_title(title, versions)
    cases = 0
    if args.policy_cases:
        for before, after, kind in [('1.1.0','1.1.1','patch'), ('1.1.2','1.2.0','minor'), ('1.1.0','1.1.0','record_only')]:
            check_transition(before, after, kind, 1); cases += 1
        for before, after, kind in [('1.1.0','2.0.0','minor'), ('1.1.0','1.2.0','patch'), ('1.1.1','1.2.1','minor'), ('1.1.0','1.1.1','record_only')]:
            try:
                check_transition(before, after, kind, 1)
            except AssertionError:
                cases += 1
            else:
                raise AssertionError(f'Invalid version transition was accepted: {before} -> {after}')
        for title in ['缺版本的提交', '【V1.01】旧标识', '【V2.0.0】禁改主版本', '【V1.1.0】']:
            try:
                check_title(title, versions)
            except AssertionError:
                cases += 1
            else:
                raise AssertionError(f'Invalid title was accepted: {title}')
    print(json.dumps({'result':'PASS','skills':len(policy['skills']),'versions':sorted(versions),'policy_cases':cases}, ensure_ascii=False))

if __name__ == '__main__':
    main()
