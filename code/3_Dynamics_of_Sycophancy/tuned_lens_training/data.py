import os
import time
import random
import requests
import subprocess
from multiprocessing import Pool, cpu_count
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


BASE_URL = "https://data.together.xyz/redpajama-data-v2/v1.0.0"
SNAPSHOT = "2023-06"
partition = "head_middle"
lang = "en"
OUTPUT_DIR = "/workspace/redpajama_2023_06_sample"

# ==========================================

DOWNLOAD_LIMIT = 1000
# ==========================================


try:
    N_CORES = cpu_count()
except:
    N_CORES = 4 

VERIFY_WORKERS = min(N_CORES, 32)

DOWNLOAD_WORKERS = 16
MAX_RETRIES = 10


def get_file_list():

    listing_url = f"{BASE_URL}/listings/{lang}-{SNAPSHOT}-{partition}.txt"
    for _ in range(3):
        try:
            resp = requests.get(listing_url, timeout=30)
            resp.raise_for_status()
            files = resp.text.strip().split('\n')
            print(f"{len(files)}")
            return files
        except:
            time.sleep(1)
    raise Exception("error")

def system_gzip_check(filepath):

    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        return (False, filepath)

    try:
        subprocess.run(
            ['gzip', '-t', '-q', filepath],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return (True, filepath)
    except subprocess.CalledProcessError:
        return (False, filepath) 
    except Exception:
        return (False, filepath)

def download_one_file(file_id):
    file_url = f"{BASE_URL}/documents/{file_id}.json.gz"
    safe_name = file_id.replace("/", "_") + ".json.gz"
    local_path = os.path.join(OUTPUT_DIR, safe_name)

    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            with requests.get(file_url, stream=True, timeout=60) as r:
                if r.status_code == 429:
                    sleep_time = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(sleep_time)
                    attempt += 1
                    continue
                r.raise_for_status()
                with open(local_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024*1024):
                        if chunk: f.write(chunk)

 
            is_valid, _ = system_gzip_check(local_path)
            if is_valid:
                return 1 
            else:
                raise Exception("Integrity check failed immediately after download")

        except Exception as e:
            sleep_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(sleep_time)
            attempt += 1
            if os.path.exists(local_path):
                try: os.remove(local_path)
                except: pass

    return f"Failed: {safe_name}"

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    try:
        all_cloud_files = get_file_list() # list of IDs
    except Exception as e:
        print(f" {e}")
        return

    if DOWNLOAD_LIMIT is not None:
        if len(all_cloud_files) > DOWNLOAD_LIMIT:
            all_cloud_files = all_cloud_files[:DOWNLOAD_LIMIT]
        else:
            print(f"no need")

    filename_to_id = {fid.replace("/", "_") + ".json.gz": fid for fid in all_cloud_files}

    existing_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".json.gz")]
    existing_paths = [os.path.join(OUTPUT_DIR, f) for f in existing_files]

    valid_files_set = set()
    deleted_count = 0

    if existing_files:
        with Pool(processes=VERIFY_WORKERS) as pool:
            results = list(tqdm(
                pool.imap_unordered(system_gzip_check, existing_paths, chunksize=10),
                total=len(existing_paths),
                unit="file",
                desc="Verifying"
            ))

        for is_valid, path in results:
            filename = os.path.basename(path)
            if is_valid:
                valid_files_set.add(filename)
            else:
                try:
                    os.remove(path)
                    deleted_count += 1
                except: pass

        print(f": {len(valid_files_set)}, {deleted_count}")
    else:
        print("no need")

    files_to_download = []
    for fname, fid in filename_to_id.items():
        if fname not in valid_files_set:
            files_to_download.append(fid)

    if not files_to_download:
        return

    success_count = 0
    fail_list = []

    with tqdm(total=len(files_to_download), unit="file", desc="Downloading") as pbar:
        with ThreadPoolExecutor(max_workers=DOWNLOAD_WORKERS) as executor:
            future_to_fid = {executor.submit(download_one_file, fid): fid for fid in files_to_download}

            for future in as_completed(future_to_fid):
                res = future.result()
                pbar.update(1)
                if res == 1:
                    success_count += 1
                else:
                    fail_list.append(res)
                    tqdm.write(f" [X] {res}")

if __name__ == "__main__":
    main()