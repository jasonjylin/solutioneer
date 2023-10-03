from utils.filter_data.filter_data import filter_data
from utils.search.metaphor_search import search_for_results
from utils.summarize.openai_summarize import summarize_findings


def search_filter_and_summarize(query, include_domains, exclude_domains):
    result, content = search_for_results(
        query=query, include_domains=include_domains, exclude_domains=exclude_domains
    )
    filtered_data, useful_products, used_links = filter_data(result, content)
    summary = summarize_findings(filtered_data)

    return summary, useful_products, used_links
