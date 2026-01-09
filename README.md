Hacker News Daily to WordPress 🚀
一个轻量级的 Python 自动化工具，每日定时抓取 Hacker News 热门文章，自动翻译并发布至 WordPress 博客，同时配备精美的特色封面图。

✨ 功能特性
数据采集：实时获取 Hacker News Top 10 热门资讯。
智能翻译：内置 Google 翻译接口，提供中英双语对照排版。
自动配图：对接 Unsplash API，为每篇博文自动上传并设置高质量科技主题封面。
动态分类：支持根据分类名称自动查找并匹配 WordPress 里的分类 ID。
全自动化：配合 Linux Crontab，实现 24/7 无人值守自动更新。

🛠️ 环境要求
Python 3.x
Ubuntu / Debian 或其他 Linux 服务器
WordPress 博客（开启 REST API 功能）

🚀 快速开始
1. 克隆项目
git clone https://github.com/你的用户名/你的项目名.git cd 你的项目名

3. 安装依赖
pip3 install requests

4. 配置 WordPress 凭据
为了安全连接，建议使用 WordPress 的应用程序密码：

登录 WP 后台 -> 用户 -> 个人资料。

在底部 “应用程序密码” 处添加新密码（如：HN-Bot）。

复制生成的 24 位代码。

4. 修改配置
打开 hackernews.py，修改配置区的参数：

WP_USER = "你的用户名" WP_APP_PASS = "xxxx xxxx xxxx xxxx xxxx xxxx" WP_BASE_URL = "https://你的域名.com/wp-json/wp/v2" TARGET_CATEGORY_NAME = "技术资讯"

⏰ 自动化部署
使用 crontab 设置每日定时运行：

执行命令： crontab -e

在文件末尾添加以下内容（例如每天上午 9 点运行）： 0 9 * * * /usr/bin/python3 /path/to/your/hackernews.py >> /path/to/hn_bot.log 2>&1

📂 项目结构
├── hackernews.py # 主程序脚本 ├── README.md # 项目说明文档 └── hn_bot.log # 运行日志（运行后自动生成）

🤝 贡献指南
欢迎提交 Issue 或 Pull Request 来优化翻译接口或增加更多资讯来源。
