#
#
#
# basware > https://careers.basware.com/


from sites.website_scraper_bs4 import BS4Scraper
import subprocess
import re

class baswareScraper(BS4Scraper):
    
    """
    A class for scraping job data from basware website.
    """
    url = 'https://cdn.jobylon.com/jobs/company-groups/195/embed/v2/?target=jobylon-jobs-widget&page_size=200#'
    url_logo = 'https://www.basware.com/assets/images/basware-logo.svg?v=1'
    company_name = 'basware'
    
    def __init__(self):
        """
        Initialize the BS4Scraper class.
        """
        super().__init__(self.company_name, self.url_logo)
        
    # def get_response(self):
    #     self.get_content(self.url)

    def unicode_to_text(self, text):
        return text.encode().decode('unicode_escape').encode('latin-1').decode('utf-8')

    def scrape_jobs(self):
        """
        Scrape job data from basware website.
        """

        self.job_titles = []
        self.job_urls = []
        self.job_cities = []
        
        command = ["curl", self.url]

        # Execute the curl command and capture the output
        output = subprocess.check_output(command)

        # Decode the output as a string
        output = output.decode("utf-8")
        
        # Define the regular expressions to extract the required information
        title_pattern = r"title: '([^']+)'"
        url_pattern = r"url: '([^']+)'"
        department_pattern = r"departments: \[\s*'([^']+)'"

        # Find all occurrences of titles, URLs, and departments using regular expressions
        titles = re.findall(title_pattern, str(output))
        urls = re.findall(url_pattern, str(output))
        departments = re.findall(department_pattern, str(output))

        # Print the extracted information
        for i in range(len(titles)):
            if departments[i].replace("u002D", "").split()[0] == "Romania":
                self.job_titles.append(self.unicode_to_text(titles[i]))
                self.job_urls.append(urls[i])
                self.job_cities.append(departments[i].replace("u002D", "").split()[-1])
        
        self.format_data()
     
    def sent_to_future(self):
        self.send_to_viitor()
    
    def return_data(self):
        self.scrape_jobs()
        return self.formatted_data, self.company_name
    
    def format_data(self):
        """
        Iterate over all job details and send to the create jobs dictionary.
        """
        for job_title, job_url, job_city in zip(self.job_titles, self.job_urls, self.job_cities):
            job_url = f"https://emp.jobylon.com{job_url}"
            self.create_jobs_dict(job_title, job_url, "România", job_city)

if __name__ == "__main__":
    basware = baswareScraper()
    basware.scrape_jobs()
    basware.sent_to_future()
    
    

