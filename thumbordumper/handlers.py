import tornado.web

import thumbordumper.context
from thumbor.context import Context

import logging

logger = logging.getLogger(__name__)

class DumpHandler(tornado.web.RequestHandler):
    def initialize(self, context):
        self.context = Context(context.server, context.config, None)
        self.context.modules = thumbordumper.context.ContextImporter(self.context, context.modules.importer)

    def put(self, **kwargs):
        remote_storage = self.context.modules.remote_storage
        storage = self.context.modules.storage

        print storage
        print remote_storage

        url = kwargs['url']
        storage.put(url, self.request.body)
        storage.put_not_uploaded(url)

        lock = storage.upload_lock(url)

        if not lock.acquire(blocking=False):
            logger.warning('URL %s already had upload lock.... strange', url)
            return

        def callback(body, error):
            try:
                if error is not None:
                    logger.error('Upload Failed to %s. error: %s', url, error)
                    return

                storage.put_uploaded(url)
                logger.info('Storing %s successful', url)
            finally:
                lock.release()


        logger.info('Asynchronously uploading to %s', url)

        remote_storage.put(url, self.request.body, callback)

        







    

