from scripts.main import BaseHandler


class Admin_BaseHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(Admin_BaseHandler, self).__init__(*args, **kwargs)
        self.use_cache = False
