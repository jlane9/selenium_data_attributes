from selenium.webdriver.common.by import By
from sda import Page, Site, structures


class ExamplePage(Page):
    """
    """

    def __init__(self, web_driver):
        """

        :param web_driver:
        """

        super(ExamplePage, self).__init__(web_driver)

        self.header = structures.Text(web_driver, By.XPATH, '//h1')
        self.text = structures.Text(web_driver, By.XPATH, '//p[1]')
        self.link = structures.Link(web_driver, By.XPATH, '//p[2]/a')


class ExampleSite(Site):
    """
    """

    def __init__(self, web_driver):
        """

        :param web_driver:
        """

        super(ExampleSite, self).__init__(web_driver)
        self.example = ExamplePage(web_driver)


class TestExampleSite(object):

    def test_click_link(self, selenium):

        site = ExampleSite(selenium)
        site.driver.get('https://example.com/')

        site.example.link.click()

        assert str(site.url) == 'https://www.iana.org/domains/reserved'

    def test_get_text(self, selenium):

        site = ExampleSite(selenium)
        site.driver.get('https://example.com/')

        assert str(site.example.header) == 'Example Domain'

    def test_get_title(self, selenium):

        site = ExampleSite(selenium)
        site.driver.get('https://example.com/')

        assert str(site.example.title) == 'Example Domain'