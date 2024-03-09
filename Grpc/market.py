import grpc
from concurrent import futures
import time
import market_pb2
import market_pb2_grpc
import seller_pb2
import seller_pb2_grpc
import buyer_pb2
import buyer_pb2_grpc 

class MarketServicer(market_pb2_grpc.MarketServicer):
    def __init__(self):
        self.sellers = {}  # Use a database to store seller information and items
        self.items = {}
        self.wishlists = {}
        self.buyers = {}

    def RegisterSeller(self, request, context):
        # print(self.sellers)
        seller_address = request.sellerAddress
        uuid = request.uuid
        print(f"Register Seller request from {uuid} at {seller_address}")
        if seller_address not in self.sellers.keys():
            self.sellers[seller_address] = uuid
            return market_pb2.Status(success=True, message="Seller registered successfully")
        else:
            
            return market_pb2.Status(success=False, message="Seller already registered")

    def check_reg(self,seller_address):
        if seller_address not in self.sellers.keys():
            return False
        else:
            return True
        
    def SellItem(self, request, context):
        seller_address = request.sellerAddress
        print(f"Sell Item request from {seller_address}")
        if self.check_reg(seller_address) == False:
            return market_pb2.Status(success=False, message="Seller not registered")
        item_id = len(self.items) + 1 # Placeholder logic for generating unique item IDs
        self.items[item_id] = {
            'id': str(item_id),
            'name': request.productName,
            'category': request.category,
            'quantity': request.quantity,
            'description': request.description,
            'seller_address': seller_address,
            'price_per_unit': request.pricePerUnit,
            'rating': 0.0,
        }
        
        
        return market_pb2.Status(success=True, message=f"Item {item_id} added successfully")

    def UpdateItem(self, request, context):
        seller_address = request.sellerAddress
        if self.check_reg(seller_address) == False:
            return market_pb2.Status(success=False, message="Seller not registered")
        
        item_id = request.itemId
        if item_id not in self.items.keys():
            return market_pb2.Status(success=False, message=f"Item {item_id} not found")
        
        if self.items[item_id]['seller_address'] != seller_address:
            return market_pb2.Status(success=False, message=f"Item {item_id} does not belong to seller {seller_address}")
        
        self.items[item_id]['price_per_unit'] = request.newPrice
        self.items[item_id]['quantity'] = request.newQuantity
        
        try:
            self.nofitify_buyers(item_id)
        except(Exception):
            print("Buyers Notification server unavailable")
            
        print(f"Update Item {item_id} request from {request.sellerAddress}")
        return market_pb2.Status(success=True, message=f"Item {item_id} updated successfully")

    def DeleteItem(self, request, context):
        seller_address = request.sellerAddress
        if self.check_reg(seller_address) == False:
            return market_pb2.Status(success=False, message="Seller not registered")
        
        item_id = request.itemId
        if item_id not in self.items.keys():
            return market_pb2.Status(success=False, message=f"Item {item_id} not found")
        
        if self.items[item_id]['seller_address'] != seller_address:
            return market_pb2.Status(success=False, message=f"Item {item_id} does not belong to seller {seller_address}")
        
        if item_id not in self.items:
            return market_pb2.Status(success=False, message=f"Item {item_id} not found")

        del self.items[item_id]

        print(f"Delete Item {item_id} request from {request.sellerAddress}")
        return market_pb2.Status(success=True, message=f"Item {item_id} deleted successfully")

    def DisplaySellerItems(self, request, context):
        # Placeholder implementation, replace with actual logic
        seller_address = request.sellerAddress
        seller_items = [item for item in self.items.values() if item['seller_address'] == seller_address]
        # print(seller_items)
        print(f"Display Items request from {seller_address}")
        return market_pb2.Items(items=[self._create_item_message(item) for item in seller_items])




    def SearchItem(self, request, context):
        # Placeholder implementation for searching items
        item_name = request.itemName
        item_category = request.category

        print(f"Search request for Item name: {item_name}, Category: {item_category}")

        filtered_items = [item for item in self.items.values() if
                          (item_name == "" or item['name'] == item_name) and (item['category'] == item_category)]

        return market_pb2.Items(items=[self._create_item_message(item) for item in filtered_items])

    def BuyItem(self, request, context):
        # Placeholder implementation for buying an item
        item_id = request.itemId
        quantity = request.quantityToBuy
        buyer_address = request.buyerAddress

        # print(self.items)
        if item_id not in self.items.keys():
            return market_pb2.Status(success=False, message=f"Item {item_id} not found")

        if self.items[item_id]['quantity'] < quantity:
            return market_pb2.Status(success=False, message=f"Not enough stock for Item {item_id}")

        # Placeholder logic for processing the purchase (deduct quantity, notify seller, etc.)
        self.items[item_id]['quantity'] -= quantity
        seller_address = self.items[item_id]['seller_address']

        print(f"Buy request {quantity} of item {item_id}, from {buyer_address}")

        # Placeholder logic for notifying the seller
        try:
            self._notify_seller(item_id, seller_address)
        except(Exception ):
            print("Seller Notification server unavailable")

        return market_pb2.Status(success=True, message=f"Purchase of {quantity} units of Item {item_id} successful")

    def AddToWishList(self, request, context):
        # Placeholder implementation for adding an item to the wishlist
        item_id = request.itemId
        buyer_address = request.buyerAddress

        if item_id not in self.items:
            return market_pb2.Status(success=False, message=f"Item {item_id} not found")

        if buyer_address not in self.wishlists:
            self.wishlists[buyer_address] = []

        if item_id not in self.wishlists[buyer_address]:
            self.wishlists[buyer_address].append(item_id)

        print(f"Wishlist request of item {item_id}, from {buyer_address}")

        return market_pb2.Status(success=True, message=f"Item {item_id} added to wishlist successfully")

    def RateItem(self, request, context):
        # Placeholder implementation for rating an item
        item_id = request.itemId
        buyer_address = request.buyerAddress
        rating = request.rating

        if item_id not in self.items:
            return market_pb2.Status(success=False, message=f"Item {item_id} not found")

        if not (1 <= rating <= 5):
            return market_pb2.Status(success=False, message="Invalid rating. Rating should be between 1 and 5")

        # Placeholder logic for updating the item rating
        self.items[item_id]['rating'] = (self.items[item_id]['rating'] + rating) / 2

        print(f"{buyer_address} rated item {item_id} with {rating} stars")

        return market_pb2.Status(success=True, message=f"Item {item_id} rated successfully")
    
    def _notify_seller(self, item_id, seller_address):
        # Placeholder implementation for notifying the seller
        seller_message = f"\n#######\nThe Following Item has been updated:\n\n" \
                         f"Item ID: {item_id}, Price: ${self.items[item_id]['price_per_unit']}, " \
                         f"Name: {self.items[item_id]['name']}, Category: {self.items[item_id]['category']}, " \
                         f"\nDescription: {self.items[item_id]['description']}, " \
                         f"Quantity Remaining: {self.items[item_id]['quantity']}, " \
                         f"\nRating: {self.items[item_id]['rating']} / 5  |  Seller: {self.items[item_id]['seller_address']}" \
                         f"\n#######"
        channel = grpc.insecure_channel(seller_address)
        stub = seller_pb2_grpc.SellerStub(channel)
        stub.Seller_Notification(seller_pb2.NotifyClientRequest(message=seller_message))

    def nofitify_buyers(self, item_id):
        for buyer_address, wishlist in self.wishlists.items():
            if item_id in wishlist:
                self._notify_buyer(item_id,buyer_address)
                
    def _notify_buyer(self, item_id, buyer_address):
        # Placeholder implementation for notifying the seller
        seller_message = f"\n#######\nThe Following Item has been updated:\n\n" \
                         f"Item ID: {item_id}, Price: ${self.items[item_id]['price_per_unit']}, " \
                         f"Name: {self.items[item_id]['name']}, Category: {self.items[item_id]['category']}, " \
                         f"\nDescription: {self.items[item_id]['description']}, " \
                         f"Quantity Remaining: {self.items[item_id]['quantity']}, " \
                         f"\nRating: {self.items[item_id]['rating']} / 5  |  Seller: {self.items[item_id]['seller_address']}" \
                         f"\n#######"
        channel = grpc.insecure_channel(buyer_address)
        stub = buyer_pb2_grpc.BuyerStub(channel)
        stub.Buyer_Notification(buyer_pb2.Notifybuyer(message=seller_message))
    
    def _create_item_message(self, item):
        # print(item)
        return market_pb2.Item(
            id=item['id'],
            name=item['name'],
            category=item['category'],
            quantityRemaining=item['quantity'],
            description=item['description'],
            sellerAddress=item['seller_address'],
            price=item['price_per_unit'],
            rating=item['rating'],
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_pb2_grpc.add_MarketServicer_to_server(MarketServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Market server started. Listening on port 50051.")
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
