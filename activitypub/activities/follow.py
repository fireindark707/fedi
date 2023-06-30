from .base_activity import BaseActivity

class Follow(BaseActivity):
    def __init__(self, activity_id, actor, follow_target):
        super().__init__(activity_id, 'Follow', actor, follow_target)
        