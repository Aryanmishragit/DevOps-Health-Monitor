# DevOps Health Monitor

A Flask-based web dashboard for checking HTTP endpoint availability, measuring response latency, and storing health-check history in SQLite.

## Features

- Add and remove monitored HTTP/HTTPS endpoints.
- Run on-demand health checks with a configurable request timeout.
- Track HTTP status code, response latency, timestamp, and error details.
- Persist services and check history in SQLite.
- View a dashboard summary of healthy, unhealthy, and unchecked services.
- Expose an application health endpoint at `/health`.
- Automated unit tests for successful responses, server errors, and timeouts.

## Technology stack

- Python 3.10+
- Flask
- Requests
- SQLite
- Pytest
- HTML/CSS

## Run locally (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser. To verify the application endpoint, open http://127.0.0.1:5000/health.

If PowerShell blocks virtual-environment activation, run the commands without activation using:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

## Run tests

```powershell
python -m pytest -v
```

## How health status is determined

- HTTP responses with status codes below 500 are considered reachable (`UP`). This includes redirects and client errors such as 404.
- HTTP 5xx responses are considered `DOWN`.
- Connection failures, DNS errors, and request timeouts are considered `DOWN`.
- Response time is measured in milliseconds.
- Checks are triggered manually in this baseline version. Scheduled checks and CI/CD are planned enhancements.

## Repository structure

```text
devops-health-monitor/
├── app.py
├── monitor.py
├── storage.py
├── requirements.txt
├── pytest.ini
├── README.md
├── BRANCHING.md
├── .gitignore
├── templates/
│   └── dashboard.html
├── static/
│   └── style.css
└── tests/
    └── test_monitor.py
```

## Git workflow

See [BRANCHING.md](BRANCHING.md) for the branch and commit workflow.

## Limitations and next steps

- No authentication; do not expose this development dashboard to the public internet.
- No background scheduler yet; checks are initiated by a user.
- SQLite is suitable for a local demo, not a high-volume distributed monitoring platform.
- Next improvements: scheduled checks, uptime metrics, charts, environment-based configuration, CI with GitHub Actions, Docker packaging, and a repeatable deployment pipeline.

## Internship task

Created as the project baseline for SWYNEX DevOps Internship Task 1: Git Workflow and Project Baseline.
