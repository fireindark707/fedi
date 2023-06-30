from .base_activity import BaseActivity

class Create(BaseActivity):
    def __init__(self, activity_id, actor, activity_object):
        super().__init__(activity_id, "Create", actor, activity_object)

class Reply(Create):
    def __init__(self, activity_id, actor, activity_object, reply_to_actor):
        super().__init__(activity_id, actor, activity_object)
        self.object["inReplyTo"] = reply_to_actor.to_json()