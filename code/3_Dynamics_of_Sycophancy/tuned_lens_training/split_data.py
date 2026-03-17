import os
import shutil
import random
from tqdm import tqdm

# === Configuration ===
# Your data directory
DATA_DIR = "/workspace/redpajama_2023_06_sample"

def main():
    if not os.path.exists(DATA_DIR):
        print(f"Error: Directory not found {DATA_DIR}")
        return

    # 1. Get all .json.gz files
    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json.gz")]
    total_files = len(files)

    if total_files == 0:
        print("Directory is empty, no operation required.")
        return

    print(f"Found {total_files} data files, preparing for 95:5 split...")

    # 2. Create train and validation subdirectories
    train_dir = os.path.join(DATA_DIR, "train")
    val_dir = os.path.join(DATA_DIR, "validation")

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    # 3. Random shuffle and allocation
    random.shuffle(files)

    # Set aside 5% (at least 1 file) for the validation set
    n_val = max(1, int(total_files * 0.05))
    val_files = files[:n_val]
    train_files = files[n_val:]

    print(f"-> Validation set: {len(val_files)} files")
    print(f"-> Training set: {len(train_files)} files")

    # 4. Move files (using shutil.move)
    print("Moving files...")

    # Move validation set
    for f in tqdm(val_files, desc="Moving to Validation"):
        src = os.path.join(DATA_DIR, f)
        dst = os.path.join(val_dir, f)
        shutil.move(src, dst)

    # Move training set
    for f in tqdm(train_files, desc="Moving to Train"):
        src = os.path.join(DATA_DIR, f)
        dst = os.path.join(train_dir, f)
        shutil.move(src, dst)

    print("\n=== Data split complete! ===")
    print(f"Current directory structure:")
    print(f"{DATA_DIR}/")
    print(f"  ├── train/       ({len(train_files)} files)")
    print(f"  └── validation/  ({len(val_files)} files)")

if __name__ == "__main__":
    main()