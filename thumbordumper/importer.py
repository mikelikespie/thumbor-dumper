import thumbor.importer

class Importer(thumbor.importer.Importer):
    def import_modules(self):
        self.config.validates_presence_of('STORAGE', 'REMOTE_STORAGE')
        self.import_item('STORAGE', 'Storage')
        self.import_item('REMOTE_STORAGE', 'Storage')

