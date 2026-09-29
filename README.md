# Job Skill Demand Forecasting (Synthetic Data)

An end‑to‑end, beginner‑friendly project that forecasts **job skill demand** from synthetic job postings (India, 2023–2025), with an interactive **Streamlit + Plotly** dashboard.

## Tech
- Python: pandas, numpy
- Visualization: plotly, streamlit
- Forecasting: prophet
- NLP: nltk (optional)
- Extras: scikit-learn (optional), BeautifulSoup (placeholder)

## Structure
```
job-skill-demand-forecasting/
├─ app.py
├─ src/
│  ├─ data_load.py
│  ├─ preprocess.py
│  ├─ features.py
│  ├─ forecast.py
│  ├─ viz.py
│  ├─ nlp_utils.py
│  └─ utils.py
├─ data/
│  └─ synthetic_job_postings_2023_2025.csv
├─ scripts/
│  └─ setup_nltk.py
├─ assets/
├─ requirements.txt
├─ .gitignore
└─ README.md
```

## Quickstart
```
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python scripts/setup_nltk.py   # optional

streamlit run app.py
```

## GitHub
```
git init
git add .
git commit -m "Initial commit: Job Skill Demand Forecasting"
git branch -M main
git remote add origin https://github.com/<your-username>/job-skill-demand-forecasting.git
git push -u origin main
```