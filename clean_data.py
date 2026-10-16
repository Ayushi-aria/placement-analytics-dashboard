import pandas as pd

folder = "placement_data/"
students = pd.read_csv(folder + "students_raw.csv")
companies = pd.read_csv(folder + "companies_raw.csv")
applications = pd.read_csv(folder + "applications_raw.csv")
offers = pd.read_csv(folder + "offers_raw.csv")

report = {}

# ---------- STUDENTS ----------
report["student duplicates removed"] = int(students.duplicated().sum())
students = students.drop_duplicates()

students["branch"] = students["branch"].str.strip()
branch_map = {"cse": "CSE", "computer sc": "CSE"}
before = students["branch"].copy()
students["branch"] = students["branch"].apply(lambda b: branch_map.get(b.lower(), b))
report["branch labels standardized"] = int((before != students["branch"]).sum())

report["missing CGPA filled"] = int(students["cgpa"].isna().sum())
students["cgpa"] = students.groupby("branch")["cgpa"].transform(lambda s: s.fillna(s.median()))

# ---------- COMPANIES ----------
companies["key"] = companies["company_name"].str.strip().str.lower()
alias = {"tata consultancy services": "tcs"}
companies["key"] = companies["key"].replace(alias)

canonical = companies.sort_values("company_id").drop_duplicates("key", keep="first")
id_map = companies["key"].map(dict(zip(canonical["key"], canonical["company_id"])))
company_id_map = dict(zip(companies["company_id"], id_map))

report["duplicate company records merged"] = len(companies) - len(canonical)
companies = canonical.drop(columns="key").reset_index(drop=True)

# ---------- APPLICATIONS ----------
applications["company_id"] = applications["company_id"].map(company_id_map)

stage_order = {"Applied": 1, "OA": 2, "Interview": 3, "Offer": 4}
applications["rank"] = applications["stage_reached"].map(stage_order)
n_before = len(applications)
applications = (applications.sort_values("rank")
                .drop_duplicates(["student_id", "company_id"], keep="last")
                .drop(columns="rank")
                .sort_values("application_id"))
report["duplicate applications removed"] = n_before - len(applications)

# ---------- OFFERS ----------
offers["company_id"] = offers["company_id"].map(company_id_map)
n_before = len(offers)
offers = offers.drop_duplicates(["student_id", "company_id"], keep="first")
report["duplicate offers removed"] = n_before - len(offers)

# ---------- SAVE ----------
students.to_csv(folder + "students_clean.csv", index=False)
companies.to_csv(folder + "companies_clean.csv", index=False)
applications.to_csv(folder + "applications_clean.csv", index=False)
offers.to_csv(folder + "offers_clean.csv", index=False)

print("\n=== DATA QUALITY REPORT ===")
for k, v in report.items():
    print(f"{k}: {v}")
print("\nFinal rows -> students:", len(students), "| companies:", len(companies),
      "| applications:", len(applications), "| offers:", len(offers))