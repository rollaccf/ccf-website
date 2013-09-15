from scripts.main import BaseHandler


class Tasks_BaseHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(Tasks_BaseHandler, self).__init__(*args, **kwargs)
        self.use_cache = False
