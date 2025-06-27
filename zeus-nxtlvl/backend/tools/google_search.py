import os
import requests

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")


def google_search(query: str, max_results: int = 5) -> list[str]:
    """Perform a Google Custom Search and return result titles."""
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        raise RuntimeError("Google API key or CSE ID not configured")

    endpoint = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": query,
        "num": max_results,
    }
    resp = requests.get(endpoint, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return [item["title"] for item in data.get("items", [])]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simple Google search tool")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--max", type=int, default=5, help="Number of results")
    args = parser.parse_args()

    for title in google_search(args.query, args.max):
        print(title)
