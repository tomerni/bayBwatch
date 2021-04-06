# bayBwatch

## Usage

* Clone this repository
```bash
$ git clone https://github.com/sthanhng/yoloface
```

* For body detection run the following command:

>**image input**
```bash
$ python yoloface.py --model-cfg "./cfg/yolov3-tiny.cfg" --model-weights "./model-weights/yolov3-tiny.weights" --image IMG_PATH --output-dir outputs/
```

>**video input**

```bash
$ python yoloface.py --model-cfg "./cfg/yolov3-tiny.cfg" --model-weights "./model-weights/yolov3-tiny.weights" --image VIDEO_PATH --output-dir outputs/
```

>**webcam**
```bash
$ python yoloface.py --model-cfg "./cfg/yolov3-tiny.cfg" --model-weights "./model-weights/yolov3-tiny.weights" --src 1 --output-dir outputs/
```

* For face detection run the following command:

>**image input**
```bash
$ python yoloface.py --model-cfg "./cfg/yolov3-face.cfg" --model-weights "./model-weights/yolov3-wider_16000.weights" --image IMG_PATH --output-dir outputs/
```

>**video input**

```bash
$ python yoloface.py --model-cfg "./cfg/yolov3-face.cfg" --model-weights "./model-weights/yolov3-wider_16000.weights" --image VIDEO_PATH --output-dir outputs/
```

>**webcam**
```bash
$ python yoloface.py --model-cfg "./cfg/yolov3-face.cfg" --model-weights "./model-weights/yolov3-wider_16000.weights" --src 1 --output-dir outputs/
```

## Flags explanation
* --model-cfg - yolov3 config path
* --model-weights - yolov3 weights path
* --image/video - image/video path
* --src - 1 for webcam
* --output-dir - the output's path
