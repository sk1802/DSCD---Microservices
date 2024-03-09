# Importing the required libraries
import pika
import sys
import json


Youtube_server_address = input("Enter Youtube server IP: ")
# Defining the function to receive notifications
def receiveNotifications(user):
    try:
        # Connecting to RabbitMQ server and creating a channel
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(Youtube_server_address))
        channel = connection.channel()

        # Declaring the queue for the user's notifications
        queue_name = f'{user}_notifications'
        channel.queue_declare(queue=queue_name)

        # Callback function to print the notifications
        def callback(ch, method, properties, body):
            print(f"New Notification: {body.decode()}")

        # Getting the notifications from the user's queue
        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)
        print(f"[*] Waiting for notifications. To exit press CTRL+C")
        channel.start_consuming()

    except pika.exceptions.AMQPConnectionError:
        print("Error connecting to RabbitMQ, ensure it's running and accessible")
    except KeyboardInterrupt:
        print("\nUser has exited the notification service.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Defining the function to update the subscription
def updateSubscription(user, youtuber, action):
    try:
        # Connecting to RabbitMQ server and creating a channel
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(Youtube_server_address))
        channel = connection.channel()

        # Publishing the subscription update to the user requests queue
        message = json.dumps({
            'user': user,
            'youtuber': youtuber,
            'subscribe': action == 's'
        })
        channel.basic_publish(
            exchange='', routing_key='user_requests', body=message)
        print('Subscription update SUCCESS')

    except pika.exceptions.AMQPConnectionError:
        print("Error connecting to RabbitMQ, ensure it's running and accessible")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Closing the connection
    finally:
        connection.close()


# Main
def main():
    try:
        # Getting the user and the action to perform
        user = sys.argv[1]
        if len(sys.argv) == 4:
            action = sys.argv[2]  # 's' for subscribe, 'u' for unsubscribe
            youtuber = sys.argv[3]

            # Updating the subscription
            updateSubscription(user, youtuber, action)

        # Receiving the notifications
        receiveNotifications(user)

    except IndexError:
        print(
            "Incorrect number of arguments provided. Please check the usage and try again.")


if __name__ == '__main__':
    main()
