import urllib.request
import urllib.parse
import sys
import json

print("Hello There!")

script_path, retro_id, postfacto_token, slack_token, slack_channel = sys.argv

print("<debug>")
print(slack_token)
print(postfacto_token)
print(retro_id)
print("</debug>")

headers = {
    'authorization': postfacto_token,
    'content-type': 'application/json',
    'Accept': "*/*",
}
url = 'https://retro-api.cfapps.io/retros/' + retro_id
request = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(request)

retro = json.loads(response.read().decode('utf-8'))["retro"]
action_items = retro["action_items"]
sorted_action_items = sorted([item for item in action_items if not item["done"]], key=lambda x: x["created_at"])

good_morning_message = ["*Good morning, fellow rabbits*:rabbit2:",]

retro_items = [item["description"] for item in sorted_action_items]
retro_items_count = len(retro_items)
retro_items_message = ["(%s) Retro items:" % retro_items_count, "```"] + retro_items + ["```"]

full_message = good_morning_message + retro_items_message

message = "\n".join(full_message)
print(message)


#TODO: Maybe add personal @user to annoy everyone
slack_url = "https://slack.com/api/chat.postMessage"

slack_data = {
    "token": slack_token,
    "channel": slack_channel,
    "text": message,
    "username": "robbit",
    "icon_emoji": ":rabbit:",
}

urllib.request.urlopen(slack_url, data=urllib.parse.urlencode(slack_data).encode('utf-8'))

