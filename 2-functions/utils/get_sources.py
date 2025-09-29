from openai.types.responses import Response

def get_sources(response: Response):
    """Extract sources from web search response"""
    if not hasattr(response, 'output'):
        return "No sources used."
    
    sources = []
    for item in response.output:
        if hasattr(item, 'type') and item.type == "web_search_call":
            if hasattr(item, 'action') and hasattr(item.action, 'sources') and item.action.sources:
                sources.extend(item.action.sources)
    
    if sources:
        print('SOURCES: ', sources)
        # Extract URLs from ActionSearchSource objects and get domain names
        urls = []
        for source in sources[:5]:  # Limit to first 5
            if hasattr(source, 'url') and source.url:  # Check that url is not None
                url = source.url
                domain = url.split('/')[2] if '//' in url else url
                urls.append(domain)
        
        if urls:
            return f"\n📚 Sources: {', '.join(urls)}\n\n"
        else:
            return "No sources used."
    else:
        return "No sources used."
