import streamlit as st
import requests
from bs4 import BeautifulSoup
import jieba
from collections import Counter
from pyecharts.charts import WordCloud, Bar, Pie, Line, Funnel, Radar, Scatter
import re
import string

# 用于获取网页文本内容的函数，去除标点、空格等，设置响应编码为utf-8
def get_text_from_url(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'  # 设置响应编码为utf-8
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        # 去除标点符号
        text = text.translate(str.maketrans("", "", string.punctuation))
        # 去除多余空白字符并替换为单个空格
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except requests.RequestException as e:
        print(f"请求出错: {e}")
        return ""

# 进行分词和词频统计的函数，要求词长度不少于两个汉字
def word_frequency(text, top_n=20):
    words = jieba.cut(text)
    # 过滤掉长度小于2的词以及空白字符（可能残留的空格等情况）
    words = [word for word in words if len(word) >= 2 and word.strip()]
    word_counts = Counter(words)
    return word_counts.most_common(top_n)

# 使用pyecharts绘制词云图的函数
def draw_wordcloud(word_counts):
    wordcloud = WordCloud()
    data = [(word, count) for word, count in word_counts]
    wordcloud.add("", data)
    return wordcloud

# 使用pyecharts绘制柱状图的函数
def draw_bar_chart(word_counts):
    bar = Bar()
    words, counts = zip(*word_counts)
    bar.add_xaxis(list(words))
    bar.add_yaxis("词频", list(counts))
    return bar

# 使用pyecharts绘制饼图的函数
def draw_pie_chart(word_counts):
    pie = Pie()
    words, counts = zip(*word_counts)
    pie.add("", [list(z) for z in zip(words, counts)])
    return pie

# 使用pyecharts绘制折线图（示例，可能不太常规用于词频展示，可根据需求调整）
def draw_line_chart(word_counts):
    line = Line()
    words, counts = zip(*word_counts)
    line.add_xaxis(list(words))
    line.add_yaxis("词频", list(counts))
    return line

# 使用pyecharts绘制漏斗图（示例，可按需调整含义）
def draw_funnel_chart(word_counts):
    funnel = Funnel()
    words, counts = zip(*word_counts)
    funnel.add("词频漏斗", [list(z) for z in zip(words, counts)])
    return funnel

# 使用pyecharts绘制雷达图（示例，需合理构造数据维度）
def draw_radar_chart(word_counts):
    radar = Radar()
    words, counts = zip(*word_counts)
    schema = [{"name": word, "max": max(counts)} for word in words]
    radar.add_schema(schema)
    radar.add("词频", [dict(zip(words, counts))])
    return radar

# 使用pyecharts绘制散点图（示例，不太常规，可根据情况调整）
def draw_scatter_chart(word_counts):
    scatter = Scatter()
    words, counts = zip(*word_counts)
    scatter.add_xaxis(list(words))
    scatter.add_yaxis("词频", list(counts))
    return scatter


st.sidebar.title("图表选择")
selected_chart = st.sidebar.selectbox("请选择图表类型", ["词云图", "柱状图", "饼图", "折线图", "漏斗图", "雷达图", "散点图"])

url = st.text_input("请输入文章URL:")
if url:
    text = get_text_from_url(url)
    word_counts = word_frequency(text)
    min_count = st.sidebar.slider("过滤低频词（词频大于等于）", min_value=1, max_value=10, value=1)
    filtered_word_counts = [(word, count) for word, count in word_counts if count >= min_count]
    if selected_chart == "词云图":
        wordcloud = draw_wordcloud(filtered_word_counts)
        st.components.v1.html(wordcloud.render_embed(), height=400)
    elif selected_chart == "柱状图":
        bar_chart = draw_bar_chart(filtered_word_counts)
        st.components.v1.html(bar_chart.render_embed(), height=400)
    elif selected_chart == "饼图":
        pie_chart = draw_pie_chart(filtered_word_counts)
        st.components.v1.html(pie_chart.render_embed(), height=400)
    elif selected_chart == "折线图":
        line_chart = draw_line_chart(filtered_word_counts)
        st.components.v1.html(line_chart.render_embed(), height=400)
    elif selected_chart == "漏斗图":
        funnel_chart = draw_funnel_chart(filtered_word_counts)
        st.components.v1.html(funnel_chart.render_embed(), height=400)
    elif selected_chart == "雷达图":
        radar_chart = draw_radar_chart(filtered_word_counts)
        st.components.v1.html(radar_chart.render_embed(), height=400)
    elif selected_chart == "散点图":
        scatter_chart = draw_scatter_chart(filtered_word_counts)
        st.components.v1.html(scatter_chart.render_embed(), height=400)