# Traya · RetainIQ

A Streamlit analytics dashboard for tracking customer retention and churn risk using synthetic Traya Health subscription data.

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## File structure

| File | Role |
|---|---|
| `churn.py` | Churn scoring logic — `calculate_churn_score()` and `get_risk_label()` |
| `data.py` | Synthetic data generator — produces a 500-row `df` with `random.seed(42)` for stable KPIs |
| `app.py` | Streamlit UI — four pages, `@st.cache_data` on scoring, active-user scoping |
| `requirements.txt` | Pinned dependencies |

## Pages

- **Overview** — Headline KPIs, conversion funnel, channel quality matrix (volume vs retention scatter), plan and stress-level breakdowns.
- **Cohorts** — Signup-month cohort retention heatmap (M1–M6), M3 trend line, M1→M3 drop-off bar chart.
- **Churn Risk** — Risk counts scoped to **active users only**, filterable risk table, signal weights, donut, score histogram. MRR-at-risk calculated from each user's actual plan.
- **Segments** — Retention by age group, plan, hair loss stage, and stress level. AI Coach Insight card highlights the highest-risk overlap.

## Key design decisions

- `random.seed(42)` in `data.py` — KPIs are stable across restarts.
- `@st.cache_data` on `build_scored_df()` — widget interactions don't recompute churn scores.
- All risk analysis scoped to `status == "active"` — churned users inflate counts and add noise to ops tables.
- MRR-at-risk uses `df["mrr"].sum()` not a hardcoded price — accurate across mixed plans.
- `channel_churn_prob` is now a column in `df` — surfaced in the Channel Quality Matrix on the Overview page.