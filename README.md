# 2022-2_URP

## 1. Data augmentation with CycleGAN
##### CycleGAN source code : https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix
##### /data/unaligned_dataset.py 에서 dataset A, B의 경로를 먼저 수정한다.

### Training

```
python train.py \
--dataroot="" \
--name=leftImg8bit_rain \
--checkpoints_dir='/media/data1/sangjun/urp22/checkpoints' \
--gpu_ids="0,2,3" \
--batch_size=3 \
--netG=resnet_6blocks \
--preprocess=crop \
--crop_size=768 \
--suffix=crop768 \
--save_by_iter \
--save_epoch_freq=2000 \
--load_iter=865000 \
--lr_policy=step \
--lr=0.0001 \
--lr_decay_iters=200000 \
```

### Generating images

```
python test.py \
--dataroot="" \
--name=leftImg8bit_rain \
--gpu_ids="3" \
--batch_size=1 \
--netG=resnet_6blocks \
--preprocess=none \
--suffix=crop768 \
--load_iter=795000 \
--dataset_mode='unaligned' \
--model='cycle_gan' \
--checkpoints_dir='/media/data1/sangjun/urp22/checkpoints' \
--results_dir='/media/data1/sangjun/urp22/results' \
--eval \
--num_test=240
```

### 생성 예시

