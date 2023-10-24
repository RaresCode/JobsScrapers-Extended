#
#
#
# etusoft > https://www.etusoft.com/locuridemunca.html


from sites.website_scraper_bs4 import BS4Scraper

class etusoftScraper(BS4Scraper):
    
    """
    A class for scraping job data from etusoft website.
    """
    url = 'https://www.etusoft.com/locuridemunca.html'
    url_logo = 'https://www.etusoft.com/assets/img/etusoft_logo.png'
    company_name = 'etusoft'
    
    
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
        Scrape job data from etusoft website.
        """

        job_titles_elements = self.get_jobs_elements('class_', 'case-studies-section')
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
            self.create_jobs_dict(job_title, job_url, "România", "Oradea")
            self.job_count += 1

if __name__ == "__main__":
    etusoft = etusoftScraper()
    etusoft.get_response()
    etusoft.scrape_jobs()
    etusoft.sent_to_future()
    
    

