import json
import socket

import struct

BUFFER_SIZE = 32768


def get_detection_request(key, value):
    buffer = []
    key_encoded = bytes(key, "utf-8")
    value_encoded = bytes(value, "utf-8")
    buffer.append(struct.pack("<H", len(key_encoded)))
    buffer.append(key_encoded)
    buffer.append(struct.pack("<H", len(value_encoded)))
    buffer.append(value_encoded)
    data_bytes = b"".join(buffer)
    header_bytes = struct.pack("<BHB", 0, len(data_bytes), 0)
    return header_bytes, data_bytes


def get_response(socket):
    response = []
    while True:
        raw_response = socket.recv(BUFFER_SIZE)
        response.append(raw_response.decode().strip())
        if len(raw_response) < BUFFER_SIZE:
            break

    return "".join(response)


def request_detection(socket_name, key, values):
    # \0 is an invalid character in many cases, so we are almost sure it cannot occur in any value
    value = "\0".join(values)
    header, data = get_detection_request(key, value)

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.connect(socket_name)
        sock.sendall(header)
        sock.sendall(data)

        response = get_response(sock)

    return json.loads(response)


def handle_request(service, params):
    response = []
    try:
        image_paths = params["image_paths"].split("\0")
        result = service.process(image_paths)
        json_result = json.dumps(result)
        response.append(json_result)
    except Exception as e:
        response.append(str(e))
    return [bytes(r, "utf-8") for r in response]
