"""
Authentication manager for Locust users.
Handles token retrieval via /api/auth/login or fallback registration via /api/auth/register.
"""

import logging
from config import (
    DEFAULT_HEADERS,
    generate_unique_email,
    generate_company_name,
)

logger = logging.getLogger(__name__)


class UserAuthContext:
    def __init__(self):
        self.token = None
        self.user_id = None
        self.email = None
        self.full_name = None
        self.system_role = "member"
        self.company_id = None
        self.company_name = None
        self.project_roles = []
        self.project_ids = []

    @property
    def auth_headers(self):
        headers = dict(DEFAULT_HEADERS)
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers


def authenticate_user(client, email=None, password="Password123!", is_admin=False):
    """
    Attempts to log in with the specified email/password.
    If login fails (e.g. 401 or 404), dynamically registers a new account
    so the load test continues without requiring external manual DB seeding.
    """
    context = UserAuthContext()

    # Step 1: Attempt Login if email was provided
    if email:
        payload = {"email": email, "password": password}
        with client.post(
            "/api/auth/login",
            json=payload,
            headers=DEFAULT_HEADERS,
            name="/api/auth/login",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                data = response.json()
                context.token = data.get("accessToken") or data.get("token")
                context.user_id = data.get("userId")
                context.email = data.get("email")
                context.full_name = data.get("fullName")
                context.system_role = data.get("systemRole", "member")
                context.company_id = data.get("companyId")
                response.success()
                _populate_profile_and_projects(client, context)
                return context
            else:
                response.failure(f"Login failed with status {response.status_code}")

    # Step 2: Auto-register dynamic user if login wasn't successful or no email provided
    reg_email = generate_unique_email(prefix="admin" if is_admin else "dev")
    reg_company = generate_company_name()
    reg_payload = {
        "email": reg_email,
        "password": password,
        "fullName": f"LoadTest {'Admin' if is_admin else 'Developer'}",
        "isCompany": is_admin,
        "companyName": reg_company if is_admin else None,
    }

    with client.post(
        "/api/auth/register",
        json=reg_payload,
        headers=DEFAULT_HEADERS,
        name="/api/auth/register",
        catch_response=True,
    ) as response:
        if response.status_code in (200, 201):
            data = response.json()
            context.token = data.get("accessToken") or data.get("token")
            context.user_id = data.get("userId")
            context.email = data.get("email", reg_email)
            context.full_name = data.get("fullName")
            context.system_role = data.get("systemRole", "admin" if is_admin else "member")
            context.company_id = data.get("companyId")
            response.success()
            _populate_profile_and_projects(client, context)
            return context
        else:
            response.failure(f"Auto-registration failed: {response.status_code} {response.text}")
            return context


def _populate_profile_and_projects(client, context):
    """Fetches /api/auth/me and /api/projects to discover accessible project IDs."""
    if not context.token:
        return

    # Call /api/auth/me
    with client.get(
        "/api/auth/me",
        headers=context.auth_headers,
        name="/api/auth/me",
        catch_response=True,
    ) as response:
        if response.status_code == 200:
            profile = response.json()
            context.company_id = profile.get("companyId") or context.company_id
            context.company_name = profile.get("companyName")
            context.system_role = profile.get("systemRole", context.system_role)
            context.project_roles = profile.get("projectRoles") or []
            for pr in context.project_roles:
                pid = pr.get("projectId")
                if pid and pid not in context.project_ids:
                    context.project_ids.append(pid)
            response.success()
        else:
            response.failure(f"Failed to fetch profile: {response.status_code}")

    # Discover projects list
    with client.get(
        "/api/projects",
        headers=context.auth_headers,
        name="/api/projects",
        catch_response=True,
    ) as response:
        if response.status_code == 200:
            try:
                res_data = response.json()
                projects = []
                if isinstance(res_data, list):
                    projects = res_data
                elif isinstance(res_data, dict):
                    projects = res_data.get("projects") or res_data.get("content") or res_data.get("data") or []

                for proj in projects:
                    pid = proj.get("projectId") or proj.get("id")
                    if pid and pid not in context.project_ids:
                        context.project_ids.append(pid)
                response.success()
            except Exception as e:
                response.failure(f"Invalid JSON from /api/projects: {e}")
        else:
            response.failure(f"/api/projects returned {response.status_code}")
