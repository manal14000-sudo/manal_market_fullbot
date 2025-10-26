# OPTIONAL placeholder for a TRADER bot (not used by Procfile)
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status":"running","role":"trader (placeholder)"}
