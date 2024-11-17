from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine



DATABASE_URI = 'postgresql+psycopg2://{}:{}@localhost/cultural_corner'
engine = create_engine(DATABASE_URI)

Base = declarative_base()

class Transactions(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True)
    date_time = Column(DateTime)
    payment_method = Column(String)
    transaction_type = Column(String)
    store_id = Column(Integer)

class Products(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_description = Column(String)
    product_category = Column(String)
    unit_price = Column(Float)
    total_sold = Column(Integer)

class Stores(Base):
    __tablename__ = 'stores'
    store_id = Column(Integer, primary_key=True)
    store_city = Column(String)
    store_address = Column(String)
    store_postalcode = Column(String)

class Stocks(Base):
    __tablename__ = 'stocks'
    store_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, primary_key=True)
    stock_level = Column(Integer)

class Transaction_Products(Base):
    __tablename__ = 'transaction_products'
    transaction_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, primary_key=True)
    quantity_sold = Column(Integer)
    discount = Column(Float)
    total_price = Column(Float)

Base.metadata.create_all(engine)