import httpx


def search(query: str, limit: int = 3, client: httpx.Client | None = None) -> list[dict]:
    """Search SNL for articles."""
    url = f"https://snl.no/api/v1/search?query={query}&limit={limit}"
    
    if client:
        response = client.get(url)
    else:
        response = httpx.get(url)
    
    if response.status_code == 200:
        return response.json()
    return []


def fetch(permalink: str, client: httpx.Client | None = None) -> str:
    """Fetch full article from SNL by permalink. Returns the JSON as a string for the AI to read."""
    import json
    url = f"https://snl.no/{permalink}.json"
    
    if client:
        response = client.get(url)
    else:
        response = httpx.get(url)
    
    if response.status_code == 200:
        return json.dumps(response.json(), ensure_ascii=False, indent=2)
    return ""


if __name__ == "__main__":
    print("Testing SNL API for Taylor Swift...\n")
    
    results = search("Taylor Swift", limit=1)
    print(f"Search results: {results}\n")
    
    if results:
        permalink = results[0].get("permalink")
        print(f"Fetching article: {permalink}\n")
        article = fetch(permalink)
        print(f"Article (first 500 chars):\n{article}")
