import urllib.request
import urllib.parse
import sys
import json

DEBUG = False

def print_debug(what, message):
    if DEBUG:
        print("<debug = {}> -> {}".format(what, message))

def send_message(slack_message):
    print_debug("slack_message", slack_message)

    slack_url = "https://slack.com/api/chat.postMessage"
    slack_data = {
        "token": slack_token,
        "channel": slack_channel,
        "text": slack_message,
        "username": "robbit",
        "icon_emoji": ":rabbit:",
    }

    response = urllib.request.urlopen(slack_url, data=urllib.parse.urlencode(slack_data).encode('utf-8'))
    print_debug("response_status", response.status)
    print_debug("response_body", response.read().decode('utf-8'))


def get_in_progress_retro_items():
    headers = {
        'authorization': postfacto_token,
        'content-type': 'application/json',
        'Accept': "*/*",
    }
    url = 'https://retros-iad-api.cfapps.io/retros/' + retro_id
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)


    retro = json.loads(response.read().decode('utf-8'))["retro"]
    in_progress_action_items = [item for item in retro["action_items"] if not item["done"]]
    sorted_in_progress_action_items = sorted(in_progress_action_items, key=lambda x: x["created_at"])

    descriptions = [item["description"] for item in sorted_in_progress_action_items]

    return descriptions

if __name__ == "__main__":
    print_debug("hello_message", "Hello There!")

    script_path, postfacto_token, retro_id, slack_token, slack_channel = sys.argv

    print_debug("postfacto_token", postfacto_token)
    print_debug("retro_id", retro_id)
    print_debug("slack_token", slack_token)
    print_debug("slack_channel", slack_channel)

    retro_items = get_in_progress_retro_items()

    #TODO: Maybe add personal @user to annoy everyone
    good_morning_message = ["*Good morning, fellow rabbits*:rabbit2:",]
    retro_items_message = ["(%s) Retro items:" % len(retro_items), "```"] + retro_items + ["```"]
    retro_items_message = good_morning_message + retro_items_message

    tracker_reminder_message=["*Also, don't forget to update <https://www.pivotaltracker.com/dashboard|Pivotal Tracker>*"]
    standup_vote_message=['</poll> <!here> "*Did you enjoy the standup this morning?*" "yay" "meh" "nay"']

    send_message("\n".join(retro_items_message))
    send_message("\n".join(tracker_reminder_message))
    # send_message("\n".join(standup_vote_message))
