class BaseActivity:
    def __init__(self, activity_id, activity_type, actor, activity_object):
        self.context = "https://www.w3.org/ns/activitystreams"
        self.id = activity_id
        self.type = activity_type
        self.actor = actor
        self.object = activity_object
        self.to = "https://www.w3.org/ns/activitystreams#Public"

    def to_json(self):
        return {
            "@context": self.context,
            'id': self.id,
            'type': self.type,
            'actor': self.actor.to_json(),
            'object': self.object.to_json(),
            'to': self.to
        }