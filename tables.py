from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Text, BigInteger
from sqlalchemy.orm import relationship
from datetime import date



Base = declarative_base()



class Consignment(Base):
    __tablename__ = 'Consignment'
    __table_args__ = {'schema': 'cw'}

    id = Column(BigInteger, primary_key=True)
    tonnage = Column(BigInteger)
    date_of_manufacturing = Column(Date)
    product_id = Column(BigInteger, ForeignKey("cw.Product.id"))
    manufacturer_id = Column(BigInteger, ForeignKey("cw.Manufacturer.id"))
    price_per_unit = Column(BigInteger)

    def __init__(self, tonnage, date_of_manufacturing, product_id, manufacturer_id, price_per_unit):
        self.tonnage = tonnage
        self.date_of_manufacturing = date_of_manufacturing
        self.product_id = product_id
        self.manufacturer_id = manufacturer_id
        self.price_per_unit = price_per_unit


class Consignment_arrival(Base):
    __tablename__ = "Consignment_arrival"
    __table_args__ = {'schema': 'cw'}

    id = Column(BigInteger, primary_key="True")
    consignment_id = Column(BigInteger, ForeignKey("cw.Consignment.id"))
    warehouse_id = Column(BigInteger, ForeignKey("cw.Warehouse.id"))
    date_of_arrival = Column(Date)

    def __init__(self, consignment_id, warehouse_id, date_of_arrival):
        self.consignment_id = consignment_id
        self.warehouse_id = warehouse_id
        self.date_of_arrival = date_of_arrival


class Manufacturer(Base):
    __tablename__ = "Manufacturer"
    __table_args__ = {'schema': 'cw'}

    id = Column(BigInteger, primary_key="True")
    adress = Column(String(100))
    internet_page = Column(Text)

    def __init__(self, adress, internet_page):
        self.adress = adress
        self.internet_page = internet_page


class Product(Base):
    __tablename__ = "Product"
    __table_args__ = {'schema': 'cw'}

    id = Column(BigInteger, primary_key="True")
    name = Column(Text)
    category_id = Column(BigInteger, ForeignKey("cw.ProductCategory.id"))
    expected_cost = Column(BigInteger)
    link = Column(Text)

    def __init__(self, name, category_id, expected_cost, link):
        self.name = name
        self.category_id = category_id
        self.expected_cost = expected_cost
        self.link = link


class ProductCategory(Base):
    __tablename__ = "ProductCategory"
    __table_args__ = {'schema': 'cw'}

    id = Column(BigInteger, primary_key="True")
    category = Column(Text)
    main_category_id = Column(BigInteger, ForeignKey("cw.MainCategory.id"))
    link = Column(Text)

    def __init__(self, category, main_category_id, link):
        self.category = category
        self.main_category_id = main_category_id
        self.link = link


class MainCategory(Base):
    __tablename__ = "MainCategory"
    __table_args__ = {'schema': 'cw'}

    id = Column(BigInteger, primary_key="True")
    category = Column(Text)
    link = Column(Text)

    def __init__(self, category, link):
        self.category = category
        self.link = link

class VolumeOfSales(Base):
    __tablename__ = "VolumeOfSales"
    __table_args__ = {'schema': 'cw'}

    id = Column(BigInteger, primary_key="True")
    warehouse_id = Column(BigInteger, ForeignKey("cw.Warehouse.id"))
    product_id = Column(BigInteger, ForeignKey("cw.Product.id"))
    date = Column(Date)
    volume = Column(BigInteger)

    def __init__(self, warehouse_id, product_id, date, volume):
        self.warehouse_id = warehouse_id
        self.product_id = product_id
        self.date = date
        self.volume = volume

class VolumeOfProduct(Base):
    __tablename__ = "Volume_of_product"
    __table_args__ = {'schema': 'cw'}

    id = Column(BigInteger, primary_key="True")
    product_id = Column(BigInteger, ForeignKey("cw.Product.id"))
    warehouse_id = Column(BigInteger, ForeignKey("cw.Product.id"))
    stored_volume = Column(BigInteger)

    def __init__(self, product_id, warehouse_id, stored_volume):
        self.product_id = product_id
        self.warehouse_id = warehouse_id
        self.stored_volume = stored_volume

class Warehouse(Base):
    __tablename__ = "Warehouse"
    __table_args__ = {'schema': 'cw'}

    id = Column(BigInteger, primary_key="True")
    adress = Column(String(100))
    max_stored_tonnage = Column(BigInteger)

    def __init__(self, adress, max_stored_tonnage):
        self.adress = adress
        self.max_stored_tonnage = max_stored_tonnage