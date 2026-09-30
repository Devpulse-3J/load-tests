"""
Configuration and test fixtures for DevPulse Locust Load Testing.
Target Domain: odineye.cse23.org
"""

import os
import uuid
import random

# Base host setting
TARGET_HOST = os.getenv("TARGET_HOST", "https://odineye.cse23.org")

# Credentials if pre-seeded accounts exist
TEST_USER_EMAIL = os.getenv("DEVPULSE_USER_EMAIL", "dev@demo.devpulse")
TEST_USER_PASSWORD = os.getenv("DEVPULSE_USER_PASSWORD", "Password123!")

ADMIN_USER_EMAIL = os.getenv("DEVPULSE_ADMIN_EMAIL", "admin@demo.devpulse")
ADMIN_USER_PASSWORD = os.getenv("DEVPULSE_ADMIN_PASSWORD", "Password123!")

# Fallback dynamic registration if seeded accounts fail
AUTO_REGISTER_USERS = os.getenv("AUTO_REGISTER_USERS", "true").lower() in ("1", "true", "yes")

# Default IDs for parameterized endpoints (can be discovered dynamically)
DEFAULT_PROJECT_ID = int(os.getenv("DEFAULT_PROJECT_ID", "1"))
DEFAULT_COMPANY_ID = int(os.getenv("DEFAULT_COMPANY_ID", "1"))
DEFAULT_REPO_ID = int(os.getenv("DEFAULT_REPO_ID", "1"))

# Common HTTP Headers
DEFAULT_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "DevPulse-LoadTest-Locust/1.0",
}

BROWSER_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
}


def generate_unique_email(prefix="loadtest"):
    """Generates a random valid email for user registration tests."""
    uid = uuid.uuid4().hex[:8]
    return f"{prefix}_{uid}@loadtest.devpulse.com"


def generate_company_name():
    """Generates a unique company name for organization registration."""
    uid = uuid.uuid4().hex[:6]
    return f"LoadTest Corp {uid.upper()}"


def generate_project_name():
    """Generates a unique project name for project creation tests."""
    uid = uuid.uuid4().hex[:6]
    return f"PerfProject-{uid}"
