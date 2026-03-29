import cv2 as cv


def pad_to_aspect_ratio(img, aspect_ratio, pad_value=(127, 127, 127), norm_offset_ops=True, norm_reverse_ops=False):
    """
    Add symetrical padding to get desired aspect ratio
    Returns image and operations to calculate coordinates change both ways
    (for absolute or normalized points, depending on flags)

    :param img: image to be padded
    :param aspect_ratio: desired aspect ratio
    :param pad_value: padding color
    :param norm_offset_ops: return offset operations for normalized points
    :param norm_reverse_ops: return reverse operations for normalized points
    :return: padded image, image to padded coordinates operations, padded to image coordinates operations
    """

    width = img.shape[1]
    height = img.shape[0]
    missing_width = 0
    missing_height = 0

    if 1.0 * width / height < aspect_ratio:
        missing_width = int(height * aspect_ratio) - width
    elif 1.0 * width / height > aspect_ratio:
        missing_height = int(width / aspect_ratio) - height

    offset_h = int(missing_height / 2)
    offset_w = int(missing_width / 2)

    padded = cv.copyMakeBorder(img,  offset_h, offset_h, offset_w, offset_w, 0, value=pad_value)

    def offset_y_op(y):
        return y + offset_h

    def offset_x_op(x):
        return x + offset_w

    def norm_offset_y_op(y):
        return (y * height + offset_h) / (height + 2 * offset_h)

    def norm_offset_x_op(x):
        return (x * width + offset_w) / (width + 2 * offset_w)

    def reverse_y_op(y):
        return y - offset_h

    def reverse_x_op(x):
        return x - offset_w

    def norm_reverse_y_op(y):
        return (y * (height + 2 * offset_h) - offset_h) / height

    def norm_reverse_x_op(x):
        return (x * (width + 2 * offset_w) - offset_w) / width

    if norm_offset_ops:
        offset_ops = (norm_offset_y_op, norm_offset_x_op)
    else:
        offset_ops = (offset_y_op, offset_x_op)

    if norm_reverse_ops:
        reverse_ops = (norm_reverse_y_op, norm_reverse_x_op)
    else:
        reverse_ops = (reverse_y_op, reverse_x_op)

    return padded, offset_ops, reverse_ops


def extend_roi(image, roi_point_min, roi_point_max, ratio):
    """
    Extend roi in all directions to be [ratio] as high and wide (as far as image allows).
    Returns extended roi copy and operations to calculate normalized coordinates from roi to extended roi

    :param image: source image
    :param roi_point_min: point min of rectangular roi (tuple)
    :param roi_point_max: point max of rectangular roi (tuple)
    :param ratio: ratio to be achieved by extended roi (if possible)
    :return: deepcopy of extended image roi, roi to extended roi coordinates operations
    """

    image_height, image_width = image.shape[:2]
    roi_height = roi_point_max[1] - roi_point_min[1]
    roi_width = roi_point_max[0] - roi_point_min[0]
    point_min = (max(0, int(roi_point_min[0] - roi_width * (ratio - 1) / 2)),
                 max(0, int(roi_point_min[1] - roi_height * (ratio - 1) / 2)))
    point_max = (min(image_width - 1, int(roi_point_max[0] + roi_width * (ratio - 1) / 2)),
                 min(image_height - 1, int(roi_point_max[1] + roi_height * (ratio - 1) / 2)))

    offset_left = abs(roi_point_min[0] - point_min[0])
    offset_right = abs(point_max[0] - roi_point_max[0])
    offset_top = abs(roi_point_min[1] - point_min[1])
    offset_bottom = abs(point_max[1] - roi_point_max[1])

    image_roi = image[point_min[1]:point_max[1], point_min[0]:point_max[0]].copy()

    def adjust_y(norm_value):
        return (norm_value * roi_height + offset_top) / (roi_height + offset_top + offset_bottom)

    def adjust_x(norm_value):
        return (norm_value * roi_width + offset_left) / (roi_width + offset_left + offset_right)

    return image_roi, (adjust_y, adjust_x)
