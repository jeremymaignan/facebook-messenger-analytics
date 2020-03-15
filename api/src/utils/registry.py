import pkgutil
from utils.logger import log


class Registry(object):

    def __init__(self):
        self.registrations = []
        self.app = None

    def discover(self, apis):
        # Auto discover APIs
        for importer, modname, ispkg in pkgutil.walk_packages(path=apis.__path__, prefix=apis.__name__ + '.'):
            log.info('Discovered %s API', modname)
            __import__(modname)

    def register(self, registration):
        log.info('Registering %s as handler for %s (%s) with method %s', *registration)
        self.registrations.append(registration)
        if self.app:
            self._add_url_rules(registration)

    def init(self, app):
        if self.app:
            raise Exception("Registry already initialized!")
        self.app = app
        for registration in self.registrations:
            self._add_url_rules(registration)

    def _add_url_rules(self, registration):
        cls, endpoint, url, method = registration
        log.info("Creating endpoint at %s with method %s", url, method)
        self.app.add_url_rule(url, view_func=cls.as_view(endpoint), methods=[method])


registry = Registry()
