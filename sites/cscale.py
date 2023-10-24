#
#
#
# c-scale > https://www.c-scale.ro/careers

from sites.website_scraper_bs4 import BS4Scraper

class CScaleScraper(BS4Scraper):
    
    """
    A class for scraping job data from c-scale website.
    """
    url = 'https://www.c-scale.ro/careers'
    url_logo = 'https://www.c-scale.ro/images/logo.png'
    company_name = 'cscale'
    
    def __init__(self):
        """
        Initialize the BS4Scraper class.
        """
        self.job_count = 1
        super().__init__(self.company_name, self.url_logo)
        
    def get_response(self):
        self.get_content(self.url)
    
    def scrape_jobs(self):
        """
        Scrape job data from c-scale website.
        """

        job_titles_elements = self.get_jobs_elements('css_', 'div > h2')
        
        self.job_titles = self.get_jobs_details_text(job_titles_elements)

        self.format_data()
        
    def sent_to_future(self):
        self.send_to_viitor()
    
    def return_data(self):
        self.get_response()
        self.scrape_jobs()
        return self.formatted_data, self.company_name

    def format_data(self):
        """
        Iterate over all job details and send to the create jobs dictionary.
        """
        for job_title in self.job_titles:
            job_url = self.url + "#" + str(self.job_count)
            self.create_jobs_dict(job_title, job_url, "România", "Craiova")
            self.job_count += 1

if __name__ == "__main__":
    cscale = CScaleScraper()
    cscale.get_response()
    cscale.scrape_jobs()
    cscale.sent_to_future()
    
    

