import psycopg2
from datetime import date
import time
from hashlib import md5
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from sqlalchemy.sql import text

class DataBaseHandler:

    # def __init__(self, user, password, host, database):
    #     try:
    #         self._connection = psycopg2.connect(user=user,
    #                                             password=password,
    #                                             host=host,
    #                                             database=database)
    #
    #         self._cursor = self._connection.cursor()
    #     except (Exception, psycopg2.Error) as error:
    #         print("Error while connecting to PostgreSQL", error)
    #         self.close_db_connection()
    #     except exc.SQLAlchemyError as e:
    #         print(e)

    def __init__(self, user, password, database, port = 5432):
        self._engine = create_engine(f'postgresql://{user}:{password}@localhost:{port}/{database}')
        Session = sessionmaker(bind=self._engine)
        self._session = Session()


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


    def add_random_product(self, quantity: int = 1):
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


    def add_random_consignment(self, quantity: int = 1):
        """
        Add given number of random consigments
        :param quantity:
        :return:
        """
        with self._engine.connect() as con:
            try:
                con.execute(f'insert into cw."Consignment"'
                                     f'(tonnage, date_of_manufacturing, product_id, manufacturer_id, price_per_unit)'
                                     f'select rnd.tonnage, rnd.date_of_manufacturing, '
                                     f'rnd.product_id, rnd.manufacturer_id, rnd.price_per_unit from '
                                     f'(select trunc(random()*100)::int as tonnage,trunc(random()*100)::int as price_per_unit,'
                                     f'(select timestamp \'2018-01-10\' + '
                                     f'random() * (timestamp \'2020-06-20\' -timestamp \'2018-01-10\')) as date_of_manufacturing,'
                                     f'trunc(random()*(select max(id) from cw."Manufacturer"))::int + 2 -(select min(id) from cw."Manufacturer") as manufacturer_id,'
                                     f'trunc(random()*(select max(id) from cw."Product"))::int + 2 -(select min(id) from cw."Product") as product_id '
                                     f'from generate_series(1, {quantity})) as rnd;')
            except exc.SQLAlchemyError as e:
                print(e)

    def add_random_warehouse(self, quantity: int = 1):
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
                                     f'trunc(random()*9000)::int + 1000 as tonnage'
                                     f'from generate_series(1, {quantity})) as rnd;')
        except exc.SQLAlchemyError as e:
            print(e)

    def add_random_consigment_arrival(self, max_arrival_time = 60):
        try:
            with self._engine.connect() as con:
                result = con.execute(f'select id from cw."Consignment" where id not in '
                            f'(select consignment_id from cw."Consignment_arrival")')
                max_war_id = con.execute('select max(id) from cw."Warehouse"').fetchone()[0]
                min_war_id = con.execute('select min(id) from cw."Warehouse"').fetchone()[0]
                for row in result:
                    con.execute(f'insert into cw."Consignment_arrival" (consignment_id, warehouse_id, date_of_arrival) '
                                f'values ({row[0]}, trunc(random()*({max_war_id} - {min_war_id})) + {min_war_id}, '
                                f'(select date from date((select date_of_manufacturing from cw."Consignment" where id=100) + '
                                f'trunc(random() * {max_arrival_time}) * \'1 day\'::interval)))')
        except exc.SQLAlchemyError as e:
            print(e)

    def add_random_volume_of_sales(self, quantity = 1):
        try:
            with self._engine.connect() as con:
                con.execute(f'select cw.add_random_volume_of_sales({quantity});')
                # to see text of the function, look at the doc folder
        except exc.SQLAlchemyError as e:
            print(e)

    #TODO Промапить таблицы в объекты, сделать view и controller, добавить консольный интерфейс,
    #TODO Реализовать запросы из ТЗ и добавить их в интерфейс, добавить индексы, и скрины, что они помогают
    #TODO Прикрепить к запросам графики из pyplot
    #TODO


db = DataBaseHandler("axel", "666524", "postgres" )

db.add_random_consigment_arrival()

