from scrapper import ReclameAqui
import unittest
import os


class TestReclameAqui(unittest.TestCase):

    def test_driver(self):
        driver_path = os.getcwd().replace("tests", "drivers/chromedriver")

        mercado_livre = ReclameAqui("mercado-livre", driver_path=driver_path)

        mercado_livre.quit_driver()

    def test_have_reviews(self):
        driver_path = os.getcwd().replace("tests", "drivers/chromedriver")

        mercado_livre = ReclameAqui("mercado-livre", driver_path=driver_path)
        mercado_livre.initialize_driver()
        mercado_livre.accept_cookies()

        self.assertTrue(mercado_livre.have_reviews())

        mercado_livre.quit_driver()

    def test_dont_have_reviews(self):
        driver_path = os.getcwd().replace("tests", "drivers/chromedriver")

        mercado_livre = ReclameAqui("mercado-livre", driver_path=driver_path, start_page=2000)
        mercado_livre.initialize_driver()
        mercado_livre.accept_cookies()

        # self.assertFalse(mercado_livre.have_reviews())

        mercado_livre.quit_driver()
