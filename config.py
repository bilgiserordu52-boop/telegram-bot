import os

# =========================
# ENV / DEPLOYMENT CONFIG
# =========================

TOKEN = os.getenv("BOT_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
STAGING_BRANCH = os.getenv("STAGING_BRANCH", "main")


# =========================
# SYSTEM BRAND CONFIG
# =========================

BOT_NAME = "NEURA CORE"
BOT_TAGLINE = "Self-Evolving AI System"
BOT_VERSION = "v0.7.5"
BOT_OWNER = "AI Platform Engine"


# =========================
# SECURITY DEFAULTS
# (ileride genişleteceğiz)
# =========================

ADMIN_LOCK = True
SAFE_MODE = True
DEBUG_MODE = False
