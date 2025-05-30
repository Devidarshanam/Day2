def print_results(self, results):
    if results:
        print("Search results:")
        for result in results:
            print(f"- {result}")  # Fixed undefined variable
    else:
        print("No results found.")
