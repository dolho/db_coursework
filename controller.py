from model import DataBaseHandler
import tables
import view
from datetime import date



class Controller:

    def __init__(self):
        self.db = DataBaseHandler("axel", "666524", "127.0.0.1", "postgres")

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
            cons = tables.Consignment(int(tonnage), date(year,month,day), int(prod_id), int(manufacturer_id), int(price_per_unit))
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
        view.insert_action("product_category ", prod_categ.id)

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

