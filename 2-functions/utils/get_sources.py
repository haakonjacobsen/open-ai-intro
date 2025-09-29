from openai.types.responses import Response

def get_sources(response: Response):
    """Extract sources from response content annotations"""
    try:
        if not hasattr(response, 'content') or not response.content:
            return "No sources used."
        
        urls = []
        
        # Look for annotations in the response content
        for content_item in response.content:
            if hasattr(content_item, 'annotations') and content_item.annotations:
                for annotation in content_item.annotations:
                    if hasattr(annotation, 'type') and annotation.type == "url_citation":
                        if hasattr(annotation, 'url') and annotation.url:
                            url = annotation.url
                            # Extract domain name from URL
                            domain = url.split('/')[2] if '//' in url else url
                            if domain not in urls:  # Avoid duplicates
                                urls.append(domain)
        
        if urls:
            # Limit to first 5 sources
            limited_urls = urls[:5]
            return f"\n📚 Sources: {', '.join(limited_urls)}\n\n"
        else:
            return ""
    except Exception as e:
        return f""
