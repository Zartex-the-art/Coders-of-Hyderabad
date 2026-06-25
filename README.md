# Coders of Hyderabad 

A data analytics project modeling the software engineering workforce of Hyderabad — inspired by the popular **Coders of Delhi** / **Coders of Bangalore** city-based analytics projects.

This project analyzes a synthetic dataset of **5,000 software engineers** across Hyderabad's major tech zones (HITEC City, Gachibowli, Financial District, Madhapur, Kondapur) to uncover patterns in compensation, skills demand, company hiring concentration, and AI tool adoption.

---

## Why Synthetic Data?

Hyderabad's tech workforce data is fragmented across job portals, salary-sharing sites, and professional networks — there is no single legal, public source that provides per-engineer salary, skill, and company data at this granularity. Scraping platforms like LinkedIn or Glassdoor for individual compensation data also violates their terms of service.

So instead of scraping, I **generated a synthetic dataset** with distributions calibrated against real, publicly reported 2026 Hyderabad market data (Levels.fyi, Glassdoor, ERI SalaryExpert, industry salary guides). This means no individual record corresponds to a real person, but the *patterns* — service vs. product company pay gaps, non-linear experience-salary growth, AI/ML skill premiums — mirror what's actually happening in the market.

| Segment | Fresher (0-1 YOE) | Senior (10+ YOE) |
|---|---|---|
| Service companies (TCS, Infosys, Wipro...) | ~₹5-6 LPA | ~₹28-32 LPA |
| Top-tier product companies (Microsoft, Amazon, Google...) | ~₹15-22 LPA | ~₹90-110+ LPA |

This calibration is what separates the dataset from a randomly generated one — every multiplier in the generation logic is grounded in a real reported number.

---

##  Project Structure

```
coders-of-hyderabad/
├── generate_data.py          # Synthetic dataset generator
├── coders_of_hyderabad.csv   # The dataset (5,000 rows × 23 columns)
├── analysis.ipynb            # Full EDA notebook with 9 charts + insights
├── sql_practice_set.md       # SQL queries (window functions, CTEs) against the dataset
└── README.md
```

---

##  Dataset Overview

**5,000 rows × 23 columns**, covering:

| Category | Columns |
|---|---|
| Identity | `engineer_id`, `name`, `age`, `gender` |
| Employment | `company`, `company_category`, `job_role`, `experience_years`, `work_mode`, `location_zone` |
| Background | `education`, `college`, `certification` |
| Skills | `skills`, `num_skills` |
| Compensation | `annual_ctc_lpa`, `annual_bonus_lpa`, `total_comp_lpa` |
| Activity & Visibility | `ai_tool_adopter`, `leetcode_problems_solved`, `github_contributions_yr`, `has_public_github`, `linkedin_followers` |

**Company categories modeled:** Service, Enterprise/MNC, Mid-tier Product, Startup, Top-tier Global Product — each with its own compensation multiplier, reflecting the real spread between IT-services firms and global product companies in Hyderabad's market.

---

##  Key Questions Explored

1. Which companies/company categories offer the highest compensation?
2. Which technical skills command the highest salary premium?
3. How strongly does experience influence compensation?
4. What is the compensation gap between company categories?
5. How widespread is AI tool adoption among engineers?
6. Which roles show the highest pay?
7. What patterns exist between coding activity (LeetCode/GitHub) and compensation?
8. How is Hyderabad's tech talent distributed across company types?

---

##  Key Findings

| Question | Finding |
|---|---|
| Highest-paying companies | Top-tier global product companies pay **3-4x** the median of service companies |
| Highest skill premium | GenAI/LLMs, Deep Learning, NLP, and System Design carry the largest pay premiums |
| Experience impact | **Non-linear** growth — sharpest jumps at 3-5 YOE and 8+ YOE |
| Category compensation gap | Service ≈ ₹11L median vs. Top-tier Global Product ≈ ₹33L median |
| AI tool adoption | Highest among junior engineers (0-2 YOE) and AI/ML specialists |
| Highest-paying roles | AI/ML Engineer and Data Engineer lead individual-contributor tracks |
| Coding activity vs. pay | **Weak** direct correlation — company category is the dominant pay driver, not LeetCode/GitHub volume |
| Talent distribution | Service companies still employ the largest single share, but product/MNC/GCC categories combined are catching up fast |

---

##  Tech Stack

- **Python** — pandas, NumPy, Faker (synthetic data generation)
- **Visualization** — Matplotlib, Seaborn
- **SQL** — SQLite, window functions, CTEs (see `sql_practice_set.md`)
- **Jupyter Notebook** — analysis & storytelling

---

##  How to Run

```bash
# 1. Install dependencies
pip install pandas numpy faker matplotlib seaborn jupyter

# 2. (Optional) Regenerate the dataset
python generate_data.py

# 3. Launch the notebook
jupyter notebook analysis.ipynb
```

The notebook is pre-executed — all charts and outputs render immediately on open, no need to re-run unless you want to verify it yourself or regenerate the dataset with different parameters.

---

##  Sample Visualizations

The notebook includes:
- Compensation distribution by company category (boxplots)
- Top 10 highest-paying companies
- Median compensation vs. experience, segmented by company category
- Top 15 highest-paying skills (premium analysis)
- AI tool adoption rates by role and experience band
- Coding activity (LeetCode/GitHub) vs. compensation scatter plots

---

##  Motivation

This project was built to demonstrate large-scale structured data analysis, statistical insight generation, and data storytelling — skills directly relevant to data analyst and data engineer roles. It follows the same city-based analytics format popularized by **Coders of Delhi** and **Coders of Bangalore**, applied to Hyderabad's distinct tech ecosystem.

---

##  Author

**Thumma Abhishek Reddy**
Final-year B.Tech CSE, Sreenidhi Institute of Science and Technology (SNIST)
[GitHub](https://github.com/) · [LinkedIn](https://linkedin.com/)

---

## 📄 License

This project is open-sourced for educational and portfolio purposes. The dataset is entirely synthetic — no real individuals or confidential company data are represented.
