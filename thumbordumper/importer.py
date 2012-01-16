import thumbor.importer

class Importer(thumbor.importer.Importer):
    def import_modules(self):
        self.config.validates_presence_of('DUMPER_STORAGE', 'REMOTE_STORAGE')
        self.import_item('DUMPER_STORAGE', 'Storage')
        self.import_item('REMOTE_STORAGE', 'Storage')

