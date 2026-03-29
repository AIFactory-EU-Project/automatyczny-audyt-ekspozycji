import json
import os
import sys
import time
from helpers import http_request, basic_auth, MultipartFormdata


data_dir = os.path.join(os.path.dirname(__file__), 'data/')


def get_adr():
    """ Return address of the service under test """
    return sys.argv[1] if len(sys.argv) >= 2 else "127.0.0.1:7552"


def test_health_check():
    r = http_request('GET', get_adr(), "/health-check")
    assert r.status == 200, (r.status, r.reason, r.read())
    result = json.loads(r.read())
    assert result == {}, result


def test_verify_grill_photo_valid_for_analysis__valid():
    ply = MultipartFormdata().file("image", data_dir+'valid.jpg', "image/jpeg")
    r = http_request('POST', get_adr(), '/verify-grill-photo-valid-for-analysis',
                     body=ply.data(),
                     head={b'Content-Type': ply.content_type(),
                           b'accept': b'application/json'})
    assert r.status == 200, (r.status, r.reason, r.read())
    result = json.loads(r.read())
    assert result == {"result": True}, result


def test_verify_grill_photo_valid_for_analysis__400():
    ply = MultipartFormdata().file("image", data_dir+'invalid.png', "image/png")
    r = http_request('POST', get_adr(), '/verify-grill-photo-valid-for-analysis',
                     body=ply.data(),
                     head={b'Content-Type': ply.content_type(),
                           b'accept': b'application/json'})
    assert r.status == 400, (r.status, r.reason, r.read())
    result = json.loads(r.read())
    assert result == {'message': 'invalid image: should be in png or jpeg format'}, result


def test_verify_shelf_photo_valid_for_analysis__valid():
    ply = MultipartFormdata().file("image", data_dir+'valid.jpg', "image/jpeg")
    r = http_request('POST', get_adr(), '/verify-shelf-photo-valid-for-analysis',
                     body=ply.data(),
                     head={b'Content-Type': ply.content_type()})
    assert r.status == 200, (r.status, r.reason, r.read())
    result = json.loads(r.read())
    assert result == {"result": True}, result


def test_verify_shelf_photo_valid_for_analysis__400():
    ply = MultipartFormdata().file("image", data_dir+'invalid.png', "image/png")
    r = http_request('POST', get_adr(), '/verify-shelf-photo-valid-for-analysis',
                     body=ply.data(),
                     head={b'Content-Type': ply.content_type()})
    assert r.status == 400, (r.status, r.reason, r.read())
    result = json.loads(r.read())
    assert result == {'message': 'invalid image: should be in png or jpeg format'}, result


def test_remove_faces_from_photo():
    ply = MultipartFormdata().file("image", data_dir+'remove_faces_from_photo-1.png', "image/png")
    r = http_request('POST', get_adr(), '/remove-faces-from-photo',
            body=ply.data(),
            head={b'Content-Type': ply.content_type()})
    assert r.status == 200, (r.status, r.reason, r.read())
    assert r.getheader("content-type") == 'image/png', r.getheader("content-type")
    result = r.read()
    with open(data_dir+'tmp.png', 'wb') as f:
        f.write(result)
    with open(data_dir+'remove_faces_from_photo-1b.png', 'rb') as f:
        target = f.read()
        assert target  == result, (len(target), len(result))
    assert len(result) > 0, len(result)


def test_generate_grill_report():
    ply = MultipartFormdata().file("image", data_dir + '7.251.jpg', "image/jpeg")
    r = http_request('POST', get_adr(), '/generate-grill-report',
                     body=ply.data(),
                     head={b'Content-Type': ply.content_type()})
    assert r.status == 200, (r.status, r.reason, r.read())
    result = json.loads(r.read())
    assert result == {'result': {'count': 18}}, result


def test_generate_grill_report__400():
    # send request without data
    r = http_request('POST', get_adr(), '/generate-grill-report')
    assert r.status == 400, (r.status, r.reason, r.read())
    result = json.loads(r.read())
    assert result == {'message': 'argument required: "image"'}, result


def test_generate_planogram_report():
    ply = MultipartFormdata().file("image", data_dir + 'dahua_172.16.1.252_12-Nov-2019_09_00_01.png', "image/png")
    ply = ply.field('planogramId', 1)
    ply = ply.field('cameraIp', '172.16.1.252')
    r = http_request('POST', get_adr(), '/generate-planogram-report',
                     body=ply.data(),
                     head={b'Content-Type': ply.content_type()})
    assert r.status == 200, (r.status, r.reason, r.read())
    result = json.loads(r.read())

    result_boxes = result['result']['boxes']
    item1={'accuracy': 99,
        'box': {'height': 89, 'topLeftX': 73, 'topLeftY': 649, 'width': 100},
        'positionFromLeft': 2,
        'shelfFromTop': 1,
        'skuIndex': '12002745'}

    def format_boxes(boxes):
        import pprint
        lst = []
        for i,rb in enumerate(boxes):
            lst.append(str(i))
            lst.append(pprint.pformat(rb))
        return '\n'.join(lst)
    if item1 not in result_boxes:
        print(format_boxes(result_boxes))
    assert len(result_boxes) >= 30, len(result_boxes)
    assert item1 in result_boxes, format_boxes(result_boxes)


def test_generate_planogram_report__400():
    ply = MultipartFormdata().file("image", data_dir + 'invalid.png', "image/png")
    r = http_request('POST', get_adr(), '/generate-planogram-report',
                     body=ply.data(),
                     head={b'Content-Type': ply.content_type()})
    assert r.status == 400, (r.status, r.reason, r.read())
    result = json.loads(r.read())
    assert result == {'message': "invalid image: should be in png or jpeg format"}, result



_run_i=0
def run(f):
    global _run_i
    k = int(sys.argv[2]) if len(sys.argv) >= 3 else None    
    print(f.__name__, '[{}]'.format(_run_i))
    if k is None or _run_i == k:
        t0 = time.time()
        f()
        t1 = time.time()
        print('... runtime_s {:.3f}'.format(t1-t0))
    else:
        print('... skip') 
    _run_i+=1

if __name__ == "__main__":
    print('testing', get_adr())
    run(test_health_check)

    run(test_verify_grill_photo_valid_for_analysis__valid)
    run(test_verify_grill_photo_valid_for_analysis__400)

    run(test_verify_shelf_photo_valid_for_analysis__valid)
    run(test_verify_shelf_photo_valid_for_analysis__400)

    run(test_remove_faces_from_photo)

    run(test_generate_grill_report)
    run(test_generate_grill_report__400)

    run(test_generate_planogram_report)
    run(test_generate_planogram_report__400)

    print('ok')



