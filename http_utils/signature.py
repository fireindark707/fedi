import base64
import datetime
import hashlib
import json

import requests
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

from .utils import get_host, get_path


def create_signature_digest(private_key, sender_url, recipient_url, current_date, message_json):
    sender_key = sender_url + '#main-key'
    recipient_host = get_host(recipient_url)
    recipient_path = get_path(recipient_url)
    digest = base64.b64encode(hashlib.sha256(json.dumps(message_json).__str__().encode('utf-8')).digest())
    signature_text = b'(request-target): post %s\ndigest: SHA-256=%s\nhost: %s\ndate: %s' % (
        recipient_path.encode('utf-8'),
        digest,
        recipient_host.encode('utf-8'),
        current_date.encode('utf-8')
    )
    raw_signature = private_key.sign(
        signature_text,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    signature_header = 'Signature keyId="%s",algorithm="%s",headers="(request-target) digest host date",signature="%s"' % (
        sender_key,
        'rsa-sha256',
        base64.b64encode(raw_signature).decode('utf-8')
    )
    return signature_header, digest.decode('utf-8')

# Split Signature: into its separate parameters.
def split_signature(signature):
    """
    Split signature into its separate parameters.
    """
    signature_params = signature.strip().split(",")
    signature_params = [param.split('=',1) for param in signature_params]
    signature_params = {param[0]: param[1].strip('"') for param in signature_params}
    return signature_params

# Construct the signature string from the value of headers.
def construct_signature_string(headers,signature_params,method,url):
    """
    Construct the signature string from the value of headers.
    """
    required_headers = signature_params['headers'].split(' ')
    signature_string = ""
    headers_lower = {header.lower(): value for header, value in headers.items()}
    for header in required_headers:
        try:
            signature_string += f"{header}: {headers_lower[header]}\n"
        except KeyError:
            if header == '(request-target)':
                signature_string += f"{header}: {method.lower()} {url}\n"
            else:
                raise KeyError(f"{header} not found in headers")
    # return in bytes
    return signature_string.strip().encode('utf-8')

# Fetch the keyId and resolve to an actor's publicKey.
def get_publickey(url):
    """
    Get public key from mastodon
    """
    r = requests.get(url, headers={'Accept': 'application/activity+json'})
    if r.status_code != 200:
        return None
    data = r.json()
    # return in bytes
    key = data['publicKey']['publicKeyPem']
    return key.encode('utf-8')

# Signature string and compare to the Base64-decoded signature as decrypted by publicKey[publicKeyPem].
def verify_signature(signature_string, signature, public_key):
    """
    Verify signature
    """
    # decode signature
    signature = base64.b64decode(signature)
    # decode public key
    public_key = load_pem_public_key(public_key, default_backend())
    # verify signature
    try:
        public_key.verify(signature, signature_string, padding.PKCS1v15(), hashes.SHA256())
        return True
    except InvalidSignature:
        return False

# Use the Date: header to check that the signed request was made within the past 12 hours.
def check_date(date):
    """
    Check date
    """
    # convert date to datetime
    date = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
    # check date
    if date > datetime.datetime.now() - datetime.timedelta(hours=12):
        return True
    else:
        return False