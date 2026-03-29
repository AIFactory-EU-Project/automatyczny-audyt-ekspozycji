import http.client
import base64
import binascii
import os


class MultipartFormdata:
    """ Usage
    mf=MultipartFormdata()
    mf.field("ala", "val")
    mf.file("file1", "path/to/file.txt", "text/plain")
    print(mf.data())
    print(mf.content_type())
    """

    def __init__(self):
        self.xs = []
        self.boundary = binascii.hexlify(os.urandom(16)).decode('ascii')

    def field(self, name, value):
        self.xs.append("--{}\r\n".format(self.boundary).encode('ascii'))
        self.xs.append("Content-Disposition: form-data; name=\"{}\"\r\n".format(name).encode('ascii'))
        self.xs.append("\r\n".encode('ascii'))
        self.xs.append("{}\r\n".format(value).encode('ascii'))
        return self

    def file(self, name, path, content_type):
        fname = os.path.basename(path)
        self.xs.append("--{}\r\n".format(self.boundary).encode('ascii'))
        self.xs.append("Content-Disposition: form-data; name=\"{}\"; filename=\"{}\"\r\n".format(name,fname).encode('ascii'))
        self.xs.append("Content-Type: {}\r\n".format(content_type).encode('ascii'))
        self.xs.append("\r\n".encode('ascii'))
        self.xs.append(open(path, 'rb').read())
        self.xs.append("\r\n".encode('ascii'))
        return self

    def data(self):
        closing_boundary = "--{}--\r\n".format(self.boundary).encode('ascii')
        return b"".join(self.xs+[closing_boundary])

    def content_type(self):
        return "multipart/form-data; boundary={}".format(self.boundary)



def basic_auth(usr,pwd):
    return b"Basic " + base64.b64encode(':'.join((usr,pwd)).encode('ascii'))


def http_request(method: str, adr: str, uri: str, body: bytes = None, head: dict = {}) -> http.client.HTTPResponse:
    """ Send http request helper function
    :param method: 'GET'|'POST'
    :param adr: ex "0.0.0.0:7001"
    :param uri: ex "/api/exam"
    :param body: ex b'{"some": ["json"]}'
    :param head: ex {b'Content-Type': b'application/json'}
    :return: HttpResponse
    """
    c = http.client.HTTPConnection(adr)
    c.request(method, uri, headers=head, body=body)
    r = c.getresponse()
    # use: r.status, r.reason, r.read()
    return r
