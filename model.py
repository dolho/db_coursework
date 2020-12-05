from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from sqlalchemy.sql import text
import tables


class DataBaseHandler:

    def __init__(self, user, password, database, port = 5432):
        self._engine = create_engine(f'postgresql://{user}:{password}@localhost:{port}/{database}')
        Session = sessionmaker(bind=self._engine)
        self._session = Session()
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
                con.execute(f'insert into cw."Consignment"'
                                     f'(tonnage, date_of_manufacturing, product_id, manufacturer_id, price_per_unit)'
                                     f'select rnd.tonnage, rnd.date_of_manufacturing, '
                                     f'rnd.product_id, rnd.manufacturer_id, rnd.price_per_unit from '
                                     f'(select trunc(random()*100 + 2)::int as tonnage,trunc(random()*100 + 2)::int as price_per_unit,'
                                     f'(select timestamp \'2018-01-10\' + '
                                     f'random() * (timestamp \'2020-06-20\' -timestamp \'2018-01-10\')) as date_of_manufacturing,'
                                     f'trunc(random()*(select max(id) from cw."Manufacturer"))::int + 2 -(select min(id) from cw."Manufacturer") as manufacturer_id,'
                                     f'trunc(random()*(select max(id) from cw."Product"))::int + 2 -(select min(id) from cw."Product") as product_id '
                                     f'from generate_series(1, {quantity})) as rnd;')
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
        except exc.SQLAlchemyError as e:
            print(e)

    def get_fullness(self, war_id):
        try:
            with self._engine.connect() as con:
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
        except exc.SQLAlchemyError as e:
            print(e)
    def commit_changes(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()




db = DataBaseHandler("axel", "666524", "postgres" )

# TODO Резрвирование данных, репликация данных, статистический анализ







