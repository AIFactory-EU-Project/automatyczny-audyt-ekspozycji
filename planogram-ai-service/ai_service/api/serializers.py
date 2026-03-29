from marshmallow import Schema, fields


class ObjectPositionSchema(Schema):
    topLeftX = fields.Integer(attribute='top_left_x')
    topLeftY = fields.Integer(attribute='top_left_y')
    width = fields.Integer()
    height = fields.Integer()


class DetectedObjectSchema(Schema):
    accuracy = fields.Float()
    shelfFromTop = fields.Integer(attribute='shelf_from_top')
    positionFromLeft = fields.Integer(attribute='position_from_left')
    skuIndex = fields.String(attribute='sku_index')
    box = fields.Nested(ObjectPositionSchema, attribute='object_position')


class DetectedObjectsSchema(Schema):
    detectedObjectsList = fields.Nested(DetectedObjectSchema, attribute='list', many=True)


class PlanogramReportSchema(Schema):
    planogramReport = fields.Nested(DetectedObjectsSchema, attribute='detected_objects_list')

