import urllib.request
import urllib.parse
import sys
import json

DEBUG = True

def print_debug(what, message):
    if DEBUG:
        print("<debug = {}> -> {}".format(what, message))

def set_channel_topic(channel_topic):
    print_debug("channel_topic", channel_topic)

    slack_url = "https://slack.com/api/channels.setTopic"
    slack_data = {
        "token": slack_token,
        "channel": slack_channel,
        "topic": channel_topic,
        "username": "robbit",
        "icon_emoji": ":rabbit:",
    }

    print_debug("slack_data", slack_data)

    response = urllib.request.urlopen(slack_url, data=urllib.parse.urlencode(slack_data).encode('utf-8'))
    print_debug("response_status", response.status)
    print_debug("response_body", response.read().decode('utf-8'))


if __name__ == "__main__":
    print_debug("hello_message", "Hello There!")

    script_path, slack_token, slack_channel = sys.argv

    print_debug("slack_token", slack_token)
    print_debug("slack_channel", slack_channel)

    channel_topic = [
        "interrupts: the team is now offline | Times: 9am - 6pm UK/Ireland time"]

    set_channel_topic("".join(channel_topic))

