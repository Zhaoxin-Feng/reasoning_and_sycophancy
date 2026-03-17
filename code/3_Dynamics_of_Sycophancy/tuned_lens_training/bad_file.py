import os
import gzip
from multiprocessing import Pool, cpu_count
from tqdm import tqdm


# DATA_DIR = "/workspace/redpajama_2023_06_sample/train"
DATA_DIR = "/workspace/redpajama_2023_06_sample"

def check_file(filepath):

    try:
        with gzip.open(filepath, 'rb') as f:

            f.seek(-1, os.SEEK_END)
            f.read(1)
        return None  
    except Exception as e:
        return filepath  

def main():
    if not os.path.exists(DATA_DIR):
        print(f"error: {DATA_DIR}")
        return

    files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith(".json.gz")]

    bad_files = []
    with Pool(processes=32) as pool:  
        for result in tqdm(pool.imap_unordered(check_file, files), total=len(files)):
            if result:
                bad_files.append(result)

    if bad_files:
        print(f" {len(bad_files)} error：")
        for f in bad_files:
            print(f"  - {f}")
            try:
                os.remove(f)
            except:
                print("    error")
    else:
        print("✅！")

if __name__ == "__main__":
    main()