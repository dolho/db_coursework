from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from sqlalchemy.sql import text
import tables
import json
import pandas
import matplotlib.pyplot as plt
import time


class DataBaseHandler:

    def __init__(self, user, password, database, port = 5432):
        self._engine = create_engine(f'postgresql://{user}:{password}@localhost:{port}/{database}')
        self._slave_engine = create_engine(f'postgresql://slave:666524@192.168.1.218:{port}/{database}')
        Session = sessionmaker(bind=self._engine)
        Slave_Session = sessionmaker(bind=self._slave_engine)
        self._session = Session()
        self._slave_session = Slave_Session()
        self.tables = {"consignment": tables.Consignment, "warehouse": tables.Warehouse,
                       "consignment_arrival": tables.Consignment_arrival, "manufacturer": tables.Manufacturer,
                       "product": tables.Product, "product_category": tables.ProductCategory,
                       "volume_of_sales": tables.VolumeOfSales, "volume_of_product": tables.VolumeOfProduct}

    # def close_db_connection(self):
    #     """closing database connection."""
    #     # if self._connection:
    #     #     self._cursor.close()
    #     #     self._connection.close()
    #     #     print("PostgreSQL connection is closed")

    def add_random_manufacturers(self, quantity:int = 1):
        """
        Add given number of random manufacturer
        :return:
        """

        with self._engine.connect() as con:
            con.execute(f'insert into cw."Manufacturer" (adress, internet_page)'
                        f'select rnd.adress, rnd.page '
                        f'from(select substr(md5(random()::text), 0, 15) as adress,'
                        f'substr(md5(random()::text), 0, 10) as page '
                        f'from generate_series(1, {quantity})) as rnd;')


    def add_random_product(self, quantity: int = 1) -> None:
        """
        Add given number of random products
        :param quantity:
        :return:
        """
        try:
            with self._engine.connect() as con:
                con.execute(f'insert into cw."Product" (name, category_id)'
                                     f'select rnd.name, rnd.ca_id from(select substr(md5(random()::text), 0, 15) '
                                     f'as name,random()*(select max(id) from cw."ProductCategory") - '
                                     f'(select min(id) from cw."ProductCategory") ')
        except exc.SQLAlchemyError as e:
            print(e)
            self.rollback()


    def add_random_consignment(self, quantity: int = 1) -> None:
        """
        Add given number of random consigments
        :param quantity:
        :return:
        """
        with self._engine.connect() as con:
            try:
                con.execute(f'select cw.add_random_consignments({quantity})')
            except exc.SQLAlchemyError as e:
                print(e)
                self.rollback()

    def add_random_warehouse(self, quantity: int = 1) -> None:
        """
        Add given number of random warehouses
        :param quantity:
        :return:
        """
        try:
            with self._engine.connect() as con:
                con.execute(f'insert into cw."Warehouse" (adress, max_stored_tonnage) '
                                     f'select rnd.adress, rnd.tonnage '
                                     f'from (select substr(md5(random()::text), 0, 15) as adress,'
                                     f'trunc(random()*9000)::int + 1000 as tonnage '
                                     f'from generate_series(1, {quantity})) as rnd;')
        except exc.SQLAlchemyError as e:
            print(e)
            self.rollback()

    def add_random_consignment_arrival(self, max_arrival_time = 60) -> None:
        try:
            with self._engine.connect() as con:
                result = con.execute(f'select id from cw."Consignment" where id not in '
                            f'(select consignment_id from cw."Consignment_arrival")')
                max_war_id = con.execute('select max(id) from cw."Warehouse"').fetchone()[0]
                min_war_id = con.execute('select min(id) from cw."Warehouse"').fetchone()[0]
                for row in result:
                    con.execute(f'insert into cw."Consignment_arrival" (consignment_id, warehouse_id, date_of_arrival) '
                                f'values ({row[0]}, trunc(random()*({max_war_id} - {min_war_id})) + {min_war_id}, '
                                f'(select date from date((select date_of_manufacturing from cw."Consignment" where id={row[0]}) + '
                                f'trunc(random() * {max_arrival_time}) * \'1 day\'::interval)))')
        except exc.SQLAlchemyError as e:
            print(e)
            self.rollback()

    def add_random_volume_of_sales(self, quantity = 1) -> None:
        try:
            with self._engine.connect() as con:
                self._engine.execute(text(f'select cw.add_random_volume_of_sales({quantity});').execution_options(autocommit=True))
                self.commit_changes()
                # to see text of the function, look at the doc folder
        except exc.SQLAlchemyError as e:
            print(e)
            self.rollback()

    def add_instanse(self, instanse: tables) -> int:
        try:
            self._session.add(instanse)
        except exc.SQLAlchemyError as e:
            print(e)
            self.rollback()


    def delete_instance(self, instanse, id: int) -> bool:
        res = self._session.query(instanse).filter(instanse.id == id).all()
        if res:
            self._session.query(instanse).filter(instanse.id == id).delete()
            return True
        else:
            return False

    def update_instance(self, instance: tables, id: int, new_values: dict) -> bool:
        res = self._session.query(instance).filter(instance.id == id).all()
        if res:
            self._session.query(instance).filter(instance.id == id).update(new_values)
            return True
        else:
            return False

    def get_instanse(self, instance: tables, id: int):
        return self._session.query(instance).filter_by(id=id).all()

    def get_date_price_product(self, id: int):
        try:
            with self._engine.connect() as con:
                result = con.execute(f'select date_of_manufacturing, trunc(avg(price_per_unit)) '
                                     f'from cw."Consignment" where product_id={id} '
                                     f'group by date_of_manufacturing '
                                     f'order by date_of_manufacturing ')

            return result
        except exc.OperationalError:
            print("Main server is not operational. Getting info from slave server")
            with self._slave_engine.connect() as con:
                result = con.execute(f'select date_of_manufacturing, trunc(avg(price_per_unit)) '
                                     f'from cw."Consignment" where product_id={id} '
                                     f'group by date_of_manufacturing '
                                     f'order by date_of_manufacturing ')
                return result
        except exc.SQLAlchemyError as e:
            print(e)

    def get_sold_volume_between_dates_warehouse(self,  warehouse_id: int, date1: date, date2: date):
        if date1 > date2:
            raise ValueError("Date1 can't be later, than Date2")
        try:
            with self._engine.connect() as con:
                result = con.execute(f'select sum(volume) from cw."VolumeOfSales" where '
                                     f'warehouse_id = {warehouse_id} and '
                                     f'date between \'{date1}\' and \'{date2}\' group by warehouse_id ')

            return result
        except exc.OperationalError:
            print("Main server is not operational. Getting info from slave server")
            with self._slave_engine.connect() as con:
                result = con.execute(f'select sum(volume) from cw."VolumeOfSales" where '
                                     f'warehouse_id = {warehouse_id} and '
                                     f'date between \'{date1}\' and \'{date2}\' group by warehouse_id ')
                return result
        except exc.SQLAlchemyError as e:
            print(e)

    def get_sold_volume_between_dates(self, product_id: int, date1, date2):
        if date1 > date2:
            raise ValueError("Date1 can't be later, than Date2")
        try:
            with self._engine.connect() as con:
                result = con.execute(f'select sum(volume) from cw."VolumeOfSales" '
                                     f'where product_id = {product_id} and '
                                     f'date between \'{date1}\' and \'{date2}\' group by product_id  ')

            return result
        except exc.OperationalError:
            print("Main server is not operational. Getting info from slave server")
            with self._slave_engine.connect() as con:
                result = con.execute(f'select sum(volume) from cw."VolumeOfSales" '
                                     f'where product_id = {product_id} and '
                                     f'date between \'{date1}\' and \'{date2}\' group by product_id  ')
                return result
        except exc.SQLAlchemyError as e:
            print(e)

    def get_fullness(self, war_id):
        try:
            with self._engine.connect() as con:
                result = con.execute(f'select (select sum(stored_volume) from cw."Volume_of_product" where warehouse_id = {war_id})'
                                     f'/ '
                                     f'(select max_stored_tonnage from cw."Warehouse" where id = {war_id});')
            return result
        except exc.OperationalError:
            print("Main server is not operational. Getting info from slave server")
            with self._slave_engine.connect() as con:
                result = con.execute(f'select (select sum(stored_volume) from cw."Volume_of_product" where warehouse_id = {war_id})'
                                     f'/ '
                                     f'(select max_stored_tonnage from cw."Warehouse" where id = {war_id});')
                return result
        except exc.SQLAlchemyError as e:
            print(e)

    def get_time_in_road(self, consignment_id):
        try:
            with self._engine.connect() as con:
                result = con.execute(f'select (select date_of_arrival from cw."Consignment_arrival" where consignment_id = {consignment_id}) '
                                     f'- '
                                     f'(select date_of_manufacturing from cw."Consignment"where id = {consignment_id})')
            return result
        except exc.OperationalError:
            print("Main server is not operational. Getting info from slave server")
            with self._slave_engine.connect() as con:
                result = con.execute(f'select (select date_of_arrival from cw."Consignment_arrival" where consignment_id = {consignment_id}) '
                                     f'- '
                                     f'(select date_of_manufacturing from cw."Consignment"where id = {consignment_id})')
                return result
        except exc.SQLAlchemyError as e:
            print(e)

    def get_avg_time_in_road_for_product(self, prod_id):
        try:
            with self._engine.connect() as con:
                result = con.execute(f'select trunc(avg(q.betwe)) from '
                                     f'(select date_of_arrival - date_of_manufacturing as betwe '
                                     f'from cw."Consignment_arrival" as ca inner join cw."Consignment" as co on ca.consignment_id = co.id '
                                     f'where product_id = {prod_id}) as q')
            return result
        except exc.OperationalError:
            print("Main server is not operational. Getting info from slave server")
            with self._slave_engine.connect() as con:
                result = con.execute(f'select trunc(avg(q.betwe)) from '
                                     f'(select date_of_arrival - date_of_manufacturing as betwe '
                                     f'from cw."Consignment_arrival" as ca inner join cw."Consignment" as co on ca.consignment_id = co.id '
                                     f'where product_id = {prod_id}) as q')
                return result
        except exc.SQLAlchemyError as e:
            print(e)

    def get_all_product_consignments_from_manufacturer(self, manufact_id, produc_id):
        try:
            with self._engine.connect() as con:
                result = con.execute(f'select date_of_manufacturing, trunc(avg(price_per_unit)) '
                                     f'from cw."Consignment" where manufacturer_id = {manufact_id} '
                                     f'and product_id = {produc_id} '
                                     f'group by date_of_manufacturing')
            return result
        except exc.OperationalError:
            print("Main server is not operational. Getting info from slave server")
            with self._slave_engine.connect() as con:
                result = con.execute(f'select date_of_manufacturing, trunc(avg(price_per_unit)) '
                                     f'from cw."Consignment" where manufacturer_id = {manufact_id} '
                                     f'and product_id = {produc_id} '
                                     f'group by date_of_manufacturing')
                return result
        except exc.SQLAlchemyError as e:
            print(e)

    def add_main_categories_json(self):
        categories = []
        with open('./scraped_data/products.json', 'r') as f:
            categories = json.loads(f.read())
        for i in categories:
            mcat = tables.MainCategory(i["category"], i["link"])
            self.add_instanse(mcat)

    def add_sub_categories_json(self):
        categories = []
        with open('./scraped_data/sub-products.json', 'r') as f:
            categories = json.loads(f.read())
        for i in categories:
            main_categ_id = self._session.query(tables.MainCategory.id).filter(tables.MainCategory.category == i['category']).scalar()
            self.add_instanse(tables.ProductCategory(i['sub_category_name'], main_categ_id, i['link']))

    def add_products_json(self):
        products = []
        with open('./scraped_data/concrete_products.json', 'r') as f:
            products = json.loads(f.read())
        for i in products:
            sub_categ_id = self._session.query(tables.ProductCategory.id).filter(
                tables.ProductCategory.category == i['sub_category']).scalar()
            self.add_instanse(tables.Product(i['name'], sub_categ_id, i['cost'], i['link']))

    def get_pandas_product_analyze(self, category):
        try:
            df1 = pandas.read_sql_table('Product', self._engine, 'cw')
            df2 = pandas.read_sql_table('ProductCategory', self._engine, 'cw')
        except exc.OperationalError:
            print("Main server is not operational. Getting info from slave server")
            df1 = pandas.read_sql_table(tables.Product, self._slave_engine)
            df2 = pandas.read_sql_table(tables.ProductCategory, self._slave_engine)
        except exc.SQLAlchemyError as e:
            print(e)
        df2 = df2.rename(columns={'id': 'category_id'})
        df = pandas.merge(df1, df2, how='inner', on='category_id')
        df = df[df.category==category]
        cost = df['expected_cost'].to_list()
        plt.ylabel(category)
        plt.xlabel("Expected cost")
        plt.hist(cost, bins=20)
        plt.show()

    def get_product_name_by_id(self, id):
        try:
            res = self._session.query(tables.Product.name).filter(tables.Product.id == id)
            return res
        except exc.OperationalError:
            print("Main server is not operational. Getting info from slave server")
            res = self._slave_session.query(tables.Product.name).filter(tables.Product.id == id)
            return res
        except exc.SQLAlchemyError as e:
            print(e)

    def get_products_below_cost(self, cost):
        try:
            with self._engine.connect() as con:
                result = con.execute(f'select * from cw."Product" where expected_cost < {cost}')
            return result
        except exc.OperationalError:
            print("Main server is not operational. Getting info from slave server")
            with self._slave_engine.connect() as con:
                result = con.execute(f'select * from cw."Product" where expected_cost < {cost}')
                return result
        except exc.SQLAlchemyError as e:
            print(e)


    def commit_changes(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()


# db = DataBaseHandler('axel', 666524, 'postgres')










