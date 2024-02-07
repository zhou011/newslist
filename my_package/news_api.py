# 文件路径：/your/project/path/my_package/news_api.py

import pandas as pd
import requests
from typing import List, Dict

# 查询最新的新闻list
def fetch_news_data(api_url: str) -> List[Dict[str, str]]:
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises a HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:  # This will handle all exceptions raised by the requests library
        print(f"Error fetching data from API: {e}")
        return []  # Return an empty list in case of an error

    data = response.json()
    data_content = data.get("result", {})  # Defensive coding, using get with default return value

    news_list = []
    for key, value in data_content.items():
        for item in value:
            result_dict = {
                '平台': key,
                'index': item.get("index", "N/A"),  # Using get with default value in case key doesn't exist
                'title': item.get("title", "N/A"),
                'hot': item.get("hot", "N/A"),
                'href': item.get("href", "N/A")
            }
            news_list.append(result_dict)

    return news_list