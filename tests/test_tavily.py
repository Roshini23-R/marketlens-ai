from tavily import TavilyClient

from app.config import TAVILY_API_KEY


def main() -> None:
    if not TAVILY_API_KEY:
        print("TAVILY_API_KEY not set — check your .env file")
        return

    client = TavilyClient(api_key=TAVILY_API_KEY)

    response = client.search(
        query="Zoho pricing",
        max_results=2,
        search_depth="basic",
    )

    results = response.get("results", [])

    print(f"Results found: {len(results)}")

    if results:
        first = results[0]
        print(f"First title: {first.get('title', 'Untitled')}")
        print(f"First URL: {first.get('url', '')}")


if __name__ == "__main__":
    main()