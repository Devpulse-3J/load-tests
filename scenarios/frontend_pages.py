"""
Scenario: Frontend Web Application Page Loads and SSR Navigation.
Tests Next.js routing, server-side rendering, and page delivery on odineye.cse23.org.
"""

from locust import task, tag
from common.base_user import BaseDevPulseUser
from config import BROWSER_HEADERS


class FrontendPageUser(BaseDevPulseUser):
    abstract = True
    """
    Simulates real browser visitors browsing through the DevPulse web application.
    Covers public landing pages, auth screens, workspaces, and admin interfaces.
    """

    @tag("frontend", "public", "landing")
    @task(5)
    def view_landing_page(self):
        """GET / - Landing page"""
        self.safe_get("/", name="UI: / (Landing Page)", headers=BROWSER_HEADERS)

    @tag("frontend", "auth", "login_page")
    @task(3)
    def view_login_page(self):
        """GET /login - User Login Page"""
        self.safe_get("/login", name="UI: /login", headers=BROWSER_HEADERS)

    @tag("frontend", "auth", "admin_login_page")
    @task(2)
    def view_admin_login_page(self):
        """GET /adminlogin - Admin Login Page"""
        self.safe_get("/adminlogin", name="UI: /adminlogin", headers=BROWSER_HEADERS)

    @tag("frontend", "auth", "register_page")
    @task(2)
    def view_register_page(self):
        """GET /register - User & Company Registration Page"""
        self.safe_get("/register", name="UI: /register", headers=BROWSER_HEADERS)

    @tag("frontend", "workspace", "select_project")
    @task(3)
    def view_select_project_page(self):
        """GET /select-project - Project Picker"""
        self.safe_get("/select-project", name="UI: /select-project", headers=BROWSER_HEADERS)

    @tag("frontend", "workspace", "dashboard")
    @task(4)
    def view_dashboard_page(self):
        """GET /dashboard - Main Workspace Dashboard"""
        self.safe_get("/dashboard", name="UI: /dashboard", headers=BROWSER_HEADERS)

    @tag("frontend", "workspace", "pull_requests")
    @task(4)
    def view_pull_requests_page(self):
        """GET /pull-requests - Pull Request Analytics Page"""
        self.safe_get("/pull-requests", name="UI: /pull-requests", headers=BROWSER_HEADERS)

    @tag("frontend", "workspace", "my_prs")
    @task(3)
    def view_my_prs_page(self):
        """GET /my-prs - User's Authored Pull Requests Page"""
        self.safe_get("/my-prs", name="UI: /my-prs", headers=BROWSER_HEADERS)

    @tag("frontend", "workspace", "dora")
    @task(4)
    def view_dora_page(self):
        """GET /dora - DORA Metrics & Engineering Health Page"""
        self.safe_get("/dora", name="UI: /dora", headers=BROWSER_HEADERS)

    @tag("frontend", "workspace", "repositories")
    @task(2)
    def view_repositories_page(self):
        """GET /repositories - Linked Repositories Page"""
        self.safe_get("/repositories", name="UI: /repositories", headers=BROWSER_HEADERS)

    @tag("frontend", "workspace", "alerts")
    @task(2)
    def view_alerts_page(self):
        """GET /alerts - Alert Rules & Notifications Page"""
        self.safe_get("/alerts", name="UI: /alerts", headers=BROWSER_HEADERS)

    @tag("frontend", "workspace", "team")
    @task(2)
    def view_team_page(self):
        """GET /team - Team Workload & Members Page"""
        self.safe_get("/team", name="UI: /team", headers=BROWSER_HEADERS)

    @tag("frontend", "admin", "admin_overview")
    @task(2)
    def view_admin_overview_page(self):
        """GET /admin/overview - Organization Admin Overview"""
        self.safe_get("/admin/overview", name="UI: /admin/overview", headers=BROWSER_HEADERS)

    @tag("frontend", "admin", "admin_projects")
    @task(2)
    def view_admin_projects_page(self):
        """GET /admin/projects - Admin Project Management Screen"""
        self.safe_get("/admin/projects", name="UI: /admin/projects", headers=BROWSER_HEADERS)

    @tag("frontend", "admin", "admin_members")
    @task(2)
    def view_admin_members_page(self):
        """GET /admin/members - Admin Member Management Screen"""
        self.safe_get("/admin/members", name="UI: /admin/members", headers=BROWSER_HEADERS)

    @tag("frontend", "admin", "admin_integrations")
    @task(1)
    def view_admin_integrations_page(self):
        """GET /admin/integrations - Integration Setup Hub"""
        self.safe_get("/admin/integrations", name="UI: /admin/integrations", headers=BROWSER_HEADERS)

    @tag("frontend", "admin", "admin_settings")
    @task(1)
    def view_admin_settings_page(self):
        """GET /admin/settings - Workspace / Company Settings"""
        self.safe_get("/admin/settings", name="UI: /admin/settings", headers=BROWSER_HEADERS)
