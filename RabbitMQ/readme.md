Certainly! Here's the revised README text without code snippets:

---

# Project README

## Setup

Ensure RabbitMQ is installed and running on your system.

The project is primarily written in Python. Make sure you have Python installed.

To install the required `pika` library, execute the following command:

```bash
pip install pika
```

## Running the Code

Open multiple terminals, one for each file.

### Step 1: Start the Server

To initiate the server, execute the following command:

```bash
python YoutubeServer.py
```

### Additional Steps (Can be Done in Any Order)

You can perform the following steps in any order.

- **Publish a Video:** To publish a video, execute `python Youtuber.py <YoutuberName> <VideoName>`. `<YoutuberName>` should not contain any white-space characters, while `<VideoName>` can contain white-space characters.

- **Login to a User's Account:** To login to a user's account and receive notifications from subscribed YouTubers, run `python User.py <UserName>`.

- **Subscribe to a YouTuber:** To subscribe to a YouTuber and start receiving notifications, use the command `python User.py <UserName> s <YoutuberName>`. This command will also log in to the user's account after subscribing to the YouTuber.

- **Unsubscribe from a YouTuber:** To unsubscribe from a YouTuber and stop receiving notifications, run `python User.py <UserName> u <YoutuberName>`. This command will also log in to the user's account after unsubscribing from the YouTuber.

### Note

Multiple YouTubers can publish their videos simultaneously, and multiple users can also log in simultaneously.

---