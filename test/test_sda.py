from selenium.webdriver.common.by import By
from sda import Locators, Page, Site, structures


class ExampleLocators(Locators):
    """
    """

    HEADER = (By.XPATH, '//h1')
    TEXT = (By.XPATH, '//p[1]')
    LINK = (By.XPATH, '//p[2]/a')


class ExamplePage(Page):
    """
    """

    def __init__(self, web_driver):
        """

        :param web_driver:
        """

        super(ExamplePage, self).__init__(web_driver)

        self.header = structures.Text(web_driver, *ExampleLocators.HEADER)
        self.text = structures.Text(web_driver, *ExampleLocators.TEXT)
        self.link = structures.Link(web_driver, *ExampleLocators.LINK)


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

    def test_get_domain(self, selenium):

        site = ExampleSite(selenium)
        site.driver.get('https://example.com/')

        assert str(site.domain) == 'example.com'

    def test_get_path(self, selenium):

        site = ExampleSite(selenium)
        site.driver.get('https://example.com/')

        assert str(site.path) == '/'

    def test_get_page_url(self, selenium):

        site = ExampleSite(selenium)
        site.driver.get('https://example.com/')

        assert str(site.example.url) == 'https://example.com/'

    def test_get_elements(self, selenium):

        site = ExampleSite(selenium)
        site.driver.get('https://example.com/')

        assert len(site.example.elements()) == 3

    def test_navigate_to(self, selenium):

        site = ExampleSite(selenium)
        site.driver.get('https://example.com/')
        site.example.navigate_to()

        assert str(site.example.url) == 'https://example.com/'

    def test_locators_dict(self):

        locators = {"HEADER": (By.XPATH, '//h1'), "TEXT": (By.XPATH, '//p[1]'), "LINK": (By.XPATH, '//p[2]/a')}

        assert ExampleLocators().as_dict() == locators

    def test_get_tag_name(self, selenium):

        site = ExampleSite(selenium)
        site.driver.get('https://example.com/')

        assert str(site.example.header.tag_name) == 'h1'

    def test_get_is_displayed(self, selenium):

        site = ExampleSite(selenium)
        site.driver.get('https://example.com/')

        assert site.example.header.is_displayed() is True

    def test_get_is_disabled(self, selenium):

        site = ExampleSite(selenium)
        site.driver.get('https://example.com/')

        assert site.example.link.is_disabled() is False

    def test_get_parent(self, selenium):

        site = ExampleSite(selenium)
        site.driver.get('https://example.com/')

        assert str(site.example.header.parent().tag_name) == 'div'
