from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .services import (
    fetch_commits,
    fetch_contributors,
    fetch_issues,
    fetch_pull_requests,
)

from typing import List


gapp = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:8000",
]

gapp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@gapp.get("/wel")
def root():
    return {"message": "My first project ykkk"}


# Endpoint to get commit data
@gapp.get("/commits")
async def get_commits(owner: str, repo: str):
    return await fetch_commits(owner, repo)


# Endpoint to get contributor data
@gapp.get("/contributors")
async def get_contributors(owner: str, repo: str):
    return await fetch_contributors(owner, repo)


# Endpoint to get issues and pull request data
@gapp.get("/issues")
async def get_issues(owner: str, repo: str):
    return await fetch_issues(owner, repo)


# Endpoint to get pull request data
@gapp.get("/pull_requests")
async def get_pull_requests(owner: str, repo: str):
    return await fetch_pull_requests(owner, repo)
