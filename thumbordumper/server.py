import logging

import tornado.web

from tornado.httpserver import HTTPServer

from thumbor.console import get_server_parameters
from thumbor.config import Config
from thumbor.context import Context

from thumbordumper.importer import Importer
from thumbordumper.handlers import DumpHandler


def main():
    server_parameters = get_server_parameters()
    logging.basicConfig(level=getattr(logging, server_parameters.log_level.upper()))
    config = Config.load(server_parameters.config_path)

    importer = Importer(config)
    importer.import_modules()

    context = Context(server=server_parameters,
                      config=config,
                      importer=importer)

    handlers = [
            (r'/(?P<url>.+)', DumpHandler, { 'context': context })
    ]

    application = tornado.web.Application(handlers)

    server = HTTPServer(application)
    server.bind(context.server.port, context.server.ip)
    server.start(1)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
