import copy
from collections import defaultdict
import copy
from ai_service.ai.scripts.meals.shelves.shelves_data import shelves_data


def bb_intersection_over_a(box_a, box_b):
    x_a = max(box_a[0], box_b[0])
    y_a = max(box_a[1], box_b[1])
    x_b = min(box_a[2], box_b[2])
    y_b = min(box_a[3], box_b[3])

    inter_area = max(0, x_b - x_a) * max(0, y_b - y_a)
    box_a_area = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
    iou = inter_area / float(box_a_area)

    return iou


def prepare_shelves(boxes, camera_ip):
    shelves = defaultdict(list)
    shelf_key = camera_ip.split(".", 2)[2]
    shelf_regions = shelves_data.get(shelf_key, None)
    if not shelf_regions:
        return []

    for region in shelf_regions:
        x, y = region["x"], region["y"]
        w, h = region["width"], region["height"]
        for box in boxes:
            box_x, box_y = box["topLeftX"], box["topLeftY"]
            box_w, box_h = box["width"], box["height"]
            iou = bb_intersection_over_a((x, y, x+w, y+h), (box_x, box_y, box_x+box_w, box_y+box_h))
            if iou:
                shelves[(x, y, w, h)].append(box)

    # sort shelves by their y-coordinate
    sorted_shelves = sorted(shelves.items(), key=lambda s: s[0][1], reverse=True)

    # sort shelf's boxes by their x-coordinate
    sorted_shelves = [sorted(shelf[1], key=lambda box: box["topLeftX"]) for shelf in sorted_shelves]

    return sorted_shelves


def planogram_boxes(boxes, camera_ip):
    """ Return boxes in format expected by api.
    Also map shelfNum and position from 0..N-1 to 1..N range
    """
    sorted_shelves = prepare_shelves(boxes, camera_ip)
    result = []
    for shelf_number, shelf in enumerate(sorted_shelves):
        for box_number, box in enumerate(shelf):
            box_c = copy.copy(box)
            result.append({
                "accuracy": box_c.pop("accuracy"),
                "shelfFromTop": shelf_number+1,
                #"shelfFromBottom": shelf_number+1,
                "positionFromLeft": box_number+1,
                "skuIndex": box_c.pop("skuIndex"),
                "box": box_c})

    return result
