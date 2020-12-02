from controller import Controller
from router import Router

cont = Controller()
rout = Router(cont)

rout.register_command("post/consignment/", cont.insert_consignment)
rout.register_command("post/consignment_arrival/", cont.insert_consignmnet_arrival())
rout.register_command("post/manufacturer/", cont.insert_manufacturer())
rout.register_command("post/product/", cont.insert_product())
rout.register_command("post/product_category/", cont.insert_product_category())
rout.register_command("post/volume_of_sales/", cont.insert_volume_of_sales())
rout.register_command("post/warehouse/", cont.insert_warehouse())




# print("Type get/help/ to see list of all commands")
while True:
    command = input("Enter command: ")
    print(command)
    if command == 'exit':
        print("Finish the program")
        break
    rout.handle_command(command)