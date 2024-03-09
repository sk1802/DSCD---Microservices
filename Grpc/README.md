# gRPC Market System

This project implements a gRPC-based market system with buyer, seller, and market services. The communication between these services is handled using gRPC, a high-performance RPC (Remote Procedure Call) framework.

## Project Structure

- **market.proto:** Protocol Buffer (.proto) file defining the gRPC service interfaces and message types for the market.

- **market_pb2.py** and **market_pb2_grpc.py:** Generated Python files from the market.proto definition using the `protoc` compiler. These files contain the message classes and gRPC service classes.

- **buyer.proto, buyer_pb2.py, buyer_pb2_grpc.py:** Protobuf and generated Python files for the buyer service.

- **seller.proto, seller_pb2.py, seller_pb2_grpc.py:** Protobuf and generated Python files for the seller service.

- **market.py:** Implementation of the market service, which manages sellers, items, wishlists, and facilitates buying and selling transactions.

- **seller.py:** Implementation of the seller service, which allows sellers to register, sell items, update items, delete items, and display their listed items.

- **buyer.py:** Implementation of the buyer service, enabling buyers to buy items, add items to their wishlist, and rate items they have purchased.

## How to Run

1. **Run Market Service:**
   - Execute `market.py` to start the market service. This will listen on port 50051 by default.

2. **Run Seller Service:**
   - Execute `seller.py` to start the seller service. You'll be prompted to enter the port for the notification server and the external IP address of the GCP instance.

3. **Run Buyer Service:**
   - Execute `buyer.py` to start the buyer service.

## Functionalities

### Market Service

- **RegisterSeller:** Allows sellers to register with the market service.

- **SellItem:** Enables sellers to list items for sale.

- **UpdateItem:** Allows sellers to update the price and quantity of their listed items.

- **DeleteItem:** Allows sellers to remove items from the market.

- **DisplaySellerItems:** Displays the items listed by a specific seller.

- **SearchItem:** Allows buyers to search for items by name and category.

- **BuyItem:** Facilitates the purchase of items by buyers, deducting the quantity from available stock.

- **AddToWishList:** Allows buyers to add items to their wishlist.

- **RateItem:** Enables buyers to rate items they have purchased.

### Seller Service

- **RegisterSeller:** Registers the seller with the market service.

- **SellItem:** Lists items for sale with details such as name, category, quantity, description, price per unit, and seller UUID.

- **UpdateItem:** Updates the price and quantity of a listed item.

- **DeleteItem:** Removes a listed item.

- **DisplaySellerItems:** Displays the items listed by the seller.

### Buyer Service

- **BuyItem:** Allows buyers to purchase items by specifying the item ID and quantity.

- **AddToWishList:** Adds items to the buyer's wishlist.

- **RateItem:** Rates items the buyer has purchased.

## Important Notes

- The gRPC services use the protocol buffer files (`proto`) to define the service interfaces and message types. The Python files (`_pb2.py` and `_pb2_grpc.py`) are generated using the `protoc` compiler.

- Ensure that the necessary gRPC Python libraries are installed:

   ```bash
   pip install grpcio grpcio-tools

- the following command is used to generate the Python files from the `.proto` definition:

   ```bash
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. market.proto
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. buyer.proto
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. seller.proto
   ```
