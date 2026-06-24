# 词频分析可视化系统

一个基于 Streamlit 的中文文本词频分析与可视化 Web 应用。

## 功能特点

- 📊 **URL抓取**: 输入文章URL自动抓取正文内容
- 🔤 **中文分词**: 使用jieba进行智能分词，支持停用词过滤
- 📈 **7种可视化图表**: 词云图、柱状图、折线图、饼图、散点图、漏斗图、雷达图
- ⚙️ **交互式参数**: 可调节最低词频阈值和Top-N显示数量
- 💾 **数据导出**: 支持下载词频统计CSV文件

## 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 启动应用
streamlit run app.py
```

浏览器访问 http://localhost:8501

## 在线部署

本项目已部署在 Streamlit Community Cloud:

[在线演示链接](待部署后填写)

## 项目结构

```
word-frequency-analyzer/
├── app.py              # Streamlit主入口
├── fetch.py            # 网页抓取模块
├── tokenize_words.py   # 分词与词频模块
├── stopwords_cn.txt    # 中文停用词表
├── requirements.txt    # 依赖清单
└── README.md           # 项目说明
```

## 技术栈

- **Web框架**: Streamlit
- **网页抓取**: requests + BeautifulSoup4
- **中文分词**: jieba
- **可视化**: pyecharts

## 使用说明

1. 在侧边栏输入文章URL或直接粘贴文本
2. 调节最低词频过滤滑块（过滤低频词）
3. 设置Top-N显示数量
4. 选择图表类型
5. 点击"开始分析"按钮

## 作者

课程设计作业 - 《软件创新思维训练》
