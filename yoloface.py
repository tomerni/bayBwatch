# *******************************************************************
#
# Author : Thanh Nguyen, 2018
# Editor: Tomer Nissim, 2021
# Email  : tomernissim@gmail.com
# Github : https://github/tomerni

# Description : yoloface.py
# The main code of the Face detection using the YOLOv3 algorithm
#
# *******************************************************************


import argparse
import sys
import os

from utils import *

#####################################################################


#####################################################################
# print the arguments
# print('----- info -----')
# print('[i] The config file: ', args.model_cfg)
# print('[i] The weights of model file: ', args.model_weights)
# print('[i] Path to image file: ', args.image)
# print('[i] Path to video file: ', args.video)
# print('###########################################################\n')

FULL_CFG_PATH = "./cfg/yolov3-spp.cfg"
FULL_WEIGHTS_PATH = "./model-weights/yolov3-spp.weights"


def load_args_and_model():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-cfg', type=str,
                        default='./cfg/yolov3-face.cfg',
                        help='path to config file')
    parser.add_argument('--model-weights', type=str,
                        default='./model-weights/yolov3-wider_16000.weights',
                        help='path to weights of model')
    parser.add_argument('--image', type=str, default='',
                        help='path to image file')
    parser.add_argument('--video', type=str, default='',
                        help='path to video file')
    parser.add_argument('--src', type=int, default=0,
                        help='source of the camera')
    parser.add_argument('--output-dir', type=str, default='outputs/',
                        help='path to the output directory')
    args = parser.parse_args()

    # check outputs directory
    if not os.path.exists(args.output_dir):
        print('==> Creating the {} directory...'.format(args.output_dir))
        os.makedirs(args.output_dir)
    else:
        print(
            '==> Skipping create the {} directory...'.format(args.output_dir))

    # Give the configuration and weight files for the model and load the network
    # using them.
    face_net = cv2.dnn.readNetFromDarknet(args.model_cfg, args.model_weights)
    face_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    face_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    body_net = cv2.dnn.readNetFromDarknet(FULL_CFG_PATH, FULL_WEIGHTS_PATH)
    body_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    body_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    return face_net, body_net, args


def _main():
    wind_name = 'face detection using YOLOv3'
    cv2.namedWindow(wind_name, cv2.WINDOW_NORMAL)
    face_net, body_net, args = load_args_and_model()
    output_file = ''
    identify_flag = False

    if args.image:
        if not os.path.isfile(args.image):
            print("[!] ==> Input image file {} doesn't exist".format(args.image))
            sys.exit(1)
        cap = cv2.VideoCapture(args.image)
        output_file = args.image[:-4].rsplit('/')[-1] + '_yoloface.jpg'
    elif args.video:
        if not os.path.isfile(args.video):
            print("[!] ==> Input video file {} doesn't exist".format(args.video))
            sys.exit(1)
        cap = cv2.VideoCapture(args.video)
        output_file = args.video[:-4].rsplit('/')[-1] + '_yoloface.avi'
    else:
        # Get data from the camera
        cap = cv2.VideoCapture(args.src)

    # Get the video writer initialized to save the output video
    if not args.image:
        video_writer = cv2.VideoWriter(os.path.join(args.output_dir, output_file),
                                       cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                       cap.get(cv2.CAP_PROP_FPS), (
                                           round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                           round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    while True:

        has_frame, frame = cap.read()

        # Stop the program if reached end of video
        if not has_frame:
            print('[i] ==> Done processing!!!')
            print('[i] ==> Output file is stored at', os.path.join(args.output_dir, output_file))
            cv2.waitKey(1000)
            break

        # Create a 4D blob from a frame.
        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (IMG_WIDTH, IMG_HEIGHT),
                                     [0, 0, 0], 1, crop=False)

        # Sets the input to the network
        face_net.setInput(blob)
        body_net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        face_outs = face_net.forward(get_outputs_names(face_net))
        body_outs = body_net.forward(get_outputs_names(body_net))

        # Remove the bounding boxes with low confidence
        faces = post_process(frame, face_outs, CONF_THRESHOLD, NMS_THRESHOLD, True)
        bodies = post_process(frame, body_outs, CONF_THRESHOLD, NMS_THRESHOLD, False)
        if len(faces) > 0 and len(bodies) > 0:
            identify_flag = True

        # initialize the set of information we'll displaying on the frame
        # info = [
        #     ('number of faces detected', '{}'.format(len(faces)))
        # ]
        #
        # for (i, (txt, val)) in enumerate(info):
        #     text = '{}: {}'.format(txt, val)
        #     cv2.putText(frame, text, (10, (i * 20) + 20),
        #                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_RED, 2)

        # Save the output video to file
        if args.image:
            cv2.imwrite(os.path.join(args.output_dir, output_file), frame.astype(np.uint8))
        else:
            video_writer.write(frame.astype(np.uint8))

        cv2.imshow(wind_name, frame)

        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):
            print('[i] ==> Interrupted by user!')
            break

    cap.release()
    cv2.destroyAllWindows()

    print('==> All done!')
    print('***********************************************************')

    return identify_flag


if __name__ == '__main__':
    print(_main())
