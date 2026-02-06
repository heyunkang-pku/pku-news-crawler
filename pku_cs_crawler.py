import requests
from bs4 import BeautifulSoup
import csv
import time
import random

# 配置项（可根据需求修改）
BASE_URL = "https://eecs.pku.edu.cn"  # 北大信科官网
NEWS_URL = f"{BASE_URL}/news/xwdt.htm"  # 新闻动态页面
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": BASE_URL
}
CSV_FILE = "pku_cs_news.csv"  # 保存结果的文件名

def get_news_list():
    """获取新闻列表（标题、时间、链接）"""
    try:
        # 发送请求（添加随机延迟，避免反爬）
        time.sleep(random.uniform(1, 3))
        response = requests.get(NEWS_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()  # 抛出HTTP错误
        response.encoding = "utf-8"  # 强制指定编码，避免乱码
        
        # 解析页面
        soup = BeautifulSoup(response.text, "html.parser")
        news_items = soup.find_all("li", class_="news_li")  # 定位新闻条目
        
        news_list = []
        for item in news_items:
            # 提取标题和链接
            title_tag = item.find("a")
            title = title_tag.get_text(strip=True)
            link = title_tag.get("href")
            # 拼接完整链接（处理相对路径）
            if not link.startswith("http"):
                link = f"{BASE_URL}{link}"
            
            # 提取发布时间
            time_tag = item.find("span", class_="news_date")
            publish_time = time_tag.get_text(strip=True) if time_tag else "未知时间"
            
            news_list.append({
                "标题": title,
                "发布时间": publish_time,
                "详情链接": link
            })
            print(f"已抓取：{publish_time} - {title}")
        
        return news_list
    
    except Exception as e:
        print(f"获取新闻列表失败：{str(e)}")
        return []

def save_to_csv(news_list):
    """将新闻数据保存为CSV文件"""
    if not news_list:
        print("无数据可保存")
        return
    
    # 写入CSV（UTF-8编码，支持中文）
    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["标题", "发布时间", "详情链接"])
        writer.writeheader()  # 写入表头
        writer.writerows(news_list)
    
    print(f"\n数据已保存到 {CSV_FILE}，共 {len(news_list)} 条新闻")

if __name__ == "__main__":
    print("===== 北大信科新闻爬虫开始运行 =====")
    news_data = get_news_list()
    save_to_csv(news_data)
    print("===== 爬虫运行结束 =====")