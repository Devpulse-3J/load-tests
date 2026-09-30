"""
Scenario: Company Admin and Engineering Manager Workflows.
Simulates organizational administration, team provisioning, alert rule management,
and DORA historical recalculations.
"""

from locust import task, tag
from common.base_user import BaseDevPulseUser
from common.auth import authenticate_user
from config import (
    ADMIN_USER_EMAIL,
    ADMIN_USER_PASSWORD,
    generate_project_name,
    generate_unique_email,
)


class AdminUser(BaseDevPulseUser):
    """
    Admin & Manager persona exercising administrative endpoints, project setup,
    team invitations, alert policies, and analytics rebuild triggers.
    """

    def on_start(self):
        """Authenticate as admin."""
        self.auth_context = authenticate_user(
            self.client,
            email=ADMIN_USER_EMAIL,
            password=ADMIN_USER_PASSWORD,
            is_admin=True,
        )

    @tag("admin", "company", "members")
    @task(4)
    def view_company_members(self):
        """GET /api/auth/company/members - List members across the company"""
        self.safe_get(
            "/api/auth/company/members",
            name="/api/auth/company/members",
            expected_statuses=(200, 403, 404),
        )

    @tag("admin", "company", "join_requests")
    @task(2)
    def view_join_requests(self):
        """GET /api/workspaces/{companyId}/join-requests - Pending membership requests"""
        cid = self.current_company_id
        self.safe_get(
            f"/api/workspaces/{cid}/join-requests",
            name="/api/workspaces/[id]/join-requests",
            expected_statuses=(200, 403, 404),
        )

    @tag("admin", "projects", "create_update")
    @task(2)
    def create_and_update_project(self):
        """POST /api/projects and PUT /api/projects/{id} - Project lifecycle"""
        p_name = generate_project_name()
        create_payload = {
            "projectName": p_name,
            "description": "Automated load test created project",
            "githubRepoUrl": f"https://github.com/loadtest/{p_name.lower()}",
            "jiraProjectKey": "PERF",
        }
        resp = self.safe_post(
            "/api/projects",
            json=create_payload,
            name="/api/projects",
            expected_statuses=(200, 201, 400, 403, 409),
        )

        if resp.status_code in (200, 201):
            try:
                data = resp.json()
                created_id = data.get("projectId") or data.get("id")
                if created_id:
                    self.safe_put(
                        f"/api/projects/{created_id}",
                        json={"projectName": f"{p_name}-Updated", "description": "Updated description"},
                        name="/api/projects/[id]",
                        expected_statuses=(200, 204, 403),
                    )
            except Exception:
                pass

    @tag("admin", "alerts", "rules")
    @task(3)
    def manage_alert_rules(self):
        """Alert rules CRUD: GET /api/alerts/rules, POST, DELETE"""
        cid = self.current_company_id
        # 1. Fetch rules
        self.safe_get(
            f"/api/alerts/rules?companyId={cid}",
            name="/api/alerts/rules",
            expected_statuses=(200, 404),
        )

        # 2. Create rule
        rule_payload = {
            "companyId": cid,
            "ruleName": f"PerfAlert-{cid}",
            "metricType": "HIGH_RISK_PR",
            "condition": "GREATER_THAN",
            "threshold": 0.8,
            "severity": "CRITICAL",
            "channels": ["SLACK", "EMAIL"],
            "enabled": True,
        }
        create_resp = self.safe_post(
            "/api/alerts/rules",
            json=rule_payload,
            name="/api/alerts/rules",
            expected_statuses=(200, 201, 400),
        )

        # 3. Cleanup created rule if ID returned
        if create_resp.status_code in (200, 201):
            try:
                rule_id = create_resp.json().get("id") or create_resp.json().get("ruleId")
                if rule_id:
                    self.safe_delete(
                        f"/api/alerts/rules/{rule_id}",
                        name="/api/alerts/rules/[id]",
                        expected_statuses=(200, 204, 404),
                    )
            except Exception:
                pass

    @tag("admin", "dora", "rebuild")
    @task(1)
    def trigger_dora_snapshots_rebuild(self):
        """POST /api/metrics/dora/snapshots/rebuild - Recalculate historical snapshots"""
        pid = self.current_project_id
        self.safe_post(
            f"/api/metrics/dora/snapshots/rebuild?projectId={pid}&days=30",
            name="/api/metrics/dora/snapshots/rebuild",
            expected_statuses=(200, 202, 403, 404),
        )

    @tag("admin", "invitations", "company_invite")
    @task(1)
    def invite_company_members(self):
        """POST /api/auth/company/invite - Bulk invite new teammates"""
        invite_email = generate_unique_email(prefix="invite")
        payload = {
            "emails": [invite_email],
            "role": "DEVELOPER",
            "projectId": self.current_project_id,
            "projectRole": "DEVELOPER",
        }
        self.safe_post(
            "/api/auth/company/invite",
            json=payload,
            name="/api/auth/company/invite",
            expected_statuses=(200, 201, 400, 403, 409),
        )

    @tag("admin", "invitations", "project_invite")
    @task(1)
    def invite_project_member(self):
        """POST /api/projects/{projectId}/invite - Direct project invitation"""
        pid = self.current_project_id
        invite_email = generate_unique_email(prefix="member")
        payload = {
            "email": invite_email,
            "role": "DEVELOPER",
        }
        self.safe_post(
            f"/api/projects/{pid}/invite",
            json=payload,
            name="/api/projects/[id]/invite",
            expected_statuses=(200, 201, 400, 403, 409),
        )
