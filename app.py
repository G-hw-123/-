import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
from fetch import fetch_text
from tokenize_words import get_top_words


def generate_wordcloud(data):
    word_dict = {word: freq for word, freq in data}
    wc = WordCloud(
        font_path=None,
        width=800,
        height=400,
        background_color='white',
        max_words=100,
        prefer_horizontal=0.9
    ).generate_from_frequencies(word_dict)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    plt.title('Word Cloud', fontsize=16)
    return fig


def generate_bar(data):
    words = [item[0] for item in data]
    freqs = [item[1] for item in data]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=freqs, y=words, ax=ax, palette='viridis')
    ax.set_title('柱状图', fontsize=16)
    ax.set_xlabel('词频', fontsize=12)
    ax.set_ylabel('词汇', fontsize=12)
    plt.tight_layout()
    return fig


def generate_line(data):
    words = [item[0] for item in data]
    freqs = [item[1] for item in data]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=range(len(words)), y=freqs, ax=ax, marker='o', color='blue')
    ax.set_title('折线图', fontsize=16)
    ax.set_xlabel('词汇序号', fontsize=12)
    ax.set_ylabel('词频', fontsize=12)
    ax.set_xticks(range(len(words)))
    ax.set_xticklabels(words, rotation=45)
    plt.tight_layout()
    return fig


def generate_pie(data):
    words = [item[0] for item in data]
    freqs = [item[1] for item in data]
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(freqs, labels=words, autopct='%1.1f%%', startangle=90)
    ax.set_title('饼图', fontsize=16)
    plt.tight_layout()
    return fig


def generate_scatter(data):
    words = [item[0] for item in data]
    freqs = [item[1] for item in data]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.scatterplot(x=range(len(words)), y=freqs, ax=ax, s=100, color='red')
    ax.set_title('散点图', fontsize=16)
    ax.set_xlabel('词汇序号', fontsize=12)
    ax.set_ylabel('词频', fontsize=12)
    plt.tight_layout()
    return fig


def generate_funnel(data):
    words = [item[0] for item in data]
    freqs = [item[1] for item in data]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    y_pos = range(len(words))
    width = [f / max(freqs) * 100 for f in freqs]
    
    for i, (word, w) in enumerate(zip(words, width)):
        ax.barh(i, w, height=0.8, alpha=0.7)
        ax.text(w + 1, i, f'{word} ({freqs[i]})', va='center')
    
    ax.set_title('漏斗图', fontsize=16)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(words)
    ax.set_xlabel('相对频率 (%)', fontsize=12)
    plt.tight_layout()
    return fig


chart_renderers = {
    "词云图": generate_wordcloud,
    "柱状图": generate_bar,
    "折线图": generate_line,
    "饼图": generate_pie,
    "散点图": generate_scatter,
    "漏斗图": generate_funnel,
}


def main():
    st.set_page_config(page_title="词频分析可视化系统", layout="wide")
    st.title("词频分析可视化系统")
    st.sidebar.header("参数设置")

    url_input = st.sidebar.text_input("输入文章URL", "")
    custom_text = st.sidebar.text_area("或直接输入文本", "")

    min_freq = st.sidebar.slider("最低词频过滤", min_value=1, max_value=20, value=1, step=1)
    top_n = st.sidebar.slider("显示Top-N词汇", min_value=5, max_value=50, value=20, step=1)

    chart_type = st.sidebar.selectbox("选择图表类型", list(chart_renderers.keys()))

    if st.sidebar.button("开始分析"):
        with st.spinner("正在分析..."):
            try:
                if url_input:
                    text = fetch_text(url_input)
                    st.info(f"成功抓取网页内容，共 {len(text)} 字符")
                elif custom_text:
                    text = custom_text
                else:
                    st.warning("请输入URL或文本")
                    return

                if not text.strip():
                    st.error("未获取到有效文本内容")
                    return

                top_words = get_top_words(text, top_n, min_freq)

                if not top_words:
                    st.warning("没有满足条件的词汇，请降低词频阈值")
                    return

                st.subheader(f"{chart_type}")
                fig = chart_renderers[chart_type](top_words)
                st.pyplot(fig)
                plt.close('all')

                st.subheader("Top-20 高频词列表")
                df = pd.DataFrame(top_words, columns=["词汇", "词频"])
                st.dataframe(df)

                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
                st.download_button(
                    label="下载词频CSV",
                    data=csv_buffer.getvalue(),
                    file_name="word_frequency.csv",
                    mime="text/csv"
                )

            except Exception as e:
                st.error(f"分析失败: {str(e)}")


if __name__ == "__main__":
    main()
