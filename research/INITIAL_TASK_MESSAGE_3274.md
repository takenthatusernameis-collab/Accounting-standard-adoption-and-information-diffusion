**Session 3274 task: BREAK THE VERIFICATION LOOP — do bounded no-cost exploratory work or formally close.**

Read research/HANDOFF.md and research/campaign_state.json (current_session 3273, next_session 3274, experiments_run 1066, last_verified_head e6d8d7c3e044a4fb73d87027e38fcf9291fe0b68).

Do NOT perform another delta-only verification pass. Sessions ~3200..3273 have each appended an identical verification row (E-1060..E-1066) without advancing any gate; the campaign is genuinely PARKED on real-world inputs (200 admitted treatment firms; free delisted/terminal-return price coverage) that are unobtainable under D-032. The protocol's operating principle (optimize for reliable knowledge, not activity) and adaptive-gate policy (do not merely write another blocker memo) require a different action.

Choose ONE and record it in research/experiment_ledger.csv and research/decision_log.md:
  (a) Bounded no-cost exploratory task (adaptive-gate policy v1): free-source inventory, coverage/count audit, power calculation from pre-outcome inputs, or identity-linkage validation. Report the precise admission/coverage gap. Register any new estimand as a new version; do not open or reuse PH-1 outcomes.
  (b) Formally close the campaign: write a PARKED/INCONCLUSIVE decision to research/decision_log.md with the quantified gap and the single highest-value next action.

Constraints unchanged: gates unchanged (cohort MET 12>=12; admitted_treatment_firm 0<200 FAIL; free_delisted_terminal_return coverage not established FAIL); primary_estimand inconclusive_by_construction; do not compute outcome returns; do not open PH-1; no paid sources; no workflows/trades. Two anomalies to carry forward: (1) duplicate E-3243 row (typo of E-1037, Session 3243) still in experiment_ledger.csv awaiting cleanup; (2) verify_artifacts.py raises SyntaxError at line 110 (pre-existing).
