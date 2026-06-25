import random
import pandas as pd

# ── Deterministic seed — stable KPIs across every restart ────────────────────
random.seed(42)

CHANNELS        = ["instagram", "youtube", "google", "referral", "organic"]
CHANNEL_WEIGHTS = [0.35, 0.20, 0.20, 0.15, 0.10]

# Churn probability by acquisition channel (used during data generation)
CHURN_PROB_BY_CHANNEL = {
    "instagram": 0.55,
    "youtube":   0.40,
    "google":    0.38,
    "referral":  0.22,
    "organic":   0.35,
}

MRR_BY_PLAN = {"basic": 999, "pro": 1499, "premium": 2199}

SIGNUP_MONTHS = [
    "2025-01", "2025-02", "2025-03",
    "2025-04", "2025-05", "2025-06",
]

FIRST_NAMES = [
    "Aarav","Aditi","Amit","Ananya","Arjun","Deepa","Divya","Gaurav",
    "Ishaan","Kavya","Kiran","Manish","Meera","Neha","Nikhil","Pooja",
    "Priya","Rahul","Raj","Riya","Rohit","Sachin","Sana","Shreya",
    "Siddharth","Sneha","Suresh","Tanvi","Tushar","Vikram",
]


def _days_since_last_app(stress_level: str, status: str) -> int:
    if stress_level == "high":
        low, high = 12, 30
    elif stress_level == "medium":
        low, high = 4, 18
    else:
        low, high = 0, 10

    if status == "churned":
        low  = min(30, low + 5)
        high = 30

    return random.randint(low, high)


customers = []

for i in range(1, 501):
    channel       = random.choices(CHANNELS, weights=CHANNEL_WEIGHTS, k=1)[0]
    plan          = random.choice(["basic", "pro", "premium"])
    stress_level  = random.choice(["low", "medium", "high"])
    months_active = random.randint(1, 6)

    if months_active >= 3:
        status = "active"
    else:
        churn_prob = CHURN_PROB_BY_CHANNEL[channel]
        status = "churned" if random.random() < churn_prob else "active"

    days_since_last_app = _days_since_last_app(stress_level, status)
    name = f"{random.choice(FIRST_NAMES)}_{i:03d}"

    customers.append({
        "id":                  i,
        "name":                name,
        "channel":             channel,
        "age_group":           random.choice(["18-25", "26-35", "36-45", "45+"]),
        "gender":              random.choice(["male", "female"]),
        "plan":                plan,
        "hair_loss_stage":     random.randint(1, 5),
        "stress_level":        stress_level,
        "diet":                random.choice(["veg", "non-veg", "vegan"]),
        "signup_month":        random.choice(SIGNUP_MONTHS),
        "months_active":       months_active,
        "status":              status,
        "days_since_last_app": days_since_last_app,
        "coach_touches_30d":   random.randint(0, 10),
        "photos_uploaded":     random.randint(0, 8),
        "days_to_renewal":     random.randint(1, 30),
        "mrr":                 MRR_BY_PLAN[plan],
        # Expose channel churn probability so the UI can surface it
        "channel_churn_prob":  CHURN_PROB_BY_CHANNEL[channel],
    })

df = pd.DataFrame(customers)