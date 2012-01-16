import thumbor.context
class ContextImporter(thumbor.context.ContextImporter):
    def __init__(self, context, importer):
        thumbor.context.ContextImporter.__init__(self, context, importer)
        self.remote_storage = importer.remote_storage

