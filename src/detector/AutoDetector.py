import os.path

import cv2
import numpy
from src.boundingBox import BoundingBox

confThreshold = 0.5  # Confidence threshold
nmsThreshold = 0.3  # Non-maximum suppression threshold
inpWidth = 416  # Width of network's input image
inpHeight = 416  # Height of network's input image
counter = 0
path = os.path.dirname(__file__)
CLASS_FILE = os.path.join(path, "coco.names")
CONFIG_FILE = os.path.join(path, "yolov3-tiny.cfg")
WEIGHT_FILE = os.path.join(path, "yolov3-tiny.weights")


def post_process(frame, outs):
    """
    get all the bounding boxes from detection and use non-maximum to reduce duplicated
    :param frame: the initial frame
    :param outs: the result from detection
    :return: list of bounding boxes
    """
    result_boxes = []
    frame_height = frame.shape[0]
    frame_width = frame.shape[1]

    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    class_ids = []
    confidences = []
    boxes = []
    # iterate through all the layers
    for out in outs:
        for detection in out:
            # confidence of each class start from 5th entry
            scores = detection[5:]
            class_id = numpy.argmax(scores)
            confidence = scores[class_id]
            if confidence > confThreshold:
                # convert from ratio to pixel
                center_x = int(detection[0] * frame_width)
                center_y = int(detection[1] * frame_height)
                width = int(detection[2] * frame_width)
                height = int(detection[3] * frame_height)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non-maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        # create bounding box for result return
        bbox = BoundingBox((left, top, width, height))
        result_boxes.append(bbox)
        # drawPred(classIds[i], confidences[i], left, top, left + width, top + height)
    print(str(len(result_boxes)) + "result detected")
    return result_boxes


class AutoDetector:
    def __init__(self):
        # Load names of classes
        with open(CLASS_FILE, 'rt') as f:
            self.classes = f.read().rstrip('\n').split('\n')

        # Give the configuration and weight files for the model and load the network using them.

        net = cv2.dnn.readNetFromDarknet(CONFIG_FILE, WEIGHT_FILE)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        self.net = net

    def get_layer_names(self):
        """
        get the list of cnn layers used for detection
        yolo use 3 layers for big medium small objects
        :return:name of the cnn layers
        """
        # Get the names of all the layers in the network
        layers_names = self.net.getLayerNames()
        # Get the names of the output layers, i.e. the layers with unconnected outputs
        layer_list = [layers_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        return layer_list

    def detect(self, frame: numpy.ndarray):
        """
        perform detection on given frame and return bounding boxes
        :param frame: frame to be detected
        :return: bounding boxes for detection
        """
        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.get_layer_names())
        result = post_process(frame, outs)
        return result