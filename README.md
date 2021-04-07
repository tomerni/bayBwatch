# bayBwatch

## Usage

* Clone this repository
```bash
$ git clone https://github.com/tomerni/bayBwatch
```

* Download the weights files:
>** yolov3-tiny weights**
>https://drive.google.com/file/d/1_XixOaRpi26B-3ykxQBBwp02Uk5CZ5O7/view?usp=sharing

>** yolov3-face weights**
>https://drive.google.com/file/d/1YFOxAtOH6Xa-1VuIJIdRsWAZxsj6rhuO/view?usp=sharing

* Install requirements:
 ```bash
$ pip install -r requirements.txt
```

### API usage:

* Run the function _main() in yoloface_api.py:
```bash
def _main(model_cfg: str, model_weights: str, output_dir: str, image="", video="", src=None):
```
* Supply the relevant config and weights (See CLI usage for more information about the detection types).
* Must supply image path/video path/src=1(webcam)

### CLI usage:

* For body detection run the following command (change the IMG_PATH/VIDEO_PATH):

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
$ python yoloface.py --model-cfg "./cfg/yolov3-tiny.cfg" --model-weights "./model-weights/yolov3-tiny.weights" --src 0 --output-dir outputs/
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
$ python yoloface.py --model-cfg "./cfg/yolov3-face.cfg" --model-weights "./model-weights/yolov3-wider_16000.weights" --src 0 --output-dir outputs/
```

### Flags explanation
* --model-cfg - yolov3 config path
* --model-weights - yolov3 weights path
* --image/video - image/video path
* --src - 0 for webcam
* --output-dir - the output's path
