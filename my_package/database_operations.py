# 文件路径：/your/project/path/my_package/database_operations.py


from db_setup import db
from typing import List, Dict, Tuple
from models import News, PlatformList


def insert_news_if_not_exists(news_list):
    inserted_count = 0
    duplicate_news = []
    platforms_added = set()  # 使用集合来记录已处理的平台名称，并确保去重

    for news_item in news_list:
        # 首先更新平台名称到 PlatformList
        platform_name = news_item['平台']
        if platform_name not in platforms_added and not PlatformList.query.filter_by(platform_name=platform_name).first():
            platform = PlatformList(platform_name=platform_name)
            db.session.add(platform)
            platforms_added.add(platform_name)

        # 检查新闻链接是否为空
        if not news_item['href']:
            # 如果链接为空，可能需要记录下来，根据实际情况处理
            continue

        # 然后，处理新闻条目的插入
        if not News.query.filter_by(title=news_item['title'], link=news_item['href']).first():
            new_news = News(
                platform=platform_name,
                title=news_item['title'],
                link=news_item['href'],
                hot_topic=news_item['hot'], 
                # 假设您有一个 date 字段，且已在 News 定义中设置为默认当前时间
                # date=...
            )
            db.session.add(new_news)
            inserted_count += 1
        else:
            duplicate_news.append(news_item)

    # 将所有挂起的更改提交到数据库
    db.session.commit()
    return inserted_count, duplicate_news