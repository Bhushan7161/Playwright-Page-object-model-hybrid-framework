# Playwright Page Object Model (Hybrid – Data-Driven + Keyword-Driven) Framework

[![Playwright Tests](https://github.com/Bhushan7161/Playwright-Page-object-model-hybrid-framework/actions/workflows/playwright-tests.yml/badge.svg)](https://github.com/Bhushan7161/Playwright-Page-object-model-hybrid-framework/actions/workflows/playwright-tests.yml)

A hybrid web automation framework built with Python, Playwright, pytest, the Page Object Model (POM), an Excel data-provider layer, a reusable keyword-action engine, Jenkins, GitHub Actions, and Allure Reports.

The test suite automates CarWale workflows for navigating to new-car pages, selecting multiple brands, validating page titles, and retrieving car names and prices from Excel-driven test data.

## Test results

- 9 automated test cases
- 100% passing in the latest Jenkins execution
- Allure features, steps, severity levels, and execution details
- Video and trace collection for debugging
- Screenshot attachment support for failed tests
- Automated GitHub Actions execution on pushes and pull requests

![Allure report showing nine passing tests](docs/allure-report.png)

## Technology stack

- Python 3.12
- Playwright
- pytest
- Page Object Model
- Reusable keyword-action engine
- openpyxl for Excel-driven test data
- Allure Reports
- Jenkins
- GitHub Actions

## Project structure

```text
PlaywrightPageObjects/
├── ConfigurationData/
│   └── conf.ini              # Application URL and element locators
├── .github/workflows/
│   └── playwright-tests.yml  # CI workflow for pushes and pull requests
├── docs/
│   └── allure-report.png     # Successful execution report
├── excel/
│   └── testdata.xlsx         # Data-driven test inputs
├── pages/                    # Page objects and reusable page actions
├── testcases/                # pytest test cases and fixtures
├── utilities/                # Configuration, Excel, and logging utilities
├── .gitignore
├── README.md
└── requirements.txt
```

## Automated scenarios

1. Navigate to the **Find New Cars** section.
2. Select BMW, MG, Toyota, and Honda using Excel test data.
3. Verify that each brand page displays the expected title.
4. Retrieve and print the available car names and prices.
5. Generate videos, Playwright traces, logs, screenshots, and Allure results.

## Hybrid framework design

This repository combines two automation approaches:

- **Data-driven testing:** `testdata.xlsx` supplies brand names and expected page titles to parameterized pytest scenarios.
- **Keyword-driven actions:** `KeywordEngine` maps reusable keywords such as `click`, `type`, and `hover` to Playwright operations. Page objects use this execution layer instead of duplicating browser-action code.

## Local setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd PlaywrightPageObjects
```

### 2. Create and activate a virtual environment

Windows:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies and Playwright Chromium

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Run the tests

Run the complete suite:

```bash
python -m pytest -v -s testcases/Test_CarWale.py
```

Run in Firefox:

Windows Command Prompt:

```cmd
set BROWSERS=firefox
python -m pytest testcases/Test_CarWale.py
```

Run in both supported browsers:

```cmd
set BROWSERS=chrome,firefox
python -m pytest testcases/Test_CarWale.py
```

Generate Allure result files:

```bash
python -m pytest -v -s testcases/Test_CarWale.py --alluredir=allure-results
```

After installing the Allure command-line tool, generate and open the report:

```bash
allure serve allure-results
```

## GitHub Actions CI

The workflow in `.github/workflows/playwright-tests.yml` runs automatically on:

- Every push to `main`
- Every pull request targeting `main`
- Manual runs from the **Actions** tab

CI runs Chromium in headless mode and retains Allure results plus failure diagnostics as downloadable workflow artifacts.

## Jenkins configuration on Windows

This project was executed successfully through a Jenkins Freestyle job with the Allure Jenkins plugin.

Use this in **Build Steps → Execute Windows batch command**:

```bat
@echo off
cd /d "%WORKSPACE%"

if not exist ".venv\Scripts\python.exe" py -3.12 -m venv .venv

".venv\Scripts\python.exe" -m pip install -r requirements.txt
".venv\Scripts\python.exe" -m playwright install chromium
".venv\Scripts\python.exe" -m pytest -v -s testcases\Test_CarWale.py --alluredir="allure-results"
```

For **Post-build Actions → Allure Report**, set the results path to:

```text
allure-results
```

## Framework design

- Page objects keep test logic separate from locators and browser actions.
- The keyword engine centralizes common `click`, `type`, and `hover` actions.
- `conf.ini` centralizes the base URL and XPath locators.
- `testdata.xlsx` supplies reusable brand and expected-title combinations.
- pytest fixtures manage browser, page, context, video, and trace lifecycles.
- Allure annotations organize test behavior, steps, features, and severity.
- Logging utilities capture framework activity for troubleshooting.
- Environment variables control browser selection and headless execution without code changes.

## Notes

- Chromium is enabled by default in the browser fixture.
- Set `BROWSERS=firefox` or `BROWSERS=chrome,firefox` to change browser coverage.
- Set `HEADLESS=true` for Jenkins, GitHub Actions, or another non-interactive CI environment.
- The test target is a public website; its UI and locators may change over time.
- Generated reports, traces, videos, logs, IDE settings, and virtual environments are intentionally excluded from Git.
