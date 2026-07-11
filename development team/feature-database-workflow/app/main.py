from fastapi import FastAPI
from app.database import engine, Base
from app.routers import projects, profile

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Video Editing SaaS")

app.include_router(projects.router, tags=["Projects"])
app.include_router(profile.router, tags=["Profile"])

@app.get("/")
def root():
    return {"message": "AI Video Editing SaaS Backend Running!"}
