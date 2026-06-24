"""
Coders of Hyderabad — Synthetic Dataset Generator
===================================================
Generates a realistic synthetic dataset modeling ~5,000 software engineers
working in Hyderabad's tech ecosystem (HITEC City, Gachibowli, Financial District).

This is a SYNTHETIC dataset — no real individuals or actual company salary
data are used. Distributions are modeled on publicly reported 2026 market
patterns (Levels.fyi, Glassdoor, ERI SalaryExpert, industry salary guides):
  - Service companies (TCS/Infosys/Wipro tier):  fresher ~3.5-6 LPA,  senior ~18-30 LPA
  - Mid-tier product companies:                   fresher ~8-15 LPA,  senior ~35-60 LPA
  - Top-tier / global product (FAANG-equivalent):  fresher ~15-30 LPA, senior ~60 LPA-1.2 Cr+
  - AI/ML, Cloud, and System Design skills carry a measurable salary premium
  - Salary growth is non-linear: steep jump at 3-5 YOE, steeper again 8+ YOE

Run: python3 generate_data.py
Output: coders_of_hyderabad.csv
"""

import numpy as np
import pandas as pd
from faker import Faker
import random

# ----------------------------------------------------------------------------
# Reproducibility
# ----------------------------------------------------------------------------
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
fake = Faker("en_IN")
Faker.seed(SEED)

N = 5000

# ----------------------------------------------------------------------------
# Reference data: companies, by category and base pay multiplier tier
# ----------------------------------------------------------------------------
COMPANIES = {
    "Service": {
        "names": ["TCS", "Infosys", "Wipro", "Tech Mahindra", "Cognizant",
                   "Capgemini", "HCLTech", "L&T Infotech", "Mindtree", "Virtusa"],
        "base_multiplier": 1.00,
        "weight": 0.40,  # 40% of Hyderabad SWE workforce
    },
    "Enterprise/MNC": {
        "names": ["Deloitte", "Accenture", "JPMorgan Chase", "Wells Fargo",
                   "Qualcomm", "Cyient", "DXC Technology", "Genpact", "CGI"],
        "base_multiplier": 1.55,
        "weight": 0.22,
    },
    "Mid-tier Product": {
        "names": ["Darwinbox", "Salesforce", "Postman", "Zeta", "Pega Systems",
                   "ValueLabs", "Sahaj Software", "CtrlS", "Innominds"],
        "base_multiplier": 2.10,
        "weight": 0.18,
    },
    "Startup": {
        "names": ["Zartex SEI", "Hyrise Labs", "Loopwork", "Nexcore AI",
                   "Bharosa Tech", "Skyforge Robotics", "Vatsa Analytics"],
        "base_multiplier": 1.35,
        "weight": 0.08,
    },
    "Top-tier Global Product": {
        "names": ["Microsoft", "Amazon", "Google", "Uber", "Meta",
                   "Oracle", "Apple", "Salesforce R&D", "Goldman Sachs", "ServiceNow"],
        "base_multiplier": 3.40,
        "weight": 0.12,
    },
}

CATEGORY_LIST = list(COMPANIES.keys())
CATEGORY_WEIGHTS = [COMPANIES[c]["weight"] for c in CATEGORY_LIST]

ROLES = [
    "Backend Engineer", "Frontend Engineer", "Fullstack Engineer",
    "AI/ML Engineer", "Data Engineer", "DevOps/Infra Engineer",
    "QA/SDET Engineer", "Mobile Engineer",
]
# Role salary multiplier (relative to baseline backend role)
ROLE_MULTIPLIER = {
    "Backend Engineer": 1.00,
    "Frontend Engineer": 0.95,
    "Fullstack Engineer": 1.03,
    "AI/ML Engineer": 1.35,
    "Data Engineer": 1.18,
    "DevOps/Infra Engineer": 1.12,
    "QA/SDET Engineer": 0.82,
    "Mobile Engineer": 0.97,
}
ROLE_WEIGHTS = [0.20, 0.14, 0.18, 0.12, 0.13, 0.11, 0.07, 0.05]

SKILLS_POOL = [
    "Python", "Java", "JavaScript", "TypeScript", "Go", "C++", "SQL",
    "React", "Node.js", "Spring Boot", "Django", "AWS", "Azure", "GCP",
    "Docker", "Kubernetes", "Terraform", "Machine Learning", "Deep Learning",
    "NLP", "LLMs/GenAI", "Data Engineering", "Apache Spark", "System Design",
    "Microservices", "CI/CD", "MongoDB", "PostgreSQL", "Redis", "Kafka",
]
# Skills that carry an extra salary premium when present
PREMIUM_SKILLS = {
    "Machine Learning": 0.06, "Deep Learning": 0.07, "LLMs/GenAI": 0.10,
    "System Design": 0.05, "Kubernetes": 0.04, "AWS": 0.03, "Azure": 0.03,
    "GCP": 0.03, "NLP": 0.06, "Apache Spark": 0.04, "Kafka": 0.03,
}

