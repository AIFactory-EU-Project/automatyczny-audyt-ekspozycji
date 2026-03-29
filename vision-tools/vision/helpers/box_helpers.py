# from http://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/
def bb_intersection_over_union(box_a, box_b):
    # determine the (x, y)-coordinates of the intersection rectangle
    x_a = max(box_a[0], box_b[0])
    y_a = max(box_a[1], box_b[1])
    x_b = min(box_a[2], box_b[2])
    y_b = min(box_a[3], box_b[3])

    # compute the area of intersection rectangle
    inter_area = max(0, x_b - x_a) * max(0, y_b - y_a)

    # compute the area of both the prediction and ground-truth
    # rectangles
    box_a_area = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
    box_b_area = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the intersection area
    iou = inter_area / float(box_a_area + box_b_area - inter_area) if float(box_a_area + box_b_area - inter_area) != 0 else 0

    # return the intersection over union value
    return iou


def bb_intersection_over_a(box_a, box_b):
    # determine the (x, y)-coordinates of the intersection rectangle
    x_a = max(box_a[0], box_b[0])
    y_a = max(box_a[1], box_b[1])
    x_b = min(box_a[2], box_b[2])
    y_b = min(box_a[3], box_b[3])

    # compute the area of intersection rectangle
    inter_area = max(0, x_b - x_a) * max(0, y_b - y_a)

    # compute the area of a rectangle
    box_a_area = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])

    iou = inter_area / float(box_a_area)
    return iou


def bb_remove_duplicates(l, thresh):
    l_copy = list(l)
    for i, box1 in enumerate(list(l_copy)):
        for box2 in list(l_copy[i + 1:]):
            if bb_intersection_over_union(box1, box2) > thresh and box1 in l:
                l.remove(box1)


def bb_translation(box, relative_box):
    return box[0] + relative_box[0], box[1] + relative_box[1], box[2] + relative_box[0], box[3] + relative_box[1]


def bb_extend(box, scale, limits):
    half_scale = scale / 2
    w_offset = int((box[2] - box[0]) * half_scale)
    h_offset = int((box[3] - box[1]) * half_scale)
    return max(0, box[0] - w_offset), max(0, box[1] - h_offset), min(limits[0], box[2] + w_offset), min(limits[1], box[3] + h_offset)


def bb_shrink(box, scale):
    half_scale = scale / 2
    w_offset = int((box[2] - box[0]) * half_scale)
    h_offset = int((box[3] - box[1]) * half_scale)
    return min(box[2] - w_offset, box[0] + w_offset), min(box[2] - w_offset, box[1] + h_offset), max(box[0] + w_offset, box[2] - w_offset), max(box[1] + h_offset, box[3] - h_offset)
