from flask import Flask, make_response, request, Response, abort
from http_utils import split_signature, construct_signature_string, get_publickey, verify_signature, get_host
import json
from config import settings

app = Flask(__name__)

# load public key
with open('config/keys/public.pem', 'rb') as f:
    public_key = f.read()

def log_save(body_data, file_name):
    actorlink = body_data["actor"]
    author = f"{actorlink.split('/')[-1]}@{get_host(actorlink)}"
    if body_data["type"] == "Create":
        with open(file_name, "a") as f:
            f.write(f"{author} say: {body_data['object']['content']}\n")
    elif body_data["type"] == "Announce":
        with open(file_name, "a") as f:
            f.write(f"{author} share: {body_data['object']}\n")
    elif body_data["type"] == "Follow":
        with open(file_name, "a") as f:
            f.write(f"{author} want follow: {body_data['object']}\n")
    elif body_data["type"] == "Like":
        with open(file_name, "a") as f:
            f.write(f"{author} like: {body_data['object']}\n")

@app.route('/users/<username>')
def user(username):
    if username != f"{settings['user_name']}":
        abort(404)

    response = make_response({
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": f"https://{settings['domain']}/users/{settings['user_name']}",
        "inbox": f"https://{settings['domain']}/users/{settings['user_name']}/inbox",
        "outbox": f"https://{settings['domain']}/users/{settings['user_name']}/outbox",
        "type": "Person",
        "name": settings['user_display_name'],
        "preferredUsername": settings['user_name'],
        "summary": settings['user_summary'],
        # avatar
        "icon": {
            "type": "Image",
            "mediaType": "image/png",
            "url": settings['user_avatar_url']
        },
        "image": {
            "type": "Image",
            "mediaType": "image/png",
            "url": settings['user_avatar_url']
        },
        "publicKey": {
            "id": f"https://{settings['domain']}/users/{settings['user_name']}/public-key",
            "owner": f"https://{settings['domain']}/users/{settings['user_name']}",
            "publicKeyPem": public_key.decode('utf-8')
        },
    })

    response.headers['Content-Type'] = 'application/activity+json'

    return response

@app.route('/.well-known/webfinger')
def webfinger():
    resource = request.args.get('resource')

    if resource != f"acct:{settings['user_name']}@{settings['domain']}":
        abort(404)

    response = make_response({
        "subject": f"acct:{settings['user_name']}@{settings['domain']}",
        "links": [
            {
                "rel": "self",
                "type": "application/activity+json",
                "href": f"https://{settings['domain']}/users/{settings['user_name']}"
            }
        ]
    })

    response.headers['Content-Type'] = 'application/jrd+json'

    return response

@app.route('/users/<username>/inbox', methods=['POST'])
def user_inbox(username):
    if username != settings['user_name']:
        abort(404)

    app.logger.info(request.headers)
    app.logger.info(request.data)

    header = dict(request.headers)
    # get dict format of data
    body = json.loads(request.data)

    if body["type"] == "Delete": # delete activity dont have public key, we omit it now
        return Response(status=204)

    # verify signature
    signature = request.headers.get('Signature')
    signature_params = split_signature(signature)
    signature_string = construct_signature_string(header,signature_params,request.method,request.path)
    public_key = get_publickey(signature_params['keyId'])
    if public_key is None:
        print("public key not found")
        abort(400)
    if not verify_signature(signature_string, signature_params['signature'], public_key):
        print("signature not verified")
        abort(400)

    # save inbox log, only save body
    log = body
    with open(settings["inbox_log_pth"], 'a') as f:
        f.write(json.dumps(log, ensure_ascii=False, indent=4) + '\n')
    log_save(body, settings["timeline_log_pth"])

    return Response("", status=202)