import httpx
import os
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("github_api_url")
TOKEN = os.getenv("github_api_token")
HEADERS = {"Authorization": f"token {TOKEN}"}


async def fetch_commits(owner: str, repo: str):
    url = f"{API_URL}{owner}/{repo}/commits"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Error fetching commits"
            )
        return response.json()


async def fetch_contributors(owner: str, repo: str):
    url = f"{API_URL}{owner}/{repo}/contributors"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Error fetching contributors"
            )
        return response.json()


async def fetch_issues(owner: str, repo: str):
    url = f"{API_URL}{owner}/{repo}/issues"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Error fetching issues"
            )
        return response.json()