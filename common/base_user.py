"""
Base HTTP User class for DevPulse load testing.
Provides standardized request wrappers with response classification,
URL name grouping, rate-limit awareness, and authentication support.
"""

import time
import logging
from locust import HttpUser, between
from config import (
    DEFAULT_HEADERS,
    BROWSER_HEADERS,
    DEFAULT_PROJECT_ID,
    DEFAULT_COMPANY_ID,
)

logger = logging.getLogger(__name__)


class BaseDevPulseUser(HttpUser):
    abstract = True
    wait_time = between(1, 3)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_context = None

    @property
    def auth_headers(self):
        if self.auth_context and self.auth_context.token:
            return self.auth_context.auth_headers
        return dict(DEFAULT_HEADERS)

    @property
    def current_project_id(self):
        if self.auth_context and self.auth_context.project_ids:
            return self.auth_context.project_ids[0]
        return DEFAULT_PROJECT_ID

    @property
    def current_company_id(self):
        if self.auth_context and self.auth_context.company_id:
            return self.auth_context.company_id
        return DEFAULT_COMPANY_ID

    def safe_get(self, url, name=None, headers=None, expected_statuses=(200,), **kwargs):
        req_headers = headers if headers is not None else self.auth_headers
        req_name = name or url

        with self.client.get(
            url,
            headers=req_headers,
            name=req_name,
            catch_response=True,
            **kwargs,
        ) as resp:
            if resp.status_code in expected_statuses:
                resp.success()
                return resp
            elif resp.status_code == 429:
                resp.failure("Rate limited (HTTP 429 - Redis RateLimiter triggered)")
                time.sleep(0.5)
                return resp
            else:
                resp.failure(f"Unexpected status {resp.status_code} for {req_name}: {resp.text[:120]}")
                return resp

    def safe_post(self, url, json=None, name=None, headers=None, expected_statuses=(200, 201), **kwargs):
        req_headers = headers if headers is not None else self.auth_headers
        req_name = name or url

        with self.client.post(
            url,
            json=json,
            headers=req_headers,
            name=req_name,
            catch_response=True,
            **kwargs,
        ) as resp:
            if resp.status_code in expected_statuses:
                resp.success()
                return resp
            elif resp.status_code == 429:
                resp.failure("Rate limited (HTTP 429)")
                time.sleep(0.5)
                return resp
            else:
                resp.failure(f"Unexpected status {resp.status_code} for {req_name}: {resp.text[:120]}")
                return resp

    def safe_put(self, url, json=None, name=None, headers=None, expected_statuses=(200,), **kwargs):
        req_headers = headers if headers is not None else self.auth_headers
        req_name = name or url

        with self.client.put(
            url,
            json=json,
            headers=req_headers,
            name=req_name,
            catch_response=True,
            **kwargs,
        ) as resp:
            if resp.status_code in expected_statuses:
                resp.success()
                return resp
            elif resp.status_code == 429:
                resp.failure("Rate limited (HTTP 429)")
                time.sleep(0.5)
                return resp
            else:
                resp.failure(f"Unexpected status {resp.status_code} for {req_name}: {resp.text[:120]}")
                return resp

    def safe_delete(self, url, name=None, headers=None, expected_statuses=(200, 204), **kwargs):
        req_headers = headers if headers is not None else self.auth_headers
        req_name = name or url

        with self.client.delete(
            url,
            headers=req_headers,
            name=req_name,
            catch_response=True,
            **kwargs,
        ) as resp:
            if resp.status_code in expected_statuses:
                resp.success()
                return resp
            elif resp.status_code == 429:
                resp.failure("Rate limited (HTTP 429)")
                time.sleep(0.5)
                return resp
            else:
                resp.failure(f"Unexpected status {resp.status_code} for {req_name}: {resp.text[:120]}")
                return resp
