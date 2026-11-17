# INITIAL TASK MESSAGE — Session 2761

Read the prior agent task from the durable handoff and complete it. Then update the handoff and write a clear initial task message for the next agent.

1. Verify committed state first (git fetch origin main; git status; parse campaign_state.json; re-derive panel counts; rebuild panel_v1.2.csv via scripts/build_panel.py --out; cmp clean; count source/experiment/decision/results rows live; confirm last_verified_head matches HEAD).
2. Report park honestly: cohort gate MET (12>=12); filing_route and price_venue_set PENDING all 141 PH-1 rows; admitted treatment-firm count 0 < 200 (FAIL); free delisted/terminal-return price coverage not established (FAIL, D-042/E-047); primary estimand inconclusive by construction; PH-1 closed. Do not compute outcome-period returns or inspect outcome data.
3. Only advance gates via free lawful sources; no paid data, credentials, GitHub Actions, workflow changes.
4. Closed probes: do not repeat unless environment changes.
5. Update durable handoff: prepend session note; keep last 10 blocks; update campaign_state.json; append ledger row raw text (11 fields); normalise trailing newlines.
6. Two-runner/append cautions.
7. Naming/state-reconciliation cautions: session 2761 writes INITIAL_TASK_MESSAGE_2761.md; keep older files intact.