# DevPulse Engineering & Dashboard Metrics Guide: DORA, DevEx & Review Velocity

The **DevPulse Workspace Dashboard** ([`src/app/(workspace)/dashboard/page.tsx`](file:///home/kalhara/Desktop/SEP/SEM5_DevPulse_Frontend/src/app/%28workspace%29/dashboard/page.tsx)) and the **DORA Metrics** page ([`src/app/(workspace)/dora/page.tsx`](file:///home/kalhara/Desktop/SEP/SEM5_DevPulse_Frontend/src/app/%28workspace%29/dora/page.tsx)) provide engineering teams with a unified view of software delivery performance, code review velocity, and developer experience (DevEx) & cognitive workload balance.

---

## Executive Summary Matrix

### 1. DORA Metrics (Delivery Performance & Stability)
| Metric | Display Unit | Direction | What it Measures |
| :--- | :--- | :--- | :--- |
| **Deployment Frequency (DF)** | `deployments/day` | **Higher is better** $\uparrow$ | Throughput, release cadence, and deployment automation |
| **Lead Time for Changes (LTC)** | `hours` | **Lower is better** $\downarrow$ | Delivery pipeline speed from commit to production |
| **Change Failure Rate (CFR)** | `%` | **Lower is better** $\downarrow$ | Release stability, QA confidence, and production defect rate |
| **Mean Time to Recovery (MTTR)** | `hours` | **Lower is better** $\downarrow$ | System resilience, observability, and incident recovery speed |

### 2. Code Review Velocity Metrics
| Metric | Display Unit | Direction | What it Measures |
| :--- | :--- | :--- | :--- |
| **Time to First Review (TTFR)** | `hours` / `mins` | **Lower is better** $\downarrow$ | Average wait time before PR receives initial review feedback |
| **Median TTFR** | `hours` / `mins` | **Lower is better** $\downarrow$ | 50th percentile review pickup speed (robust against outliers) |
| **Review Turnaround Time** | `hours` / `days` | **Lower is better** $\downarrow$ | Elapsed time from first review comment to merge/closure |
| **Review Coverage** | `%` | **Higher is better** $\uparrow$ (Target: $>80\%$) | Percentage of pull requests reviewed prior to merging |
| **Review Cycles / Iterations** | `cycles` | **Balanced** ($\approx 1.0 - 2.5$) | Feedback loops and rework friction per pull request |

### 3. Developer Experience (DevEx) & Workload Metrics
| Metric | Display Unit | Direction | What it Measures |
| :--- | :--- | :--- | :--- |
| **Overall DevEx Flow** | `0 – 100` | **Higher is better** $\uparrow$ | Team-wide frictionless execution and uninterrupted focus |
| **Team Health Status** | `Banner Tier` | `HEALTHY` | Burnout and strain warning (Healthy, Moderate Strain, Burnout Risk) |
| **Context Switching (CSI)** | `0.0 – 10.0` | **Lower is better** $\downarrow$ | Cognitive load across multi-repo switching and concurrent WIP |
| **Team Review Burden** | `ratio` | **Balanced** ($\approx 1.00\text{x}$) | Ratio of completed peer reviews to authored PRs |
| **Capacity Load Percentage** | `%` | **Balanced** ($\approx 70\% - 100\%$) | Active concurrent PRs relative to target member capacity |
| **Workload Status** | `Status Pill` | `OPTIMAL` | Individual balance (Optimal, Overloaded, Underutilized) |

---

## Detailed Breakdown of Metrics

### 1. Deployment Frequency (DF)

#### 📊 What is it showing?
Deployment Frequency measures how frequently code is successfully deployed to production (or target deployment environments) over the selected time window (e.g., 30 days). On the dashboard, it is rendered as rate of deployments per day (e.g., `0.85/day` or `6.2/day`).

#### 🧮 How is it calculated?
$$\text{Deployment Frequency} = \frac{\text{Total Successful Deployments in Window}}{\text{Total Days in Time Window}}$$

* **Data Inputs**: Successful deployment events recorded across the project's linked git repositories over the active window period (e.g., 7, 14, or 30 days).
* **Sample Size**: Total number of successful deployment events recorded during the window.

#### 💡 What does it mean?

##### For a Manager:
* **Organizational Agility**: Reflects how fast the business can ship value, fixes, and new features to end users.
* **Batch Size Indicator**: High deployment frequency indicates small, incremental, lower-risk pull requests rather than risky "big bang" quarterly releases.
* **Bottleneck Identifier**: Low deployment frequency points to deployment friction, manual approvals, or release freeze gates holding back software delivery.

##### For a Developer:
* **Release Friction**: High frequency means automated CI/CD pipelines allow quick, frictionless deployments upon merging PRs.
* **Feedback Loop**: Small, frequent deploys ensure faster feedback on whether newly committed code works properly in production.

---

### 2. Lead Time for Changes (LTC)

#### 📊 What is it showing?
Lead Time for Changes measures the average elapsed time from code commit (or PR creation) until that code is successfully deployed to production. On the dashboard, it is displayed in hours (e.g., `4.1 h` or `18.5 h`).

#### 🧮 How is it calculated?
$$\text{Lead Time} = \frac{\sum (\text{Deployed Timestamp} - \text{Commit / PR Created Timestamp})}{\text{Total Deployed Changes}}$$

* **Data Inputs**: Commits and pull requests linked to production deployments during the active time window.
* **Sample Size**: Total number of evaluated pull requests/commits deployed.

#### 💡 What does it mean?

##### For a Manager:
* **Time-to-Value**: Shows how long an approved product feature sits in the pipeline between developer completion and customer impact.
* **Process Latency**: Long lead times signal queues in code review, QA validation, or staging environment bottlenecks.

##### For a Developer:
* **PR Review & Merge Efficiency**: Highlights idle time spent waiting for code reviews, secondary approvals, or long build/test execution times.
* **Context Switching**: Shorter lead time keeps code fresh in the developer’s mind, minimizing context switching between pull requests.

---

### 3. Change Failure Rate (CFR)

#### 📊 What is it showing?
Change Failure Rate measures the percentage of production deployments that result in a degraded service, production incident, or require an immediate rollback/hotfix. It is displayed as a percentage (e.g., `4.2%` or `12.0%`).

#### 🧮 How is it calculated?
$$\text{Change Failure Rate (\%)} = \left( \frac{\text{Failed or Rolled Back Deployments}}{\text{Total Deployments}} \right) \times 100$$

* **Data Inputs**: Deployment statuses tagged as `failed` or `rolled_back`, plus deployment-linked incident triggers during the window.
* **Sample Size**: Total deployment attempts evaluated.

#### 💡 What does it mean?

##### For a Manager:
* **Release Quality & Risk**: Quantifies stability risk. High CFR indicates fragile release artifacts or insufficient automated regression testing.
* **Balance of Speed vs. Stability**: Helps balance speed (Deployment Frequency) with quality. High speed paired with high failure rate is unsustainable.

##### For a Developer:
* **Testing & Pipeline Confidence**: Low CFR means unit, integration, and staging test suites are reliably catching bugs before reaching production.
* **Deployment Anxiety**: High CFR creates fear around deploying code, causing developers to delay releases and accumulate larger, riskier code changes.

---

### 4. Mean Time to Recovery (MTTR)

#### 📊 What is it showing?
Mean Time to Recovery measures the average duration required to restore normal service when a production failure, failed deployment, or outage occurs. It is displayed in hours (e.g., `1.2 h` or `5.5 h`).

#### 🧮 How is it calculated?
$$\text{MTTR} = \frac{\sum (\text{Failure Recovered Timestamp} - \text{Failure / Incident Reported Timestamp})}{\text{Total Incident / Failure Recovery Events}}$$

* **Data Inputs**: Time delta between deployment failure / alert generation and the corresponding resolution / recovery timestamp.
* **Sample Size**: Count of recovery/incident resolution events during the window.

#### 💡 What does it mean?

##### For a Manager:
* **Operational Resilience**: Evaluates how gracefully the team handles unexpected production issues and outages.
* **Downtime Impact**: Lower MTTR minimizes SLA breaches, customer churn, and operational cost incurred during outages.

##### For a Developer:
* **Observability & Recovery Tools**: Quick recovery depends on good logging, alert monitoring, and quick rollback scripts or feature flags.
* **On-Call & Stress Reduction**: Shorter MTTR means developers spend less time in emergency firefighting sessions.

---

## Part 2: Code Review Velocity Metrics

Surfaced on the Manager Dashboard via [`ReviewVelocityCard.tsx`](file:///home/kalhara/Desktop/SEP/SEM5_DevPulse_Frontend/src/components/dashboard/ReviewVelocityCard.tsx) and `/metrics/review-velocity`. Code review is frequently the largest source of idle wait time in modern software delivery.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Code Review Velocity                         30-day window · 12 total PRs   │
│                                              [● TTFR: Good (<4h)]           │
├────────────────────┬────────────────────┬────────────────┬──────────────────┤
│ Avg Time to First  │ Median TTFR        │ Avg Turnaround │ Avg Review       │
│ Review             │ (50th percentile)  │ Time           │ Cycles           │
│ 3.5h               │ 2.1h               │ 14.2h          │ 2.0 iterations   │
├────────────────────┴────────────────────┴────────────────┴──────────────────┤
│ Review Coverage: 83.3% (10 / 12 PRs)  [========>            ] Target: >80%  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1. Time to First Review (TTFR) — Average & Median
* **Average TTFR**: The average duration elapsed from when a pull request is submitted (or marked ready for review) until a teammate leaves the first review comment, approval, or change request.
* **Median TTFR**: The 50th percentile response time. Median TTFR is critical because it represents typical engineer experience without being distorted by outlier PRs that remained open for long periods.
* **Visual Status Pill (`getTtfrStatus`)**:
  * 🟢 **Good (< 4h)**: Fast review feedback loop; author stays in flow without mental fatigue or context switching.
  * 🟡 **Moderate (4 – 24h)**: Acceptable response time; reviews handled within one business day.
  * 🔴 **Alert (> 24h)**: Significant review queue bottleneck; engineers are blocked waiting for peer feedback.

### 2. Average Turnaround Time
* **What it is**: The average time from the **first review comment** to the pull request being merged or closed.
* **What it means**: Differentiates between delays in picking up PRs (TTFR) versus protracted code revision cycles, debates, or merge conflicts during review.

### 3. Review Coverage (%)
* **What it is**: The proportion of pull requests that underwent peer review before merging:
  $$\text{Review Coverage} = \left(\frac{\text{Reviewed PRs}}{\text{Total PRs}}\right) \times 100$$
* **Color Bar**:
  * 🟢 **$\ge 80\%$ (Success)**: Strong peer review governance; high code quality assurance.
  * 🟡 **$60\% - 79\%$ (Warning)**: Moderate review gaps.
  * 🔴 **$< 60\%$ (Danger)**: Too many unreviewed PRs bypassing peer scrutiny.

### 4. Average Review Cycles (Iterations)
* The mean number of review iterations per PR (review feedback $\rightarrow$ developer fixes $\rightarrow$ re-review). Balanced range is $1.0 - 2.5$. Higher values ($> 3.0$) suggest architectural ambiguity, oversized pull requests, or nitpicking over formatting instead of automated linting.

### 5. Pull Requests Drilldown List
* An expandable section (`Recent PR Review Speeds`) displaying recent PRs with their specific PR number, title, review count, individual turnaround time, individual TTFR badge, and Git lifecycle state (`open`, `merged`, `closed`).

---

## Part 3: Developer Experience (DevEx) & Workload Balance

Surfaced via [`DevExWorkloadView.tsx`](file:///home/kalhara/Desktop/SEP/SEM5_DevPulse_Frontend/src/components/dashboard/DevExWorkloadView.tsx) and `/metrics/devex`. DevEx metrics measure human flow, cognitive friction, and burnout risk rather than pure commit output.

```
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [● MODERATE STRAIN]  30-day assessment                                                         │
│ Moderate Strain: Noticeable multi-repo context switching or localized review load.             │
│                                                                                                │
│ Overall DevEx Flow:    66.06 / 100                                                             │
│ Avg Context Switching:  1.1 / 10.0 CSI                                                         │
│ Team Review Burden:    0.00x rev/author                                                        │
│ Distribution:          [0 Optimal]  [0 Overloaded]  [4 Underutilized]                          │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1. Team Health Status Banner
DevPulse computes an overall team sustainability tier:
* 🟢 **Healthy Team Flow (`HEALTHY`)**: Balanced peer review distribution, manageable context switching, and sustainable work-in-progress (WIP).
* 🟡 **Moderate Strain (`MODERATE`)**: Noticeable multi-repo context switching, localized review load on specific members, or extreme underutilization/overload imbalances.
* 🔴 **Burnout Risk Alert (`BURNOUT_RISK`)**: Severe developer overload, fragmented cognitive focus across many repositories, and chronic review bottlenecks.

### 2. Overall DevEx Flow Score (e.g. `66.06 / 100`)
* **What it is**: A composite flow score from $0$ to $100$ evaluating how smoothly engineering work progresses without friction or blockages.
* **Why is it `66.06` in your dashboard?**
  * Even though multi-repo context switching is low (`1.1 CSI`), the team has a **0.00x review burden** (no peer code reviews completed in the period) and **100% of developers are underutilized (0 active PRs)**.
  * A healthy engineering flow requires both low cognitive drag *and* active peer review collaboration. Inactive PR cycles lower the flow index below optimal ($>80$).

### 3. Average Context Switching Index (e.g. `1.1 / 10.0 CSI`)
* **What it is**: The team's average cognitive load index on a $0.0$ to $10.0$ scale.
* **Thresholds**:
  * 🟢 **$0.0 – 3.5$ (Low CSI)**: Minimal task fragmentation; developers focus on a single repository or feature at a time.
  * 🟡 **$3.6 – 7.0$ (Moderate CSI)**: Multi-repo branching or frequent task switching.
  * 🔴 **$7.1 – 10.0$ (High CSI - Alert)**: Severe cognitive thrashing across multiple repositories and concurrent tasks.
* **In your dashboard**: `1.1 CSI` is low, meaning developers are working within single repositories rather than jumping between microservices.

### 4. Team Review Burden Ratio (e.g. `0.00x rev/author`)
* **What it is**: The ratio of completed peer code reviews to authored pull requests across the entire team:
  $$\text{Team Review Burden} = \frac{\text{Total Completed Peer Reviews}}{\text{Total Authored Pull Requests}}$$
* **Interpretation**:
  * $\approx 1.00\text{x}$: Healthy collective code ownership; every authored PR is matched by peer reviews.
  * $> 2.50\text{x}$: Review bottleneck; reviews concentrated on a small fraction of the team.
  * `0.00x`: No peer reviews completed during the time window (PRs were either merged without review or no active PR review workflow was triggered).

### 5. Workload Distribution Badges (`0 Optimal`, `0 Overloaded`, `4 Underutilized`)
* Aggregates team members into three capacity buckets based on concurrent active PRs and WIP limits:
  * **Optimal**: Developers operating within healthy WIP limits ($1 - 3$ active PRs).
  * **Overloaded**: Developers exceeding active PR limits ($>120\%$ load) or carrying disproportionate review burdens.
  * **Underutilized**: Developers with 0 active PRs or load percentage significantly below sprint targets.

---

## Part 4: Developer Workload & Cognitive Load Index Table

The interactive member table in [`DevExWorkloadView.tsx`](file:///home/kalhara/Desktop/SEP/SEM5_DevPulse_Frontend/src/components/dashboard/DevExWorkloadView.tsx) provides a granular breakdown per developer:

| Column | What It Displays | Dashboard Sample Value | Interpretation |
| :--- | :--- | :--- | :--- |
| **Developer** | Full name and system user ID | `Didula Jeewandara`<br>`ID: 40` | Member identification from linked Git/auth system. |
| **Workload Status** | Individual status pill | `○ UNDERUTILIZED` | No active pull requests in-flight (`0(0%)`). |
| **DevEx Score** | Individual flow rating ($0 - 100$) with progress bar | `64.75` / `70` | Reflects personal flow based on active WIP, review participation, and cycle time. |
| **Active PRs (Load %)** | Active WIP PRs and percentage of target capacity | `0(0%)` | Developer currently has 0 open PRs against their target capacity. |
| **Context Switching (CSI)** | Cognitive load gauge ($0.0 - 10.0$) | `1.5 / 10.0` (or `0.0 / 10.0`) | Visual bar: Green ($\le 3.5$) indicates single-repo focus; Yellow ($3.6-7.0$); Red ($>7.0$). |
| **Review Burden** | Review ratio and count of completed reviews | `0.00x ratio`<br>`0 reviews completed` | Member has not completed any peer reviews during the window. |
| **Repos / Cycle Time** | Repositories touched and average branch cycle time | `1 repo`<br>`Cycle: 1m` (or `N/A`) | Touched 1 repository; branch lifecycle from first commit to merge was 1 minute. |

### Analysis of Your Dashboard Data
In your dashboard snapshot:
1. **Underutilization across all 4 developers** (`Didula`, `kalhara`, `Umaya`, `Didu`): All members currently have `0` active in-flight PRs, indicating either a lull between sprint deliverables or that tasks have already been completed and merged.
2. **Cycle Time of `1m`**: Pull requests were created and immediately merged within 1 minute (typical for automated scripts, test PRs, or direct merges without formal review waits).
3. **`0.00x` Review Burden**: No peer code reviews were logged for these changes, which causes the Overall DevEx Flow score to sit at `66.06` rather than an elite score of $90+$.

---

## Part 5: Developer Workload Chart (Target Active PR Capacity)

Rendered in [`WorkloadChart.tsx`](file:///home/kalhara/Desktop/SEP/SEM5_DevPulse_Frontend/src/components/charts/WorkloadChart.tsx) on the Manager Dashboard:

### 📊 What is it showing?
A horizontal bar chart visualizing the workload percentage of each developer relative to their configured active-PR capacity target.

### 🧮 How is it calculated?
$$\text{Load Percentage (\%)} = \left(\frac{\text{Current Active In-Flight PRs}}{\text{Target PR Capacity}}\right) \times 100\%$$

* **Target Capacity**: The expected concurrent PR WIP limit (typically 2 to 3 concurrent PRs per developer).
* **Color Coding**:
  * 🟢 **Green ($< 100\%$)**: Safe capacity; developer has bandwidth.
  * 🟡 **Yellow ($100\% - 119\%$)**: Warning threshold; developer is operating at maximum intended WIP.
  * 🔴 **Red ($\ge 120\%$)**: Danger threshold; developer is overloaded with too many open branches and PRs, increasing risk of merge conflicts and context fatigue.

---

## Part 6: Recent Production Deployments Feed

Rendered on the Manager Dashboard ([`ManagerDashboard.tsx`](file:///home/kalhara/Desktop/SEP/SEM5_DevPulse_Frontend/src/app/%28workspace%29/dashboard/ManagerDashboard.tsx)):

```
┌────────────────────────────────────────────────────────┐
│ Recent production deployments                          │
├────────────────────────────────────────────────────────┤
│ 8a675ae1          Oct 1, 2026 · 12:44        [SUCCESS] │
│ 8a675ae1          Oct 1, 2026 · 12:44        [SUCCESS] │
│ 3336d7a4          Oct 1, 2026 · 12:25        [SUCCESS] │
│ d6255b48          Oct 1, 2026 · 12:05        [PENDING] │
│ 6190539c          Oct 1, 2026 · 11:38        [SUCCESS] │
└────────────────────────────────────────────────────────┘
```

### 1. Elements Displayed:
* **Commit SHA**: The short 8-character Git commit hash deployed (e.g., `8a675ae1`, `3336d7a4`, `d6255b48`, `6190539c`). Clicking or referencing this SHA links directly to the specific release artifact.
* **Timestamp**: Date and time of deployment execution (e.g., `Oct 1, 2026 · 12:44`).
* **Deployment Status Badge**:
  * 🟢 **`success`**: Deployment completed and passed production health checks. Feeds into **Deployment Frequency**.
  * 🟡 **`pending`**: Deployment currently executing in the CI/CD pipeline or awaiting health check confirmation.
  * 🔴 **`failed`**: Deployment failed during pipeline execution or was rolled back. Increases **Change Failure Rate (CFR)** and initiates an **MTTR** recovery clock.
  * ⚪ **`rolled_back`**: Service automatically or manually reverted to a previous stable commit.

---

## Part 7: Developer-Specific Dashboard (Sprint & Jira Workload)

When accessed with a developer role, [`DeveloperDashboard.tsx`](file:///home/kalhara/Desktop/SEP/SEM5_DevPulse_Frontend/src/app/%28workspace%29/dashboard/DeveloperDashboard.tsx) and [`DeveloperWorkloadView.tsx`](file:///home/kalhara/Desktop/SEP/SEM5_DevPulse_Frontend/src/components/dashboard/DeveloperWorkloadView.tsx) present personal sprint metrics:

### 1. Jira Workload Summary Cards
* **Assigned Jira Tasks**: Total count of active Jira issues assigned to the logged-in engineer.
* **In Progress**: Active tasks currently being worked on.
* **Completed Issues**: Tasks successfully closed/resolved during the sprint.
* **Story Points Committed**: Total sum of story points assigned to the developer, juxtaposed with active Git PR load.

### 2. Task Filters & Priority Classification
* **Priority**: 🔴 `High / Critical`, 🟡 `Medium`, ⚪ `Low`.
* **Issue Types**: `Bug`, `Story`, `Task` with direct ticket keys (e.g., `DEV-42`).
* **Scope Switch**: Toggle between `Assigned to me` and `All project tasks`.

### 3. Personal Pull Request Feed
* Live list of pull requests authored by the developer across all repositories, showing PR numbers, titles, repository names, and current states (`open`, `merged`, `draft`).

---

## Part 8: Dashboard Architecture & Visual Indicators

```
                          ┌───────────────────────────┐
                          │   Dashboard Router        │
                          │   src/app/.../page.tsx    │
                          └─────────────┬─────────────┘
                                        │
                 ┌──────────────────────┴──────────────────────┐
                 │                                             │
      Project Role: MANAGER / ADMIN                 Project Role: DEVELOPER
                 ▼                                             ▼
  ┌───────────────────────────────┐             ┌───────────────────────────────┐
  │      ManagerDashboard         │             │      DeveloperDashboard       │
  │ • DORA Metric Grid (4 KPIs)   │             │ • Personal Sprint KPIs        │
  │ • Review Velocity Card        │             │ • Assigned Jira Issues Table  │
  │ • DevEx Workload & Health     │             │ • Personal Pull Requests Feed │
  │ • PR Capacity Workload Chart  │             │ • Capacity Load Percentage    │
  │ • Recent Production Deploys   │             └───────────────────────────────┘
  └───────────────────────────────┘
```

### 1. Performance Tiers (Rating Badges)
Evaluated across DORA metrics by backend benchmarks ([`DoraMetricGrid.tsx`](file:///home/kalhara/Desktop/SEP/SEM5_DevPulse_Frontend/src/features/dora/DoraMetricGrid.tsx)):
* **ELITE** (Green): Industry-leading performance.
* **HIGH** (Blue): Strong delivery pace and stability.
* **MEDIUM** (Yellow): Average performance with room for pipeline optimization.
* **LOW** (Red): Needs immediate process or automation improvement.
* **NOT AVAILABLE** (Gray): Insufficient sample data within the selected time window.

### 2. Comparative Window Delta (`+` / `−` Trends)
Calculated by [`describeMetricChange`](file:///home/kalhara/Desktop/SEP/SEM5_DevPulse_Frontend/src/features/dora/metric-display.ts):
* Shows difference relative to the preceding time window (e.g., `−1.4 h vs previous window`).
* Dynamically highlighted in **Green** for improvements (e.g., decreased lead time, increased deployment frequency) or **Red** for regressions.

### 3. Historical Trend Snapshots Chart
Plots daily metric snapshots over time ([`DoraChart.tsx`](file:///home/kalhara/Desktop/SEP/SEM5_DevPulse_Frontend/src/components/charts/DoraChart.tsx)), allowing teams to track whether CI/CD pipeline investments, code review practices, or workload balancing efforts are creating sustained improvements over extended time horizons.

