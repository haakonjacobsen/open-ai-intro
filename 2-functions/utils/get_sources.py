from anthropic.types import Message


def get_sources(response: Message):
    """Extract the web sources Claude cited, as a list of domain names"""
    domains = []

    # When Claude uses web search, the text blocks in the reply carry citations
    for block in response.content:
        if block.type != "text" or not block.citations:
            continue
        for citation in block.citations:
            if citation.type != "web_search_result_location":
                continue
            # Extract the domain name from the URL, e.g. https://www.bbc.com/news/... -> www.bbc.com
            domain = citation.url.split("/")[2] if "//" in citation.url else citation.url
            if domain not in domains:  # Avoid duplicates
                domains.append(domain)

    if not domains:
        return ""

    # Limit to the first 5 sources
    return f"\n📚 Sources: {', '.join(domains[:5])}\n"
