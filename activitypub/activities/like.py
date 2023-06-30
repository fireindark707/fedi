from .base_activity import BaseActivity

class Like(BaseActivity):
    def __init__(self, activity_id, actor, activity_object):
        super().__init__(activity_id, "Like", actor, activity_object)
