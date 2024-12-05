import scrapy
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from scrapy.http import HtmlResponse


class WeatherSpider(scrapy.Spider):
    name = "weather"
    allowed_domains = ["tianqi.2345.com"]

    def __init__(self, start_date, end_date, *args, **kwargs):
        super(WeatherSpider, self).__init__(*args, **kwargs)
        # 将 start_date 和 end_date 转换为日期对象
        self.start_date = datetime.strptime(start_date, '%Y-%m')
        self.end_date = datetime.strptime(end_date, '%Y-%m')

    def start_requests(self):
        current_date = self.start_date

        while current_date <= self.end_date:
            # 构造 URL
            year = current_date.year
            month = current_date.month

            url = f"https://tianqi.2345.com/Pc/GetHistory?areaInfo%5BareaId%5D=57083&areaInfo%5BareaType%5D=2&date%5Byear%5D={year}&date%5Bmonth%5D={month}"

            # 发送请求
            yield scrapy.Request(url, self.parse)

            # 增加一个月
            current_date += relativedelta(months=1)

    def parse(self, response):
        # 解析 JSON 数据
        data = json.loads(response.text)
        weather_data = data.get('data', '')

        # 如果 html_content 存在且有效
        if "history-table" in weather_data:
            # 将 HTML 内容包装成 Scrapy 的 Response 对象
            html_response = HtmlResponse(url=response.url, body=weather_data, encoding='utf-8')

            # 调用 parse_table 函数来解析该 HTML 内容
            yield from self.parse_table(html_response)

    def parse_table(self, response):
        # 解析 HTML 表格数据
        rows = response.xpath('//table[@class="history-table"]/tr')[1:]  # 跳过表头行

        for row in rows:
            date = row.xpath('./td[1]/text()').get().strip().split(' ')[0]  # 提取日期
            high_temp = row.xpath('./td[2]/text()').get().strip()  # 提取最高温
            low_temp = row.xpath('./td[3]/text()').get().strip()  # 提取最低温
            weather = row.xpath('./td[4]/text()').get().strip()  # 提取天气情况
            wind = row.xpath('./td[5]/text()').get().strip()  # 提取风力风向
            aqi = row.xpath('./td[6]/span/text()').get().strip()  # 提取空气质量指数

            yield {
                'date': date,
                'high_temp': float(high_temp.replace('°', '')),
                'low_temp': float(low_temp.replace('°', '')),
                'weather': weather,
                'wind': wind,
                'aqi': int(aqi.split(' ')[0]),
            }
