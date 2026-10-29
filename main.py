import re
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Job Match Assistant")
model = SentenceTransformer("all-MiniLM-L6-v2")

SKILLS = [
    "python", "c#", "c++", "java", "javascript", "typescript", "sql",
    "html", "css", "react", "angular", ".net", "asp.net", "django",
    "flask", "fastapi", "docker", "kubernetes", "git", "aws", "azure",
    "linux", "rest", "api", "machine learning", "pandas", "tensorflow",
    "pytorch", "postgresql", "mongodb",
]


class MatchRequest(BaseModel):
    resume: str
    job: str


def find_skills(text):
    text = text.lower()
    found = set()
    for skill in SKILLS:
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"s?(?![a-z0-9])"
        if re.search(pattern, text):
            found.add(skill)
    if "asp.net" in found:
        found.add(".net")
    return found


@app.post("/match")
def match(req: MatchRequest):
    embeddings = model.encode([req.resume, req.job], convert_to_tensor=True)
    score = util.cos_sim(embeddings[0], embeddings[1]).item()

    resume_skills = find_skills(req.resume)
    job_skills = find_skills(req.job)

    return {
        "match_score": round(max(score, 0) * 100, 1),
        "matched_skills": sorted(job_skills & resume_skills),
        "missing_skills": sorted(job_skills - resume_skills),
    }

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("static/index.html")