from model import DataBaseHandler
import tables
import view
from datetime import date



class Controller:

    def __init__(self):
        self.db = DataBaseHandler("axel", "666524", "postgres")

    def insert_consignment(self):
        while True:
            tonnage = input("Enter tonnage ")
            if not tonnage.isnumeric() or int(tonnage) < 1:
                print("Incorrect tonnage value")
                continue
            prod_id = input("Enter product_id ")
            if not prod_id.isnumeric() or int(prod_id) < 1:
                print("Incorrect prod_id value")
                continue
            manufacturer_id = input("Enter manufacturer_id ")
            if not manufacturer_id.isnumeric() or int(manufacturer_id) < 1:
                print("Incorrect tonnage value")
                continue
            price_per_unit = input("Enter price_per_unit ")
            if not price_per_unit.isnumeric() or int(price_per_unit) < 1:
                print("Incorrect price_per_unit value")
                continue
            year = input("Enter year ")
            if not year.isnumeric() or int(year) < 1:
                print("Incorrect year value")
                continue
            month = input("Enter month ")
            if not month.isnumeric() or int(month) < 1 or int(month) > 12:
                print("Incorrect month value")
                continue
            day = input("Enter day ")
            if not day.isnumeric() or int(day) < 1 or int(day) > 31:
                print("Incorrect day value")
                continue
            cons = tables.Consignment(int(tonnage), date(int(year), int(month), int(day)), int(prod_id), int(manufacturer_id), int(price_per_unit))
            self.db.add_instanse(cons)
            self.db.commit_changes()
            break

    def delete_consignment(self, id):
        self.db.delete_instance(tables.Consignment, id)

    def insert_consignmnet_arrival(self):
        while True:
            year = input("Enter year ")
            if not year.isnumeric() or int(year) < 1:
                print("Incorrect year value")
                continue
            month = input("Enter month ")
            if not month.isnumeric() or int(month) < 1 or int(month) > 12:
                print("Incorrect month value")
                continue
            day = input("Enter day ")
            if not day.isnumeric() or int(day) < 1 or int(day) > 31:
                print("Incorrect day value")
                continue
            cons_id = input("Enter price_per_unit ")
            if not cons_id.isnumeric() or int(cons_id) < 1:
                print("Incorrect cons_id value")
                continue
            war_id = input("Enter price_per_unit ")
            if not war_id.isnumeric() or int(war_id) < 1:
                print("Incorrect war_id value")
                continue
            cons_arrival = tables.Consignment_arrival(int(cons_id), int(war_id), date(year, month, day))
            self.db.add_instanse(cons_arrival)
            self.db.commit_changes()
            break


    def insert_manufacturer(self):
        adress = input("Enter adress ")
        internet_page = input("Enter internet_page ")
        manufac = tables.Manufacturer(adress, internet_page)
        self.db.add_instanse(manufac)
        self.db.commit_changes()

    def insert_product(self):
        name = input("Enter name ")
        while True:
            category_id = input("Enter category_id ")
            if not category_id.isnumeric() or int(category_id) < 1:
                print("Incorrect category_id value")
                continue
            break
        prod = tables.Product(name, category_id)
        self.db.add_instanse(prod)
        self.db.commit_changes()


    def insert_product_category(self):
        category = input("Enter category ")
        additional_info = input("Enter additional_info ")
        prod_categ = tables.ProductCategory(category, additional_info)
        self.db.add_instanse(prod_categ)
        self.db.commit_changes()
        view.print_action("insert", "product_category ", prod_categ.id)

    def insert_volume_of_sales(self):
        while True:
            war_id = input("Enter price_per_unit ")
            if not war_id.isnumeric() or int(war_id) < 1:
                print("Incorrect war_id value")
                continue
            prod_id = input("Enter product_id ")
            if not prod_id.isnumeric() or int(prod_id) < 1:
                print("Incorrect prod_id value")
                continue
            volume = input("Enter volume ")
            if not volume.isnumeric() or int(volume) < 1:
                print("Incorrect volume value")
                continue
            year = input("Enter year ")
            if not year.isnumeric() or int(year) < 1:
                print("Incorrect year value")
                continue
            month = input("Enter month ")
            if not month.isnumeric() or int(month) < 1 or int(month) > 12:
                print("Incorrect month value")
                continue
            day = input("Enter day ")
            if not day.isnumeric() or int(day) < 1 or int(day) > 31:
                print("Incorrect day value")
                continue
            vol_sales = tables.VolumeOfSales(war_id, prod_id, date(year, month, day), volume)
            self.db.add_instanse(vol_sales)
            self.db.commit_changes()
            break

    def insert_warehouse(self):
        adress = input("Enter warehouse adress")
        while True:
            max_tonnage = input("Enter max_tonnage ")
            if not max_tonnage.isnumeric() or int(max_tonnage) < 1:
                print("Incorrect max_tonnage value")
                continue
            warehouse = tables.Warehouse(adress, max_tonnage)
            self.db.add_instanse(warehouse)
            self.db.commit_changes()
            break

    def get_price_dynamics(self):
        while True:
            print("Enter product id ")
            prod_id = input()
            if not prod_id.isnumeric() or int(prod_id) < 1:
                print("Incorrect max_tonnage value")
                continue
            res = self.db.get_date_price_product(prod_id)
            date_manufac = []
            cost = []
            for i in res:
                date_manufac.append(i[0])
                cost.append(i[1])
            view.print_dot_plot(date_manufac, cost)
            break

    def get_sold_volume_between_dates_warehouse(self):
        while True:
            print("Enter warehouse id ")
            war_id = input()
            if not war_id.isnumeric() or int(war_id) < 1:
                print("Incorrect war_id value")
                continue
            war_id = int(war_id)
            print("Enter first date")
            date1 = self.create_date()
            print("Enter second date")
            date2 = self.create_date()
            res = tuple(self.db.get_sold_volume_between_dates_warehouse(war_id, date1, date2))
            view.print_action("get", f"sold product volume from warhouse with id {war_id}", res[0][0])
            break

    def get_sold_volume_between_dates_product(self):
        while True:
            print("Enter product id ")
            prod_id = input()
            if not prod_id.isnumeric() or int(prod_id) < 1:
                print("Incorrect prod_id value")
                continue
            prod_id = int(prod_id)
            print("Enter first date")
            date1 = self.create_date()
            print("Enter second date")
            date2 = self.create_date()
            res = list(self.db.get_sold_volume_between_dates(prod_id, date1, date2))
            view.print_action("get", f"sold volume of product with id {prod_id} ", res[0][0])
            break

    def get_fulness_of_warehouse(self):
        while True:
            print("Enter warehouse id ")
            war_id = input()
            if not war_id.isnumeric() or int(war_id) < 1:
                print("Incorrect war_id value")
                continue
            war_id = int(war_id)
            res = list(self.db.get_fullness(war_id))
            if not res:
                print("No data for such input")
                break
            view.print_action("get fullness", "warehouse ", str(res[0][0] * 100) + '%')
            break

    def get_time_in_road(self):
        while True:
            print("Enter consignment id ")
            cons_id = input()
            if not cons_id.isnumeric() or int(cons_id) < 1:
                print("Incorrect cons_id value")
                continue
            cons_id = int(cons_id)
            res = list(self.db.get_time_in_road(cons_id))
            if not res:
                print("No data for such input")
                break
            view.print_action(f"get time in road", "consignment with id {cons_id} ", res[0][0])
            break

    def get_average_time_in_road_for_product(self):
        while True:
            print("Enter product id ")
            prod_id = input()
            if not prod_id.isnumeric() or int(prod_id) < 1:
                print("Incorrect prod_id value")
                continue
            prod_id = int(prod_id)
            res = list(self.db.get_avg_time_in_road_for_product(prod_id))
            if not res:
                print("No data for such input")
                break
            view.print_action("get average time in road for", f"product with id {prod_id}", res[0][0])
            break

    def get_price_dynamics_by_manufacturer(self):
        while True:
            print("Enter product id ")
            prod_id = input()
            if not prod_id.isnumeric() or int(prod_id) < 1:
                print("Incorrect prod_id value")
                continue
            prod_id = int(prod_id)

            manufacturer_id = input("Enter manufacturer_id ")
            if not manufacturer_id.isnumeric() or int(manufacturer_id) < 1:
                print("Incorrect tonnage value")
                continue
            manufacturer_id = int(manufacturer_id)
            res = self.db.get_all_product_consignments_from_manufacturer(manufacturer_id, prod_id)
            if not res:
                print("No data for such input")
                break
            date_manufac = []
            cost = []
            for i in res:
                date_manufac.append(i[0])
                cost.append(i[1])
            view.print_dot_plot(date_manufac, cost)
            break

    def get_expected_cost_by_categ(self):
        categ= input("Enter category name: ")
        self.db.get_pandas_product_analyze(categ)

    def get_product_name_by_id(self):
        while True:
            print("Enter product id ")
            prod_id = input()
            if not prod_id.isnumeric() or int(prod_id) < 1:
                print("Incorrect prod_id value")
                continue
            break
        res = self.db.get_product_name_by_id(prod_id)
        if not res:
            print("No data for such input")
        else:
            view.print_action("get name", "Product", str(tuple(res)))

    def create_date(self) -> date:
        while True:
            year = input("Enter year ")
            if not year.isnumeric() or int(year) < 1:
                print("Incorrect year value")
                continue
            month = input("Enter month ")
            if not month.isnumeric() or int(month) < 1 or int(month) > 12:
                print("Incorrect month value")
                continue
            day = input("Enter day ")
            return date(int(year), int(month),int(day))

    def get_products_below_cost(self):
        while True:
            print("Cost")
            cost = input()
            if not cost.isnumeric() or int(cost) < 1:
                print("Incorrect prod_id value")
                continue
            break
        res = self.db.get_products_below_cost(cost)
        if not res:
            print("No data for such input")
        else:
            view.print_action("get below cost","produc", tuple(res))


