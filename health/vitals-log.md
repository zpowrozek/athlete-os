# Recovery Vitals Log

> **Demo data** for a fictional athlete.

Auto-pulled each morning from COROS (via the `coros` MCP connector) by
`recovery-check` and `daily-brief`. If today's row is missing when either skill
runs, it pulls RHR, HRV, sleep, Sleep Score and Recovery % from COROS and
appends a row. The athlete can hand-edit the Notes column. Never delete
history; append one row per day.

- **Date** is the morning the reading informs (the night just slept).
- **Sleep (h)** is "Main Sleep (asleep)" only, in decimal hours.
- **Sleep Quality** is derived from Sleep Score: 0–59 Low, 60–79 Productive, 80–100 Optimal.
- **Recovery %** is a proprietary COROS metric: corroborating context, never the driver of a call.

| Date | RHR | HRV | Sleep (h) | Sleep Quality | Sleep Score | Recovery % | Notes |
|------|-----|-----|-----------|---------------|-------------|------------|-------|
| 2027-03-25 | 57 | 88 | 6.9 | Productive | 74 | 71 | Legs heavy after Wed brick |
| 2027-03-26 | 56 | 90 | 7.3 | Productive | 77 | 78 | |
| 2027-03-27 | 56 | 91 | 7.8 | Optimal | 82 | 84 | |
| 2027-03-28 | 55 | 93 | 8.1 | Optimal | 85 | 92 | |
| 2027-03-29 | 54 | 95 | 7.9 | Optimal | 84 | 96 | |
| 2027-03-30 | 54 | 97 | 7.6 | Optimal | 83 | 100 | |
| 2027-03-31 | 53 | 99 | 7.7 | Optimal | 86 | 100 | |
| 2027-04-01 | 55 | 94 | 7.4 | Optimal | 80 | 94 | Work deadline, felt like a poor night |
| 2027-04-02 | 56 | 91 | 7.2 | Productive | 78 | 88 | |
| 2027-04-03 | 55 | 93 | 7.5 | Optimal | 81 | 85 | |
| 2027-04-04 | 54 | 96 | 8.3 | Optimal | 88 | 97 | |
| 2027-04-05 | 54 | 95 | 7.8 | Optimal | 84 | 100 | |
| 2027-04-06 | 57 | 89 | 5.6 | Low | 58 | 76 | Up at 3 AM, couldn't get back to sleep |
| 2027-04-07 | 55 | 93 | 7.6 | Optimal | 83 | 88 | |
