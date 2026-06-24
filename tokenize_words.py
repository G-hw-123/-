# tokenize_words.py
import jieba
from collections import Counter

# 加载停用词
def load_stopwords(file_path: str = "stopwords_cn.txt") -> set:
    """加载中文停用词表"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            stopwords = {line.strip() for line in f.readlines()}
        return stopwords
    except FileNotFoundError:
        return set()

STOP_WORDS = load_stopwords()

def get_word_frequency(text: str, min_freq: int = 1) -> Counter:
    """
    文本分词、去停用词、统计词频
    :param text: 原始文本
    :param min_freq: 最低词频过滤阈值
    :return: 词频计数器
    """
    if not text or text.startswith("ERROR"):
        return Counter()

    # 分词
    words = jieba.lcut(text)
    # 过滤停用词、单字符、低频词
    filter_words = [
        w for w in words
        if len(w) > 1 and w not in STOP_WORDS
    ]
    word_count = Counter(filter_words)
    # 按最低词频过滤
    filtered_count = Counter({k: v for k, v in word_count.items() if v >= min_freq})
    return filtered_count
