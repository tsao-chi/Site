# coding=utf-8
import os
import inspect
import importlib
import logging

import falcon

from mako.template import Template
from mako.lookup import TemplateLookup

from mimetypes import guess_type

from ultros_site.base_route import BaseRoute
from ultros_site.base_sink import BaseSink

__author__ = "Gareth Coles"
CURRENT_DIR = os.path.dirname(__file__)
log = logging.getLogger("Routes")

if CURRENT_DIR[-1] == "/":
    ROUTES_DIR = CURRENT_DIR + "routes/"
else:
    ROUTES_DIR = CURRENT_DIR + "/routes/"


class RouteManager:
    def __init__(self):
        self.app = None
        self.template_lookup = TemplateLookup(["./templates/"])

    def set_app(self, app: falcon.API):
        self.app = app

    def get_template(self, uri) -> Template:
        return self.template_lookup.get_template(uri)

    def render_template(self, uri, *args, **kwargs):
        template = self.get_template(uri)

        kwargs["bots"] = "N/A"

        return (
            guess_type(uri)[0],
            template.render(*args, **kwargs)
        )

    def load_routes(self):
        log.info("Loading routes...")
        log.info("")

        for filename in os.listdir(ROUTES_DIR):
            path = ROUTES_DIR + filename

            if not os.path.isfile(path):
                continue

            if not path.endswith(".py"):
                continue

            module_name = "ultros_site.routes.{}".format(
                os.path.basename(path).split(".py", 1)[0]
            )

            if module_name.endswith("__init__"):
                continue

            log.info("Loading module: {}".format(module_name))

            try:
                module_obj = importlib.import_module(module_name)

                for name, clazz in inspect.getmembers(module_obj):
                    try:
                        if inspect.isclass(clazz):
                            if clazz == BaseRoute or clazz == BaseSink:
                                continue

                            if name.startswith("__") and name.endswith("__"):
                                continue

                            if BaseRoute in clazz.__mro__:
                                log.info("-> Loading route class: {}".format(name))

                                route = clazz(self)
                                args = route.get_args()

                                self.app.add_route(*args)
                            elif BaseSink in clazz.__mro__:
                                log.info("-> Loading sink class:  {}".format(name))

                                route = clazz(self)
                                args = route.get_args()

                                self.app.add_sink(*args)
                    except Exception as e:
                        log.info("   -> Failed to load: {}".format(e))
            except Exception as e:
                log.info("Failed to load routes: {}".format(e))
            log.info("")
