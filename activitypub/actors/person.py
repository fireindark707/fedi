from .base_actor import BaseActor

class Person(BaseActor):
    def __init__(self, actor_id, name, public_key, summary=None, avatar_img=None):
        super().__init__(actor_id, 'Person')
        self.name = name
        self.publicKey = public_key
        self.summary = summary
        self.avatar = avatar_img

    def to_json(self):
        json_object = super().to_json()
        json_object['name'] = self.name
        json_object['publicKey'] = {
            "id": self.id + "/public-key",
            "owner": self.id,
            "publicKeyPem": self.publicKey.decode('utf-8')
        },
        json_object['summary'] = self.summary
        json_object['icon'] = {
            "type": "Image",
            "mediaType": "image/png",
            "url": self.avatar
        },
        json_object['image'] = {
            "type": "Image",
            "mediaType": "image/png",
            "url": self.avatar
        },
        return json_object
