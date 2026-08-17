from fastapi import FastAPI

app = FastAPI(title="course_recommendation_api")

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
