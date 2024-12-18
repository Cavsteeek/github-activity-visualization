import httpx
import os
from fastapi import HTTPException
from dotenv import load_dotenv
from .models import Commit, Contributor, Issue, PullRequest
from datetime import datetime
from collections import defaultdict


load_dotenv()

API_URL = os.getenv("GITHUB_API_URL")
TOKEN = os.getenv("GITHUB_API_TOKEN")

# Ensure API_URL and TOKEN are set
if not API_URL:
    raise ValueError("API_URL is not set. Check your .env file.")
if not TOKEN:
    raise ValueError("GitHub API token is not set. Check your .env file.")

HEADERS = {"Authorization": f"Bearer {TOKEN}"}


# async def fetch_commits(owner: str, repo: str):
#     url = f"{API_URL}{owner}/{repo}/commits"
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=HEADERS)
#         if response.status_code != 200:
#             raise HTTPException(
#                 status_code=response.status_code, detail="Error fetching commits"
#             )
#         commits_data = response.json()
#         return [
#             Commit(
#                 sha=commit["sha"],
#                 message=commit["commit"]["message"],
#                 author_name=commit["commit"]["author"]["name"],
#                 date=commit["commit"]["author"]["date"],
#             )
#             for commit in commits_data
#         ]

# to return a lot of commits
# async def fetch_commits(owner: str, repo: str):
#     url = f"{API_URL}{owner}/{repo}/commits"
#     all_commits = []
#     page = 1

#     async with httpx.AsyncClient() as client:
#         while True:
#             response = await client.get(
#                 url, headers=HEADERS, params={"per_page": 100, "page": page}
#             )
#             if response.status_code != 200:
#                 raise HTTPException(
#                     status_code=response.status_code, detail="Error fetching commits"
#                 )
#             commits_data = response.json()

#             if not commits_data:  # Stop if there are no more commits
#                 break

#             all_commits.extend(
#                 Commit(
#                     sha=commit["sha"],
#                     message=commit["commit"]["message"],
#                     author_name=commit["commit"]["author"]["name"],
#                     date=commit["commit"]["author"]["date"],
#                 )
#                 for commit in commits_data
#             )
#             page += 1

#     return all_commits


# to return the top 10 commits
async def fetch_commits(owner: str, repo: str):
    url = f"{API_URL}{owner}/{repo}/commits"

    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.get(
            url, headers=HEADERS, params={"per_page": 10, "page": 1}
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Error fetching commits"
            )

        commits_data = response.json()
        return [
            Commit(
                sha=commit["sha"],
                message=commit["commit"]["message"],
                author_name=commit["commit"]["author"]["name"],
                date=commit["commit"]["author"]["date"],
            )
            for commit in commits_data
        ]


async def fetch_contributors(owner: str, repo: str):
    url = f"{API_URL}{owner}/{repo}/contributors"
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Error fetching contributors"
            )
        contributors_data = response.json()
        return [
            Contributor(
                login=contributor["login"],
                contributions=contributor["contributions"],
            )
            for contributor in contributors_data
        ]


async def fetch_issues(owner: str, repo: str):
    url = f"{API_URL}{owner}/{repo}/issues"
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Error fetching issues"
            )
        issues_data = response.json()
        return [
            Issue(
                title=issue["title"],
                state=issue["state"],
                created_at=issue["created_at"],
            )
            for issue in issues_data
        ]


# Fetch pull requests
async def fetch_pull_requests(owner: str, repo: str):
    url = f"{API_URL}{owner}/{repo}/pulls?state=all"
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Error fetching pull requests"
            )
        pull_requests_data = response.json()
        return [
            PullRequest(
                title=pull_request["title"],
                state=pull_request["state"],
                created_at=pull_request["created_at"],
            )
            for pull_request in pull_requests_data
        ]


def calculate_commit_frequency(commits):
    frequency = defaultdict(int)

    for commit in commits:
        commit_date = datetime.strptime(commit.date, "%Y-%m-%dT%H:%M:%SZ")
        week_year = commit_date.strftime("%Y-W%U")
        frequency[week_year] += 1

    return [{"date": date, "count": count} for date, count in frequency.items()]


def count_issues(issues):
    open_count = sum(1 for issue in issues if issue.state == "open")
    closed_count = sum(1 for issue in issues if issue.state == "closed")
    return {"open": open_count, "closed": closed_count}


def count_pull_requests(pull_requests):
    open_count = sum(1 for pr in pull_requests if pr.state == "open")
    merged_count = sum(1 for pr in pull_requests if pr.state == "closed")
    return {"open": open_count, "merged": merged_count}
