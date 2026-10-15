#!/usr/bin/env python3
"""Fail-closed, non-fabrication KiCad 10.0.6 ERC/DRC/parity evidence collector.

Never releases RC18 for fabrication. Uses a staged copy; does not alter source.
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import zipfile

EXPECTED_ZIP_SHA256 = '1368263c3e304ee0d046cd6d53907e7c171bfeb3886191e603a53a34dfb3b24b'
EXPECTED_PROJECT_DIR = 'RC18_E27S_ANALOG_SUPPLY_NAME_CANDIDATE_NONFAB_HOLD'
EXPECTED_KICAD_VERSION = '10.0.6'
EXPECTED_MANIFEST_FILES = 40
PROJECT = 'RC18_RevB_SI'


def digest(path):
    h = hashlib.sha256()
    with pathlib.Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def extract_guarded(archive, destination):
    with zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            p = pathlib.PurePosixPath(member.filename)
            if p.is_absolute() or '..' in p.parts or '\\' in member.filename:
                raise RuntimeError('Refusing archive path: ' + member.filename)
        z.extractall(destination)


def verify_manifest(project):
    manifest = project / 'MANIFEST_SHA256.txt'
    if not manifest.is_file():
        raise RuntimeError('Missing KiCad input manifest')
    records = []
    for row in manifest.read_text(encoding='utf-8').splitlines():
        if not row.strip():
            continue
        m = re.fullmatch(r'([0-9a-f]{64})  (.+)', row)
        if not m:
            raise RuntimeError('Bad manifest row ' + row[:70])
        expected, rel = m.groups()
        p = pathlib.PurePosixPath(rel)
        if p.is_absolute() or '..' in p.parts:
            raise RuntimeError('Manifest path traversal')
        f = project.joinpath(*p.parts)
        if not f.is_file() or digest(f) != expected:
            raise RuntimeError('KiCad manifest mismatch: ' + rel)
        records.append(rel)
    if len(records) != EXPECTED_MANIFEST_FILES or len(set(records)) != EXPECTED_MANIFEST_FILES:
        raise RuntimeError(f'Expected {EXPECTED_MANIFEST_FILES} unique manifest files, found {len(records)}')
    needed = [PROJECT + ext for ext in ('.kicad_pro', '.kicad_sch', '.kicad_pcb')] + ['sym-lib-table', 'fp-lib-table']
    for n in needed:
        if not (project / n).is_file():
            raise RuntimeError('Missing ' + n)
    if len(list(project.glob('[0-9][0-9]_*.kicad_sch'))) != 15:
        raise RuntimeError('Expected 15 hierarchical sheets')
    return records


def run_cli(exe, args, cwd, log):
    command = [exe] + [str(x) for x in args]
    try:
        p = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=600, check=False)
        log.write_text('COMMAND: ' + ' '.join(command) + '\n' + p.stdout + '\nEXIT_CODE=' + str(p.returncode) + '\n', encoding='utf-8')
        return p.returncode
    except Exception as e:
        log.write_text('COMMAND: ' + ' '.join(command) + '\nERROR=' + repr(e) + '\n', encoding='utf-8')
        return 255


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--input', default='rc18_inputs/RC18_E27S_PIN_LABEL_ECO_CANDIDATE_NONFAB_HOLD_20261015.zip')
    a.add_argument('--out', default='native_gate_results')
    a.add_argument('--preflight', action='store_true')
    args = a.parse_args()
    archive = pathlib.Path(args.input).resolve()
    out = pathlib.Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    report = {
        'stage': 'E27S',
        'date_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'required_native_kicad_version': EXPECTED_KICAD_VERSION,
        'source_zip': archive.name,
        'source_zip_expected_sha256': EXPECTED_ZIP_SHA256,
        'manufacturing': 'HOLD_NO_POWER_NO_AC_NO_ORDER_NO_FAB',
        'manufacturing_release': False,
        'native_attempted': False,
        'native_zero_gate': False,
        'context': '17 source release blockers remain open pending separate proofs; missing 64 FIT etc',
        'errors': [],
    }
    try:
        if not archive.is_file():
            raise RuntimeError('E27S source archive not found')
        actual = digest(archive)
        report['source_zip_actual_sha256'] = actual
        if actual != EXPECTED_ZIP_SHA256:
            raise RuntimeError('Source archive SHA256 mismatch')
        src = out / 'UNPACKED_SOURCE_FOR_PREFLIGHT'
        if src.exists():
            shutil.rmtree(src)
        src.mkdir(parents=True)
        extract_guarded(archive, src)
        project = src / EXPECTED_PROJECT_DIR
        records = verify_manifest(project)
        report['verified_source_files'] = len(records)
        report['preflight'] = 'PASS_SOURCE_INTEGRITY_ONLY'
        if args.preflight:
            report['status'] = 'PREFLIGHT_OK_NATIVE_NOT_RUN'
            return 0
        exe = shutil.which('kicad-cli')
        if not exe:
            raise RuntimeError('kicad-cli missing on runner')
        ver = subprocess.run([exe, 'version'], capture_output=True, text=True, timeout=60, check=False)
        version_text = (ver.stdout + '\n' + ver.stderr).strip()
        (out / 'kicad-cli-version.txt').write_text(version_text + '\n', encoding='utf-8')
        if ver.returncode != 0 or not re.search(r'(?<!\d)10\.0\.6(?!\d)', version_text):
            raise RuntimeError('Exact KiCad 10.0.6 required; found: ' + version_text)
        # Stage a separate copy for DRC zone refill; the evidence source never changes.
        stage = out / 'WORKING_COPY_ONLY'
        if stage.exists():
            shutil.rmtree(stage)
        shutil.copytree(project, stage)
        report['native_attempted'] = True
        sch = stage / (PROJECT + '.kicad_sch')
        pcb = stage / (PROJECT + '.kicad_pcb')
        cmds = {
            'ERC': ['sch', 'erc', '--format', 'report', '--severity-error', '--severity-warning',
                    '--exit-code-violations', '--output', str(out / 'E27S_ERC.rpt'), str(sch)],
            'DRC_REFILL': ['pcb', 'drc', '--format', 'report', '--all-track-errors', '--schematic-parity',
                           '--severity-error', '--severity-warning', '--exit-code-violations',
                           '--refill-zones', '--save-board', '--output', str(out / 'E27S_DRC_REFILL.rpt'), str(pcb)],
            'DRC_FINAL': ['pcb', 'drc', '--format', 'report', '--all-track-errors', '--schematic-parity',
                          '--severity-error', '--severity-warning', '--exit-code-violations',
                          '--output', str(out / 'E27S_DRC_FINAL.rpt'), str(pcb)],
        }
        exits = {}
        for label, argv in cmds.items():
            exits[label] = run_cli(exe, argv, stage, out / (label + '_CLI.log'))
        report['native_exit_codes'] = exits
        report['original_unpacked_source_unchanged'] = all(
            digest(project / rel) == digest(stage / rel) if rel != PROJECT + '.kicad_pcb' else True
            for rel in records)
        report['source_manifest_still_matches'] = bool(verify_manifest(project))
        erc = (out / 'E27S_ERC.rpt').read_text(errors='replace') if (out / 'E27S_ERC.rpt').is_file() else ''
        drc = (out / 'E27S_DRC_FINAL.rpt').read_text(errors='replace') if (out / 'E27S_DRC_FINAL.rpt').is_file() else ''
        evidence = {
            'erc_zero': bool(re.search(r'ERC messages:\s*0\s+Errors\s+0\s+Warnings', erc, re.I)),
            'drc_zero': bool(re.search(r'Found\s+0\s+DRC violations', drc, re.I)),
            'unconnected_zero': bool(re.search(r'Found\s+0\s+unconnected pads', drc, re.I)),
            'footprint_zero': bool(re.search(r'Found\s+0\s+Footprint errors', drc, re.I)),
            'parity_flag_enabled': True,
        }
        report['native_zero_evidence'] = evidence
        report['native_zero_gate'] = (all(v == 0 for v in exits.values())
                                      and all(evidence.values())
                                      and report['original_unpacked_source_unchanged']
                                      and report['source_manifest_still_matches'])
        report['status'] = 'NATIVE_ZERO_GATE_ONLY_FAB_HOLD' if report['native_zero_gate'] else 'NATIVE_FINDINGS_REQUIRE_FIX_FAB_HOLD'
        return 0 if report['native_zero_gate'] else 2
    except Exception as e:
        report['errors'].append(str(e))
        report['status'] = 'ERROR_FAB_HOLD'
        return 2
    finally:
        write_json(out / 'AUDIT_RESULT.json', report)
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    sys.exit(main())
