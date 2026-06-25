"""
churn.py — Churn scoring logic for Traya RetainIQ.

Weights are manually calibrated for MVP; replace with a trained model
once real churn labels are available.

Score interpretation
--------------------
0.0 – 0.39  → Low    (stable, monitor monthly)
0.40 – 0.69 → Medium (at-risk, monitor weekly)
0.70 – 1.0  → High   (immediate coach action required)
"""


def calculate_churn_score(user_row) -> float:
    """Return a churn probability in [0, 1] based on five behavioural signals."""
    score = 0.0

    days_since_last_app = user_row["days_since_last_app"]
    coach_touches_30d   = user_row["coach_touches_30d"]
    photos_uploaded     = user_row["photos_uploaded"]
    days_to_renewal     = user_row["days_to_renewal"]
    hair_loss_stage     = user_row["hair_loss_stage"]

    # Signal weights — must sum to ≤ 1.0
    if days_since_last_app > 14:  score += 0.35   # biggest driver: disengagement
    if coach_touches_30d == 0:    score += 0.25   # no coach contact
    if photos_uploaded == 0:      score += 0.20   # no progress tracking
    if days_to_renewal <= 7:      score += 0.15   # renewal pressure
    if hair_loss_stage >= 4:      score += 0.05   # severe stage → frustration risk

    return round(min(score, 1.0), 2)


def get_risk_label(score: float) -> str:
    if score >= 0.70:
        return "High"
    if score >= 0.40:
        return "Medium"
    return "Low"


if __name__ == "__main__":
    test_user = {
        "days_since_last_app": 20,
        "coach_touches_30d":   0,
        "photos_uploaded":     0,
        "days_to_renewal":     5,
        "hair_loss_stage":     4,
    }
    score = calculate_churn_score(test_user)
    label = get_risk_label(score)
    print(f"score={score}, label=\"{label}\"")   # score=1.0, label="High"