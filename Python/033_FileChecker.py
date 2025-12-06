import hashlib
import os
import argparse

def get_file_hash(filepath):
    """Calculates the SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except IOError:
        print(f"Could not read file: {filepath}")
        return None

def generate_baseline(baseline_file, target_dir):
    """Generates a baseline hash file for the target directory."""
    print(f"--- Generating baseline for {target_dir} ---")
    with open(baseline_file, "w") as f:
        for dirpath, dirnames, filenames in os.walk(target_dir):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                file_hash = get_file_hash(full_path)
                if file_hash:
                    f.write(f"{full_path},{file_hash}\n")
    print(f"--- Baseline created at {baseline_file} ---")

def load_baseline(baseline_file):
    """Loads the baseline file into a dictionary."""
    baseline = {}
    try:
        with open(baseline_file, "r") as f:
            for line in f:
                path, file_hash = line.strip().split(',', 1)
                baseline[path] = file_hash
    except FileNotFoundError:
        return {}
    return baseline

def check_integrity(baseline_file, target_dir):
    """Checks the integrity of the target directory against the baseline."""
    baseline_data = load_baseline(baseline_file)
    if not baseline_data:
        print(f"Error: Baseline file '{baseline_file}' not found or is empty. Please generate a baseline first using the --generate flag.")
        return

    print(f"--- Starting Integrity Check for {target_dir} ---")
    scanned_files = set()

    for dirpath, dirnames, filenames in os.walk(target_dir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            scanned_files.add(full_path)
            
            current_hash = get_file_hash(full_path)
            if current_hash is None:
                continue

            if full_path in baseline_data:
                baseline_hash = baseline_data[full_path]
                if baseline_hash != current_hash:
                    print(f"ALERT: File has been MODIFIED: {full_path}")
            else:
                print(f"ALERT: NEW file detected: {full_path}")
    
    baseline_files = set(baseline_data.keys())
    deleted_files = baseline_files - scanned_files
    for deleted_file in deleted_files:
        print(f"ALERT: File has been DELETED: {deleted_file}")

    print("--- Check Complete ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Integrity Checker")
    parser.add_argument("target_dir", help="The directory to scan.")
    parser.add_argument("--mode", choices=['generate', 'check'], required=True, help="Operation mode: 'generate' a new baseline or 'check' against an existing one.")
    parser.add_argument("--baseline", default="baseline.txt", help="The path to the baseline file.")
    
    args = parser.parse_args()

    if args.mode == 'generate':
        generate_baseline(args.baseline, args.target_dir)
    elif args.mode == 'check':
        check_integrity(args.baseline, args.target_dir)
        