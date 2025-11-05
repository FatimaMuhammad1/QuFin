from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def main():
    # set up the Chrome webdriver with Selenium
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    # maximize the Chrome window
    driver.maximize_window()

    # specify the URL of the Yahoo Finance news page to scrape
    url = "https://finance.yahoo.com/news/"

    # load the Yahoo Finance news page using Selenium
    driver.get(url)

    main_content = driver.find_element(By.ID, "Main")

    articles = (
        main_content.find_elements(By.CSS_SELECTOR, "[data-locator='subtree-root']")[1]
        .find_element(By.TAG_NAME, "ul")
        .find_elements(By.TAG_NAME, "li")
    )

    # input()

    # extract the news article headlines and summaries using Selenium
    links = []
    for article in articles:
        try:
            links.append(article.find_element(By.CSS_SELECTOR, "a[class^='js-content-viewer']").get_attribute("href"))
        except Exception:
            pass

    # close the Chrome webdriver
    driver.quit()


if __name__ == "__main__":
    main()
