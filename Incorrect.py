def search(self, keyword):
    results = []
    for url, text in self.index.items():
        if keyword.lower() in text.lower():  # Fixed logic
            results.append(url)
    return results
