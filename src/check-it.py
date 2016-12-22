import urllib.request
import sys
import json

print("Hello There!")

script_path, slack_token, postfacto_token, retro_id = sys.argv


print("Debug!")
print(slack_token)
print(postfacto_token)
print(retro_id)

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

message = "\n".join([item["description"] for item in sorted_action_items])

print(message)
