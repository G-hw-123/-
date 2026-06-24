# app.py
import streamlit as st
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import WordCloud, Bar, Line, Pie, Scatter, Funnel, Radar
from pyecharts.globals import ThemeType

from fetch import fetch_text
from tokenize_words import get_word_frequency

# ===================== 页面基础配置 =====================
st.set_page_config(page_title="文本词频分析系统", layout="wide")
st.title("📄 网页文本词频分析与可视化平台")

# ===================== 侧边栏配置 =====================
with st.sidebar:
    st.header("功能设置")
    url = st.text_input("请输入文章URL：", value="")
    min_frequency = st.slider("最低词频过滤阈值", min_value=1, max_value=20, value=2)
    chart_type = st.selectbox(
        "选择可视化图表类型",
        [
            "词云图", "柱状图", "折线图", "饼图",
            "散点图", "漏斗图", "雷达图"
        ]
    )
    run_btn = st.button("开始分析")

# ===================== 图表渲染函数（字典派发） =====================
def render_wordcloud(data):
    words = [(k, v) for k, v in data.most_common(50)]
    c = (
        WordCloud(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width="1000px", height="600px"))
        .add(series_name="词频", data_pair=words, word_size_range=[10, 80])
        .set_global_opts(title_opts=opts.TitleOpts(title="文本词云图"))
    )
    return c.render_embed()

def render_bar(data):
    top20 = data.most_common(20)
    x = [i[0] for i in top20]
    y = [i[1] for i in top20]
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width="1000px", height="600px"))
        .add_xaxis(x)
        .add_yaxis("词频", y)
        .set_global_opts(title_opts=opts.TitleOpts(title="Top20 词汇词频柱状图"), xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)))
    )
    return c.render_embed()

def render_line(data):
    top20 = data.most_common(20)
    x = [i[0] for i in top20]
    y = [i[1] for i in top20]
    c = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width="1000px", height="600px"))
        .add_xaxis(x)
        .add_yaxis("词频", y, is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="Top20 词汇词频折线图"), xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)))
    )
    return c.render_embed()

def render_pie(data):
    top10 = data.most_common(10)
    c = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width="1000px", height="600px"))
        .add("", top10, radius=["30%", "75%"], center=["50%", "50%"])
        .set_global_opts(title_opts=opts.TitleOpts(title="Top10 词汇占比饼图"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return c.render_embed()

def render_scatter(data):
    top20 = data.most_common(20)
    x = [str(i+1) for i in range(len(top20))]
    y = [i[1] for i in top20]
    c = (
        Scatter(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width="1000px", height="600px"))
        .add_xaxis(x)
        .add_yaxis("词频", y)
        .set_global_opts(title_opts=opts.TitleOpts(title="词汇词频散点图"))
    )
    return c.render_embed()

def render_funnel(data):
    top10 = data.most_common(10)
    c = (
        Funnel(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width="1000px", height="600px"))
        .add("词频漏斗", top10, sort_="descending")
        .set_global_opts(title_opts=opts.TitleOpts(title="词频漏斗图"))
    )
    return c.render_embed()

def render_radar(data):
    # 雷达图限制Top6，避免溢出（修复Bug）
    top6 = data.most_common(6)
    indicators = [opts.RadarIndicatorItem(name=k, max_=max([x[1] for x in top6])) for k, _ in top6]
    values = [[v for _, v in top6]]
    c = (
        Radar(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width="1000px", height="600px"))
        .add_schema(schema=indicators)
        .add("词频", values)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(title_opts=opts.TitleOpts(title="Top6 词汇雷达图"))
    )
    return c.render_embed()

# 图表路由字典（替代if-elif，代码优化）
chart_dispatch = {
    "词云图": render_wordcloud,
    "柱状图": render_bar,
    "折线图": render_line,
    "饼图": render_pie,
    "散点图": render_scatter,
    "漏斗图": render_funnel,
    "雷达图": render_radar
}

# ===================== 主逻辑执行 =====================
if run_btn and url.strip():
    with st.spinner("正在抓取网页、分析文本，请稍候..."):
        # 1. 抓取文本
        raw_text = fetch_text(url)
        if raw_text.startswith("ERROR"):
            st.error(raw_text)
        else:
            # 2. 词频统计
            word_counter = get_word_frequency(raw_text, min_frequency)
            if not word_counter:
                st.warning("未分析出有效词汇，请调整词频阈值或更换URL！")
            else:
                # 3. 基础数据展示
                st.subheader("📊 词频统计表(Top20)")
                df = pd.DataFrame(word_counter.most_common(20), columns=["词汇", "词频"])
                st.dataframe(df, use_container_width=True)

                # 4. 渲染选中图表
                st.subheader("📈 可视化图表")
                chart_html = chart_dispatch[chart_type](word_counter)
                st.components.v1.html(chart_html, height=620)

                # 5. 导出CSV（Should级功能）
                st.download_button(
                    label="📥 下载词频数据(CSV)",
                    data=df.to_csv(index=False, encoding="utf-8-sig"),
                    file_name="word_frequency.csv",
                    mime="text/csv"
                )
elif run_btn and not url.strip():
    st.warning("请先输入有效的网页URL！")
