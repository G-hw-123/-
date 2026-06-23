import requests
from bs4 import BeautifulSoup
import re

def fetch_text(url: str) -> str:
    """
    从指定URL抓取网页正文内容
    
    Args:
        url: 网页地址
        
    Returns:
        网页正文文本
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=10)
        resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        for script in soup(["script", "style", "noscript", "iframe", "nav", "header", "footer"]):
            script.decompose()
        
        text = soup.get_text(separator='\n', strip=True)
        text = re.sub(r'\n+', '\n', text).strip()
        
        return text
    except requests.RequestException as e:
        raise Exception(f"抓取网页失败: {str(e)}")
    except Exception as e:
        raise Exception(f"解析网页失败: {str(e)}")

if __name__ == "__main__":
    url = "https://www.example.com"
    text = fetch_text(url)
    print(text[:500])
