import jieba
from collections import Counter
import os

def load_stopwords(filepath: str = 'stopwords_cn.txt') -> set:
    """
    加载停用词文件
    
    Args:
        filepath: 停用词文件路径
        
    Returns:
        停用词集合
    """
    stopwords = set()
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word:
                    stopwords.add(word)
    return stopwords

def tokenize(text: str) -> list:
    """
    对文本进行分词处理
    
    Args:
        text: 输入文本
        
    Returns:
        分词结果列表
    """
    if not text or not isinstance(text, str):
        return []
    
    words = jieba.lcut(text)
    stopwords = load_stopwords()
    
    filtered_words = [
        word for word in words 
        if word not in stopwords and len(word) >= 2
    ]
    
    return filtered_words

def get_word_freq(text: str, min_freq: int = 1) -> Counter:
    """
    计算词频统计
    
    Args:
        text: 输入文本
        min_freq: 最小词频阈值
        
    Returns:
        词频计数器
    """
    if not text:
        return Counter()
    
    words = tokenize(text)
    counter = Counter(words)
    
    if min_freq > 1:
        counter = Counter({k: v for k, v in counter.items() if v >= min_freq})
    
    return counter

def get_top_words(text: str, top_n: int = 20, min_freq: int = 1) -> list:
    """
    获取Top-N高频词
    
    Args:
        text: 输入文本
        top_n: 返回数量
        min_freq: 最小词频阈值
        
    Returns:
        按词频降序排列的(词, 频率)列表
    """
    counter = get_word_freq(text, min_freq)
    return counter.most_common(top_n)

if __name__ == "__main__":
    test_text = """人工智能是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。
    人工智能领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。"""
    
    words = tokenize(test_text)
    print("分词结果:", words[:10])
    
    freq = get_word_freq(test_text)
    print("词频统计:", freq.most_common(10))
    
    top_words = get_top_words(test_text, 5)
    print("Top-5高频词:", top_words)
