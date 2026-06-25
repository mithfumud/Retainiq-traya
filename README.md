# RetainIQ

RetainIQ is a product analytics dashboard built around Traya Health's subscription model. Traya users stay on treatment for several months, regularly interact with coaches, and renew their subscriptions over time. The real challenge isn't knowing that churn happens. It's identifying which active subscribers are most likely to leave before their renewal date.

This project explores how a retention team could monitor user health, identify risk early, and prioritize coach outreach from a single dashboard.

**Live Demo:** https://retainiq-traya.streamlit.app/

---

## The Problem

Users rarely churn without warning. They gradually become less engaged.

They stop opening the app, miss coach check ins, skip progress photo uploads, and eventually choose not to renew their subscription.

At the same time, acquisition channels behave differently. Referral users often stay longer than paid social users, and different customer segments show different retention patterns.

A retention team needs answers to questions like:

* Where are users dropping off during the subscription journey?
* Which acquisition channels retain customers the longest?
* Which active subscribers should coaches contact this week?
* How much monthly revenue is currently at risk?

RetainIQ is my attempt at solving those problems using a synthetic dataset that mimics a subscription based healthcare business.

---

## Features

### Overview

The overview page provides a high level snapshot of the business.

It includes:

* Key business metrics
* Conversion funnel from hair test to Month 6 retention
* Retention by acquisition channel
* Channel quality matrix
* Retention by subscription plan
* Retention by stress level
* Executive insights

---

### Cohorts

The cohort view tracks how different signup months perform over time.

It includes:

* Monthly retention heatmap
* Month 3 retention trend
* Month 1 to Month 3 drop off analysis

This makes it easier to identify onboarding issues and compare different customer cohorts.

---

### Churn Risk

This page focuses only on active subscribers.

Each user receives a churn score based on recent engagement signals and is classified as:

* High Risk
* Medium Risk
* Low Risk

Users can be filtered by:

* Risk level
* Subscription plan
* Renewal window
* Acquisition channel

The dashboard also calculates Monthly Recurring Revenue at risk using each subscriber's actual plan value.

---

### Segments

The segmentation page breaks retention down across different customer groups.

Metrics are available by:

* Age group
* Subscription plan
* Hair loss stage
* Stress level

This helps identify long term behavioural trends across the customer base.

---

## Churn Scoring

The scoring model is intentionally simple and rule based. It is designed as an MVP rather than a machine learning model.

| Behaviour                       | Weight |
| ------------------------------- | ------ |
| No app activity for 14+ days    | +0.35  |
| No coach interaction in 30 days | +0.25  |
| No progress photos uploaded     | +0.20  |
| Renewal within 7 days           | +0.15  |
| Hair loss stage 4 or above      | +0.05  |

Scores are capped at **1.0**.

Risk categories:

* **High:** ≥ 0.70
* **Medium:** 0.40 to 0.69
* **Low:** < 0.40

The scoring logic lives in `churn.py` and can easily be replaced with a trained model using historical churn data.

---

## Project Structure

```text
├── app.py
├── churn.py
├── data.py
├── requirements.txt
```

**app.py**

Contains the Streamlit application, page layouts, styling, filters, and visualizations.

**churn.py**

Calculates churn scores and assigns risk categories.

**data.py**

Generates a synthetic dataset of 500 users with realistic behavioural patterns including acquisition channels, engagement, stress levels, renewals, and subscription plans.

---

## Tech Stack

* Python
* Streamlit
* Pandas
* Plotly
* NumPy

---

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The application will be available at:

```
http://localhost:8501
```

---

## Notes

* All customer data is synthetic and generated for demonstration purposes.
* Churn scores are based on business rules and not on a trained predictive model.
* Risk analysis is intentionally limited to active subscribers since the goal is to identify users who can still be retained.
* The project is built as a product case study and is not affiliated with Traya Health.

---

## Future Improvements

Some ideas if this were extended into a production product:

* Predictive churn model trained on historical user behaviour
* Automated coach task assignment
* Real time event ingestion
* CRM integration
* Email and WhatsApp intervention workflows
* Experiment tracking for retention initiatives

---

Built as a product analytics case study exploring customer retention for a subscription based healthcare business.