EDUCATION = ["B.Tech", "B.E.", "M.Tech", "MCA", "B.Sc CS", "Dual Degree (B.Tech+M.Tech)"]
EDUCATION_WEIGHTS = [0.45, 0.20, 0.16, 0.08, 0.07, 0.04]

COLLEGES = [
    "IIT Hyderabad", "BITS Pilani Hyderabad", "Osmania University",
    "JNTU Hyderabad", "SNIST", "CBIT", "VNR VJIET", "Mahindra University",
    "Vasavi College of Engineering", "Vardhaman College of Engineering",
    "Other Tier-2 College", "Other Tier-3 College",
]
COLLEGE_WEIGHTS = [0.03, 0.04, 0.07, 0.09, 0.06, 0.07, 0.06, 0.05, 0.05, 0.05, 0.24, 0.19]

WORK_MODE = ["Work From Office", "Hybrid", "Remote"]
WORK_MODE_WEIGHTS = [0.45, 0.42, 0.13]

CERTIFICATIONS = [
    "None", "AWS Certified Solutions Architect", "Azure Fundamentals (AZ-900)",
    "Google Cloud Associate Engineer", "CKA (Kubernetes)", "PMP",
    "Databricks Certified Data Engineer", "Coursera ML Specialization",
]
CERT_WEIGHTS = [0.42, 0.13, 0.10, 0.08, 0.06, 0.05, 0.08, 0.08]


def sample_experience():
    """Right-skewed experience distribution: lots of junior engineers, fewer senior."""
    return min(20, max(0, int(np.random.gamma(shape=2.0, scale=2.3))))


