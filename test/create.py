import datetime
import requests

from activitypub.activities import Create
from http_utils import load_private_key, create_signature_digest, get_host
from activitypub.objects import Note
from activitypub.actors import BaseActor

from config import settings
domain = settings["domain"]
user_name = settings["user_name"]
target_inboxs = [
    "https://example.org/inbox",
    "https://example2.com/inbox",
]

timestamp = int(datetime.datetime.utcnow().timestamp())
post_id = f"https://{domain}/users/{user_name}/post/" + str(timestamp)
activity_id = f"https://{domain}/create/" + str(timestamp)
user_id = f"https://{domain}/users/{user_name}"

post = Note(post_id, "你好，联邦宇宙", BaseActor(user_id))
create_post = Create(activity_id, BaseActor(user_id), post).to_json()

print(create_post.__str__())

current_date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

for target in target_inboxs:
    signature, digest = create_signature_digest(
        load_private_key("config/keys/private.pem"),
        user_id,
        target,
        current_date,
        create_post
    )

    headers = {
        "Date": current_date,
        "Content-Type": "application/activity+json",
        "Host": get_host(target),
        "Signature": signature,
        "Digest": "SHA-256=%s" % digest,
    }

    r = requests.post(target, headers=headers, json=create_post)
    print(target, r.text, r.status_code)