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

def get_slack_username_for_pair(name):
    pair_board_to_slack_user = {
        "dave":"dhiston",
        "scott":"smuc",
        "zhou":"zyu",
        "gareth": "gds",
        "diego":"dlresende",
        "steve":"sfreeman",
        "alberto":"aleal",
        "abhishek":"achander",
        "hannes":"hhorl",
        "andrew":"andrew.thorburn",
    }
    username = pair_board_to_slack_user.get(name, name)

    return "@" + username

def get_ci_pair_and_pms():
    url = 'https://pcf-rmq.pezapp.io/state.json'
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)


    pair_board = json.loads(response.read().decode('utf-8'))
    ci_pair_number = 0

    print_debug("pair_board", pair_board)
    print_debug("pair_board['badges']", pair_board["badges"])
    print_debug("pair_board['assignments']", pair_board["assignments"])

    for k,v in pair_board["badges"].items():
        if "CI" in v:
            ci_pair_number = k

    ci_pair = pair_board["assignments"][ci_pair_number]
    print_debug("ci_pair_number", ci_pair_number)
    print_debug("ci_pair", ci_pair)

    pms = pair_board["assignments"]["pm"]
    print_debug("pms", pms)

    return ci_pair, pms

def format_usernames(list_of_users):
    if len(list_of_users) == 1:
        return get_slack_username_for_pair(list_of_users[0])
    elif len(list_of_users) == 2:
        return "{} and {}".format(
            get_slack_username_for_pair(list_of_users[0]),
            get_slack_username_for_pair(list_of_users[1])
        )
    raise "Weird list_of_users: {}".format(list_of_users)

if __name__ == "__main__":
    print_debug("hello_message", "Hello There!")

    script_path, slack_token, slack_channel = sys.argv

    print_debug("slack_token", slack_token)
    print_debug("slack_channel", slack_channel)

    ci_pair, pms = get_ci_pair_and_pms()

    channel_topic = [
        "interrupts: ",
        format_usernames(pms),
        " for product, ",
        format_usernames(ci_pair),
        " for engineering | Times: 9am - 6pm UK/Ireland time"]

    set_channel_topic("".join(channel_topic))

