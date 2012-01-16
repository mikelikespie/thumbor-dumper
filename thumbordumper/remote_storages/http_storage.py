import posixpath
import urlparse

import tornado.httpclient

import thumbor.storages
import thumbor.loaders.http_loader

import posixpath

import logging
logger = logging.getLogger(__name__)

def _canonical_url(url):
    """URL normalization code from http://stackoverflow.com/a/4317446/64941"""
    parsed = urlparse.urlparse(url)
    if '..' in posixpath.split(parsed.path):
        raise ValueError('Cannot have ".." as a path component in URLs')

    new_path = posixpath.normpath(parsed.path)
    if parsed.path.endswith('/'):
        # Compensate for issue1707768
        new_path += '/'
    cleaned = parsed._replace(path=new_path)
    return cleaned.geturl()


def _wrap_cb(fn):
    def wrapper(response):
        if response.error:
            logger.error("Request for failed. error: %s", response.error)
        else:
            logger.info("Request succeeded for %s", response.request.url)
        fn(response.body, response.error)

    return wrapper

#callbacks take a body and an error argument
class Storage(thumbor.storages.BaseStorage):
    http_client = None

    def put(self, path, bytes, callback):
        url = _canonical_url(path)
        request = tornado.httpclient.HTTPRequest(url,
                                                 method='PUT', 
                                                 body=bytes)
        self.fetch(request, callback)

    def get(self, path, callback):
        url = _canonical_url(path)
        request = tornado.httpclient.HTTPRequest(url,
                                                 method='GET')
        self.fetch(request, callback)

    def fetch(self, request, callback):
        self.sign_request(request)
        self.client.fetch(request, callback=_wrap_cb(callback))

    @property
    def client(self):
        if self.__class__.http_client is None:
            self.__class__.http_client = tornado.httpclient.AsyncHTTPClient()
        
        return self.__class__.http_client

    def sign_request(self, request):
        pass

