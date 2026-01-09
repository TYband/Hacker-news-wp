import requests
import json
from datetime import datetime

# ================= 配置区 =================
WP_USER = "wordpress中设置的"
WP_APP_PASS = "wordpress中设置的" 
# 注意：WP_URL 建议拆分为 BASE，方便后续调用媒体和分类接口
WP_BASE_URL = "https://你的网站/wp-json/wp/v2" 
HN_API = "https://hacker-news.firebaseio.com/v0"

# 自定义部分
TARGET_CATEGORY_NAME = "技术资讯"  # 在这里输入你想指定的分类名称
# ==========================================

def translate_text(text):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=zh-CN&dt=t&q={text}"
        res = requests.get(url, timeout=10)
        return res.json()[0][0][0]
    except Exception as e:
        print(f"翻译失败: {e}")
        return text

def get_category_id(name):
    """根据分类名称自动获取 ID"""
    try:
        res = requests.get(f"{WP_BASE_URL}/categories?search={name}", auth=(WP_USER, WP_APP_PASS))
        cats = res.json()
        if cats and isinstance(cats, list):
            return cats[0]['id']
        return 1 # 找不到则返回默认分类
    except:
        return 1

def upload_featured_image():
    """获取随机技术封面并上传到 WP 媒体库"""
    print("正在生成随机封面图...")
    # 使用 Unsplash Source API 获取随机科技图
    img_url = "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80"
    try:
        img_res = requests.get(img_url, timeout=15)
        if img_res.status_code == 200:
            headers = {
                'Content-Type': 'image/jpeg',
                'Content-Disposition': 'attachment; filename=hn_daily_cover.jpg'
            }
            # 上传至 WordPress 媒体库
            up_res = requests.post(f"{WP_BASE_URL}/media", data=img_res.content, headers=headers, auth=(WP_USER, WP_APP_PASS))
            return up_res.json().get('id')
    except Exception as e:
        print(f"图片上传失败: {e}")
    return None

def get_hn_top10():
    print("正在抓取并翻译 Hacker News 数据...")
    top_ids = requests.get(f"{HN_API}/topstories.json").json()[:10]
    html_content = "<blockquote>这是由机器人自动生成的今日 Hacker News 热点资讯。</blockquote><hr><ul>"
    
    for story_id in top_ids:
        item = requests.get(f"{HN_API}/item/{story_id}.json").json()
        raw_title = item.get('title')
        translated_title = translate_text(raw_title)
        link = item.get('url', f"https://news.ycombinator.com/item?id={story_id}")
        
        html_content += f"""
        <li style='margin-bottom: 15px;'>
            <strong>{translated_title}</strong><br>
            <span style='font-size: 0.85em; color: #666;'>原文：{raw_title}</span><br>
            🔗 <a href='{link}' target='_blank'>阅读原文 →</a>
        </li>"""
        
    html_content += "</ul>"
    return html_content

def post_to_wp(content):
    """发布到 WordPress (带分类和封面图)"""
    today = datetime.now().strftime("%Y年%m月%d日")
    
    # 1. 获取分类 ID
    cat_id = get_category_id(TARGET_CATEGORY_NAME)
    
    # 2. 上传封面图
    image_id = upload_featured_image()
    
    payload = {
        "title": f"Hacker News 今日热点精华 ({today})",
        "content": content,
        "status": "publish",
        "categories": [cat_id],
        "featured_media": image_id  # 关联特色图片 ID
    }
    
    res = requests.post(
        f"{WP_BASE_URL}/posts",
        json=payload,
        auth=(WP_USER, WP_APP_PASS)
    )
    
    if res.status_code == 201:
        print(f"✅ 发布成功！文章 ID: {res.json().get('id')}，已分类至: {TARGET_CATEGORY_NAME}")
    else:
        print(f"❌ 发布失败: {res.status_code} - {res.text}")

if __name__ == "__main__":
    # 执行主逻辑
    hn_content = get_hn_top10()
    post_to_wp(hn_content)
