## Requirements

python 3.6
mxnet 1.5.0
GlounCV 0.10.5
Numpy 1.16.6
opencv-python 3.3.1.11
Matplotlib 3.3.4
PyPNG 0.0.21

## Download models

You can checkout the pre-trained models in pretrained/\* branches.

## Run a cli-demo

Simplest:

```
python3 test.py /path/to/image
```

Details:

```
$ python3 test.py --help
usage: test.py [-h] [--dims DIMS] [--threshold THRESHOLD] [--plt_w PLT_W]
               [--plt_h PLT_H] [--seq_len SEQ_LEN] [--no_yolo] [--beam]
               [--beam_size BEAM_SIZE] [--device_id DEVICE_ID] [--gpu]
               IMG [IMG ...]

Start a ALPR tester.

positional arguments:
  IMG                   path of the image file[s]

optional arguments:
  -h, --help            show this help message and exit
  --dims DIMS           set the sample dimentions (default: 208)
  --threshold THRESHOLD
                        set the positive threshold (default: 0.9)
  --plt_w PLT_W         set the max width of output plate images (default:
                        144)
  --plt_h PLT_H         set the max height of output plate images (default:
                        48)
  --seq_len SEQ_LEN     set the max length of output sequences (default: 8)
  --no_yolo             do not extract automobiles using YOLOv3
  --beam                using beam search
  --beam_size BEAM_SIZE
                        set the size of beam (default: 5)
  --device_id DEVICE_ID
                        select device that the model using (default: 0)
  --gpu                 using gpu acceleration
```

## Run a demo server

Simplest:

```
python3 server.py
```

Details:

```
$ python3 server.py --help
usage: server.py [-h] [--dims DIMS] [--threshold THRESHOLD] [--plt_w PLT_W]
                 [--plt_h PLT_H] [--seq_len SEQ_LEN] [--beam_size BEAM_SIZE]
                 [--no_yolo] [--addr ADDR] [--port PORT]
                 [--device_id DEVICE_ID] [--gpu]

Start a ALPR demo server.

optional arguments:
  -h, --help            show this help message and exit
  --dims DIMS           set the sample dimentions (default: 208)
  --threshold THRESHOLD
                        set the positive threshold (default: 0.9)
  --plt_w PLT_W         set the max width of output plate images (default:
                        144)
  --plt_h PLT_H         set the max height of output plate images (default:
                        48)
  --seq_len SEQ_LEN     set the max length of output sequences (default: 8)
  --beam_size BEAM_SIZE
                        set the size of beam (default: 5)
  --addr ADDR           set address of ALPR server (default: 0.0.0.0)
  --port PORT           set port of ALPR server (default: 80)
  --device_id DEVICE_ID
                        select device that the model using (default: 0)
  --gpu                 using gpu acceleration
```

## References

* [License Plate Detection and Recognition in Unconstrained Scenarios](http://sergiomsilva.com/pubs/alpr-unconstrained/)
* [Chinese City Parking Dataset](https://github.com/detectRecog/CCPD)
