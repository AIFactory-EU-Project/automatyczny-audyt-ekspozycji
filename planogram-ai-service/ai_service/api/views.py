import logging
import io
import cv2
import numpy as np
from io import BytesIO
import uuid

from PIL import Image
from flask import Blueprint, jsonify, send_file, request
from flask_apispec import FlaskApiSpec

from ai_service.ai.scripts.remove_faces import remove_faces
from ai_service.api.common.exceptions import ImageIsMissing, ArgumentRequired, ArgumentInvalid
from ai_service.api.common.input_validators import validate_image
from ai_service.ai.scripts.grills.grill_report import grill_report
from ai_service.ai.scripts.meals.planogram_report import planogram_report


api_blueprint = Blueprint('api', __name__)
api_doc = FlaskApiSpec()


def read_image(bytes_img,image_id):
    """ """
    if bytes_img is None:
        raise ImageIsMissing()
    img = Image.open(bytes_img).convert()
    output = io.BytesIO()
    img.save(output, format='PNG')
    # disabled for now; maybe log only when exception occured?
    #if image_id:
    #    img.save('/home/appuser/logs/{}.png'.format(image_id))
    output.seek(0, 0)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    return img


@api_blueprint.route('/verify-grill-photo-valid-for-analysis', methods=['POST'])
def verify_grill_photo_valid_for_analysis():
    if 'image' not in request.files:
        raise ArgumentRequired('image')
    if not validate_image(request.files['image']):
        raise ArgumentInvalid('invalid image: should be in png or jpeg format')

    logging.info("verify-grill-photo-valid-for-analysis")

    return jsonify({'result': True}), 200


@api_blueprint.route('/verify-shelf-photo-valid-for-analysis', methods=['POST'])
def verify_shelf_photo_valid_for_analysis():
    if 'image' not in request.files:
        raise ArgumentRequired('image')
    if not validate_image(request.files['image']):
        raise ArgumentInvalid('invalid image: should be in png or jpeg format')

    logging.info("verify-shelf-photo-valid-for-analysis")

    return jsonify({'result': True}), 200


@api_blueprint.route('/remove-faces-from-photo', methods=['POST'])
def remove_faces_from_photo():
    if 'image' not in request.files:
        raise ArgumentRequired('image')
    if not validate_image(request.files['image']):
        raise ArgumentInvalid('invalid image: should be in png or jpeg format')
    req_id = uuid.uuid4()
    logging.info("remove-faces-from-photo req_id={}".format(req_id))

    # decode image
    request.files['image'].stream.seek(0)
    img = request.files['image'].stream.read()
    img = np.frombuffer(img, np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)

    # gpu operation
    img = remove_faces(img)

    # encode image
    retval, buf = cv2.imencode(".png", img)
    if not retval:
        e = Exception('cannot encode image: imencode retval {}'.format(retval))
        logging.error(e)
        raise e
    output = BytesIO(buf.tobytes())

    return send_file(output, mimetype="image/png"), 200


@api_blueprint.route('/generate-grill-report', methods=['POST'])
def generate_grill_report():
    if 'image' not in request.files:
        raise ArgumentRequired('image')
    if not validate_image(request.files['image']):
        raise ArgumentInvalid('invalid image: should be in png or jpeg format')
    
    req_id = uuid.uuid4()
    logging.info('generate-grill-report req_id={}'.format(req_id))

    img = read_image(request.files['image'], image_id=req_id)
    count = grill_report(img)
    return jsonify({"result": {"count": count}}), 200


@api_blueprint.route('/generate-planogram-report', methods=['POST'])
def generate_planogram_report():
    """
    Should generate smth like this: {
        "result": {
            "boxes": [
                {
                    "accuracy": float,
                    "shelfFromTop": int,
                    "positionFromLeft": int,
                    "skuIndex": string,
                    "box": {
                        topLeftX: int,
                        topLeftY: int,
                        width: int,
                        height: int
                    }
                },
                ...
            ]
        }
    }
    """
    if 'image' not in request.files:
        raise ArgumentRequired('image')
    if not validate_image(request.files['image']):
        raise ArgumentInvalid('invalid image: should be in png or jpeg format')
    if 'planogramId' not in request.form:
        raise ArgumentRequired('planogramId')
    if 'cameraIp' not in request.form:
        raise ArgumentRequired('cameraIp')

    planogramId = request.form['planogramId']
    cameraIp = request.form['cameraIp']
    req_id = uuid.uuid4()
    logging.info('generate_planogram_report planogramId={} cameraIp={} req_id={}'.format(planogramId, cameraIp, req_id))
    img = read_image(request.files['image'], image_id=req_id)
    boxes = planogram_report(img, request.form['cameraIp'])
    return jsonify({'result': {'boxes': boxes}}), 200


@api_blueprint.route('/health-check', methods=['GET'])
def health_check():
    return jsonify({}), 200


