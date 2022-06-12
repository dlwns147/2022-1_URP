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
--continue_train
# --checkpoints_dir='/media/data1/sangjun/urp22/checkpoints' \
# --checkpoints_dir='./checkpoints' \