from .base_activity import BaseActivity

class Accept(BaseActivity):
    def __init__(self, activity_id, actor, activity_object):
        super().__init__(activity_id, "Accept", actor, activity_object)
