# Importing the required libraries
import pika
import json
import sys

rabbit_server = input("Enter RabbitMQ server IP: ")
# Main
def main():
    try:
        # Connecting to RabbitMQ server and creating a channel.
        connection = pika.BlockingConnection(
            pika.ConnectionParameters("0.0.0.0"))
        channel = connection.channel()

        # Declaring queues for user requests and youtuber uploads
        channel.queue_declare(queue='user_requests')
        channel.queue_declare(queue='youtuber_uploads')

        # Defining the data structures to store user and youtuber data
        users = {}  # {username: {subscriptions: set(youtuber_names)}}
        youtubers = {}  # {youtuber_name: [videos]}

        # Function to notify users about new videos
        def notify_users(youtuber, videoName):
            # Iterating through the users and their subscriptions
            for user, data in users.items():
                try:
                    # If the youtuber is in the user's subscriptions
                    if youtuber in data['subscriptions']:
                        # Creating the notification message, queue name and declaring the queue
                        notification = f"{youtuber} uploaded {videoName}"
                        user_queue = f"{user}_notifications"
                        channel.queue_declare(queue=user_queue)

                        # Publishing the notification to the user's queue
                        channel.basic_publish(
                            exchange='', routing_key=user_queue, body=notification)
                        print(f"Notified {user} about {youtuber}'s new video: {videoName}")
                    else:
                        print(f"{user} is not subscribed to {youtuber}")

                except Exception as e:
                    print(f"Error notifying {user}: {e}")
                    
        # Defining the callback functions for consuming user requests
        def consume_user_requests(ch, method, properties, body):
            try:
                # Decoding the JSON request
                request = json.loads(body)
                username = request['user']

                # If the user is new, add them to the users dictionary
                users.setdefault(username, {'subscriptions': set()})
                if 'youtuber' in request:
                    youtuber = request['youtuber']
                    if request.get('subscribe'):
                        users[username]['subscriptions'].add(youtuber)
                        action = 'subscribed'
                    else:
                        users[username]['subscriptions'].discard(youtuber)
                        action = 'unsubscribed'
                    print(f'{username} {action} to {youtuber}')

                else:
                    print(f'{username} logged in')

            except json.JSONDecodeError:
                print("Error decoding JSON from user request")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        # Defining the callback function for consuming youtuber uploads
        def consume_youtuber_requests(ch, method, properties, body):
            try:
                # Decoding the JSON request
                request = json.loads(body)
                youtuber, videoName = request['youtuber'], request['videoName']

                # Adding the video to the youtuber's videos
                youtubers.setdefault(youtuber, []).append(videoName)
                print(f'{youtuber} uploaded {videoName}')

                # Notifying the users about the new video
                notify_users(youtuber, videoName)

            except json.JSONDecodeError:
                print("Error decoding JSON from user request")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        # Consuming the requests
        channel.basic_consume(
            queue='user_requests', on_message_callback=consume_user_requests, auto_ack=True)
        channel.basic_consume(
            queue='youtuber_uploads', on_message_callback=consume_youtuber_requests, auto_ack=True)

        # Starting the server and waiting for messages
        print('Starting YouTube server. Waiting for messages.')
        channel.start_consuming()

    except pika.exceptions.AMQPConnectionError:
        print("Error connecting to RabbitMQ, ensure it's running and accessible")
    except KeyboardInterrupt:
        print("\nServer shutdown requested. Exiting...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Closing the connection
    finally:
        try:
            connection.close()
            print("RabbitMQ connection closed.")

        except Exception:
            pass


if __name__ == '__main__':
    main()
