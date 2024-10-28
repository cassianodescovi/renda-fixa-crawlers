from abc import ABC, abstractmethod
from pathlib import Path
from random import random, randrange
from time import sleep

from botocore.exceptions import BotoCoreError
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from decorators.time import execution_time
from loggers import logger
from utils.cloud import save_on_s3
from utils.files import read_configs
from utils.web import build_driver_option

LOCAL = True


class AbsCrawler(ABC):
    """
    Abstract class for crawlers
    """

    @abstractmethod
    def run(self):
        pass


class SelicBacenCrawler(AbsCrawler):
    """
    Crawler for Selic BACEN website
    https://www.bcb.gov.br/controleinflacao/historicotaxasjuros
    """

    def __init__(self, configs_path: Path):
        self.configs_path = configs_path

    @execution_time
    def run(self):
        """
        Run the crawler
        :return:
        """

        driver = webdriver.Chrome(options=build_driver_option())

        try:
            configs = read_configs(
                path=self.configs_path,
                service="crawler",
                theme="selic",
                location="bacen",
            )

            sleep(randrange(3, 5))
            driver.get(configs["url"])
            WebDriverWait(driver, randrange(6, 8))
            sleep(randrange(3, 5))
            data_table = driver.find_element(
                By.CLASS_NAME, "table-responsive"
            ).get_attribute("innerHTML")
            soup = bs(data_table, "html.parser")

            save_on_s3(soup, configs=configs, local=LOCAL)

            driver.quit()

        except (
            FileNotFoundError,
            TimeoutException,
            NoSuchElementException,
            WebDriverException,
            BotoCoreError,
        ) as e:
            logger.error(f"Error running Selic Bacen crawler: {str(e)}")

        finally:
            if "driver" in locals():
                driver.quit()


class SelicIpeaCrawler(AbsCrawler):
    """
    Crawler for Selic Ipea website
    http://www.ipeadata.gov.br/exibeserie.aspx?serid=38402
    """

    def __init__(self, configs_path: Path):
        self.configs_path = configs_path

    @execution_time
    def run(self):
        """
        Run the crawler
        :return:
        """

        driver = webdriver.Chrome(options=build_driver_option())

        try:
            configs = read_configs(
                path=self.configs_path,
                service="crawler",
                theme="selic",
                location="ipea",
            )

            sleep(randrange(3, 5))
            driver.get(configs["url"])
            WebDriverWait(driver, randrange(6, 8))
            sleep(randrange(3, 5))
            xpath = '//*[@id="grd"]/tbody/tr/td'
            data_table = driver.find_element(By.XPATH, xpath).get_attribute("innerHTML")
            soup = bs(data_table, "html.parser")

            save_on_s3(soup, configs=configs, local=LOCAL)

        except (
            FileNotFoundError,
            TimeoutException,
            NoSuchElementException,
            WebDriverException,
            BotoCoreError,
        ) as e:
            logger.error(f"Error running Selic Bacen crawler: {str(e)}")

        finally:
            if "driver" in locals():
                driver.quit()
