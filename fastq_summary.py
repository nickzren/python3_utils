#!/usr/bin/env python3
"""
Recursively check the provided paths for .fastq.gz & .fastq.gz.md5 files
and report the number and total size of each.
"""
import argparse
import os

def summarize_fastqs(fh):
    fastq_count, fastq_size, md5_count, md5_size = 0, 0, 0, 0
    for line in fh:
        path = line.strip()
        if not os.path.isdir(path):
            print(f"Didn't find expected directory: {path}")
            continue
        for root, dirs, files in os.walk(path):
            print(dirs)
            fastq_count_in_dir = 0
            md5_count_in_dir = 0
            for name in files:
                if name.endswith(".fastq.gz"):
                    fastq_count += 1
                    fastq_count_in_dir += 1
                    fastq_size += os.stat(os.path.join(root, name)).st_size
                elif name.endswith(".fastq.gz.md5sum"):
                    md5_count += 1
                    md5_size += os.stat(os.path.join(root, name)).st_size
                    md5_count_in_dir += 1
            
            # missing fastq or md5
            if(fastq_count_in_dir != md5_count_in_dir):
                print(root)

    print(f"total fastq file number: {fastq_count}")
    print(f"total fastq file size: {fastq_size}")
    print("")
    print(f"total fastq md5sum file number: {md5_count}")
    print(f"total fastq md5sum file size: {md5_size}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("FILE", type=argparse.FileType("r"), help="the input file name")
    args = parser.parse_args()
    try:
        summarize_fastqs(args.FILE)
    finally:
        args.FILE.close()
