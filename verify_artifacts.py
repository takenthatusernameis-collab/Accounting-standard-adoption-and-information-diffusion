import csv, hashlib, json, os

# Verify panel_v1.2.csv
with open('research/panel_v1.2.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
print('panel_v1.2.csv: %d rows, %d cols' % (len(rows), len(rows[0]) if rows else 0))
print('  non-empty timing_cohort: %d' % sum(1 for r in rows if r.get('timing_cohort', '') != ''))
print('  distinct timing_cohort: %d' % len(set(r.get('timing_cohort', '') for r in rows if r.get('timing_cohort', '') != '')))
print('  cohort values: %s' % sorted(set(r.get('timing_cohort', '') for r in rows if r.get('timing_cohort', '') != '')))
print('  non-empty T_A: %d' % sum(1 for r in rows if r.get('T_A', '') != ''))
print('  T_A jurisdictions: %s' % sorted(set(r.get('T_A', '') for r in rows if r.get('T_A', '') != '')))
print('  in_registered_panel=true: %d' % sum(1 for r in rows if r.get('in_registered_panel', '') == 'true'))
print('  filing_route distinct: %s' % sorted(set(r.get('filing_route', '') for r in rows)))
print('  price_venue_set distinct: %s' % sorted(set(r.get('price_venue_set', '') for r in rows)))

print('')

# Verify panel_v1.1.csv
with open('research/panel_v1.1.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
print('panel_v1.1.csv: %d rows, in_registered_panel=true: %d' % (len(rows), sum(1 for r in rows if r.get('in_registered_panel', '') == 'true'))
print('  non-empty T_A: %d' % sum(1 for r in rows if r.get('T_A', '') != ''))
print('  T_A jurisdictions: %s' % sorted(set(r.get('T_A', '') for r in rows if r.get('T_A', '') != '')))

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
EOF