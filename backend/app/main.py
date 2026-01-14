from fastapi import FastAPI

app = FastAPI(
    title="PAP Security Backend",
    description="Backend para deteção de logins suspeitos",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.get("/health")
def health():
    return {"status": "ok"}
