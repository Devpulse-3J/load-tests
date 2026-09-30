"""
DevPulse Load Testing Suite using Locust.
Target Domain: odineye.cse23.org

This suite covers all endpoints discovered in the DevPulse frontend and backend:
- Frontend Pages / SSR Routes (Next.js)
- Public & Auth APIs (Spring Cloud Gateway, Auth Service)
- Developer Journey (Pull Requests, DORA Metrics, Workload, DevEx)
- Admin & Management Flows (Members, Projects, Alert Rules, Snapshot Rebuilds)
- Third-party Integrations (GitHub, Jira, Slack, Notifications, Webhooks)
"""

import logging
from locust import events, task, tag
from config import TARGET_HOST

# Import scenario classes
from scenarios.frontend_pages import FrontendPageUser
from scenarios.auth_public import PublicApiUser
from scenarios.developer_flow import DeveloperUser
from scenarios.admin_flow import AdminUser
from scenarios.integrations_flow import IntegrationsUser

logger = logging.getLogger("locustfile")


class WebsiteVisitor(FrontendPageUser):
    """Browsing frontend pages, SSR rendering, landing, dashboard UI (weight: 20%)"""
    weight = 20


class AnonymousApiUser(PublicApiUser):
    """Anonymous visitors, authentication, OAuth connect URLs, public webhooks (weight: 10%)"""
    weight = 10


class StandardDeveloper(DeveloperUser):
    """Active software engineers checking PRs, DORA metrics, review velocity (weight: 45%)"""
    weight = 45


class EngineeringManager(AdminUser):
    """Managers & Admins creating projects, managing rules, inviting users (weight: 15%)"""
    weight = 15


class IntegrationServiceUser(IntegrationsUser):
    """Integrations with GitHub, Jira, Slack, and alert dispatches (weight: 10%)"""
    weight = 10


# Backward compatibility alias for DevPulseUser so legacy invocations succeed
class DevPulseUser(DeveloperUser):
    """
    All-in-one DevPulse User covering frontend landing, developer workflow, and metrics.
    Ensures backward compatibility if invoked directly.
    """
    weight = 30

    @tag("health", "public", "landing")
    @task(3)
    def landing_page_check(self):
        """GET / - Public Landing Page Health Check"""
        self.client.get("/", name="Health: / (Landing Page)")


@events.init.add_listener
def on_locust_init(environment, **_kwargs):
    logger.info("Initializing DevPulse Load Testing Suite")
    if environment.host is None:
        environment.host = TARGET_HOST
    logger.info(f"Targeting host: {environment.host}")


@events.test_start.add_listener
def on_test_start(environment, **_kwargs):
    logger.info("==================================================")
    logger.info("      Starting DevPulse Locust Load Test          ")
    logger.info(f"Target Host: {environment.host}")
    logger.info("==================================================")


@events.test_stop.add_listener
def on_test_stop(environment, **_kwargs):
    logger.info("==================================================")
    logger.info("      DevPulse Locust Load Test Completed         ")
    logger.info("==================================================")
