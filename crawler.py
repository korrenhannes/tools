'''
A web crawler for extracting email addresses from web pages.
Takes a string of URLs and requests each page, checks to see if we've
found any emails and writes each email it finds to a file.
'''

import argparse
import re
import sys
import requests
import ssl
from urllib.parse import urlparse

class Crawler(object):

    def __init__(self, urls):
        self.urls = urls.split(',')

    def crawl(self):
        with open('emails.txt', 'w') as file:
            processed_urls = set()
            for url in self.urls:
                self.crawl_url(url, file, processed_urls)

    def crawl_url(self, url, file, processed_urls):
        if url in processed_urls:
            return
        processed_urls.add(url)

        print(f"Processing URL: {url}")
        try:
            data = self.request(url)
            found_emails = False
            for email in self.process(data):
                found_emails = True
                print(f"Found email: {email}")
                file.write(email + '\n')

            if not found_emails:
                print("No emails found on this page.")

            for link in self.get_links(data):
                if self.is_subdomain(link, url):
                    self.crawl_url(link, file, processed_urls)
        except Exception as e:
            print(f"Error processing {url}: {e}")

    @staticmethod
    def get_links(data):
        # Extract links from the page data
        links = re.findall(r'href=["\'](https?://[^"\']+)["\']', data)
        return links

    def is_subdomain(self, link, main_url):
        # Improved check for subdomains
        main_domain = urlparse(main_url).netloc
        link_domain = urlparse(link).netloc

        # Normalize by removing 'www.'
        main_domain = main_domain.replace('www.', '')
        link_domain = link_domain.replace('www.', '')

        # Check if the link domain ends with the main domain
        return link_domain.endswith(main_domain) and link_domain != main_domain

    @staticmethod
    def request(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            # Add other headers if necessary
        }

        session = requests.Session()
        try:
            response = session.get(url, headers=headers)
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise


    @staticmethod
    def process(data):
        # Updated regex pattern to match a broader range of email formats
        pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        for email in re.findall(pattern, data):
            yield email


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--urls', dest='urls', required=True, help='A comma-separated string of URLs.')
    try:
        parsed_args = argparser.parse_args()
        crawler = Crawler(parsed_args.urls)
        crawler.crawl()
    except SystemExit:
        print("You need to provide URLs using the --urls argument.")
        return 1  # Return a non-zero value to indicate error

if __name__ == '__main__':
    sys.exit(main())
