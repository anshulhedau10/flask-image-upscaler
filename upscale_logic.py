
import cv2
from cv2 import dnn_superres
from pathlib import Path

base_path = Path(__file__).parent

def imageUpscale(input_filename, result_filename, file_ext):

    # Create an SR object
    sr = dnn_superres.DnnSuperResImpl_create()

    # Read image
    image = cv2.imread('./static/data/' + str(input_filename + file_ext))

    # Read the desired model
    path = "./model/EDSR_x3.pb"
    sr.readModel(path)

    # # Set CUDA backend and target to enable GPU inference
    # sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    # sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)


    # Set the desired model and scale to get correct pre- and post-processing
    sr.setModel("edsr", 3)

    # Upscale the image
    result = sr.upsample(image)

    # Save the image
    cv2.imwrite('./static/data/' + str(result_filename + file_ext), result)

