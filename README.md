# 반려동물 행동 구분 영상 데이터셋을 활용한 학습 환경 구성

## Fork history
원본 repository를 AI Hub 데이터를 연결해 실행을 편하게 하기 위해 Fork 했습니다.<br>
개인적인 학습의 용도로 사용할 예정입니다. 원작자 분들 감사합니다.<br>
<br>

## Prerequisite
설치가 필요한 Linux 패키지는 [VM에 필요한 ubuntu 패키지 설치 가이드](./VM-INSTALL.md)에 설치 방법을 작성하였습니다. 

- NVIDIA GPUs : GPU memory 14GB 이상 (최소 Tesla T4)
- NVIDIA Drivers : 450.51 (or later R450), 470.57 (or later R470), 510.47 (or later R510), or 515.65 (or later R515)
- Docker : 최신 버전 설치
- AI Hub 데이터셋 [반려동물 구분을 위한 동물 영상](https://aihub.or.kr/aidata/34146) 다운로드 (강아지 기준 약 45GB 이상의 디스크 공간 필요)
<br>

## Structure
```
tutorial-ai-hub-pet-recognition-asap
│  .gitignore
│  docker_run.sh        // Docker 기반 학습환경 실행 파일
│  README.md
│
├─data                 // AI허브에서 다운받은 영상별 라벨 json 파일 위치
│    ... <하단 데이터 사전 작업 참고>
│
├─demo
│    ... <각 디렉토리 README.md 참고>
│
├─HRNet
│    ... <각 디렉토리 README.md 참고>
│
├─KeypointRCNN
│    ... <각 디렉토리 README.md 참고>
│      
└─ST-GCN
      ... <각 디렉토리 README.md 참고>
```
<br>

## 데이터 폴더 구성
다운로드 받은 데이터셋 중 `[원본] 데이터셋 zip` 파일은 `data/<training 또는 validation>/image` 폴더에, `[라벨] 데이터셋 zip` 파일은 `data/<training 또는 validation>/label` 폴더로 각각 이동해 압축을 해제한다.
해제한 후 data 폴더의 모습은 아래와 같이 구조를 가진다.
  ```
  tutorial-ai-hub-pet-recognition-asap
  ├─data
  │    ├─training
  │    │    ├─image
  │    │    │    ├─BODYLOWER
  │    │    │    ├─BODYSCRATCH
  │    │    │    ├─BODYSHAKE
  │    │    │    ├─FEETUP
  │    │    │    ├─FOOTUP
  │    │    │    ├─HEADING
  │    │    │    ├─LYING
  │    │    │    ├─MOUNTING
  │    │    │    ├─SIT
  │    │    │    ├─TAILING
  │    │    │    ├─TAILLOW
  │    │    │    ├─TURN
  │    │    │    └─WALKRUN
  │    │    │ 
  │    │    └─label
  │    │          └─(training/image 와 동일 폴더 반복)
  │    │
  │    └─validation
  │          ├─image
  │          │    └─(training/image 와 동일 폴더 반복)
  │          │ 
  │          └─label
  │               └─(training/image 와 동일 폴더 반복)
  ...
  ```
<br>

## 학습 환경 기동
1. **Docker container 기동** <br>
  docker container 기동을 위한 bash script를 실행한다.
    ```bash
    chmod +x docker_run.sh
    sh docker_run.sh
    ```
<br>

2. 스크립트 실행에 성공하면, docker container 내 /workspace 위치에 있게 된다.
<br>


## 데이터 전처리
1. Keypoint 감지 모델 (KeypointRCNN) 학습을 위한 데이터셋 구조로 변경하기 위해 아래와 같이 코드를 실행한다. 
    ```bash
    cd data
    python data_formmatter.py
    ```
<br>

2. **전처리 파일 확인**<br>
  data 폴더 내에 `data_annotaion.csv` 파일이 생성되었는지 확인한다. 
<br>


## Demo 서비스 기동
Demo 서비스를 기동하기 위해서는 필요한 Python package 설치 후, 먼저 전처리한 데이터셋을 가지고 Keypoint 감지 모델을 학습해야 한다. <br>
설치 대상 라이브러리는 demo/requirements.txt에 작성되어 있다.

1. **Python package 설치**<br>
    ```bash
    pip install -r demo/requirements.txt
    ```

2. **Keypoint 감지 모델 학습**<br>
    ```bash
    cd KeypointRCNN
    python train.py
    ```

3. **테스트 데이터 셋팅**<br>
    테스트 방식은 2가지를 제공한다.

    - 반려동물 영상을 Frame image로 변환해 테스트 하는 방법
    - 미리 Frame image로 변환한 폴더를 확보해 테스트 하는 방법 <br>
    <br>
  
    Demo 시연용으로 테스트할 데이터셋은 `test` 폴더에 위치 시킨다. <br>
    예를 들면, 학습에 사용되지 않은 AI Hub의 validation 영상 `20201117-dog-walkrun-002943`을 테스트 하고자 한다면, 아래와 같이 위치 시킨다. 영상이 없는 경우에는 프레임 이미지 폴더만 위치시켜도 무방하다. 

      ```
      tutorial-ai-hub-pet-recognition-asap
      ├─test
      │    ├─20201117-dog-walkrun-002943.mp4    // 테스트 영상
      │    │
      │    └─20201117-dog-walkrun-002943        // 영상에 대한 프레임 이미지 폴더
      │          ├─ frame_0_timestamp_0.jpg  
      │          └─ ...
      ...
      ```

4. **Demo 테스트**<br>
    ```bash
    # CLI 상에서 테스트
    cd demo
    python test_final.py recognition -c work_dir/stgcn_demo.yaml
    ```


<br>
<br>

# ASAP: AI State Analysis of Pets 🐾
Analysis of Pets Using Keypoint Detection and Skeleton-Based Action Recognition.<br>
(2021.07.05~2021.08.23)

## Overview
ASAP(AI State Analysis of Pets)는 반려동물의 행동을 분석해주는 서비스입니다. <br>

본 프로젝트의 목표는 국내에서 양육되는 다양한 개의 품종에 대해 행동을 분석하는 범용적인 모델을 제시하고, 최종적으로 영상 속 반려동물에 대해 10가지 행동 분석을 제공하는 서비스를 제작하는 것입니다. 행동 분석을 위해서는 먼저 반려동물을 촬영한 영상 속 반려동물의 관절 키포인트를 검출한 후, 관절 키포인트를 기반으로 형상한 반려동물의 뼈대를 통해 행동 유형을 분류합니다.<br>

반려동물을 담은 영상을 올릴 시 키포인트 인식을 기반으로 행동을 알려줍니다. 

## Data
AI-Hub에서 제공하는 [반려동물 구분을 위한 동물 영상](https://aihub.or.kr/aidata/34146) 데이터 중 개(반려견)의 데이터만을 사용하여 모델 학습을 진행하였습니다.<br>

Keypoint Detection 모델 학습시 영상 데이터(영상의 프레임 별 이미지)를, Action Recognition 모델 학습시 라벨 데이터를 사용하였으며 각 학습 데이터의 형식은 다음과 같습니다.
* **Keypoint Detection** <br>
  | Original | Keypoint | Label |
  | :------: | :------: | :---- |
  | <img width="250" alt="data-img" src="https://user-images.githubusercontent.com/63901494/129929470-e2def238-963b-42c8-98b6-59bb0ad3b4c6.jpg"> | <img width="250" alt="data-keypoint" src="https://user-images.githubusercontent.com/63901494/129929529-235d5f39-1ec5-4452-8299-490c84702ebf.png"> | 0: 코<br>1: 이마 정 중앙<br>2: 입꼬리(입끝)<br>3: 아래 입술 중앙<br>4: 목<br>5: 앞다리 오른쪽 시작<br>6: 앞다리 왼쪽 시작<br>7: 앞다리 오른쪽 발목<br>8: 앞다리 왼쪽 발목<br>9: 오른쪽 대퇴골<br>10: 왼쪽 대퇴골<br>11: 뒷다리 오른쪽 발목<br>12: 뒷다리 왼쪽 말목<br>13: 꼬리 시작<br>14: 꼬리 끝 |

  키포인트 감지 모델 학습을 위해서는 키포인트 좌표 데이터가 필요합니다. 다음과 같은 csv 파일 형식으로 이미지의 경로와 키포인트 정보를 구성해 주세요. <br>
  <img width="800" alt="data-csv" src="https://user-images.githubusercontent.com/63901494/129934622-ec6e8130-50de-4893-92d6-7d040220cac9.png">

* **Action Recognition** <br>
  행동 분류 모델의 학습을 위해서는 키포인트 좌표값과 각 포인트에 대한 confidence score, 영상의 라벨인 action class 정보가 필요합니다. 다음과 같은 형식의 json 파일을 각 영상에 대해 구성해 주세요.
  ```
  {
    "data":[
      {"frame_index":1, "skeleton":[
        {"pose":[x.xxx, x.xxx, x.xxx, ...],   // keypoint
         "score":[x.xxx, x.xxx, x.xxx, ...]   // confidence score
        }]
      },
      {"frame_index":2, "skeleton":[
        {"pose":[x.xxx, x.xxx, x.xxx, ...],
         "score":[x.xxx, x.xxx, x.xxx, ...]
        }]
      },
      ...,]
      "label": "걷거나 뜀",
      "label_index": 5
    ...
  }
  ```
  영상의 각 프레임별 스켈레톤 정보로부터 '앉기', '두 앞발을 들어 올림', '앞발 하나를 들어 올림', '몸을 턴다', '엎드리기', '걷거나 뜀', '꼬리를 위로 올리고 흔듦', '빙글빙글 돈다', '마운팅', '꼬리가 아래로 향함' 과 같은 행동 분류를 진행하였습니다. 

## Models
* [Keypoint Detection] **Keypoint RCNN** - [Mask-RCNN, 2017 (Kaiming He, Georgia Gkioxari, Piotr Dollár, Ross Girshick)](https://arxiv.org/pdf/1703.06870v3.pdf)
* [Keypoint Detection] **HRNet** - [Deep High-Resolution Representation Learning for Visual Recognition, 2019 (Jingdong Wang, Ke Sun, Tianheng Cheng, Borui Jiang, Chaorui Deng, Yang Zhao, Dong Liu, Yadong Mu, Mingkui Tan, Xinggang Wang, Wenyu Liu, Bin Xiao)](https://arxiv.org/pdf/1908.07919.pdf)
* [Action Recognition] **ST-GCN** - [Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action Recognition, 2018 (Sijie Yan, Yuanjun Xiong, Dahua Lin)](https://arxiv.org/pdf/1801.07455.pdf)

해당 모델들은 모두 Pytorch 프레임워크를 사용하여 학습하였습니다. 

<!--
**Flowchart** <br>
<img width="500" alt="tech stack" src="https://user-images.githubusercontent.com/63901494/129585982-4705c85e-c81b-4b97-87ef-20a37119d999.png"> 
-->

## Usage
학습시 모델의 용량 문제로 인해 GPU 환경에서 실행하기를 권장합니다. <br>
Google Colab을 활용할 시 [런타임] - [런타임 유형 변경] - [GPU]로 설정을 바꿔주세요.
### 1. Installation
```
git clone https://github.com/Taehee-K/ASAP.git
cd ASAP
```
### 2. Train
[Keypoint RCNN](./KeypointRCNN)
```
cd KeypointRCNN
pip install -r requirements.txt
python train.py
```
[HRNet](./HRNet)
```
cd HRNet
pip install -r requirements.txt
python train.py
```
[ST-GCN](./ST-GCN)
```
cd ST-GCN
pip install -r requirements.txt
python torchlight/setup.py install
python main.py recognition -c config/st_gcn/kinetics-skeleton/train.yaml --device 0
```
### 3. Inference
```
cd demo
pip install -r requirements.txt
python torchlight/setup.py install

// Test
python test_final.py recognition -c work_dir/stgcn_demo.yaml

// Streamlit Demo
streamlit run app.py
```

## Result
Streamlit 라이브러리를 통해 서비스 프로토타입을 제작하였습니다. <br>

<img width="600" alt="demo-streamlit" src="https://user-images.githubusercontent.com/63901494/130213347-a7735515-7440-4a09-8431-60786c1818ac.gif">

## Reference
* [pytorch/vision](https://github.com/pytorch/vision)
* [yysijie/st-gcn](https://github.com/yysijie/st-gcn)
* [leoxiaobin/deep-high-resolution-net.pytorch](https://github.com/leoxiaobin/deep-high-resolution-net.pytorch)
* [MaiHon/dacon-motion-keypoints](https://github.com/MaiHon/dacon-motion-keypoints)

## Contributors
<table>
  <tr>
    <td align="center"><a href="https://github.com/treblenalto"><img src="https://user-images.githubusercontent.com/63901494/129619988-1a959834-313c-443c-84c2-4fc2db8ef8f6.jpg" width="100" height="100"><br /><sub><b>김태희</b></sub></td>
    <td align="center"><a href="https://github.com/wonjae-yang"><img src="https://user-images.githubusercontent.com/63901494/129583717-42d19759-7586-4de0-aea9-5e935295f4dd.png" width="100" height="100"><br /><sub><b>양원재</b></sub></td>
    <td align="center"><a href="https://github.com/SK-jeong"><img src="https://user-images.githubusercontent.com/63901494/129582209-1d1d194e-cf3e-48d6-b097-35a7b855a683.jpg" width="100" height="100"><br /><sub><b>정성경</b></sub></td>
    <td align="center"><a href="https://github.com/miso-choi"><img src="https://user-images.githubusercontent.com/78155086/132087934-79862c4f-7076-4e2c-907b-a456d6980b90.jpeg" width="100" height="100"><br /><sub><b>최미소</b></sub></td>
    <td align="center"><a href="https://github.com/HwangChaewon"><img src="https://user-images.githubusercontent.com/63901494/129582279-430df734-43ae-451a-991d-7bb62a170eb0.png" width="100" height="100"><br /><sub><b>황채원</b></sub></td>
    <td align="center"><a href="https://github.com/HyeJung-Hwang"><img src="https://user-images.githubusercontent.com/63901494/129582233-ccf2137f-89db-4559-9bc3-be23a133e2a3.png" width="100" height="100"><br /><sub><b>황혜정</b></sub></td>
  </tr>
</table>
