import thumbordumper.remote_storages.http_storage
import email
import hashlib
import mimetypes
import base64
import hmac
import urlparse

required_headers = ('content-md5',
                    'content-type',
                    'date') # sorted

amz_prefix = 'x-amz-'

allowed_query_params = set(('acl',
                            'versionid',
                            'versioning'))

def _canonical_string(request):
    headers = request.headers
    method = request.method
    url = request.url
    
    lower_iter = ((k.lower(),unicode(v).strip())
                  for k,v
                  in headers.iteritems())
    lower_headers = dict((k,v)
                         for k,v
                         in lower_iter
                         if k in required_headers \
                            or k.startswith(amz_prefix))


    if 'x-amz-date' in lower_headers:
        lower_headers['date'] = ''

#    if expires is not None:
#        lower_headers['date'] = unicode(expires)
    
    sign_items = [unicode(method).upper()]
    sign_items += [lower_headers.get(k, '') for k in required_headers]
    sign_items += [k + ':' + v 
                   for k,v 
                   in lower_headers.iteritems()
                   if k.startswith(amz_prefix)]

    parsed = urlparse.urlsplit(url)

    canonical_url = parsed.path
    if parsed.query:
        canonical_string += urllib.urlencode(q 
                                             for q 
                                             in urlparse.parse_qsl(parsed.query) 
                                             if q in allowed_query_params)

    sign_items.append(canonical_url)

    return '\n'.join(sign_items)
        
class Storage(thumbordumper.remote_storages.http_storage.Storage):

    def __init__(self, context):
        thumbordumper.remote_storages.http_storage.Storage.__init__(self, context)

        if not context.config.S3_SECRET_ACCESS_KEY:
            raise RuntimeError("S3_SECRET_ACCESS_KEY can't be empty if s3_storage specified")
        self.s3_secret_access_key = context.config.S3_SECRET_ACCESS_KEY

        if not context.config.S3_ACCESS_KEY_ID:
            raise RuntimeError("S3_ACCESS_KEY_ID can't be empty if s3_storage specified")
        self.s3_access_key_id = context.config.S3_ACCESS_KEY_ID

        self.s3_put_x_amz_acl = context.config.S3_PUT_X_AMZ_ACL if hasattr(context.config, 'S3_PUT_X_AMZ_ACL') else None

    def sign_request(self, request):
        if 'Date' not in request.headers:
            request.headers['Date'] = email.utils.formatdate(None, False, True)

        if request.body is not None:
            request.headers['Content-Md5'] = base64.encodestring(hashlib.md5(request.body).digest()).strip()

        if 'Content-Type' not in request.headers:
            type = mimetypes.guess_type(request.url, False)[0]
            if type is not None:
                request.headers['Content-Type'] = type

        if self.s3_put_x_amz_acl:
            request.headers['x-amz-acl'] = self.s3_put_x_amz_acl

        canonical_string = _canonical_string(request)

        digest = hmac.new(self.s3_secret_access_key, canonical_string, hashlib.sha1).digest()
        signature = base64.encodestring(digest).strip()

        request.headers['Authorization'] = 'AWS %s:%s' % (self.s3_access_key_id, signature)
