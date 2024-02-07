# 文件路径：app.py

from flask import Flask, render_template, request, jsonify
from my_package.news_api import fetch_news_data
from my_package.database_operations import insert_news_if_not_exists
from db_setup import init_app
from models import News, PlatformList
from datetime import date,datetime
from db_setup import db

app = Flask(__name__)

# 设置这里的 SQLALCHEMY_DATABASE_URI 和其他必要配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 将数据库实例与 Flask 应用关联
init_app(app)

@app.route('/')
def index():
    platforms = PlatformList.query.all()  # 获取所有平台
    today_str = date.today().isoformat()  # 获取今天的日期字符串

    platform_news = {}
    for platform in platforms:
        # 根据您错误信息中的提示，这里应该是 platform.platform_name 而非 platform.name
        platform_news[platform.platform_name] = News.query.filter(
            News.platform == platform.platform_name,  # 使用 platform.platform_name 访问平台名称
            db.func.strftime('%Y-%m-%d', News.date) == today_str
        ).order_by(News.date.desc()).all()

    return render_template('index.html', today=today_str, platform_news=platform_news)

@app.route('/update_news', methods=['POST'])
def update_news():
    api_url = "https://api.oioweb.cn/api/common/HotList"  # 确保该 url 正确且 API 有效
    news_data = fetch_news_data(api_url)
    inserted_count, duplicates = insert_news_if_not_exists(news_data)
    # 返回更新结果给前端
    return jsonify({'inserted': inserted_count, 'duplicates': len(duplicates)})

@app.route('/news_list')
def news_list():
    # 获取请求中的 date 参数
    date_param = request.args.get('date')
    
    # 根据是否有日期参数，准备查询
    if date_param:
        # 如果提供了日期，确保格式正确
        try:
            query_date = datetime.strptime(date_param, '%Y-%m-%d').date()
        except ValueError:
            # 如果日期格式不正确，可以返回错误提示或默认查询所有
            query_date = None
        if query_date:
            news_items = News.query.filter(db.func.date(News.date) == query_date).all()
        else:
            news_items = News.query.all()
    else:
        news_items = News.query.all()

    # 获取按平台组织的新闻
    platform_news = {}
    for platform in PlatformList.query.all():
        if date_param and query_date:
            platform_news[platform.platform_name] = News.query.filter(
                News.platform == platform.platform_name, 
                db.func.date(News.date) == query_date
            ).all()
           # print(f"平台: {platform.platform_name}, 新闻数量: {len(platform_news)}")  
        else:
            platform_news[platform.platform_name] = News.query.filter_by(platform=platform.platform_name).all()
           # print(f"平台: {platform.platform_name}, 新闻数量: {len(platform_news)}")


    
    return render_template(
        'news_list.html', 
        news_items=news_items, 
        platform_news=platform_news, 
        selected_date=date_param
    )

@app.route('/news', methods=['GET'])
def get_news_by_platform_and_date():
    platform = request.args.get('platform')
    date_str = request.args.get('date')  # 日期应该以YYYY-MM-DD格式传递

    try:
        # 尝试将传入的字符串转换为日期对象
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        # 如果日期格式不正确，返回一个错误响应
        return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD format.'}), 400

    # 使用传入的平台和日期值查询新闻
    news_items = News.query.filter(News.platform == platform, db.func.date(News.date) == date_obj.date()).all()

    # 将查询结果转换为字典列表
    news_list = [{'title': item.title, 'date': item.date, 'link': item.link, 'hot_topic': item.hot_topic} for item in news_items]

    return jsonify(news_list)


if __name__ == '__main__':
    app.run(debug=True)