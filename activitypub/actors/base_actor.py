class BaseActor:
    def __init__(self, activity_id, actor_type=None):
        self.context = "https://www.w3.org/ns/activitystreams"
        self.id = activity_id
        self.inbox = activity_id + "/inbox"
        self.outbox = activity_id + "/outbox"
        self.type = actor_type

    def to_json(self):
        if self.type is None:
            return self.id
        else:
            return {
                "@context": self.context,
                'id': self.id,
                'type': self.type,
                'inbox': self.inbox,
                'outbox': self.outbox
            }