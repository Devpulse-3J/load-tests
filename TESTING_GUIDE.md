# DevPulse Load Testing Guide & System Capacity Analysis

This guide explains the Locust load testing commands available for DevPulse ([odineye.cse23.org](https://odineye.cse23.org)), details what each test type accomplishes, and analyzes how many concurrent users the system can handle.

---

## 🚀 Quick Execution Commands

```bash
# 1. Fast Smoke Test (1 user, 30 seconds - Quick Health & Route Check)
./run_smoke_test.sh

# 2. Standard Load Test (10 concurrent users, 2 minutes - Realistic Daily Traffic)
./run_load_test.sh

# 3. Stress Test (50 concurrent users, 3 minutes - Finding System Limits)
./run_stress_test.sh

# 4. Spike Test (100 users burst, 1 minute - Sudden Traffic Surge Resilience)
./run_spike_test.sh

# 5. Interactive Web Dashboard (Real-time charts in browser)
.venv/bin/locust
```

---

## 📖 What Each Test Does

### 1. Fast Smoke Test (`./run_smoke_test.sh`)
- **Parameters:** 1 virtual user, runs for 30 seconds.
- **Purpose:** A sanity check before running heavy tests or after deploying a new backend/frontend change.
- **What it does:** Sends requests across all user personas (Frontend UI, Auth, DORA, PR metrics, and Integrations) to confirm that:
  - DNS resolves properly.
  - The domain `odineye.cse23.org` is reachable.
  - No endpoints return unexpected `500 Internal Server Error` or `404 Not Found`.
- **When to use:** Anytime you want quick, immediate validation (takes only 30s).

---

### 2. Standard Load Test (`./run_load_test.sh`)
- **Parameters:** 10 concurrent users, spawns at 2 users/second, runs for 2 minutes.
- **Purpose:** Simulates **normal, daily business traffic** of active engineering teams.
- **What it does:** Simulates 5 distinct personas working simultaneously:
  - **Standard Developer (45%):** Checking DORA metrics, PR risk predictions, review turnaround time, and personal PRs.
  - **Website Visitor (20%):** Navigating Next.js server-side rendered pages (`/dashboard`, `/dora`, `/team`, `/pull-requests`).
  - **Engineering Manager (15%):** Managing project rosters, viewing alert policies, and triggering snapshot updates.
  - **Integrations User (10%):** Querying GitHub repository sync status, Jira issues, and Slack alerts.
  - **Anonymous Visitor (10%):** Hitting public pages, OAuth connect URLs, and logins.
- **When to use:** To measure baseline response times (latency) and verify system stability under expected day-to-day load.

---

### 3. Stress Test (`./run_stress_test.sh`)
- **Parameters:** 50 concurrent users, ramps up at 5 users/second, runs for 3 minutes.
- **Purpose:** Pushes the system beyond normal operating capacity to identify its **breaking points**.
- **What it does:** Continuously increases traffic load to answer:
  - At how many concurrent users do response times begin to slow down?
  - Does the database connection pool get exhausted?
  - At what point does the API Gateway rate limiter start throttling requests (HTTP 429)?
  - Does the system recover cleanly once the traffic decreases?
- **When to use:** When preparing for team onboarding, major releases, or determining infrastructure scaling requirements.

---

### 4. Interactive Web Dashboard (`.venv/bin/locust`)
- **Parameters:** Configured interactively through a graphical web browser interface.
- **Access:** Runs a local web server at [http://localhost:8089](http://localhost:8089).
- **Purpose:** Gives you live, real-time visualization of performance metrics while the test is running.
- **Features:**
  - Real-time graphs for **Requests Per Second (RPS)**, **Response Times (Median & 95th Percentile)**, and **Number of Users**.
  - A live table showing per-endpoint latency and failure rates.
  - A **"Download Data"** tab to export HTML reports and CSV logs anytime.

---

## 👥 How Many People Can Use the System at Once?

To determine how many people can use the system at once, we must understand two key metrics:

### 1. "Concurrent Virtual Users" vs. "Real Human Users"
- **A Locust virtual user** sends requests continuously with only 1 to 3 seconds of pause (`wait_time = between(1, 3)`).
- **A real human engineer** spends time reading PR comments, reviewing code diffs, or analyzing DORA charts, clicking or refreshing only once every **5 to 15 seconds** (called "think time").
- Therefore, **1 active Locust user generates the load of roughly 3 to 5 real human users**.

---

### 2. The Gateway Rate Limiter Bottleneck
In the DevPulse API Gateway configuration (`application.yml`), rate limiting is enforced via Redis:

```yaml
redis-rate-limiter.replenishRate: 10    # 10 sustained requests / second
redis-rate-limiter.burstCapacity: 20    # short spikes up to 20 requests
```

1. **Sustained Throughput:** The gateway permits **10 requests per second** across the API routes.
2. **Burst Allowance:** A temporary spike can handle up to **20 simultaneous requests** in a single second.
3. **What happens when exceeded:** Any request exceeding 10 req/s (after consuming burst tokens) receives **HTTP 429 Too Many Requests**, protecting the microservices from crashing.

---

### 3. Calculated Capacity Breakdown

| User Behavior Profile | Typical Action Frequency | Maximum Concurrent Users Supported |
|---|---|---|
| **Intense / Constant Activity** (fast clicking every 1–2s) | ~1.0 req/s per user | **10 – 15 users** at the exact same second |
| **Normal Team Usage** (browsing dashboards, checking PRs every 5s) | ~0.2 req/s per user | **50 – 70 active users** |
| **Typical Office Workday** (users have tabs open, reading code, occasional clicks every 15s) | ~0.07 req/s per user | **120 – 150 concurrent users** |

---

### 4. How to Find the Exact Limit for Your Deployment

To observe your exact capacity live:
1. Run `./run_stress_test.sh` (or use `.venv/bin/locust` in the web browser).
2. Look at the generated report in `reports/` (e.g. `reports/load_test_latest.html`).
3. Check the **Requests Statistics** and **Error Report**:
   - As long as **failures = 0%** and average response time is **< 500ms**, the system is well within capacity.
   - The user count where HTTP `429 Too Many Requests` begins appearing is the **exact rate-limit ceiling** of the current gateway configuration.
   - If response times spike to several seconds without 429s, the bottleneck is downstream (PostgreSQL queries or microservice CPU/RAM).
