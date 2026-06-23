import streamlit as st
import pandas as pd
import io
from fetch import fetch_text
from tokenize_words import get_top_words, get_word_freq
from pyecharts.charts import WordCloud, Bar, Line, Pie, Scatter, Funnel, Radar
from pyecharts import options as opts

st.set_page_config(page_title="词频分析可视化系统", layout="wide")

def generate_wordcloud(data):
    words = [(word, freq) for word, freq in data]
    wc = (
        WordCloud()
        .add("", words, word_size_range=[20, 100])
        .set_global_opts(title_opts=opts.TitleOpts(title="词云图"))
    )
    return wc.render_embed()

def generate_bar(data):
    words = [item[0] for item in data]
    freqs = [item[1] for item in data]
    bar = (
        Bar()
        .add_xaxis(words)
        .add_yaxis("词频", freqs)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="柱状图"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45))
        )
    )
    return bar.render_embed()

def generate_line(data):
    words = [item[0] for item in data]
    freqs = [item[1] for item in data]
    line = (
        Line()
        .add_xaxis(words)
        .add_yaxis("词频", freqs)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="折线图"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45))
        )
    )
    return line.render_embed()

def generate_pie(data):
    pie = (
        Pie()
        .add("", data)
        .set_global_opts(title_opts=opts.TitleOpts(title="饼图"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return pie.render_embed()

def generate_scatter(data):
    words = [item[0] for item in data]
    freqs = [item[1] for item in data]
    indices = list(range(1, len(words) + 1))
    scatter = (
        Scatter()
        .add_xaxis(indices)
        .add_yaxis("词频", list(zip(indices, freqs)))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="散点图"),
            xaxis_opts=opts.AxisOpts(name="词序"),
            yaxis_opts=opts.AxisOpts(name="词频")
        )
    )
    return scatter.render_embed()

def generate_funnel(data):
    funnel = (
        Funnel()
        .add("词频", data)
        .set_global_opts(title_opts=opts.TitleOpts(title="漏斗图"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return funnel.render_embed()

def generate_radar(data):
    top6 = data[:6]
    indicator = [{"name": item[0], "max": max([d[1] for d in data])} for item in top6]
    values = [[item[1] for item in top6]]
    
    radar = (
        Radar()
        .add_schema(indicator=indicator)
        .add("高频词", values)
        .set_global_opts(title_opts=opts.TitleOpts(title="雷达图（Top-6）"))
    )
    return radar.render_embed()

chart_renderers = {
    "词云图": generate_wordcloud,
    "柱状图": generate_bar,
    "折线图": generate_line,
    "饼图": generate_pie,
    "散点图": generate_scatter,
    "漏斗图": generate_funnel,
    "雷达图": generate_radar
}

def main():
    st.title("📊 词频分析可视化系统")
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
                
                st.subheader(f"📈 {chart_type}")
                chart_html = chart_renderers[chart_type](top_words)
                st.components.v1.html(chart_html, height=500)
                
                st.subheader("📋 Top-20 高频词列表")
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
