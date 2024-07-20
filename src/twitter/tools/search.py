import requests
import json
import os

from langchain.tools import tool
from langchain_community.document_loaders import WebBaseLoader

class SearchTools:

    @tool('search twitter')
    def search_twitter(query: str) -> str:
        """
        Use this tool to search Twitter. This tool returns 5 results relevant to the query from Twitter.
        """
        return SearchTools.search(query, limit=5)

    @tool('open page')
    def open_page(url: str) -> str:
        """
        Use this tool to open a webpage and get the content.
        """
        loader = WebBaseLoader(url)    
        return loader.load()

    def search(query, limit=5):
        url = "https://api.twitter.com/2/tweets/search/recent"
        headers = {
            'Authorization': f"Bearer {os.getenv('TWITTER_BEARER_TOKEN')}",
            'Content-Type': 'application/json'
        }
        params = {
            "query": query,
            "max_results": limit
        }
        response = requests.get(url, headers=headers, params=params)
        results = response.json()

        # Assuming the API returns a list of tweets in 'data'
        string = []
        if 'data' in results:
            for result in results['data']:
                tweet_url = f"https://twitter.com/user/status/{result['id']}"
                string.append(f"{result['text']}\n{tweet_url}\n\n")

        return f"Search results for '{query}':\n\n" + "\n".join(string)

if __name__ == "__main__":
    print(SearchTools.open_page("https://www.python.org/"))