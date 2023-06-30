from .base_object import ActivityObject
import datetime

class Note(ActivityObject):
    def __init__(self, object_id, content, author):
        super().__init__(object_id, 'Note')
        self.published = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        self.content = content
        self.attributedTo = author
        self.to = "https://www.w3.org/ns/activitystreams#Public"

    def to_json(self):
        json_object = super().to_json()
        json_object['content'] = self.content
        json_object['published'] = self.published
        json_object['attributedTo'] = self.attributedTo.to_json()
        json_object['to'] = self.to
        return json_object