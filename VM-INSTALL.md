# VM에 필요한 ubuntu 패키지 설치 가이드
신규 Linux 머신에 필요한 패키지 설치에 대한 가이드 파일입니다. <br>
설치 전에 **반드시** 설치 확인 명령어를 통해 설치된 버전이 있는지 먼저 확인한 후 설치가 되어 있지 않으면 설치를 진행합니다.<br>

- Git 
    ```bash
    # Git 설치 확인
    git --version

    # Git 설치
    sudo apt update
    sudo apt install git

    # Git 설치 재확인
    git --version
    ```

- Docker: Docker 설치 스크립트 `docker_install.sh` 파일을 실행한 후 편하게 실행하기 위해 몇가지 설정을 추가합니다.
    ```bash
    # Docker 설치 확인
    docker --version

    # Docker 설치
    sh docker_install.sh

    # Docker 설치 재확인
    docker --version

    # Docker 명렁어 테스트: Permission denied: /var/run/docker.sock 오류가 발생
    docker ps

    # 시스템 부팅 시 Docker 자동 실행 설정
    sudo systemctl enable docker 

    # Docker 실행 권한 추가 
    sudo chmod 666 /var/run/docker.sock
    sudo service docker restart

    # Docker 명렁어 테스트 
    docker ps
    ```

- NVIDIA Drivers
    1. Linux Debian 11 기준 (GCP VM 기본 설정)으로 [CUDA Toolkit Downloads](https://developer.nvidia.com/cuda-downloads) 페이지를 참고하였습니다.
        ```bash
        # NVIDIA Driver 설치 확인
        nvidia-smi

        # apt repository 설정
        sudo add-apt-repository contrib

        # 위 명령어에서 add-apt-repository가 없다고 나오면 아래 실행. 그렇지 않으면 skip해도 됨
        sudo apt-get -y install software-properties-common

        # NVIDIA Driver 설치 (network 모드)
        wget https://developer.download.nvidia.com/compute/cuda/repos/debian11/x86_64/cuda-keyring_1.1-1_all.deb
        sudo dpkg -i cuda-keyring_1.1-1_all.deb
        sudo apt-get update
        sudo apt-get -y install cuda

        # NVIDIA Driver 설치 재확인
        nvidia-smi
        ```

    2. Linux Ubuntu 20.04 기준 
        ```bash
        # NVIDIA Driver 설치 확인
        nvidia-smi

        # apt repository 설정
        sudo apt-get update && sudo apt-get upgrade
        ubuntu-drivers devices

        # 위 명령어에서 추천하는 driver 버전을 확인한 후 설치
        sudo apt install nvidia-driver-<버전>

        # VM 리부팅
        sudo reboot 

        # NVIDIA Driver 설치 재확인
        nvidia-smi
        ```


- Unzip
    ```bash
    # Unzip 설치 확인
    unzip

    # Unzip 설치
    sudo apt install unzip

    # Unzip 설치 재확인
    unzip
    ```
