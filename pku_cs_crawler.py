import requests
from bs4 import BeautifulSoup
import csv
import time
import random

# 1. 替换为你实际的新闻页面地址（需与截图对应）
NEWS_URL = "https://eecs.pku.edu.cn/index/xwdt.htm"
BASE_URL = "https://eecs.pku.edu.cn"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": BASE_URL
}
CSV_FILE = "pku_cs_news.csv"

def get_news_list():
    try:
        time.sleep(random.uniform(1, 3))
        response = requests.get(NEWS_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 2. 匹配截图中的新闻条目结构：<div class="box">
        news_items = soup.find_all("div", class_="box")
        if not news_items:
            print("未找到新闻条目，请确认页面地址正确")
            return []
        
        news_list = []
        for item in news_items:
            # 3. 匹配标题：<div class="text">下的<a class="tit">
            text_div = item.find("div", class_="text")
            if not text_div:
                continue
            title_tag = text_div.find("a", class_="tit")
            if not title_tag:
                continue
            
            # 提取标题与链接
            title = title_tag.get_text(strip=True)
            link = title_tag.get("href")
            # 拼接完整链接（适配截图中的相对路径）
            if link and link.startswith(".."):
                link = link.replace("..", BASE_URL)
            elif link and not link.startswith("http"):
                link = f"{BASE_URL}{link}"
            
            # 4. 匹配时间：<div class="text">下的<div class="date">
            time_tag = text_div.find("div", class_="date")
            publish_time = time_tag.get_text(strip=True) if time_tag else "未知时间"
            
            news_list.append({
                "标题": title,
                "发布时间": publish_time,
                "详情链接": link
            })
            print(f"已抓取：{publish_time} - {title}")
        
        return news_list
    
    except Exception as e:
        print(f"获取新闻失败：{str(e)}")
        return []

def save_to_csv(news_list):
    if not news_list:
        print("无数据可保存")
        return
    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["标题", "发布时间", "详情链接"])
        writer.writeheader()
        writer.writerows(news_list)
    print(f"\n数据已保存到 {CSV_FILE}，共 {len(news_list)} 条新闻")

if __name__ == "__main__":
    print("===== 北大信科新闻爬虫开始运行 =====")
    news_data = get_news_list()
    save_to_csv(news_data)
    print("===== 爬虫运行结束 =====")
