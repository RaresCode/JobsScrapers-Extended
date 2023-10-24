from tests.module_names import module_names
from tests.logger import get_logger
from tests.utils import TestUtils
from peviitor import Peviitor
from browser import browser
import importlib
import pytest
import time

# This is a class containing setup and utility functions for testing.
class SetupTests:
    def import_all_modules(self):
        """
        Dynamically imports modules and retrieves scraper classes.
        """
        # Initialize an empty list to store scraper classes.
        scraper_classes = []

        # Iterate through module names and their corresponding class names.
        for module_name, class_name in module_names.items():
            try:
                # Dynamically import the module.
                module = importlib.import_module(f"sites.{module_name}")
                # Get the class from the module.
                class_obj = getattr(module, class_name)
                # Append the class object to the list.
                scraper_classes.append(class_obj)
                print(f"Imported class {class_name} from module {module_name}")
            except ModuleNotFoundError:
                print(f"Module not found: {module_name}")
            except AttributeError:
                print(f"Class not found: {class_name} in module {module_name}")
        
        # Return the list of scraper classes.
        return scraper_classes
    
    def get_jobs_careers(self, scraper_class):
        """
        Fixture for scraping process from the career section.
        """
        self.scraper_data = scraper_class().return_data()

# This is a class for UI testing.
class TestUI:
    # This is a pytest fixture that parametrizes the scraper_class.
    @pytest.fixture(params=SetupTests().import_all_modules())
    def scraper_class(self, request):
        return request.param
    
    # Set up a logger for the test.
    def set_logger(self, test_name):
        self.test_name = test_name
        self.logger = get_logger(self.test_name)
    
    # This is a pytest fixture for handling browser-related operations.
    @pytest.fixture
    def command_browser(self, driver, expected_wait):
        self.driver = driver
        self.browser = browser(driver, expected_wait)
        self.peviitor = Peviitor(expected_wait)
        self.browser.open_webpage()  # Open the webpage before each test
        
        yield self.browser
        
        self.browser.close_browser()  # Close the browser after each test
    
    # Function to interact with the UI and get job information.
    def get_jobs_ui(self, company_name):
        self.peviitor.search_company(company_name)
        self.peviitor.click_on_search()
        self.peviitor.load_all_jobs()

        job_titles = self.peviitor.get_all_job_titles()
        job_countries = self.peviitor.get_all_job_locations()
        job_urls = self.peviitor.get_all_job_urls()
        
        return job_titles, job_countries, job_urls
        
    # This is a test case for scraping jobs data.
    @pytest.mark.regression
    def test_scrapers(self, scraper_class, command_browser):
        setup_tests = SetupTests()
        setup_tests.get_jobs_careers(scraper_class)
        self.set_logger(setup_tests.scraper_data[1])
        
        # You can now use the utility methods from TestUtils to avoid code duplication
        try:
            scraped_jobs_data = TestUtils.scrape_jobs(setup_tests.scraper_data[0])
        except Exception as e:
            self.logger.error(f"'{self.test_name}' Test failed to get data from the jobs site because of {e}")

        try:
            peviitor_jobs_data = self.get_jobs_ui(setup_tests.scraper_data[1])
        except Exception as e:
            self.logger.error(f"'{self.test_name}' Test failed to get data from peviitor because of {e}")

        job_titles_scraper, job_countries_scraper, job_urls_scraper = sorted(scraped_jobs_data[0]), sorted(scraped_jobs_data[2]), sorted(scraped_jobs_data[3])
        job_titles_peviitor, job_countries_peviitor, job_urls_peviitor = sorted(peviitor_jobs_data[0]), sorted(peviitor_jobs_data[1]), sorted(peviitor_jobs_data[2])
            
        # Test Title
        try:
            if job_titles_scraper == job_titles_peviitor:
                self.logger.info(f"Test '{self.test_name}' for titles passed")
            else:
                self.logger.error(f"Test '{self.test_name}' for titles failed")
        except Exception as e:
            self.logger.error(f"Test '{self.test_name}' for titles failed because of {e}")
        finally:
            assert job_titles_scraper == job_titles_peviitor
    
        # Test job country
        try:
            if job_countries_scraper == job_countries_peviitor:
                self.logger.info(f"Test '{self.test_name}' for countries passed")
            else:
                self.logger.error(f"Test '{self.test_name}' for countries failed")
        except Exception as e:
            self.logger.error(f"Test '{self.test_name}' for countries failed because of {e}")
        finally:
            assert job_countries_scraper == job_countries_peviitor

            
        # Test job  link
        try:
            if job_urls_scraper == job_urls_peviitor:
                self.logger.info(f"Test '{self.test_name}' for urls passed")
            else:
                self.logger.error(f"Test '{self.test_name}' for urls failed")
        except Exception as e:
            self.logger.error(f"Test '{self.test_name}' for urls failed because of {e}")
        finally:
            assert job_urls_scraper == job_urls_peviitor