def sample_skills(role):
    """Pick 4-9 skills, biased toward role-relevant ones."""
    k = random.randint(4, 9)
    role_bias = {
        "AI/ML Engineer": ["Python", "Machine Learning", "Deep Learning", "NLP", "LLMs/GenAI"],
        "Data Engineer": ["SQL", "Apache Spark", "Data Engineering", "Kafka", "Python"],
        "DevOps/Infra Engineer": ["Docker", "Kubernetes", "Terraform", "AWS", "CI/CD"],
        "Frontend Engineer": ["JavaScript", "TypeScript", "React"],
        "Backend Engineer": ["Java", "Python", "Spring Boot", "SQL", "Microservices"],
        "Fullstack Engineer": ["JavaScript", "React", "Node.js", "SQL"],
        "Mobile Engineer": ["JavaScript", "TypeScript"],
        "QA/SDET Engineer": ["Python", "Java", "CI/CD"],
    }
    biased = role_bias.get(role, [])
    chosen = set(random.sample(biased, min(len(biased), k // 2))) if biased else set()
    remaining_pool = [s for s in SKILLS_POOL if s not in chosen]
    chosen.update(random.sample(remaining_pool, max(0, k - len(chosen))))
    return sorted(chosen)


def compute_salary(category, role, experience, skills, education):
    """
    Builds CTC (in LPA - Lakhs Per Annum) from a baseline x multipliers.
    Baseline calibrated so:
      Service fresher  ~ 4.2 LPA      Service senior(10y)  ~ 22 LPA
      Top-tier fresher ~ 14 LPA       Top-tier senior(10y) ~ 75+ LPA
    """
    base = 4.2  # baseline fresher service-company salary in LPA

    # Experience curve: non-linear, steep jumps at 3-5y and 8y+
    if experience <= 2:
        exp_mult = 1.0 + experience * 0.18
    elif experience <= 5:
        exp_mult = 1.36 + (experience - 2) * 0.30
    elif experience <= 8:
        exp_mult = 2.26 + (experience - 5) * 0.42
    else:
        exp_mult = 3.52 + (experience - 8) * 0.55

    company_mult = COMPANIES[category]["base_multiplier"]
    role_mult = ROLE_MULTIPLIER[role]

    skill_premium = 1.0 + sum(PREMIUM_SKILLS.get(s, 0) for s in skills) * 0.5
    skill_premium = min(skill_premium, 1.45)  # cap stacking

    edu_mult = 1.10 if education in ("M.Tech", "Dual Degree (B.Tech+M.Tech)") else 1.0

    noise = np.random.normal(1.0, 0.09)  # market noise / negotiation variance
    noise = max(0.7, min(1.35, noise))

    salary = base * exp_mult * company_mult * role_mult * skill_premium * edu_mult * noise
    return round(salary, 2)


def compute_bonus(salary_lpa, category):
    """Annual bonus as a % of CTC, higher at product/top-tier companies."""
    bonus_pct = {
        "Service": 0.06, "Enterprise/MNC": 0.09, "Mid-tier Product": 0.12,
        "Startup": 0.07, "Top-tier Global Product": 0.16,
    }[category]
    bonus_pct *= np.random.uniform(0.6, 1.4)
    return round(salary_lpa * bonus_pct, 2)


def sample_ai_adoption(role, experience):
    """AI tool adoption (Copilot/ChatGPT/Cursor etc.) - higher among junior + AI/ML folks."""
    base_prob = 0.55
    if role == "AI/ML Engineer":
        base_prob += 0.25
    if experience <= 3:
        base_prob += 0.15
    elif experience >= 10:
        base_prob -= 0.10
    prob = min(0.97, max(0.15, base_prob))
    return np.random.rand() < prob


def sample_coding_activity():
    """Simulated public coding profile activity: LeetCode-solved count + GitHub contributions/yr."""
    leetcode = max(0, int(np.random.gamma(shape=1.3, scale=130)))
    leetcode = min(leetcode, 2500)
    github_contribs = max(0, int(np.random.gamma(shape=1.5, scale=180)))
    github_contribs = min(github_contribs, 3000)
    return leetcode, github_contribs


def sample_gender():
    return np.random.choice(["Male", "Female", "Other"], p=[0.72, 0.27, 0.01])


def sample_visibility():
    """LinkedIn followers + has public GitHub flag — proxy for 'professional visibility'."""
    linkedin_followers = max(0, int(np.random.gamma(shape=1.2, scale=350)))
    has_public_github = np.random.rand() < 0.68
    return linkedin_followers, has_public_github


# ----------------------------------------------------------------------------
# Build records
# ----------------------------------------------------------------------------
records = []
for i in range(N):
    category = np.random.choice(CATEGORY_LIST, p=CATEGORY_WEIGHTS)
    company = random.choice(COMPANIES[category]["names"])
    role = np.random.choice(ROLES, p=ROLE_WEIGHTS)
    experience = sample_experience()
    gender = sample_gender()
    age = min(58, max(21, 22 + experience + np.random.randint(-1, 3)))
    education = np.random.choice(EDUCATION, p=EDUCATION_WEIGHTS)
    college = np.random.choice(COLLEGES, p=COLLEGE_WEIGHTS)
    skills = sample_skills(role)
    certification = np.random.choice(CERTIFICATIONS, p=CERT_WEIGHTS)
    work_mode = np.random.choice(WORK_MODE, p=WORK_MODE_WEIGHTS)
    salary = compute_salary(category, role, experience, skills, education)
    bonus = compute_bonus(salary, category)
    ai_adopter = sample_ai_adoption(role, experience)
    leetcode_solved, github_contribs = sample_coding_activity()
    linkedin_followers, has_public_github = sample_visibility()
    location_zone = np.random.choice(
        ["HITEC City", "Gachibowli", "Financial District", "Madhapur", "Kondapur"],
        p=[0.28, 0.24, 0.20, 0.16, 0.12],
    )

    records.append({
        "engineer_id": f"COH{i+1:05d}",
        "name": fake.name(),
        "age": age,
        "gender": gender,
        "company": company,
        "company_category": category,
        "job_role": role,
        "experience_years": experience,
        "education": education,
        "college": college,
        "location_zone": location_zone,
        "work_mode": work_mode,
        "skills": ", ".join(skills),
        "num_skills": len(skills),
        "certification": certification,
        "annual_ctc_lpa": salary,
        "annual_bonus_lpa": bonus,
        "total_comp_lpa": round(salary + bonus, 2),
        "ai_tool_adopter": ai_adopter,
        "leetcode_problems_solved": leetcode_solved,
        "github_contributions_yr": github_contribs,
        "has_public_github": has_public_github,
        "linkedin_followers": linkedin_followers,
    })

df = pd.DataFrame(records)

# Light realistic missingness (real-world datasets are never fully clean)
missing_idx = df.sample(frac=0.015, random_state=SEED).index
df.loc[missing_idx, "certification"] = np.nan

out_path = "coders_of_hyderabad.csv"
df.to_csv(out_path, index=False)

print(f"Generated {len(df)} records -> {out_path}")
print(df.head(3).to_string())
print("\nCompany category distribution:")
print(df["company_category"].value_counts())
print("\nSalary (Total Comp LPA) summary:")
print(df["total_comp_lpa"].describe().round(2))
