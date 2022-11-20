from BoundingBox import BoundingBox

WIDTH = 320
HEIGHT = 240


def analysis(bbox: BoundingBox):
    x, y = bbox.get_center()
    if 0 <= x < WIDTH * 0.4:
        return 5
    elif WIDTH * 0.4 <= x < WIDTH * 0.6:
        return 0
    else:
        return 6

