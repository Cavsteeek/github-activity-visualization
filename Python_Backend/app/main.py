from fastapi import FastAPI, HTTPException
from services import fetch_commits, fetch_contributors, fetch_issues
from pydantic import BaseModel

gapp = FastAPI()


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
