class ObjectPosition:

    def __init__(self, top_left_x, top_left_y, width, height):
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.width = width
        self.height = height


class DetectedObject:

    def __init__(self, accuracy, shelf_from_top,
                 position_from_left, sku_index,
                 object_position: ObjectPosition):
        self.accuracy = accuracy
        self.shelf_from_top = shelf_from_top
        self.position_from_left = position_from_left
        self.sku_index = sku_index
        self.object_position = object_position


class DetectedObjects:
    def __init__(self) -> None:
        self.list = []


class PlanogramReport:

    def __init__(self) -> None:
        self.detected_objects_list = DetectedObjects()

    def add_detected_object(self, **kwargs):
        self.detected_objects_list.list.append(DetectedObject(**kwargs))

