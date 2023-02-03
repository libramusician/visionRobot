import boundingBox
import logger.logger

WIDTH = 416
HEIGHT = 416
REGION_L1 = 0.45
REGION_R1 = 0.55


# def analysis(bbox: boundingBox.BoundingBox):
#     x, y = bbox.get_center()
#     if 0 <= x < WIDTH * 0.4:
#         return "5"
#     elif WIDTH * 0.4 <= x < WIDTH * 0.6:
#         return "0"
#     else:
#         return "6"

@logger.logger.add_log
def analysis(bbox: tuple[int, int, int, int]):
    x, y = boundingBox.get_center_from_box(bbox)
    if 0 <= x < WIDTH * REGION_L1:
        return "5"
    elif WIDTH * REGION_L1 <= x < WIDTH * REGION_R1:
        return "0"
    else:
        return "6"
