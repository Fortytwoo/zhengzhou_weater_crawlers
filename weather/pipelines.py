# pipelines.py
from weather.models import Session, WeatherInfo


class MySQLPipeline:
    def open_spider(self, spider):
        # 创建数据库会话
        self.session = Session()

    def close_spider(self, spider):
        # 提交事务并关闭会话
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        # 创建 WeatherInfo 对象并添加到 session 中
        weather_data = WeatherInfo(
            date=item['date'],
            high_temp=item['high_temp'],
            low_temp=item['low_temp'],
            weather=item['weather'],
            wind=item.get('wind'),
            aqi=item.get('aqi')
        )
        self.session.add(weather_data)
        return item
