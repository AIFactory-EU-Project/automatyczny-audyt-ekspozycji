from flask import Flask, request, Response
from camera_service.frame_reader import get_frame, Error
from werkzeug.exceptions import abort

app = Flask(__name__)


@app.route("/")
def hello():
    return "camera_service\n"


@app.route("/image/<string:cam_ip>/<string:cam_type>", methods=['GET'])
def image(cam_ip, cam_type):
    auth = request.authorization
    if auth is None:
        return Response(status=401, headers={'WWW-Authenticate': 'Basic realm = "camera_service"'})

    try:
        img = get_frame(cam_ip=cam_ip, cam_type=cam_type, usr=auth['username'], pwd=auth['password'])
        return Response(response=img, status=200, content_type="image/png")
    except Error as e:
        abort(e.status, e.description)


if __name__ == "__main__":
    app.run()
