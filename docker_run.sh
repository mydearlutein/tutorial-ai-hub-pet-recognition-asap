#!/bin/bash

docker run -it --gpus '"device=0"' --name pet-recog-demo -v `pwd`:/workspace nvcr.io/nvidia/pytorch:22.12-py3 /bin/bash