from playwright.sync_api import sync_playwright


URL = "http://192.168.1.26:8502"

OUTPUT = "docs/images/dashboard_before_optimization.png"


with sync_playwright() as p:

    browser = p.chromium.launch()

    page = browser.new_page(
        viewport={
            "width": 1440,
            "height": 1200
        }
    )

    page.goto(URL)

    # attendre le chargement Streamlit
    page.wait_for_timeout(5000)


    # capture complète de toute la page
    page.screenshot(
        path=OUTPUT,
        full_page=True
    )


    browser.close()


print(
    f"Capture enregistrée : {OUTPUT}"
)
