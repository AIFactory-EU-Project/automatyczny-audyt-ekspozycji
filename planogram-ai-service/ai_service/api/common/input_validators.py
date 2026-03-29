from PIL import Image
from webargs import fields


def validate_image(file):
    if file.mimetype in ["image/png", "image/jpeg"]:
        try:
            img = Image.open(file)
            img.verify()
            img.close()
            return True
        except:
            pass
    return False


default_args = {
    "image": fields.Field(
        location="files", validate=validate_image, required=True
    ),
}

planogram_report_args = {
    "image": fields.Field(
        location="files", validate=validate_image, required=True
    ),
    "planogram_id": fields.Integer(required=True)
}
