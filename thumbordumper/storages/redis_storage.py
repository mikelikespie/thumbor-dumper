import thumbor.storages.redis_storage
from datetime import datetime, timedelta

class Storage(thumbor.storages.redis_storage.Storage):
    not_uploaded_key = 'thumbor-dumper-not-uploaded'

    def __upload_lock_for(self, url):
        return 'thumbor-dumper-uploading-%s' % url

    def put(self, path, bytes):
        self.storage.set(path, bytes)

    def put_not_uploaded(self, path):
        self.storage.sadd(self.not_uploaded_key, path)

    def put_uploaded(self, path):
        self.storage.srem(self.not_uploaded_key, path)
        self.storage.expireat(path, datetime.now() + timedelta(seconds=self.context.config.STORAGE_EXPIRATION_SECONDS))

    def upload_lock(self, path):
        return self.storage.lock(self.__upload_lock_for(path), self.context.config.STORE_LOCK_TIMEOUT)
