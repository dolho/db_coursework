from controller import Controller
from router import Router

cont = Controller()
rout = Router(cont)

rout.register_command("post/consignment/", cont.insert_consignment)
rout.register_command("post/consignment_arrival/", cont.insert_consignmnet_arrival)
rout.register_command("post/manufacturer/", cont.insert_manufacturer)
rout.register_command("post/product/", cont.insert_product)
rout.register_command("post/product_category/", cont.insert_product_category)
rout.register_command("post/volume_of_sales/", cont.insert_volume_of_sales)
rout.register_command("post/warehouse/", cont.insert_warehouse)

rout.register_command("get/price_dynamics/", cont.get_price_dynamics)
rout.register_command("get/sold_volume_from_war/", cont.get_sold_volume_between_dates_warehouse)
rout.register_command("get/sold_volume_of_product/", cont.get_sold_volume_between_dates_product)
rout.register_command("get/fullness_of_warehouse/", cont.get_fulness_of_warehouse)
rout.register_command("get/time_in_road_consignment/", cont.get_time_in_road)
rout.register_command("get/average_time_in_road_product/", cont.get_average_time_in_road_for_product)
rout.register_command("get/price_dynamics_manufacturer/", cont.get_price_dynamics_by_manufacturer)
rout.register_command("get/expected_cost_by_category/", cont.get_expected_cost_by_categ)
rout.register_command("get/product_name/", cont.get_product_name_by_id)
rout.register_command("get/products_below_cost/", cont.get_products_below_cost)

print("Type get/help/ to see list of all commands")
while True:
    command = input("Enter command: ")
    print(command)
    if command == 'exit':
        print("Finish the program")
        break
    rout.handle_command(command)