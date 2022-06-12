python val.py \
--dat data/vfp.yaml \
--weights /home/sangjun/yolov5/runs/train/vfp_mixed2/weights/epoch29.pt \
--img-size 1280 \
--batch-size 32 \
--task val \
--device "0,1,2,3" \
--name vfp_mixed \
# --weights /home/sangjun/yolov5/runs/train/vfp_rain18/weights/epoch29.pt \