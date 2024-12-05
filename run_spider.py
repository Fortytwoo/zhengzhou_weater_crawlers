import sys
from scrapy.cmdline import execute

if __name__ == "__main__":
    # 读取命令行参数
    start_date = sys.argv[1] if len(sys.argv) > 1 else '2019-01'
    end_date = sys.argv[2] if len(sys.argv) > 2 else '2024-09'

    # 使用 execute 启动 Scrapy 爬虫，并传递日期参数
    execute(['scrapy', 'crawl', 'weather', '-a', f'start_date={start_date}', '-a', f'end_date={end_date}'])
