import os

TOKEN = os.getenv("TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
STAGING_BRANCH = os.getenv("STAGING_BRANCH", "staging")

ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
