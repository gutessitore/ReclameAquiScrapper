from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
import requests
import time
import sys


class ReclameAqui:

    def __init__(self,
                 company: str = None,
                 link: str = None,
                 driver=None,
                 driver_path: str = None,
                 start_page: int = None,
                 max_page: int = None,
                 headless: bool = False):
        """

        :param company: company name
        :param link: link to craw over to,
        https://www.reclameaqui.com.br/empresa/{company}/lista-reclamacoes/?page={self.start_page} as default
        :param driver: selenium.webdriver object, webdriver.Chrome as default
        :param driver_path: path to the webdriver driver
        :param start_page: page where it will start crawling, default  1
        :param max_page: page to stop crawling, default 10
        :param headless: option to run headless, default False
        """
        default_options = Options()
        if headless:
            default_options.add_argument("--headless")

        self.company = company
        self.driver = driver or webdriver.Chrome(driver_path, options=default_options)
        self.start_page = start_page or 1
        self.current_page = start_page
        self.link = link or f"https://www.reclameaqui.com.br/empresa/{company}/lista-reclamacoes/?page={self.start_page}"
        self.max_page = max_page or 10
        self.reviews = pd.DataFrame()

        self.validate_link()

    def __len__(self):
        return len(self.reviews)

    def validate_link(self):
        request = requests.get(self.link)
        request.raise_for_status()

    def initialize_driver(self):
        self.driver.get(self.link)

    def go_to_page(self, page):
        self.driver.get(f"https://www.reclameaqui.com.br/empresa/{self.company}/lista-reclamacoes/?page={page}")

    def quit_driver(self):
        self.driver.quit()

    def accept_cookies(self):
        time.sleep(1)
        self.driver.find_element_by_id("onetrust-accept-btn-handler").click()

    def click_next_page(self):
        action = webdriver.ActionChains(self.driver)
        next_page_button = self.driver.find_elements_by_xpath(
            "/html/body/ui-view/div/div[4]/div[2]/div[2]/div[2]/div/div[3]/div[3]/div[3]/ul/li")[-1]

        action.move_to_element(next_page_button)
        action.click(on_element=next_page_button)
        time.sleep(1)
        action.perform()

    def find_page_reviews(self):
        return self.driver.find_elements_by_xpath(
            "/html/body/ui-view/div/div[4]/div[2]/div[2]/div[2]/div/div[3]/div[3]/div[2]/div/ul[1]/li")

    def get_reviews(self):
        have_content = True
        in_page_range = True

        self.initialize_driver()
        self.accept_cookies()

        reviews = list()
        load_index = 0
        characters = ['.', '..', '...']
        while have_content and in_page_range:
            # Print loading text
            sys.stdout.write('\rCollecting data ' + characters[0])
            sys.stdout.flush()

            have_content = self.have_reviews()
            in_page_range = self.inside_page_range()

            review_elements = self.find_page_reviews()
            reviews.extend([review.text for review in review_elements])

            self.click_next_page()
            characters.append(characters.pop(0))
            load_index += 1

        self.quit_driver()
        self.reviews = reviews

    def get_current_page(self):
        try:
            self.current_page = int(self.driver.current_url.split("=")[-1])
        except:
            self.current_page = 1

    def inside_page_range(self) -> bool:
        self.get_current_page()
        if self.current_page <= self.max_page:
            return True
        else:
            return False

    def have_reviews(self) -> bool:
        if self.driver.find_element_by_class_name(
                "lacking-results").text == "Ainda não há reclamações para esse filtro.":
            return False
        else:
            return True

    @property
    def to_data_frame(self):

        all_reviews = self.reviews

        review_df = pd.DataFrame({"review": all_reviews})
        review_df[["review", "date", "city"]] = review_df.review.str.split("|", expand=True)
        review_df[["review", "status"]] = review_df.review.str.rsplit("\n", 1, expand=True)
        review_df.dropna(inplace=True)
        review_df.drop_duplicates(inplace=True)

        return review_df


