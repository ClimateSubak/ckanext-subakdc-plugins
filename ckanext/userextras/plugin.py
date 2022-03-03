import logging

import ckan.plugins as p

log = logging.getLogger(__name__)

class UserExtrasPlugin(p.SingletonPlugin):

    def myfunc():
        return