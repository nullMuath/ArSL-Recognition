# Configuration

How to change ArSL Recognition's settings, run on CPU or GPU, add letters and build a Windows executable. For setup, see the [README](../README.md).

## Settings

Settings are constants near the top of [`App.py`](../App.py). Restart the app after changing them.

```python
WEIGHTS  = resource_path("runs/train/arsl21l/weights/best.pt")  # model file
IMG_SIZE = 640     # inference size in pixels
CONF     = 0.45    # minimum confidence for a detection (0–1)
DEVICE   = 0       # 0 = first NVIDIA GPU, "cpu" = CPU only
```

| Setting | Default | Description |
|---|---|---|
| `WEIGHTS` | `runs/train/arsl21l/weights/best.pt` | Path to the YOLO weights the app loads |
| `IMG_SIZE` | `640` | Input size for inference. It should match the training size |
| `CONF` | `0.45` | Detections below this confidence are ignored. Raise it to reduce false positives, or lower it to catch weaker signs |
| `DEVICE` | `0` | Inference device: a GPU index, or `"cpu"` |
| `HAND_SIGNS_DIR` | `hand_signs/` | Folder of reference hand-sign images |
| `SOUNDS_DIR` | `assets/sounds/` | Folder of pronunciation audio |

The camera is chosen in the app's **Settings** dialog (gear icon), not in code.

## CPU or GPU

`DEVICE = 0` needs an NVIDIA GPU and a CUDA build of PyTorch. The project's `pyproject.toml` installs PyTorch from the CUDA 12.8 index, so `uv sync` sets this up for you.

On a machine without a supported GPU, set:

```python
DEVICE = "cpu"
```

| Device | Typical speed |
|---|---|
| CPU | ~15–30 FPS, depending on the processor |
| NVIDIA GPU | ~60+ FPS |

## Adding or changing letters

Each letter is identified by its **key**, the class name the model predicts (for example `meem`). Everything else is looked up by that key.

1. **Model:** add the class to `names` in [`config/data.yaml`](../config/data.yaml), label your images and retrain. See [TRAINING.md](TRAINING.md).
2. **Text:** add an entry to `LETTER_DATA` in `App.py`:

   ```python
   "meem": {
       "arabic":   "م",
       "name_en":  "Meem",
       "name_ar":  "الميم",
       "phonetic": "M – eem",
       "desc_en":  "Close the hand into a fist and point\nthe index finger straight downward.",
       "desc_ar":  "إغلاق قبضة اليد بالكامل وتوجيه السبابة بشكل مستقيم للأسفل",
   },
   ```

3. **Hand-sign image:** save it as `hand_signs/{key}_arsl.png`. A square PNG works best, since it's shown at 116 × 116.
4. **Audio:** save it as `assets/sounds/{key}_arsl.mp3` (`.wav` and `.ogg` also work). `src/LettersGenerator.py` can generate these with Google Text-to-Speech:

   ```bash
   pip install gTTS
   python src/LettersGenerator.py
   ```

`al`, `la`, `toot` and `yaa` don't have hand-sign images yet, so the panel shows a placeholder tile for them.

## Building the Windows executable

The app is packaged with PyInstaller using [`App.spec`](../App.spec), which bundles `assets/`, `hand_signs/`, `runs/`, `config/` and `src/`.

```bash
pip install pyinstaller
pyinstaller App.spec
```

The result is `dist/ArSL_Recognition/ArSL_Recognition.exe`. Ship the whole `dist/ArSL_Recognition/` folder, since the executable depends on the files next to it. Paths are resolved through `resource_path()`, so the app finds its bundled files both from source and from the build.
