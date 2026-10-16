import pandas as pd
import numpy as np
import random
import os

np.random.seed(42)
random.seed(42)
os.makedirs("placement_data", exist_ok=True)

# ---------- STUDENTS ----------
branches = ["CSE", "ECE", "EE", "ME", "Civil", "MCA", "Maths & Computing"]
n_students = 300
students = pd.DataFrame({
    "student_id": range(1001, 1001 + n_students),
    "branch": np.random.choice(branches, n_students, p=[.25, .15, .12, .15, .08, .15, .10]),
    "cgpa": np.clip(np.random.normal(7.8, 0.8, n_students), 6.0, 9.9).round(2),
    "batch_year": 2026,
})

# messy: missing CGPA, branch spelling variants, duplicate rows
students.loc[students.sample(15, random_state=1).index, "cgpa"] = np.nan
variant_idx = students[students.branch == "CSE"].sample(20, random_state=2).index
students.loc[variant_idx, "branch"] = random.choices(["cse", "Computer Sc"], k=20)
students = pd.concat([students, students.sample(10, random_state=3)], ignore_index=True)

# ---------- COMPANIES ----------
base = [
    ("Tiger Analytics", "Analytics", 12), ("ZS Associates", "Consulting", 14),
    ("Amgen", "Pharma", 16), ("Axtria", "Analytics", 11), ("Sun King", "Fintech", 10),
    ("Hyperface", "Fintech", 9), ("ENTNT", "Software", 8), ("TCS", "IT Services", 4),
    ("Infosys", "IT Services", 4), ("Wipro", "IT Services", 4), ("Accenture", "IT Services", 6),
    ("Deloitte", "Consulting", 10), ("Goldman Sachs", "Finance", 25), ("Microsoft", "Software", 40),
    ("Flipkart", "E-commerce", 30), ("Mu Sigma", "Analytics", 7), ("Fractal", "Analytics", 11),
    ("Tata Steel", "Core", 8), ("L&T", "Core", 7), ("Cognizant", "IT Services", 5),
]
companies = pd.DataFrame(base, columns=["company_name", "sector", "ctc_lpa"])
companies.insert(0, "company_id", range(1, len(companies) + 1))

# messy: same company, different spelling, new id
variants = pd.DataFrame([
    (21, "tiger analytics", "Analytics", 12), (22, "ZS Associates ", "Consulting", 14),
    (23, "AMGEN", "Pharma", 16), (24, "Tata Consultancy Services", "IT Services", 4),
], columns=companies.columns)
companies = pd.concat([companies, variants], ignore_index=True)

# ---------- APPLICATIONS ----------
n_apps = 1500
stages = ["Applied", "OA", "Interview", "Offer"]
applications = pd.DataFrame({
    "application_id": range(1, n_apps + 1),
    "student_id": np.random.choice(students.student_id.unique(), n_apps),
    "company_id": np.random.choice(companies.company_id, n_apps),
    "stage_reached": np.random.choice(stages, n_apps, p=[.45, .30, .15, .10]),
})

# messy: duplicate (student, company) applications
dups = applications.sample(40, random_state=4).copy()
dups["application_id"] = range(n_apps + 1, n_apps + 41)
applications = pd.concat([applications, dups], ignore_index=True)

# ---------- OFFERS ----------
offers = applications[applications.stage_reached == "Offer"][["student_id", "company_id"]].drop_duplicates()
offers = offers.merge(companies[["company_id", "ctc_lpa"]], on="company_id")
offers["ctc_lpa"] = (offers.ctc_lpa * np.random.uniform(0.9, 1.15, len(offers))).round(2)
offers.insert(0, "offer_id", range(1, len(offers) + 1))

# ---------- SAVE ----------
students.to_csv("placement_data/students_raw.csv", index=False)
companies.to_csv("placement_data/companies_raw.csv", index=False)
applications.to_csv("placement_data/applications_raw.csv", index=False)
offers.to_csv("placement_data/offers_raw.csv", index=False)

print("students:", len(students), "| companies:", len(companies),
      "| applications:", len(applications), "| offers:", len(offers))