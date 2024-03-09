# Importing the required libraries
import pika
import sys
import json

youtube_server_address = input("Enter Youtube server IP: ")
# Defining the function to publish the video
def publishVideo(youtuber, videoName):
    try:
        # Connecting to RabbitMQ server and creating a channel
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(youtube_server_address))
        channel = connection.channel()

        # Publishing the video to the youtuber uploads queue
        message = json.dumps({'youtuber': youtuber, 'videoName': videoName})
        channel.basic_publish(
            exchange='', routing_key='youtuber_uploads', body=message)
        print('SUCCESS: Video published')

    except pika.exceptions.AMQPConnectionError:
        print("Error connecting to RabbitMQ, ensure it's running and accessible")
    except Exception as e:
        print(f"An unexpected error occurred while publishing video: {e}")

    # Closing the connection
    finally:
        connection.close()


if __name__ == '__main__':
    try:
        # Publishing the video if the required arguments are provided
        if len(sys.argv) < 3:
            print("Usage: Youtuber.py <YoutuberName> <VideoName>")
        else:
            youtuber = sys.argv[1]
            videoName = ' '.join(sys.argv[2:])
            publishVideo(youtuber, videoName)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
