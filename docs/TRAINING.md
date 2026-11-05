# Training

The model behind ArSL Recognition, how it was trained and how to retrain it. For the dataset itself, see [DATASET.md](DATASET.md).

## Model

| | |
|---|---|
| Architecture | YOLO26s (Ultralytics), ~22M parameters |
| Base weights | `yolo26s.pt` (pretrained, downloaded automatically by Ultralytics) |
| Task | Object detection: one bounding box per hand, labeled with one of 32 letter classes |
| Input size | 640 × 640 |
| Output weights | `runs/train/arsl21l/weights/best.pt` |

## Training setup

From [`runs/train/arsl21l/args.yaml`](../runs/train/arsl21l/args.yaml):

| Parameter | Value |
|---|---|
| Epochs | 50 |
| Batch size | 16 |
| Image size | 640 |
| Optimizer | `auto` (chosen by Ultralytics) |
| Initial learning rate | 0.01 |
| Device | GPU 0 |

## Results

Validation metrics from [`results.csv`](../runs/train/arsl21l/results.csv):

| Metric | Final epoch (50) | Best epoch (35) |
|---|:---:|:---:|
| Precision | 96.3% | 97.3% |
| Recall | 95.5% | 95.6% |
| mAP@50 | 96.7% | 97.7% |
| mAP@50–95 | 83.6% | 84.6% |

The training curves, confusion matrices and precision–recall curves are in [`runs/train/arsl21l/`](../runs/train/arsl21l/):

<p align="center">
  <img src="../runs/train/arsl21l/results.png" width="720" alt="Training and validation loss and metric curves">
</p>

<p align="center">
  <img src="../runs/train/arsl21l/confusion_matrix_normalized.png" width="600" alt="Normalized confusion matrix for the 32 classes">
</p>

## Retraining

1. Get the dataset in YOLO format: an `images/` folder, a matching `labels/` folder of `.txt` box files, and `train.txt` / `val.txt` lists of image paths.
2. Set `path` in [`config/data.yaml`](../config/data.yaml) to the dataset folder. `train` and `val` are resolved relative to it.
3. Adjust the constants at the top of [`src/train.py`](../src/train.py) if needed:

   ```python
   EPOCHS     = 50          # increase to 100 for better accuracy
   BATCH_SIZE = 16          # reduce to 8 if the GPU runs out of memory
   IMG_SIZE   = 640
   MODEL      = "yolo26s"   # yolo26n = fastest, yolo26s = balanced, yolo26m/l/x = larger
   DEVICE     = 0           # 0 = first GPU, "cpu" to force CPU
   ```

4. Run:

   ```bash
   python src/train.py
   ```

The new weights are written to `runs/train/arsl21l/weights/best.pt` (best epoch) and `last.pt` (final epoch). The app loads `best.pt` automatically. `last.pt` and the batch preview images are not committed to the repository. Training on a CPU works but is very slow.
