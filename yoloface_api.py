# *******************************************************************
#
# Author : Thanh Nguyen, 2018
# Email  : sthanhng@gmail.com
# Github : https://github.com/sthanhng
#
# BAP, AI Team
# Face detection using the YOLOv3 algorithm
#
# Description : yoloface.py
# The main code of the Face detection using the YOLOv3 algorithm
#
# *******************************************************************


import os

from yolo_utils import *

#####################################################################


#####################################################################
# print the arguments
# print('----- info -----')
# print('[i] The config file: ', args.model_cfg)
# print('[i] The weights of model file: ', args.model_weights)
# print('[i] Path to image file: ', args.image)
# print('[i] Path to video file: ', args.video)
# print('###########################################################\n')

def load_args_and_model(model_cfg: str, model_weights: str, output_dir: str):

    # check outputs directory
    if not os.path.exists(output_dir):
        print('==> Creating the {} directory...'.format(output_dir))
        os.makedirs(output_dir)
    else:
        print(
            '==> Skipping create the {} directory...'.format(output_dir))

    # Give the configuration and weight files for the model and load the
    # network using them.
    net = cv2.dnn.readNetFromDarknet(model_cfg, model_weights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    return net


def _main(model_cfg: str, model_weights: str, output_dir: str, image=None,
          video=None, src=None):
    if not image and not video and not src:
        return False
    wind_name = 'Detection using YOLOv3'
    cv2.namedWindow(wind_name, cv2.WINDOW_NORMAL)
    net = load_args_and_model(model_cfg, model_weights, output_dir)
    output_file = ''
    identify_flag = False

    if image:
        if not os.path.isfile(image):
            print("[!] ==> Input image file {} doesn't exist".format(image))
            return False
        cap = cv2.VideoCapture(image)
        output_file = image[:-4].rsplit('/')[-1] + '_yoloface.jpg'
    elif video:
        if not os.path.isfile(video):
            print("[!] ==> Input video file {} doesn't exist".format(video))
            return False
        cap = cv2.VideoCapture(video)
        output_file = video[:-4].rsplit('/')[-1] + '_yoloface.avi'
    else:
        # Get data from the camera
        cap = cv2.VideoCapture(src)

    # Get the video writer initialized to save the output video
    if not image:
        video_writer = cv2.VideoWriter(os.path.join(output_dir, output_file),
                                       cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                       cap.get(cv2.CAP_PROP_FPS), (
                                           round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                           round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    while True:

        has_frame, frame = cap.read()

        # Stop the program if reached end of video
        if not has_frame:
            print('[i] ==> Done processing!!!')
            print('[i] ==> Output file is stored at', os.path.join(output_dir, output_file))
            cv2.waitKey(1000)
            break

        # Create a 4D blob from a frame.
        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (IMG_WIDTH, IMG_HEIGHT),
                                     [0, 0, 0], 1, crop=False)

        # Sets the input to the network
        net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        outs = net.forward(get_outputs_names(net))

        # Remove the bounding boxes with low confidence
        faces = post_process(frame, outs, CONF_THRESHOLD, NMS_THRESHOLD)
        if len(faces) > 0:
            identify_flag = True
        print('[i] ==> # detected persons: {}'.format(len(faces)))
        print('#' * 60)

        # initialize the set of information we'll displaying on the frame
        info = [
            ('number of persons detected', '{}'.format(len(faces)))
        ]

        for (i, (txt, val)) in enumerate(info):
            text = '{}: {}'.format(txt, val)
            cv2.putText(frame, text, (10, (i * 20) + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_RED, 2)

        # Save the output video to file
        if image:
            cv2.imwrite(os.path.join(output_dir, output_file), frame.astype(np.uint8))
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

