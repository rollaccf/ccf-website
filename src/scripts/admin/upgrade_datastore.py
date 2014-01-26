from google.appengine.ext import webapp, ndb
from scripts.admin import Admin_BaseHandler


class Admin_Upgrade_Handler(Admin_BaseHandler):
    def __init__(self, *args, **kwargs):
        super(Admin_Upgrade_Handler, self).__init__(*args, **kwargs)

        def remove_attr(model_instance, simulate, attr_name):
            if hasattr(model_instance, attr_name):
                if not simulate:
                    delattr(model_instance, attr_name)
                return "[{}] Removing {}".format(model_instance.__class__.__name__, attr_name)

        def rename_attr(model_instance, simulate, attr_name, new_attr_name):
            if hasattr(model_instance, attr_name):
                if not simulate:
                    attr_value = getattr(model_instance, attr_name)
                    setattr(model_instance, new_attr_name, attr_value)
                    delattr(model_instance, attr_name)
                return "[{}] Renaming {} to {}".format(model_instance.__class__.__name__, attr_name, new_attr_name)

        self.change_instructions = [
            # Model, function, [args]
            ('HousingApplication', remove_attr, ['SemesterToBegin', ]),
            ('HousingApplication', remove_attr, ['PrintFormatedDateTime', ]),
            ('HousingApplicationNote', remove_attr, ['PrintFormatedDateTime', ]),
        ]

    def get(self):
        changes = self.upgrade_datastore(self.change_instructions, simulate=True)
        self.template_vars['changes'] = changes
        self.render_template("admin/upgrade_datastore.html")

    def post(self):
        self.upgrade_datastore(self.change_instructions, simulate=False)
        self.redirect(self.request.path)

    def upgrade_datastore(self, change_instructions, simulate):
        changes = []
        for model_name, func, args in change_instructions:
            model = type(model_name, (ndb.Expando, ), {})
            all_instances = model.query()
            for model_instance in all_instances:
                change = func(model_instance, simulate, *args)
                if change:
                    changes.append(change)
                    model_instance.put()
        # if left as is, this code will produce the following error
        # UndefinedError: 'scripts.admin.upgrade_datastore.HousingApplication object' has no attribute 'TimeSubmitted_cdt'
        # clearing memcache and restarting the instance(s) so it reloads the correct types fixes it
        # "del model" might work but is untested
        return changes


application = webapp.WSGIApplication([
    ('/admin/upgrade.*', Admin_Upgrade_Handler),
    ], debug=Admin_BaseHandler.debug)
