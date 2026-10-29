# Job Match Assistant

Paste your CV and a job posting, get a match score and a list of matched and missing skills.

**Live demo:** https://job-match-assistant-46so.onrender.com
*(Hosted on a free tier: the first load may take up to a minute while it wakes up.)*

## How it works

- **Match score:** both texts are converted to embeddings with the `all-MiniLM-L6-v2` sentence-transformers model, and the score is their cosine similarity.
- **Skill gap:** a keyword list of common tech skills is searched in both texts. Skills in the job but not in the CV are shown as missing.
- **API:** FastAPI backend with a single `POST /match` endpoint (interactive docs at `/docs`), plus a simple HTML page.

## Tech stack

Python, FastAPI, sentence-transformers, HTML/CSS/JavaScript, deployed on Render.

## Run locally

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

Then open http://127.0.0.1:8000/

## Limitations and next steps

- The skill list is hand-written and covers about 30 common skills.
- The score is raw semantic similarity, so it is best used for comparing jobs against each other rather than as an absolute number.
- Ideas: extract skills with an NLP model instead of a fixed list, support PDF upload for CVs.