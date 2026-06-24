# fetch.py
import requests
from bs4 import BeautifulSoup

def fetch_text(url: str, timeout: int = 10) -> str:
    """
    根据URL抓取网页正文，过滤脚本、样式标签
    :param url: 目标网页地址
    :param timeout: 请求超时时间
    :return: 纯文本内容
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=timeout)
        # 自动识别网页编码，解决乱码
        resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.text, "html.parser")

        # 移除无用标签
        for tag in soup(["script", "style", "iframe", "noscript"]):
            tag.decompose()

        return soup.get_text(strip=True)
    except requests.RequestException as e:
        return f"ERROR: 网页请求失败 -> {str(e)}"
