"""
Visits each Streamlit demo and wakes it if it has gone to sleep.

Streamlit Community Cloud puts apps to sleep after a period without
visitors. A sleeping app shows a "Yes, get this app back up!" button,
which only a real browser can click, so this uses Playwright.
Run by .github/workflows/keep-streamlit-awake.yml on a schedule.
"""
import sys

from playwright.sync_api import sync_playwright

APPS = [
    "https://rohan-retail-dashboard.streamlit.app/",
    "https://rohan-attrition-analytics.streamlit.app/",
    "https://realtime-kpi-pipeline.streamlit.app/",
    "https://bias-auditor-hiring.streamlit.app/",
    "https://explain-any-model.streamlit.app/",
    "https://fraud-detection-api1.streamlit.app/",
]

WAKE_BUTTON = "Yes, get this app back up"


def main() -> int:
    failures = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for url in APPS:
            try:
                page.goto(url, timeout=60_000)
                page.wait_for_timeout(8_000)
                button = page.get_by_role("button", name=WAKE_BUTTON)
                if button.count() > 0:
                    button.first.click()
                    page.wait_for_timeout(5_000)
                    print(f"WOKE    {url}")
                else:
                    print(f"AWAKE   {url}")
            except Exception as exc:  # keep going so one slow app doesn't block the rest
                failures += 1
                print(f"FAILED  {url}: {exc}")
        browser.close()
    return 1 if failures == len(APPS) else 0


if __name__ == "__main__":
    sys.exit(main())
