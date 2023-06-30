import datetime
import requests

from activitypub.activities import Follow
from http_utils import load_private_key, create_signature_digest, get_host
from activitypub.actors import BaseActor

from config import settings
domain = settings["domain"]
user_name = settings["user_name"]
target_inbox = "https://example.org/inbox"
target_user_id = "https://example.org/users/example_user"

timestamp = int(datetime.datetime.utcnow().timestamp())
activity_id = f"https://{domain}/follow/" + str(timestamp)
user_id = f"https://{domain}/users/{user_name}"

follow = Follow(activity_id, BaseActor(user_id), BaseActor(target_user_id)).to_json()

print(follow.__str__())

current_date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

signature, digest = create_signature_digest(
    load_private_key("config/keys/private.pem"),
    user_id,
    target_inbox,
    current_date,
    follow
)

headers = {
    "Date": current_date,
    "Content-Type": "application/activity+json",
    "Host": get_host(target_inbox),
    "Signature": signature,
    "Digest": "SHA-256=%s" % digest,
}

r = requests.post(target_inbox, headers=headers, json=follow)
print(r.text, r.status_code)