![image](https://user-images.githubusercontent.com/77950714/173223826-b52ba38f-d49d-474c-aa68-13d503dea7e6.png)
![image](https://user-images.githubusercontent.com/77950714/173223832-52f64153-47ea-41a3-a49c-a374f32ce697.png)
![image](https://user-images.githubusercontent.com/77950714/173223835-ee2a2d0d-d95e-4814-ab75-3479b57c8e65.png)


## 2. Object Detection with generated images

##### Yolo v5 source code : https://github.com/ultralytics/yolov5
##### /data/vfp.yaml을 수정하거나 또는 새로운 yaml 파일을 생성
##### 경로가 변경되었다면 /utils/datasets.py 의 img2label_paths 함수가 label을 생성하도록 변경

### Training
```
python train.py \
--dat data/vfp.yaml \
--cfg models/yolov5m.yaml \
--img 1280 \
--hyp data/hyps/hyp.scratch.yaml \
--batch-size 32 \
--weights yolov5m.pt \
--epochs 30 \
--device "0,1,2,3" \
--name vfp_mixed \
--noval \
--save-period 1
```

### Inference
```
python val.py \
--dat data/vfp.yaml \
--weights /home/sangjun/yolov5/runs/train/vfp_mixed2/weights/epoch29.pt \
--img-size 1280 \
--batch-size 32 \
--task val \
--device "0,1,2,3" \
--name vfp_mixed
```

### 실험 결과
![image](https://user-images.githubusercontent.com/77950714/173227351-a97e0a55-1b06-43f5-b7f1-f4cc287a5690.png)

실험 결과를 위의 표로 나타내었다. Normal VFP 290K의 테스트 셋으로 학습하였기에 Normal VFP 데이터셋으로 학습한 모델이 가장 우수한 성능을 보인다. 이후 Mixed VFP, Rain VFP 290K 데이터셋으로 학습한 모델이 순차적으로 성능을 보여주었다. Rain VFP 데이터 셋과 Mixed VFP 데이터셋은 mAP@.5의 성능이 Normal VFP 데이터셋에 비해 20.29%, 5.28%의 성능 감소를 보였다. 이는 Mixed VFP dataset을 사용하여도 일반적인 환경에서의 쓰러진 사람을 감지하는데 큰 영향을 미치지 않다는 점을 알 수 있다.

## 3. Simple FakeTagger implementation

![image](https://user-images.githubusercontent.com/77950714/173223624-f2afc2b4-500f-4ee2-81f2-11a7b1c0b4f4.png)

 FakeTagger는 총 5개의 module로 구성되어있다. 
 
 1. Message Generator는 0, 1로 이루어진 메시지에 redundant data를 추가한다.
 2. Image Encoder는 Message Generator가 생성해낸 redundant message를 input image에 삽입하고 원본 이미지(input image)와 구분이 안가는 embedded image를 생성해낸다. 
 3. GAN Simulator는 embedded image에 딥페이크를 적용하여 manipulated embedded image를 생성한다.
 4. Image Decoder는 image encoder에서 나온 embedded image 또는 GAN Simulator에서 나온 manipulated embedded image에서 redundant message를 추출해낸다.
 5. Message decoder는 image deocder가 추출해낸 redundant message에서 원본 message를 추출해낸다.
 
 이 중 image encoder, GAN simulator, image decoder 부분을 구현해보기로 하였다.
 
 ### Image Encoder, Decoder
 ![image](https://user-images.githubusercontent.com/77950714/173226563-75952226-d58b-4320-b3a8-b49b37f9af2b.png)

  - Image encoder는 입력으로 message와 image를 받아 둘을 결합하여 embedded image를 생성해내며 논문에서와 같이 U-Net 을 차용하였고 U-Net Decoder에서 U-Net Encoder의 feature map을 받을 때 메시지도 concatenation 하여 함께 들어간다.
  
  - Image decoder는 입력으로 image를 받아들여 message를 추출해내며 논문과 동일하게 7개의 Convolution layer를 쌓고 FC layer 에서 message 길이 만큼의 vector를 뽑아 sigmoid를 적용하였다.
 
 ![image](https://user-images.githubusercontent.com/77950714/173226674-ac13c08f-9a8a-416c-8862-282524e358f2.png)

### GAN Simulator
-  GAN Simulator 는 embedded image에 deepfake 를 적용하여 이미지를 manipulation 하며, 한 개의 Encoder와 두 개의 Decoder로 두 인물의 얼굴을 바꾸는 faceswap을 차용하였다.
-  Faceswap source : https://github.com/Oldpan/Faceswap-Deepfake-Pytorch

### Training

```
python train.py --batch_size 128 --name name
```

### Inference

```
python train.py --batch_size 128 --name name
```
 
 ### 생성 예시
 
 ![image](https://user-images.githubusercontent.com/77950714/173226638-e1ee9f6b-d5df-4a46-9b77-138a7d05b3ce.png)

![image](https://user-images.githubusercontent.com/77950714/173226646-2e10034c-a593-42a9-ae54-ff5c4cb1847e.png)


 ### 실험 결과
 
 #### 1) 𝜆 = 1, 𝛼 = 0.1
 ![image](https://user-images.githubusercontent.com/77950714/173226808-37daa08a-b233-49ce-aeb2-34a07351e9a4.png)

위의 표는 image encoder가 생성해낸 encoded (embedded) image와 GAN Simulator가 deepfake를적용한 manipulated encoded image에서 image decoder가 message를 얼마나 잘 추출하였는 지를 나타낸다. Image decoder는 encoded image, manipulated encoded image에서 대부분의 메시지를 잘 추출하였으며 딥페이크가 적용된 manipulated encoded image는 encoded image에 비해 4%의 성능 감소만 보여준다.

 ![image](https://user-images.githubusercontent.com/77950714/173226813-52a25ecc-56ca-402b-8174-058f1ed1a611.png)
 
위의 표는 image encoder가 생성해낸 embedded image가 원본 image와 얼마나 유사한 지를 나타낸다. 대체적으로 좋은 성능을 보이며 SSIM는 좋은 결과를 보이나 PSNR이 30에 조금 못 미치는 결과를 보여준다.

 #### 2) 𝜆 = 10, 𝛼 = 0.1
 ![image](https://user-images.githubusercontent.com/77950714/173226839-f26c00ce-b347-4392-adac-67fdab1ba600.png)

![image](https://user-images.githubusercontent.com/77950714/173226843-dc7677b7-264e-4cd0-9a75-571ba746ff56.png)

 𝜆가 너무 크면 image encoder는 noisy, 구분 가능한 이미지를 생성하는데, 위의 그림과 표는 𝜆 = 10, 𝛼 = 0.1 일 때 모델의 결과물과 message reconstruction accuracy를 나타낸다. 𝜆 값이 커짐에 따라 message reconstruction은 더 좋은 성능을 보이나 Image 유사도는 더 낮아진 것을 확인할 수가 있다.

 #### 3) 𝜆 = 1, 𝛼 = 0.5
 ![image](https://user-images.githubusercontent.com/77950714/173226866-6539001a-ee3a-4553-afa4-d227ebdc4e50.png)
 ![image](https://user-images.githubusercontent.com/77950714/173226869-7ade5cc2-2480-46e6-a4bb-6b3915197771.png)

 𝛼 값이 너무 크면 image decoder는 메시지를 추출할 수가 없는데, 위의 그림과 표는 𝜆 = 1, 𝛼 = 0.5 일 때 모델의 결과물과 message reconstruction accuracy를 나타낸다. 𝛼 값이 커짐에 따라 Image 유사도는 더 높아지나 message reconstruction은 성능이 감소한다.

