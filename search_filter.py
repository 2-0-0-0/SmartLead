# --- search_filter.py ---
import requests

SERPAPI_API_KEY = "c38b7e3912279028f7b5520bd4fe3842f7ba91df9ac7a8155db6ddb2848efebf"  # Replace with your SerpAPI key

def smart_search(query, location=""):
    params = {
        "q": f"{query} companies {location}",
        "engine": "google",  # or "bing"
        "api_key": SERPAPI_API_KEY
    }

    response = requests.get("https://serpapi.com/search", params=params)

    if response.status_code == 200:
        results = response.json()
        companies = []

        for res in results.get("organic_results", [])[:5]:  # top 5 results
            title = res.get("title", "Unknown")
            link = res.get("link", "")
            snippet = res.get("snippet", "No description")

            companies.append({
                "company": title,
                "domain": link,
                "location": location,
                "description": snippet
            })
        return companies

    else:
        return [{
            "company": "No results",
            "domain": "N/A",
            "location": location,
            "description": f"Search failed: {response.text}"
        }]
