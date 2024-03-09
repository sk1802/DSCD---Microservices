import grpc
import market_pb2
import market_pb2_grpc
from concurrent import futures
import uuid
import seller_pb2
import seller_pb2_grpc

class NotificationServicer(seller_pb2_grpc.SellerServicer):
    def Seller_Notification(self, request, context):
        print(f"Notification received: {request.message}")
        return seller_pb2.Void()


class SellerClient:
    def __init__(self, server_address, notification_server_address):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = market_pb2_grpc.MarketStub(self.channel)

        # Notification server setup
        self.notification_channel = grpc.insecure_channel(notification_server_address)
        self.notification_server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        self.notification_servicer = NotificationServicer()
        seller_pb2_grpc.add_SellerServicer_to_server(self.notification_servicer, self.notification_server)
        self.notification_server.add_insecure_port(f'[::]:{notification_server_address.split(":")[-1]}')
        self.notification_server.start()
        self.notification_address = f"{notification_server_address.split(':')[0]}:{notification_server_address.split(':')[-1]}"
        print(f"Notification server started on {self.notification_address}")

        

    def register_seller(self, seller_address, uuid):
        request = market_pb2.RegisterSellerRequest(sellerAddress=seller_address, uuid=uuid)
        response = self.stub.RegisterSeller(request)
        print(f"Server response: {response.success}, Message: {response.message}")

    def sell_item(self,item_name, category, quantity, description, price_per_unit, seller_address, seller_uuid):
        # category_enum = market_pb2.Item.Category.Value(name = 'FASHION')
        # print(f"Category: {category_enum}")
        try:
            # Convert the provided category to enum value
            category_enum = market_pb2.Item.Category.Value(category)
        except ValueError:
            # Handle the case where the provided category is not in the enum
            print(f"Error: Category '{category}' is not available. Please choose a valid category.")
            return
        request = market_pb2.SellItemRequest(
            productName=item_name,
            category=category_enum,
            quantity=quantity,
            description=description,
            sellerAddress=seller_address,
            pricePerUnit=price_per_unit,
            sellerUuid=seller_uuid
        )
        response = self.stub.SellItem(request)
        print(f"Server response: {response.success}, Message: {response.message}")
        
    def test_sell_item(self,seller_address,seller_uuid):
        # print(market_pb2.Item.Category.Value('fghj'))
        request = market_pb2.SellItemRequest(
            productName='item_name',
            category=market_pb2.Item.Category.Value('FASHION'),
            quantity=1,
            description='jhgf',
            sellerAddress=seller_address,
            pricePerUnit=10,
            sellerUuid=seller_uuid
        )
        response = self.stub.SellItem(request)
        print(f"Server response: {response.success}, Message: {response.message}")

    def test_sell_item1(self,seller_address,seller_uuid):
        request = market_pb2.SellItemRequest(
            productName='item_name1',
            category=market_pb2.Item.Category.Value('ELECTRONICS'),
            quantity=1,
            description='jhgf',
            sellerAddress=seller_address,
            pricePerUnit=20,
            sellerUuid=seller_uuid
        )
        response = self.stub.SellItem(request)
        print(f"Server response: {response.success}, Message: {response.message}")

    def update_item(self, item_id, new_price, new_quantity, seller_address, seller_uuid):
        request = market_pb2.UpdateItemRequest(
            itemId=item_id,
            newPrice=new_price,
            newQuantity=new_quantity,
            sellerAddress=seller_address,
            sellerUuid=seller_uuid
        )
        response = self.stub.UpdateItem(request)
        print(f"Server response: {response.success}, Message: {response.message}")

    def delete_item(self, item_id, seller_address, seller_uuid):
        request = market_pb2.DeleteItemRequest(itemId=item_id, sellerAddress=seller_address, sellerUuid=seller_uuid)
        response = self.stub.DeleteItem(request)
        print(f"Server response: {response.success}, Message: {response.message}")

    def display_seller_items(self, seller_address, seller_uuid):
        # items_list = ['ELECTRONICS', 'FASHION', 'OTHERS']
        request = market_pb2.DisplaySellerItemsRequest(sellerAddress=seller_address, sellerUuid=seller_uuid)
        response = self.stub.DisplaySellerItems(request)
        
        for item in response.items:
            category_name = market_pb2.Item.Category.Name(item.category)
            print(f"\nItem ID: {item.id},\n Price: RS {item.price},\n "
                f"Name: {item.name},\n Category: {category_name},\n "
                f"Description: {item.description},\n "
                f"Quantity Remaining: {item.quantityRemaining},\n "
                f"Rating: {item.rating} / 5  \n Seller: {item.sellerAddress}\n\n")



if __name__ == "__main__":
    notif_addr = input("Enter the port for the notification server: [Ip:port]")
    compute_addr = input('Enter External IP address of the GCP instance: ')
    server_address = compute_addr+":50051"  # Update with the actual server address and port

    # Placeholder values, replace with actual values
    seller_address = notif_addr
    seller_uuid = str(uuid.uuid1())

    seller_client = SellerClient(server_address, seller_address)
    
    while True:
        print("\nSeller Menu:")
        print("1. Register Seller")
        print("2. Sell Item")
        print("3. Update Item")
        print("4. Delete Item")
        print("5. Display Seller Items")
        print("6. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            seller_client.register_seller(seller_address, seller_uuid)
        elif choice == "2":
            # seller_client.test_sell_item(seller_address, seller_uuid)
            # seller_client.test_sell_item1(seller_address, seller_uuid)
            item_name = input("Enter item name: ")
            category = input("Enter category: ").upper()
            quantity = int(input("Enter quantity: "))
            description = input("Enter description: ")
            price_per_unit = float(input("Enter price per unit: "))
            seller_client.sell_item(item_name, category, quantity, description, price_per_unit, seller_address, seller_uuid)
            
        elif choice == "3":
            item_id = int(input("Enter item ID to update: "))
            new_price = float(input("Enter new price: "))
            new_quantity = int(input("Enter new quantity: "))
            seller_client.update_item(item_id, new_price, new_quantity, seller_address, seller_uuid)
        elif choice == "4":
            item_id = int(input("Enter item ID to delete: "))
            seller_client.delete_item(item_id, seller_address, seller_uuid)
        elif choice == "5":
            seller_client.display_seller_items(seller_address, seller_uuid)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")
