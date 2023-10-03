from utils.search_filter_summarize import search_filter_and_summarize


def main():
    while True:
        query = input("Enter a search query (or 'exit' to quit): ")
        if query.lower() == "exit":
            break

        include_domains_input = input(
            "Enter a list of domains to include (comma-separated, or press Enter to skip): "
        )
        include_domains = [
            domain.strip()
            for domain in include_domains_input.split(",")
            if domain.strip()
        ]
        if not include_domains:
            include_domains = None

        exclude_domains_input = input(
            "Enter a list of domains to exclude (comma-separated, or press Enter to skip): "
        )
        exclude_domains = [
            domain.strip()
            for domain in exclude_domains_input.split(",")
            if domain.strip()
        ]
        if not exclude_domains:
            exclude_domains = None

        summary, products, links = search_filter_and_summarize(
            query=query,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
        )

        print("\nSummary:")
        print(summary)

        if links:
            print("\nUseful Links:")
            for link in links:
                print(link)

        if products:
            print("\nPotentially Useful Resources:")
            for resource in products:
                print(resource)

        


if __name__ == "__main__":
    main()
