#!/usr/bin/env python
"""
Creates data/images/<class>/*.jpg @224×224 for 4 target classes.
Run:  python src/prepare_data.py
"""
import json, shutil, random, itertools, csv
from pathlib import Path
import cv2
import numpy as np
from tqdm import tqdm

# -------- user‑config --------
TARGET_SIZE = 224
CLASSES = {
    "trash":        ["trash", "glass"],
    "recycle":      ["plastic", "cardboard", "paper", "metal", "can", "bottle"],
    "compost":      ["organic", "food", "biological"],
    "electronics":  ["battery", "electronic", "cellphone", "laptop"]
}
RAW = Path("data/raw")
OUT = Path("data/images")
# -----------------------------

def resize_pad(img, size=224):
    h, w = img.shape[:2]
    s = size / max(h, w)
    img = cv2.resize(img, (int(w*s), int(h*s)))
    h2, w2 = img.shape[:2]
    top = (size - h2)//2
    left = (size - w2)//2
    canvas = np.full((size, size, 3), 255, np.uint8)
    canvas[top:top+h2, left:left+w2] = img
    return canvas

def ensure_out():
    if OUT.exists(): shutil.rmtree(OUT)
    for c in CLASSES: (OUT/c).mkdir(parents=True, exist_ok=True)

def iter_trashnet():
    """
    Yield (filepath, label) pairs no matter how TrashNet is nested.

    Works with ALL of these layouts:
      • data/raw/trashnet-master/data/<class>/*.jpg
      • data/raw/trashnet-master/<class>/*.jpg
      • data/raw/trashnet-master/**/dataset-resized/*.jpg    (flat files)
    """
    root = RAW / "trashnet-master"
    if not root.exists():
        return

    for img_p in root.rglob("*.jp*g"):
        parts = img_p.parts

        # If it's .../data/<class>/file.jpg  →  class = parent folder
        if "data" in parts:
            cls = img_p.parent.name.lower()
        else:
            # flat file like plastic135.jpg → take alpha prefix
            cls = ''.join(filter(str.isalpha, img_p.stem)).lower()

        yield img_p, cls




def iter_taco():
    taco_json = json.load(open(RAW/"taco"/"data"/"annotations.json"))
    for ann in taco_json["annotations"]:
        cat_name = taco_json["categories"][ann["category_id"]]["name"].lower()
        img_file = RAW/"taco"/"data"/"images"/taco_json["images"][ann["image_id"]]["file_name"]
        yield img_file, cat_name
def iter_extra():
    """
    Yield (filepath, label) for all images under data/raw/compost and data/raw/electronics
    """
    for cls in ("compost", "electronics"):
        folder = RAW/cls
        if not folder.exists():
            continue
        for img_p in folder.rglob("*.jp*g"):
            yield img_p, cls


def main():
    ensure_out()
    m = {alias: cls for cls, aliases in CLASSES.items() for alias in aliases}
    for img_p, old_label in itertools.chain(
        iter_trashnet(),
        iter_taco(),
        iter_extra()
    ):

        cls = m.get(old_label)
        if not cls: continue
        img = cv2.imread(str(img_p))
        if img is None: continue
        out_p = OUT/cls/f"{img_p.stem}_{img_p.stat().st_ino}.jpg"
        cv2.imwrite(str(out_p), resize_pad(img, TARGET_SIZE))
    # write labels.txt
    with open("data/labels.txt","w") as f: f.write("\n".join(CLASSES.keys()))
    print("Done — images prepared!")

if __name__ == "__main__":
    main()
