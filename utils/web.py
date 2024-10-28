import random

from selenium import webdriver

proxies = [
    {"http": "103.160.150.251:8080", "https": "103.160.150.251:8080"},
    {"http": "38.65.174.129:80", "https": "38.65.174.129:80"},
    {"http": "46.105.50.251:3128", "https": "46.105.50.251:3128"},
    {"http": "103.23.199.24:8080", "https": "103.23.199.24:8080"},
    {"http": "223.205.32.121:8080", "https": "103.23.199.24:8080"},
]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0",
]


def get_random_user_agent(user_agents_list: list) -> str:
    """
    Get a random user agent from a preset list
    :param user_agents_list:
    :return:
    """
    return random.choice(user_agents_list)


def get_random_proxy(proxy_list: list) -> str:
    """
    Get a random proxy from a preset list
    :param proxy_list:
    :return:
    """
    return random.choice(proxy_list)


def build_driver_option():
    """
    Build a webdriver option with a random user agent and proxy
    :return:
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")

    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument(f"--proxy-server={get_random_proxy(proxies)}")
    # options.add_argument(f"--user-agent={get_random_user_agent(user_agents)}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    return options
