from seleniumbase import SB
def scrape_activites():
        with SB(
            uc_cdp=True,
            guest_mode=True,
            headless=False,
            undetected=True,
            timeout_multiplier=1,
        ) as sb:
            sb.open("https://www.118712.fr/")
scrape_activites()