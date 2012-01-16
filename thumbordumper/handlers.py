import tornado.web

import thumbordumper.context
from thumbor.context import Context

class DumpHandler(tornado.web.RequestHandler):
    def initialize(self, context):
        self.context = Context(context.server, context.config, None)
        self.context.modules = thumbordumper.context.ContextImporter(self.context, context.modules.importer)

    def put(self, **kwargs):
        remote_storage = self.context.modules.remote_storage
        storage = self.context.modules.storage

        storage.put(kwargs['url'], self.request.body)
    

