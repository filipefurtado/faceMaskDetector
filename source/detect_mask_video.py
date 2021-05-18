from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from datetime import datetime
from auxiliar import alerts
import numpy as np
import cv2
import os
# ================================================================= #
def detect_and_predict_mask(frame, faceNet, maskNet):

  (h, w) = frame.shape[:2]
  blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

  faceNet.setInput(blob)
  detections = faceNet.forward()

  faces = []
  locs = []
  preds = []

  for i in range(0, detections.shape[2]):

    confidence = detections[0, 0, i, 2]

    if confidence > 0.5:

      box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
      (startX, startY, endX, endY) = box.astype("int")

      (startX, startY) = (max(0, startX), max(0, startY))
      (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

      face = frame[startY:endY, startX:endX]
      face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
      face = cv2.resize(face, (224, 224))
      face = img_to_array(face)
      face = preprocess_input(face)

      faces = []
      faces.append(face)
      locs.append((startX, startY, endX, endY))

      if len(faces) > 0:

        faces = np.array(faces, dtype="float32")
        preds.append(maskNet.predict(faces, batch_size=32))

  return (locs, preds)

# ================================================================= #
def startFaceDetection(root, userData):

  prototxtPath = os.path.join(os.path.dirname(__file__), 'face_detector', 'deploy.prototxt')
  weightsPath = os.path.join(os.path.dirname(__file__), 'face_detector', 'res10_300x300_ssd_iter_140000.caffemodel')
  faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
  maskNet = load_model(os.path.join(os.path.dirname(__file__), 'mask_detector.model'))

  camera = cv2.VideoCapture(0)
  root.withdraw()

  lastTime = datetime.now()

  while True:

    try:
      _, frame = camera.read()

      try:
        (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)
      except Exception:
        locs = [(0, 0, 0, 0)]
        preds = [[0, 0]]

      if len(preds) > 0:
        peopleWithoutMask = 0  
        for (box, pred) in zip(locs, preds):

          (startX, startY, endX, endY) = box
          (mask, withoutMask) = pred[0]

          label = "Mask" if mask > withoutMask else "No Mask"
          color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

          label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

          cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
          cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
          cv2.putText(frame, "To close this window, press 'Q' on your keyboard!", (15, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.80, (0, 255, 0), 2)
          cv2.imshow("Face Mask Detector - Version 1.0", frame)

          if "No Mask" in label:
            peopleWithoutMask += 1

        if userData != {}:
          if userData['alertStatus'] and peopleWithoutMask != 0:
              diffTime = (datetime.now() - lastTime).total_seconds() / 60

              if int(userData['alertTime']) == 1:
                if diffTime > 5:
                  alerts.sendMessage(userData['emailUser'], userData['cameraName'], peopleWithoutMask)
                  lastTime = datetime.now()
              elif int(userData['alertTime']) == 2:
                if diffTime > 10:
                  alerts.sendMessage(userData['emailUser'], userData['cameraName'], peopleWithoutMask)
                  lastTime = datetime.now()
              elif int(userData['alertTime']) == 3:
                if diffTime > 15:
                  alerts.sendMessage(userData['emailUser'], userData['cameraName'], peopleWithoutMask)
                  lastTime = datetime.now()
              elif int(userData['alertTime']) == 4:
                if diffTime > 30:
                  alerts.sendMessage(userData['emailUser'], userData['cameraName'], peopleWithoutMask)
                  lastTime = datetime.now()
              elif int(userData['alertTime']) == 5:
                if diffTime > 60:
                  alerts.sendMessage(userData['emailUser'], userData['cameraName'], peopleWithoutMask)
                  lastTime = datetime.now()

      else:
        cv2.putText(frame, "To close this window, press 'Q' on your keyboard!", (15, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.80, (0, 255, 0), 2)
        cv2.imshow("Face Mask Detector - Version 1.0", frame)

      key = cv2.waitKey(1) & 0xFF

      if key == ord("q"):
        break

    except Exception:
      pass

  camera.release()
  cv2.destroyAllWindows()

# ================================================================= #