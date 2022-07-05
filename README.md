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
