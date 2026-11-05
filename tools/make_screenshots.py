"""
Generate README screenshots without a webcam.

Feeds still photos into the real App.py window as if they were webcam
frames, runs the trained model on each one, and saves a PNG of the whole
window. Also writes an animated GIF that cycles through all of them.

Usage (from the repo root):
    python tools/make_screenshots.py photo1.jpg photo2.jpg ...
    python tools/make_screenshots.py path/to/folder_of_photos

Output goes to docs/screenshots/ unless --out is given.
"""

import argparse
import os
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)                       # App.resource_path() is cwd-relative
sys.path.insert(0, str(ROOT))

import cv2
from PySide6.QtCore import QTimer, QEventLoop
from PySide6.QtGui import QImage, QPixmap, QPalette, QColor
from PySide6.QtWidgets import QApplication

import App

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
OUT_DIR    = ROOT / "docs" / "screenshots"


def wait(ms: int):
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit)
    loop.exec()


def collect_images(inputs):
    paths = []
    for item in inputs:
        p = Path(item)
        if p.is_dir():
            paths += sorted(f for f in p.rglob("*") if f.suffix.lower() in IMAGE_EXTS)
        elif p.suffix.lower() in IMAGE_EXTS:
            paths.append(p)
    return paths


def to_pixmap(bgr) -> QPixmap:
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb.shape
    return QPixmap.fromImage(QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888).copy())


def trim_letterbox(bgr, thresh=240):
    """Strip solid white/black padding bars from the edges of a photo."""
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    def is_bar(line):
        return line.std() < 6 and (line.mean() > thresh or line.mean() < 255 - thresh)

    top, bottom = 0, gray.shape[0]
    while top < bottom - 1 and is_bar(gray[top]):
        top += 1
    while bottom - 1 > top and is_bar(gray[bottom - 1]):
        bottom -= 1
    left, right = 0, gray.shape[1]
    while left < right - 1 and is_bar(gray[top:bottom, left]):
        left += 1
    while right - 1 > left and is_bar(gray[top:bottom, right - 1]):
        right -= 1
    return bgr[top:bottom, left:right]


def as_webcam_frame(bgr, w=640, h=480):
    """Center-crop/resize a photo to a 4:3 webcam-sized frame."""
    ih, iw = bgr.shape[:2]
    target = w / h
    if iw / ih > target:
        nw = int(ih * target)
        x0 = (iw - nw) // 2
        bgr = bgr[:, x0:x0 + nw]
    else:
        nh = int(iw / target)
        y0 = (ih - nh) // 2
        bgr = bgr[y0:y0 + nh]
    return cv2.resize(bgr, (w, h), interpolation=cv2.INTER_AREA)


def setup_app():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    App.SANS_FONT   = App._load_or_download("Inter", "Segoe UI")
    App.ICON_FONT   = App._load_or_download("Material Icons", "Material Icons")
    App.ARABIC_FONT = App._load_arabic_font()

    pal = QPalette()
    pal.setColor(QPalette.Window,     QColor(App.BG))
    pal.setColor(QPalette.WindowText, QColor(App.TEXT))
    pal.setColor(QPalette.Base,       QColor(App.SURFACE))
    pal.setColor(QPalette.Button,     QColor(App.SURFACE3))
    pal.setColor(QPalette.ButtonText, QColor(App.TEXT))
    app.setPalette(pal)
    return app


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="image files and/or folders")
    ap.add_argument("--no-crop", action="store_true", help="keep the photo's aspect ratio instead of a 4:3 webcam crop")
    ap.add_argument("--gif-ms", type=int, default=1400, help="frame duration of the GIF")
    ap.add_argument("--out", default=str(OUT_DIR), help="output folder (default: docs/screenshots)")
    args = ap.parse_args()

    images = collect_images(args.inputs)
    if not images:
        sys.exit("No images found.")

    try:
        import torch
        if not torch.cuda.is_available():
            App.DEVICE = "cpu"
    except Exception:
        App.DEVICE = "cpu"

    app = setup_app()
    win = App.ArSLMainWindow()
    if win.model is None:
        sys.exit("Model failed to load.")
    win.show()
    wait(800)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    win.grab().save(str(out_dir / "idle.png"))
    print("saved idle.png")

    win.status_bar.set_webcam_on()
    frames = []
    for path in images:
        bgr = cv2.imread(str(path))
        if bgr is None:
            print(f"skip (unreadable): {path}")
            continue
        bgr = trim_letterbox(bgr)
        if not args.no_crop:
            bgr = as_webcam_frame(bgr)

        res = win.model.predict(bgr, imgsz=App.IMG_SIZE, conf=App.CONF,
                                device=App.DEVICE, verbose=False)[0]
        if not res.boxes:
            print(f"skip (no detection): {path.name}")
            continue
        top = max(res.boxes, key=lambda b: float(b.conf))
        key = win.model.names[int(top.cls)]

        win.canvas.set_frame(to_pixmap(res.plot()))
        win.canvas.set_fps(random.uniform(26, 31))
        win.letter_panel.show_letter(key, auto_hold=False)
        wait(700)  # let the panel's fade animation finish

        out = out_dir / f"detect_{key}.png"
        n = 2
        while out in frames:
            out = out_dir / f"detect_{key}_{n}.png"
            n += 1
        win.grab().save(str(out))
        frames.append(out)
        print(f"saved {out.name}  ({path.name} -> {key} {float(top.conf):.2f})")

    win.close()
    app.processEvents()

    if len(frames) > 1:
        from PIL import Image
        imgs = [Image.open(f).convert("RGB") for f in frames]
        imgs = [im.resize((im.width * 3 // 4, im.height * 3 // 4), Image.LANCZOS) for im in imgs]
        imgs = [im.quantize(colors=200, method=Image.Quantize.MEDIANCUT) for im in imgs]
        imgs[0].save(out_dir / "demo.gif", save_all=True, append_images=imgs[1:],
                     duration=args.gif_ms, loop=0, optimize=True)
        print("saved demo.gif")


if __name__ == "__main__":
    main()
