class ActivityObject:
    def __init__(self, activity_id, object_type=None):
        self.context = "https://www.w3.org/ns/activitystreams"
        self.id = activity_id
        self.type = object_type

    def to_json(self):
        if self.type is None:
            return self.id
        else:
            return {
                "@context": self.context,
                'id': self.id,
                'type': self.type
            }