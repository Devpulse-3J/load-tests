"""
Scenario: Public & Authentication API Endpoints.
Covers unauthenticated endpoints, registration, login load, OAuth handshakes, and public webhooks.
"""

from locust import task, tag
from common.base_user import BaseDevPulseUser
from config import (
    DEFAULT_HEADERS,
    generate_unique_email,
    generate_company_name,
)


class PublicApiUser(BaseDevPulseUser):
    abstract = True
    """
    Simulates anonymous traffic, authentication spikes, and public webhook triggers.
    """

    @tag("api", "auth", "login")
    @task(5)
    def test_login_endpoint(self):
        """POST /api/auth/login - Authentication credential validation"""
        payload = {
            "email": "test_guest@demo.devpulse",
            "password": "Password123!",
        }
        # Both 200 (if account exists) and 401 (if invalid credentials) are valid HTTP responses
        self.safe_post(
            "/api/auth/login",
            json=payload,
            name="/api/auth/login",
            headers=DEFAULT_HEADERS,
            expected_statuses=(200, 401),
        )

    @tag("api", "auth", "register")
    @task(3)
    def test_register_endpoint(self):
        """POST /api/auth/register - User & Company Registration"""
        email = generate_unique_email(prefix="loaduser")
        company = generate_company_name()
        payload = {
            "email": email,
            "password": "SecurePassword123!",
            "fullName": "Locust Load Tester",
            "isCompany": True,
            "companyName": company,
        }
        self.safe_post(
            "/api/auth/register",
            json=payload,
            name="/api/auth/register",
            headers=DEFAULT_HEADERS,
            expected_statuses=(200, 201),
        )

    @tag("api", "oauth", "github")
    @task(2)
    def test_github_connect_url(self):
        """GET /api/auth/me/github/connect - GitHub OAuth Connect URL"""
        self.safe_get(
            "/api/auth/me/github/connect",
            name="/api/auth/me/github/connect",
            headers=DEFAULT_HEADERS,
            expected_statuses=(200, 401),
        )

    @tag("api", "oauth", "jira")
    @task(2)
    def test_jira_oauth_install_url(self):
        """GET /api/integrations/jira/oauth/install - Jira OAuth install entrypoint"""
        self.safe_get(
            "/api/integrations/jira/oauth/install?companyId=1",
            name="/api/integrations/jira/oauth/install",
            headers=DEFAULT_HEADERS,
            expected_statuses=(200, 302, 400, 404),
        )

    @tag("api", "oauth", "slack")
    @task(2)
    def test_slack_oauth_install_url(self):
        """GET /api/slack/oauth/install - Slack OAuth install entrypoint"""
        self.safe_get(
            "/api/slack/oauth/install",
            name="/api/slack/oauth/install",
            headers=DEFAULT_HEADERS,
            expected_statuses=(200, 302, 404),
        )

    @tag("api", "webhooks", "demo_alert")
    @task(2)
    def test_synthetic_alert_webhook(self):
        """POST /api/webhooks/test-high-risk-alert - Test alert demonstration webhook"""
        self.safe_post(
            "/api/webhooks/test-high-risk-alert",
            name="/api/webhooks/test-high-risk-alert",
            headers=DEFAULT_HEADERS,
            expected_statuses=(200, 204),
        )
