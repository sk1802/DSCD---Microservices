import grpc
import market_pb2
import market_pb2_grpc
import buyer_pb2
import buyer_pb2_grpc
from concurrent import futures

class NotificationServicer(buyer_pb2_grpc.BuyerServicer):
    def Buyer_Notification(self, request, context):
        print(f"Notification received: {request.message}")
        return buyer_pb2.Void1()

class BuyerClient:
    def __init__(self, server_address,notification_server_address):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = market_pb2_grpc.MarketStub(self.channel)
        
        self.notification_channel = grpc.insecure_channel(notification_server_address)
        self.notification_server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        self.notification_servicer = NotificationServicer()
        buyer_pb2_grpc.add_BuyerServicer_to_server(self.notification_servicer, self.notification_server)
        self.notification_server.add_insecure_port(f'[::]:{notification_server_address.split(":")[-1]}')
        self.notification_server.start()
        self.notification_address = f"{notification_server_address.split(':')[0]}:{notification_server_address.split(':')[-1]}"
        print(f"Notification server started on {self.notification_address}")

    def search_item(self, item_name="", category="ANY"):
        if category.upper() == "ANY":
                # Search for items in all categories
            for category_enum in market_pb2.Item.Category.keys():
                request = market_pb2.SearchItemRequest(itemName=item_name, category=category_enum)
                response = self.stub.SearchItem(request)
                self.display_search_results(response)
        else:
            # Handle the case when a specific category is specified
            try:
                category_enum = market_pb2.Item.Category.Value(category)
                request = market_pb2.SearchItemRequest(itemName=item_name, category=category_enum)
                response = self.stub.SearchItem(request)
                self.display_search_results(response)
            except ValueError:
                print(f"Invalid category: {category}")
                
    def display_search_results(self, response):
        items_list = ['ELECTRONICS', 'FASHION', 'OTHERS']
        for item in response.items:
            print(f"\nItem ID: {item.id},\n Price: RS {item.price},\n "
                  f"Name: {item.name},\n Category: {items_list[item.category]},\n "
                  f"Description: {item.description},\n "
                  f"Quantity Remaining: {item.quantityRemaining},\n "
                  f"Rating: {item.rating} / 5  \n Seller: {item.sellerAddress}\n\n")
            
    def buy_item(self, item_id, quantity, buyer_address):
        request = market_pb2.BuyItemRequest(itemId=item_id, quantityToBuy=quantity, buyerAddress=buyer_address)
        response = self.stub.BuyItem(request)
        print(f"Server response: {response.success}, Message: {response.message}")

    def add_to_wishlist(self, item_id, buyer_address):
        request = market_pb2.AddToWishListRequest(itemId=item_id, buyerAddress=buyer_address)
        response = self.stub.AddToWishList(request)
        print(f"Server response: {response.success}, Message: {response.message}")

    def rate_item(self, item_id, rating, buyer_address):
        request = market_pb2.RateItemRequest(itemId=item_id, rating=rating, buyerAddress=buyer_address)
        response = self.stub.RateItem(request)
        print(f"Server response: {response.success}, Message: {response.message}")

if __name__ == "__main__":
    compute_addr = input('Enter External IP address of the GCP instance: ')
    server_address = compute_addr+":50051"  # Update with the actual server address and port

    # Generate a unique UUID for the buyer
    buyer_notif_address = input("Enter the port for the notification server: [Ip:port]")
    # buyer_notif_address = f"34.42.81.176:{buyer_notif_port}"

    buyer_client = BuyerClient(server_address,buyer_notif_address)

    while True:
        print("\nBuyer Menu:")
        print("1. Search Item")
        print("2. Buy Item")
        print("3. Add to Wishlist")
        print("4. Rate Item")
        print("5. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            item_name = input("Enter item name (leave blank to display all items): ")
            category = input("Enter category (ELECTRONICS, FASHION, OTHERS, ANY): ")
            buyer_client.search_item(item_name=item_name, category=category)
        elif choice == "2":
            item_id = int(input("Enter item ID to buy: "))
            quantity = int(input("Enter quantity to purchase: "))
            buyer_client.buy_item(item_id, quantity, buyer_address=buyer_notif_address)
        elif choice == "3":
            item_id = int(input("Enter item ID to add to wishlist: "))
            buyer_client.add_to_wishlist(item_id, buyer_address=buyer_notif_address)
        elif choice == "4":
            item_id = int(input("Enter item ID to rate: "))
            rating = int(input("Enter rating (1 to 5): "))
            buyer_client.rate_item(item_id, rating, buyer_address=buyer_notif_address)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")
