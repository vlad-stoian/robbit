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

retro = json.loads(response.read().decode('utf-8'))
action_items = retro["retro"]["action_items"]
sorted_action_items = sorted([item for item in action_items if not item["done"]], key=lambda x: x["created_at"])

good_morning = ["*Good morning, fellow rabbits*:rabbit2:",]
retro_items = ["Retro items:", "```"] + [item["description"] for item in sorted_action_items] + ["```"]

message = "\n".join(good_morning + retro_items)
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

