def main():
    crawler = WebCrawler()
    start_url = "https://example.com"
    crawler.crawl(start_url)  # Fixed typo

    keyword = "test"
    results = crawler.search(keyword)
    crawler.print_results(results)

if __name__ == "__main__":
    main()
