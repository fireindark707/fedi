from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def load_private_key(file):
    with open(file, "rb") as key_file:
        private_key = key_file.read()
    return crypto_serialization.load_pem_private_key(private_key, password=None, backend=crypto_default_backend())

def load_public_key(file):
    with open(file, "rb") as key_file:
        public_key = key_file.read()
    return public_key.decode('utf-8')

class RSAKeyPairGenerator:
    def __init__(self, key_size=2048, private_key_file='keys/private.pem', public_key_file='keys/public.pem'):
        self.key_size = key_size
        self.private_key_file = private_key_file
        self.public_key_file = public_key_file

    def generate_keys(self):
        key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=self.key_size
        )

        private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            crypto_serialization.NoEncryption()
        )

        public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return private_key, public_key

    def save_keys(self, private_key, public_key):
        with open(self.private_key_file, 'wb') as f:
            f.write(private_key)
        with open(self.public_key_file, 'wb') as f:
            f.write(public_key)

    def print_keys(self, private_key, public_key):
        print("SECRET:",private_key.decode('utf-8'))
        print("PUBLIC:",public_key.decode('utf-8'))

    def run(self):
        private_key, public_key = self.generate_keys()
        self.save_keys(private_key, public_key)
        self.print_keys(private_key, public_key)
