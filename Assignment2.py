import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse
import unittest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO


class WebCrawler:
    def __init__(self):
        self.index = defaultdict(str)
        self.visited = set()

    def crawl(self, url, base_url=None):
        if url in self.visited:
            return
        self.visited.add(url)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            self.index[url] = soup.get_text()

            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    full_url = urljoin(base_url or url, href)
                    if full_url.startswith(base_url or url):
                        self.crawl(full_url, base_url=base_url or url)
        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def search(self, keyword):
        results = []
        for url, text in self.index.items():
            if keyword.lower() in text.lower():
                results.append(url)
        return results

    def print_results(self, results):
        if results:
            print("Search results:")
            for result in results:
                print(f"- {result}")
        else:
            print("No results found.")


def main():
    crawler = WebCrawler()
    start_url = "https://example.com"  # Replace with real URL to test
    crawler.crawl(start_url)

    keyword = "test"
    results = crawler.search(keyword)
    crawler.print_results(results)


# ===========================
# Unit Tests
# ===========================
class WebCrawlerTests(unittest.TestCase):
    @patch('requests.get')
    def test_crawl_success(self, mock_get):
        sample_html = """
        <html><body>
            <h1>Welcome!</h1>
            <a href="/about">About Us</a>
            <a href="https://www.external.com">External Link</a>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = sample_html
        mock_get.return_value = mock_response

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        self.assertIn("https://example.com", crawler.index)
        self.assertIn("https://example.com", crawler.visited)
        self.assertIn("https://example.com/about", crawler.visited)

    @patch('requests.get')
    def test_crawl_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Test Error")

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        self.assertIn("https://example.com", crawler.visited)

    def test_search(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "This has the keyword"
        crawler.index["page2"] = "No match here"

        results = crawler.search("keyword")
        self.assertEqual(results, ["page1"])

    def test_print_results(self):
        crawler = WebCrawler()
        results = ["https://test.com/result"]

        captured_output = StringIO()
        sys.stdout = captured_output
        crawler.print_results(results)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("Search results:", output)
        self.assertIn("https://test.com/result", output)


# Run main and tests only if executed directly
if __name__ == "__main__":
    # Run tests first
    unittest.main(exit=False)

    # Then run the crawler
    print("\n--- Running Main Crawler ---")
    main()
