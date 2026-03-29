#!/usr/bin/env python3
import sys
import http.client
import http.server
import base64

def get_camserv_adr():
    """ Return address of the service under test """
    return sys.argv[1] if len(sys.argv) == 2 else "127.0.0.1:5000"

# TODO: dahua and hikvision camera mock-up
#def run():
#    httpd = http.server.HTTPServer(('127.0.0.1', 8000),
#                                   BaseHTTPRequestHandler)
#    httpd.serve_forever()

def req(adr:str, uri:str, auth, method='GET')->http.client.HTTPResponse:
    """ Send request to camera service
    :param adr: adr
    :param uri: uri
    :param auth: Optional (username, password)
    :param opath: Optional path where to save image
    :param method: 'GET'|'POST'
    :return:
    """
    h = {}
    if auth:
        httpauth=base64.b64encode(':'.join(auth).encode('ascii'))
        h[b"Authorization"]=b"Basic "+httpauth
    c = http.client.HTTPConnection(adr)
    c.request(method, uri, headers=h)
    r = c.getresponse()
    return r

def test_image_200_alltypes(camera_service):
    print('test_image_200_alltypes')
    # all camera types -> 200 Found
    r = req(
        adr=camera_service,
        uri="/image/{}/{}".format('172.16.1.252', 'dahua'),
        auth=("admin", "111222qqqwww"))
    assert r.status == 200
    x = r.read()
    assert len(x)>0
    r = req(
        adr=camera_service,
        uri="/image/{}/{}".format('172.16.1.253', 'hikvision'),
        auth=("admin", "111222qqqwww"))
    assert r.status==200
    x = r.read()
    assert len(x)>0

def test_image_504_badip(camera_service):
    print('test_image_504_badip')
    # incorrect ip -> 504 Gateway timeout
    r = req(
        adr=camera_service,
        uri="/image/{}/{}".format('999.222.999.111', 'dahua'),
        auth=("admin", "111222qqqwww"))
    assert r.status == 504
    r.read()

def test_image_400_badtype(camera_service):
    print('test_image_400_badtype')
    # 400 Bad camera type -> bad cam type
    r = req(
        adr=camera_service,
        uri="/image/{}/{}".format('172.16.1.252', 'blabla'),
        auth=("admin", "111222qqqwww"))
    assert r.status == 400
    r.read()

def test_image_401_noauth(camera_service):
    print('test_image_401_noauth')
    # no auth -> 401 Unauthorized
    r = req(
        adr=camera_service,
        uri="/image/{}/{}".format('172.16.1.252', 'dahua'),
        auth=None)
    assert r.status == 401
    r.read()

def test_image_401_badauth(camera_service):
    print('test_image_401_badauth')
    # incorrect auth -> 401 Unauthorized
    r = req(
        adr=camera_service,
        uri="/image/{}/{}".format('172.16.1.252', 'dahua'),
        auth=("admin", "blabla"))
    assert r.status == 401
    r.read()

if __name__=="__main__":
    camera_service = get_camserv_adr()
    test_image_200_alltypes(camera_service)
    
    test_image_400_badtype(camera_service)
    test_image_401_noauth(camera_service)
    test_image_401_badauth(camera_service)
    test_image_504_badip(camera_service)
    



