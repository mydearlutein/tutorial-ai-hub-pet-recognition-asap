import os
import re

from rcnn import KeypointDataset, get_frame, get_video, collate_fn, pred_keypoints
from stgcn import match_format, MakeNumpy
import torch

#!/usr/bin/env python
import argparse
import sys
sys.path.append('./torchlight')

# torchlight
import torchlight
from torchlight import import_class

import warnings
warnings.filterwarnings('ignore')

if __name__ == "__main__":

    ### Keypoint Detection using RCNN
    if torch.cuda.is_available():
        DEVICE = torch.device('cuda')
    else:
        DEVICE = torch.device('cpu')
        print(DEVICE)

    # 테스트 방법 1) Video를 가지고 테스트하고 싶다면, 아래 get_video를 통해 frame image를 얻어야 함
    # video_path = '../test_video_wide.mp4'
    # frame_path= '../test'

    # if get_video(video_path, frame_path)==True:
    #     print('video successfully fetched!')

    # 테스트 방법 2) Frame만 가지고 테스트 - AI Hub에서 제공한 데이터 중 학습에 사용되지 않은 임의의 Frame image 경로 지정 
    test_path = '../data/validation/'
    frame_path = test_path + [name for name in os.listdir(test_path) if not os.path.isfile(name)][0]

    # Keypoint RCNN 모델명 확보
    model_dir = '../models'
    pattern = r'RCNN_ep5_[0-9]+.[0-9]+.pt'
    model_path = model_dir + [name for name in os.listdir(model_dir) if re.match(pattern, name)][0]

    pred_key = pred_keypoints(frame_path, model_path, DEVICE)

    ### Make input data for STGCN
    output_dict, folder_list = match_format(pred_key)

    sample = MakeNumpy(output_dict, folder_list)
    sample_total_npy = sample.fill_data_numpy()
    sample_tuple_pkl = sample.save_tuple_to_pkl()
    sample.save_total_npy()

    ### Action Recognition using STGCN
    parser = argparse.ArgumentParser(description='Processor collection')

    # region register processor yapf: disable
    processors = dict()
    processors['recognition'] = import_class('processor.recognition.REC_Processor')
  
    #endregion yapf: enable

    # add sub-parser
    subparsers = parser.add_subparsers(dest='processor')
    for k, p in processors.items():
        subparsers.add_parser(k, parents=[p.get_parser()])

    # read arguments
    arg = parser.parse_args()

    # start
    Processor = processors[arg.processor]
    p = Processor(sys.argv[2:])
    
    p.start()


