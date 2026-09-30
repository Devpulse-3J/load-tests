"""
Scenario: Authenticated Developer User Journey.
Simulates active software engineers tracking pull requests, DORA metrics,
review velocities, workload distribution, and developer experience metrics.
"""

from locust import task, tag
from common.base_user import BaseDevPulseUser
from common.auth import authenticate_user
from config import TEST_USER_EMAIL, TEST_USER_PASSWORD


class DeveloperUser(BaseDevPulseUser):
    abstract = True
    """
    Developer persona exercising core project metrics and pull request analysis.
    """

    def on_start(self):
        """Authenticate on user initialization."""
        self.auth_context = authenticate_user(
            self.client,
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD,
            is_admin=False,
        )

    @tag("developer", "auth", "profile")
    @task(3)
    def view_profile(self):
        """GET /api/auth/me - Current user identity and project roles"""
        self.safe_get("/api/auth/me", name="/api/auth/me")

    @tag("developer", "projects", "list")
    @task(4)
    def list_projects(self):
        """GET /api/projects - List projects accessible to user"""
        self.safe_get("/api/projects", name="/api/projects")

    @tag("developer", "metrics", "prs")
    @task(5)
    def view_pull_requests(self):
        """GET /api/metrics/prs - Project pull requests with risk scores"""
        pid = self.current_project_id
        self.safe_get(
            f"/api/metrics/prs?projectId={pid}&limit=25&offset=0",
            name="/api/metrics/prs",
            expected_statuses=(200, 404),
        )

    @tag("developer", "metrics", "my_prs")
    @task(4)
    def view_my_pull_requests(self):
        """GET /api/metrics/prs?myPrs=true - Pull requests authored by caller"""
        pid = self.current_project_id
        self.safe_get(
            f"/api/metrics/prs?myPrs=true&projectId={pid}&limit=25&offset=0",
            name="/api/metrics/prs?myPrs=true",
            expected_statuses=(200, 404),
        )

    @tag("developer", "metrics", "relink")
    @task(1)
    def relink_authored_prs(self):
        """POST /api/metrics/authors/relink - Catch-up linking for historical PRs"""
        self.safe_post(
            "/api/metrics/authors/relink",
            name="/api/metrics/authors/relink",
            expected_statuses=(200, 204),
        )

    @tag("developer", "dora", "summary")
    @task(5)
    def view_dora_summary(self):
        """GET /api/metrics/dora - Four key DORA metrics"""
        pid = self.current_project_id
        self.safe_get(
            f"/api/metrics/dora?projectId={pid}&windowDays=30&historyDays=30",
            name="/api/metrics/dora",
            expected_statuses=(200, 404),
        )

    @tag("developer", "dora", "review_velocity")
    @task(3)
    def view_review_velocity(self):
        """GET /api/metrics/review-velocity - PR review turnaround times"""
        pid = self.current_project_id
        self.safe_get(
            f"/api/metrics/review-velocity?projectId={pid}&windowDays=30",
            name="/api/metrics/review-velocity",
            expected_statuses=(200, 404),
        )

    @tag("developer", "dora", "devex")
    @task(3)
    def view_devex_summary(self):
        """GET /api/metrics/devex - Developer experience friction summary"""
        pid = self.current_project_id
        self.safe_get(
            f"/api/metrics/devex?projectId={pid}&windowDays=30",
            name="/api/metrics/devex",
            expected_statuses=(200, 404),
        )

    @tag("developer", "dora", "workload")
    @task(3)
    def view_workload_metrics(self):
        """GET /api/metrics/workload - Workload distribution"""
        pid = self.current_project_id
        self.safe_get(
            f"/api/metrics/workload?projectId={pid}&windowDays=30",
            name="/api/metrics/workload",
            expected_statuses=(200, 404),
        )

    @tag("developer", "dora", "deployments")
    @task(2)
    def view_deployments(self):
        """GET /api/metrics/deployments - Deployment log history"""
        pid = self.current_project_id
        self.safe_get(
            f"/api/metrics/deployments?projectId={pid}&limit=20&offset=0",
            name="/api/metrics/deployments",
            expected_statuses=(200, 404),
        )

    @tag("developer", "projects", "members")
    @task(2)
    def view_project_members(self):
        """GET /api/projects/{projectId}/members - List members on the project"""
        pid = self.current_project_id
        self.safe_get(
            f"/api/projects/{pid}/members",
            name="/api/projects/[id]/members",
            expected_statuses=(200, 404),
        )

    @tag("developer", "integrations", "repos")
    @task(2)
    def view_repositories(self):
        """GET /api/integrations/repositories - Linked repositories list"""
        self.safe_get(
            "/api/integrations/repositories",
            name="/api/integrations/repositories",
            expected_statuses=(200, 404),
        )

    @tag("developer", "auth", "github_status")
    @task(1)
    def check_github_status(self):
        """GET /api/auth/me/github/status - Linked GitHub account status"""
        self.safe_get(
            "/api/auth/me/github/status",
            name="/api/auth/me/github/status",
            expected_statuses=(200, 404),
        )
