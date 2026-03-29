
class ValidationError(Exception):
    message = ''
    field = 'image'


class LowResolutionImage(ValidationError):
    message = 'low resolution image'


class ImageIsMissing(ValidationError):
    message = 'image is missing'


class ArgumentRequired(ValidationError):
    def __init__(self, name):
        self.message = 'argument required: "{}"'.format(name)

class ArgumentInvalid(ValidationError):
    def __init__(self, msg):
        self.message = "{}".format(msg)
