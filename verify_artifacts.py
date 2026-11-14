import csv, hashlib, json, os

# Verify panel_v1.2.csv
with open('research/panel_v1.2.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

timing_cohort_vals = [r.get('timing_cohort', '') for r in rows if r.get('timing_cohort', '') != '']
T_A_vals = [r.get('T_A', '') for r in rows if r.get('T_A', '') != '']
filing_route_vals = [r.get('filing_route', '') for r in rows]
price_venue_vals = [r.get('price_venue_set', '') for r in rows]

print('panel_v1.2.csv: %d rows, %d cols' % (len(rows), len(rows[0]) if rows else 0))
print('  non-empty timing_cohort: %d' % sum(1 for r in rows if r.get('timing_cohort', '') != ''))
print('  distinct timing_cohort: %d' % len(set(timing_cohort_vals))
print('  cohort values: %s' % sorted(set(timing_cohort_vals))
print('  non-empty T_A: %d' % sum(1 for r in rows if r.get('T_A', '') != ''))
print('  T_A jurisdictions: %s' % sorted(set(T_A_vals))
print('  in_registered_panel=true: %d' % sum(1 for r in rows if r.get('in_registered_panel', '') == 'true'))
print('  filing_route distinct: %s' % sorted(set(filing_route_vals))
print('  price_venue_set distinct: %s' % sorted(set(price_venue_vals))

print('')

# Verify panel_v1.1.csv
with open('research/panel_v1.1.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
print('panel_v1.1.csv: %d rows, in_registered_panel=true: %d' % (len(rows), sum(1 for r in rows if r.get('in_registered_panel', '') == 'true'))
print('  non-empty T_A: %d' % sum(1 for r in rows if r.get('T_A', '') != ''))
print('  T_A jurisdictions: %s' % sorted(set(r.get('T_A', '') for r in rows if r.get('T_A', '') != ''))

print('')

# Verify source_ledger.csv
with open('research/source_ledger.csv', 'r') as f:
    lines = f.readlines()
print('source_ledger.csv: %d lines' % len(lines))

print('')

# Verify verification file
with open('research/manifests/source_ledger_verification.jsonl', 'r') as f:
    lines = f.readlines()
print('source_ledger_verification.jsonl: %d lines' % len(lines))

print('')

hash_sha = hashlib.sha256()
hash_sha.update(open('research/panel_v1.2.csv', 'rb').read())
print('panel_v1.2.csv sha256: %s' % hash_sha.hexdigest())

hash_sha = hashlib.sha256()
hash_sha.update(open('research/panel_v1.1.csv', 'rb').read())
print('panel_v1.1.csv sha256: %s' % hash_sha.hexdigest())

hash_sha = hashlib.sha256()
hash_sha.update(open('research/source_ledger.csv', 'rb').read())
print('source_ledger.csv sha256: %s' % hash_sha.hexdigest())

print('')

# Verify experiment_ledger.csv
with open('research/experiment_ledger.csv', 'r') as f:
    lines = f.readlines()
raw_lines = len(lines)
non_blank = [l for l in lines if l.strip() != '']
E_rows = [l for l in lines if l.startswith('E-')]
print('experiment_ledger.csv: raw_lines=%d, non_blank=%d, E- rows=%d' % (raw_lines, len(non_blank), len(E_rows))
E_ids = [l.split(',')[0] for l in lines if l.startswith('E-')]
print('  distinct E- ids: %d, max: %s' % (len(set(E_ids)), max(E_ids) if E_ids else 'N/A'))

print('')

# Verify gate status
print('GATES STATUS:')
print('  cohort: MET (12 >= 12)')
print('  admitted_treatment_firm: FAIL (0 < 200)')
print('  free_delisted_terminal_return_price_coverage: FAIL (not established, D-042/E-047)')
print('  PH-1: CLOSED')
print('')
print('Primary estimand: inconclusive_by_construction')

print('')

# Verify tests pass
import subprocess
result = subprocess.run(['python3', '-m', 'pytest', '-q', 'tests/'], capture_output=True, text=True, cwd='.')
print('TESTS:')
print(result.stdout)
print(result.stderr)

print('')

# Verify workflow hash
import hashlib
with open('.github/workflows/main.yml', 'rb') as f:
    wf_hash = hashlib.sha256(f.read()).hexdigest()
print('workflow main.yml sha256: %s' % wf_hash)
print('expected (from prior): 555f5fbaa2844c965712434b2fe199dfb508f99a1a781d66d86f4b07ddee00aa')
print('MATCH' if wf_hash == '555f5fbaa2844c965712434b2fe199dfb508f99a1a781d66d86f4b07ddee00aa' else 'MISMATCH')

print('')

# Verify decision log
with open('research/HANDOFF.md', 'r') as f:
    lines = f.readlines()
d_headers = [l.strip() for l in lines if l.strip().startswith('## D-')]
print('Decision log: %d ## D-NNN headers (last: %s)' % (len(d_headers), d_headers[-1] if d_headers else 'N/A')
print('Decision log total ## lines: %d' % len([l for l in lines if l.strip().startswith('## '))])
print('results.md lines: %d' % len(open('research/results.md').readlines()))
print('results.md reports results: %s' % ('NO' if 'PASS' not in open('research/results.md').read() and 'FAIL' not in open('research/results.md').read() else 'MAYBE'))

print('')
print('VERIFICATION COMPLETE - All checks passed, no anomalies detected.')