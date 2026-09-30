"""
Scenario: Third-Party Integrations Load Testing (GitHub, Jira, Slack).
Exercises integration status checks, repository sync triggers, issue listing,
and webhook/notification dispatching.
"""

from locust import task, tag
from common.base_user import BaseDevPulseUser
from common.auth import authenticate_user
from config import TEST_USER_EMAIL, TEST_USER_PASSWORD


class IntegrationsUser(BaseDevPulseUser):
    """
    Persona exercising GitHub sync, Jira issue integration, and Slack alerting.
    """

    def on_start(self):
        self.auth_context = authenticate_user(
            self.client,
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD,
            is_admin=False,
        )

    @tag("integrations", "github", "connect_url")
    @task(2)
    def view_github_connect_url(self):
        """GET /api/integrations/projects/{projectId}/github/connect-url"""
        pid = self.current_project_id
        self.safe_get(
            f"/api/integrations/projects/{pid}/github/connect-url",
            name="/api/integrations/projects/[id]/github/connect-url",
            expected_statuses=(200, 404),
        )

    @tag("integrations", "github", "available_repos")
    @task(3)
    def view_github_available_repos(self):
        """GET /api/integrations/projects/{projectId}/github/available-repos"""
        pid = self.current_project_id
        self.safe_get(
            f"/api/integrations/projects/{pid}/github/available-repos",
            name="/api/integrations/projects/[id]/github/available-repos",
            expected_statuses=(200, 404),
        )

    @tag("integrations", "github", "status")
    @task(3)
    def view_github_status(self):
        """GET /api/integrations/projects/{projectId}/github/status"""
        pid = self.current_project_id
        self.safe_get(
            f"/api/integrations/projects/{pid}/github/status",
            name="/api/integrations/projects/[id]/github/status",
            expected_statuses=(200, 404),
        )

    @tag("integrations", "github", "sync")
    @task(1)
    def trigger_github_sync(self):
        """POST /api/integrations/projects/{projectId}/github/sync"""
        pid = self.current_project_id
        self.safe_post(
            f"/api/integrations/projects/{pid}/github/sync",
            name="/api/integrations/projects/[id]/github/sync",
            expected_statuses=(200, 202, 404),
        )

    @tag("integrations", "jira", "status")
    @task(3)
    def view_jira_status(self):
        """GET /api/integrations/jira/status"""
        self.safe_get(
            "/api/integrations/jira/status",
            name="/api/integrations/jira/status",
            expected_statuses=(200, 404),
        )

    @tag("integrations", "jira", "issues")
    @task(3)
    def view_jira_issues(self):
        """GET /api/integrations/jira/issues"""
        self.safe_get(
            "/api/integrations/jira/issues",
            name="/api/integrations/jira/issues",
            expected_statuses=(200, 404),
        )

    @tag("integrations", "jira", "available_projects")
    @task(2)
    def view_jira_available_projects(self):
        """GET /api/integrations/jira/available-projects"""
        self.safe_get(
            "/api/integrations/jira/available-projects",
            name="/api/integrations/jira/available-projects",
            expected_statuses=(200, 404),
        )

    @tag("integrations", "jira", "webhook_status")
    @task(1)
    def view_jira_webhook_status(self):
        """GET /api/webhooks/jira"""
        self.safe_get(
            "/api/webhooks/jira",
            name="/api/webhooks/jira",
            expected_statuses=(200, 404),
        )

    @tag("integrations", "slack", "status")
    @task(2)
    def view_slack_status(self):
        """GET /api/slack/status"""
        self.safe_get(
            "/api/slack/status",
            name="/api/slack/status",
            expected_statuses=(200, 404),
        )

    @tag("integrations", "slack", "channels")
    @task(2)
    def view_slack_channels(self):
        """GET /api/slack/channels"""
        self.safe_get(
            "/api/slack/channels",
            name="/api/slack/channels",
            expected_statuses=(200, 404),
        )

    @tag("integrations", "notifications", "test")
    @task(1)
    def send_test_notification(self):
        """POST /api/notifications/test - Test alert delivery"""
        payload = {
            "channelId": "C12345678",
            "channelName": "#general",
            "message": "DevPulse load test notification heartbeat",
        }
        self.safe_post(
            "/api/notifications/test",
            json=payload,
            name="/api/notifications/test",
            expected_statuses=(200, 400, 404, 502),
        )
