import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SECURITY_KEY = os.environ.get('SECURITY_KEY')
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{SECURITY_KEY}@localhost:5432/mydb"

# このengineを使用してデータベース操作を行う
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# このクラスを継承して各データベースモデルまたはクラス（ORMモデル）を作成する
Base = declarative_base()

# *****DUPLICATED*******
# SECURITY_KEY = os.environ.get('SECURITY_KEY')
# DIALECT = 'postgresql'
# HOST = 'localhost'
# PORT = '5432'
# CHARSET_TYPE = 'utf8mb4'
# db_name = 'postgresql'
#
# def db_config():
#     return create_engine(f"{DIALECT}://rsato:{SECURITY_KEY}@{HOST}:{PORT}/{db_name}?charset={CHARSET_TYPE}")
