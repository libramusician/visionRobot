# Initialize the parameters
import cv2 as cv
import numpy as np

from boundingBox import BoundingBox

confThreshold = 0.5  # Confidence threshold
nmsThreshold = 0.4  # Non-maximum suppression threshold
inpWidth = 416  # Width of network's input image
inpHeight = 416  # Height of network's input image
counter = 0


# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    list = [layersNames[i - 1] for i in net.getUnconnectedOutLayers()]
    #  print(list)
    return list


# def drawPred(classId, conf, left, top, right, bottom):
#     # Draw a bounding box.
#     cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)
#
#     label = '%.2f' % conf
#
#     # Get the label for the class name and its confidence
#     if classes:
#         assert (classId < len(classes))
#         label = '%s:%s' % (classes[classId], label)
#
#     # Display the label at the top of the bounding box
#     labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
#     top = max(top, labelSize[1])
#     cv.rectangle(frame, (left, top - round(1.5 * labelSize[1])), (left + round(1.5 * labelSize[0]), top + baseLine),
#                  (255, 255, 255), cv.FILLED)
#     cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)


# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs):
    result_boxes = []
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            # print(detection)
            scores = detection[5:]
            #  print(scores)
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        bbox = BoundingBox()
        bbox.set_xywh(left, top, width, height)
        result_boxes.append(bbox)
        # drawPred(classIds[i], confidences[i], left, top, left + width, top + height)
    return result_boxes


def detect(frame):
    blob = cv.dnn.blobFromImage(frame, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)
    net.setInput(blob)
    outs = net.forward(getOutputsNames(net))
    result = postprocess(frame, outs)
    # t, _ = net.getPerfProfile()
    # label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
    # cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
    return result



