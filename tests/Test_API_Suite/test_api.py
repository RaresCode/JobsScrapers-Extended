from tests.module_names import module_names
from tests.logger import get_logger
from tests.utils import TestUtils
import importlib
import pytest

class SetupTests:
    def import_all_modules(self):

        scraper_classes = []

        # for module_name, class_name in zip(module_names, class_names):
        for module_name, class_name in module_names.items():
            try:
                module = importlib.import_module(f"sites.{module_name}")
                class_obj = getattr(module, class_name)
                scraper_classes.append(class_obj)
                print(f"Imported class {class_name} from module {module_name}")
                # You can now use class_obj for further operations
            except ModuleNotFoundError:
                print(f"Module not found: {module_name}")
            except AttributeError:
                print(f"Class not found: {class_name} in module {module_name}")
        
        return scraper_classes
    
    def get_jobs_careers(self, scraper_class):
        """
        Fixture for scraping process from the career section.
        """
        self.scraper_data = scraper_class().return_data()

class TestScrapers:
    @pytest.fixture(params=SetupTests().import_all_modules())
    def scraper_class(self, request):
        return request.param
    
    def set_logger(self, test_name):
        self.test_name = test_name
        self.logger = get_logger(self.test_name)
    
    @pytest.mark.regression
    def test_scrapers(self, scraper_class):
        setup_tests = SetupTests()
        setup_tests.get_jobs_careers(scraper_class)
        self.set_logger(setup_tests.scraper_data[1])
        
        # You can now use the utility methods from TestUtils to avoid code duplication
        try:
            scraped_jobs_data = TestUtils.scrape_jobs(setup_tests.scraper_data[0])
        except Exception as e:
            self.logger.error(f"'{self.test_name}' Test failed to get data from the jobs site because of {e}")
        
        try:
            peviitor_jobs_data = TestUtils.scrape_peviitor(setup_tests.scraper_data[1], 'România')
        except Exception as e:
            self.logger.error(f"'{self.test_name}' Test failed to get data from peviitor because of {e}")

        # Test Title
        try:
            if sorted(scraped_jobs_data[0]) == sorted(peviitor_jobs_data[0]):
                self.logger.info(f"Test '{self.test_name}' for titles passed")
            else:
                self.logger.error(f"Test '{self.test_name}' for titles failed")
        except Exception as e:
            self.logger.error(f"Test '{self.test_name}' for titles failed because of {e}")
        
        # Test job city
        try:
            if sorted(scraped_jobs_data[1]) == sorted(peviitor_jobs_data[1]):
                self.logger.info(f"Test '{self.test_name}' for cities passed")
            else:
                self.logger.error(f"Test '{self.test_name}' for cities failed")
        except Exception as e:
            self.logger.error(f"Test '{self.test_name}' for cities failed because of {e}")
    
        # Test job country
        try:
            if sorted(scraped_jobs_data[2]) == sorted(peviitor_jobs_data[2]):
                self.logger.info(f"Test '{self.test_name}' for countries passed")
            else:
                self.logger.error(f"Test '{self.test_name}' for countries failed")
        except Exception as e:
            self.logger.error(f"Test '{self.test_name}' for countries failed because of {e}")
            
        # Test job  link
        try:
            if sorted(scraped_jobs_data[3]) == sorted(peviitor_jobs_data[3]):
                self.logger.info(f"Test '{self.test_name}' for urls passed")
            else:
                self.logger.error(f"Test '{self.test_name}' for urls failed")
        except Exception as e:
            self.logger.error(f"Test '{self.test_name}' for urls failed because of {e}")
        
        assert sorted(scraped_jobs_data[0]) == sorted(peviitor_jobs_data[0])
        assert sorted(scraped_jobs_data[1]) == sorted(peviitor_jobs_data[1])
        assert sorted(scraped_jobs_data[2]) == sorted(peviitor_jobs_data[2])
        assert sorted(scraped_jobs_data[3]) == sorted(peviitor_jobs_data[3])