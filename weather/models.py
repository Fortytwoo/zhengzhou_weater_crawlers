from sqlalchemy import Column, Integer, String, DateTime, Float, Index, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


# 定义天气数据映射类
class WeatherInfo(Base):
    __tablename__ = 'weather_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False, index=True)  # 提取日期
    high_temp = Column(Float)  # 提取最高温
    low_temp = Column(Float)  # 提取最低温
    weather = Column(String(100))  # 提取天气情况
    wind = Column(String(100), nullable=True)  # 提取风力风向
    aqi = Column(Integer, nullable=True)  # 提取空气质量指数
    created_at = Column(DateTime, default=datetime.utcnow)  # 创建时间
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间


# 创建数据库连接和Session
DATABASE_URL = 'mysql+pymysql://root:123456@localhost:3306/weather_data'

# 创建引擎和Session工厂
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)

# 创建所有表（如果尚未创建）
Base.metadata.create_all(engine)
