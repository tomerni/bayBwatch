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
import time
from alarm import switch_alarm
from yolo_utils import *
from main import check_borders
from send_and_recive import get_string
#####################################################################


FULL_CFG_PATH = "./cfg/yolov3-tiny.cfg"
FULL_WEIGHTS_PATH = "./model-weights/yolov3-tiny.weights"
ADULT_CHILD_RATIO = 5.5
HEAD_PERCENTAGE = 0.75


# TODO:
#  create hot zones and manage them
#  merge the changes in the api file
#  counter for frames in which child in hot zone - it takes about
#  15 seconds to analyze 10 frames so if a child is in the hot zone for enough
#  time we will be able to detect him
#  need to figure out how to integrate with HELI

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

    net_load = time.time()

    face_net = cv2.dnn.readNetFromDarknet(args.model_cfg, args.model_weights)
    face_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    face_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    body_net = cv2.dnn.readNetFromDarknet("cfg/yolov3-tiny.cfg","model-weights/yolov3-tiny.weights")
    body_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    body_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    print("net loading time: {}".format(time.time() - net_load))

    return face_net, body_net, args



def get_cap_and_output(args):
    if args.image:
        if not os.path.isfile(args.image):
            print(
                "[!] ==> Input image file {} doesn't exist".format(args.image))
            sys.exit(1)
        cap = cv2.VideoCapture(args.image)
        output_file = args.image[:-4].rsplit('/')[-1] + '_yoloface.jpg'
    elif args.video:
        if not os.path.isfile(args.video):
            print(
                "[!] ==> Input video file {} doesn't exist".format(args.video))
            sys.exit(1)
        cap = cv2.VideoCapture(args.video)
        output_file = args.video[:-4].rsplit('/')[-1] + '_yoloface.avi'
    else:
        # Get data from the camera
        cap = cv2.VideoCapture(args.src)
        output_file = ''

    return cap, output_file


def analyze_objects_in_frame(faces_list, bodies_list):
    adult_in_frame_counter, child_in_frame_counter = 0, 0
    identify_flag, alarm_flag = False, False
    # any match
    if len(faces_list) > 0 and len(bodies_list) > 0:
        identify_flag = True
    # incompatible number of heads and bodies
    if len(faces_list) != len(bodies_list):
        print("Balagan")
        # continue
    else:
        for i in range(len(faces_list)):
            ratio = (bodies_list[i][0] + HEAD_PERCENTAGE * faces_list[i][0]) / \
                    faces_list[i][0]
            if ratio <= ADULT_CHILD_RATIO:
                child_in_frame_counter += 1
            else:
                adult_in_frame_counter += 1
            print("Body Head Ratio: {}".format(ratio))
    if child_in_frame_counter >= 1 and adult_in_frame_counter == 0:
        alarm_flag = True
    return identify_flag, alarm_flag


def _main():
    wind_name = 'face detection using YOLOv3'
    cv2.namedWindow(wind_name, cv2.WINDOW_NORMAL)
    load_time_start = time.time()
    face_net, body_net, args = load_args_and_model()
    print("loading time: {}".format(time.time() - load_time_start))
    cap_time_start = time.time()
    cap, output_file = get_cap_and_output(args)
    print("cap time: {}".format(time.time() - cap_time_start))
    child_in_zone = 0

    # Get the video writer initialized to save the output video
    if not args.image:
        video_writer = cv2.VideoWriter(
            os.path.join(args.output_dir, output_file),
            cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
            cap.get(cv2.CAP_PROP_FPS), (
                round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    while True:
        start = time.time()
        has_frame, frame = cap.read()
        faces_list, bodies_list = list(), list()
        hot_zones_list = [HotZone(100, 100, 200, 200, 2)]

        # Stop the program if reached end of video
        if not has_frame:
            print('[i] ==> Done processing!!!')
            print('[i] ==> Output file is stored at',
                  os.path.join(args.output_dir, output_file))
            cv2.waitKey(1000)
            break

        # Create a 4D blob from a frame.
        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (IMG_WIDTH, IMG_HEIGHT),
                                     [0, 0, 0], 1, crop=False)

        # Sets the input to the network
        face_net.setInput(blob)
        body_net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        forward_time = time.time()
        face_outs = face_net.forward(get_outputs_names(face_net))
        body_outs = body_net.forward(get_outputs_names(body_net))
        print("forwarding time: {}".format(time.time() - forward_time))
        # Remove the bounding boxes with low confidence and returns lists
        # with the bodies and faces in the frame
        post_process_time = time.time()
        post_process(frame, face_outs, CONF_THRESHOLD, NMS_THRESHOLD,
                     True, faces_list, bodies_list, hot_zones_list)
        post_process(frame, body_outs, CONF_THRESHOLD, NMS_THRESHOLD,
                     False, faces_list, bodies_list, hot_zones_list)
        print("post process time is: {}".format(post_process_time - time.time()));

    # sort the faces and bodies to find matches
        faces_list.sort(key=lambda x: x[1])
        bodies_list.sort(key=lambda x: x[1][0])

        identify_flag, alarm_flag = analyze_objects_in_frame(faces_list,
                                                             bodies_list)

        if not alarm_flag:
            child_in_zone = 0
            # TODO: need to receive coordinates of child in frame
        elif (child_in_zone) == 9: #and (check_borders([]))

            switch_alarm()
            print("ALARMMMMMM")  # NEED TO BE HELI
            child_in_zone = 0
        else:
            child_in_zone += 1

        # Save the output video to file
        saving_time = time.time()
        if args.image:
            cv2.imwrite(os.path.join(args.output_dir, output_file),
                        frame.astype(np.uint8))
        else:
            video_writer.write(frame.astype(np.uint8))
        print("saving time: {}".format(time.time() - saving_time))

        show_time = time.time()
        cv2.imshow(wind_name, frame)
        print("show time: {}".format(time.time() - saving_time))
        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):
            print('[i] ==> Interrupted by user!')
            break
        end = time.time()
        print("Time for round: {}".format(end - start))

        # check if a shutting down request was received:
        off_req = get_string()
        if off_req == "true":
            exit(1)
        # if the request is a number, turn off for this amount of minutes
        elif off_req.isnumeric():
            time.sleep(off_req)




    cap.release()
    cv2.destroyAllWindows()

    print('==> All done!')
    print('***********************************************************')


if __name__ == '__main__':
    print(_main())
