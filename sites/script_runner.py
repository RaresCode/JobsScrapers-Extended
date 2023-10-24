
import os
import subprocess

class Scraper:
    def __init__(self, exclude):
        """
        Initialize the Scraper class.
        """
        self.exclude = exclude

    def run(self):
        """
        Run the scraper for each Python file in the current directory, excluding the specified files.
        """
        path = os.path.dirname(os.path.abspath(__file__))
        for site in os.listdir(path):
            if site.endswith('.py') and site not in self.exclude:
                try:
                    subprocess.check_call(['python', os.path.join(path, site)])
                    print("Success scraping " + site)
                except subprocess.CalledProcessError as e:
                    print("Error in " + site)
                    print(e.output.decode('utf-8'))

if __name__ == "__main__":
    # exclude files
    exclude = ['__init__.py',
               'script_runner.py',
               'setup_api.py',
               'update_logo.py',
               'website_scraper_api.py',
               'website_scraper_bs4.py',
               'website_scraper_selenium.py',
               'sephora.py', # returns wrong jobs
               'zucchetti.py', # gives api error
               'reinest.py', # This does not have a career's page now
               'typingdna.py', # This does not have a career's page now
               'netrom.py', # This does not have a career's page now
               'kaizengaming.py', # Website changed
               'brillio.py', # there are no jobs available
               'aeroportoradea.py', # Removed as they changed the page layout, to be fixed
               'mennekes.py', # This does not have jobs at this moment
               'test.py'
                ]

    scraper = Scraper(exclude)
    scraper.run()
