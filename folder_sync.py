import os
import shutil
import time
import argparse
import logging


def log_message(message):
    "logs console and file"
    logging.info(message)
    print(message)


def files_differ(source_item, replica_item):
    """
    compare size and update time 
    returns true if diferent else false.
    """
    return (
        os.path.getsize(source_item) != os.path.getsize(replica_item)
        or os.path.getmtime(source_item) > os.path.getmtime(replica_item)
    )


def sync_folders(source, replica):
    """
    Sync the replica folder with the source folder:
    - Copies new/updated files from source to replica.
    - Removes files/folders in replica that are not in source.
    """
    # Ensure replica folder exists
    if not os.path.exists(replica):
        log_message(f"Replica folder '{replica}' does not exist. Creating it.")
        os.makedirs(replica)

    # Sync files and directories from source to replica
    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        replica_item = os.path.join(replica, item)

        if os.path.isdir(source_item):
            # If it's a directory, recursively sync
            sync_folders(source_item, replica_item)
        else:
            # If it's a file, check if it needs to be copied/updated
            if not os.path.exists(replica_item):
                log_message(f"File created: {source_item} → {replica_item}")
                shutil.copy2(source_item, replica_item)
            elif files_differ(source_item, replica_item):
                log_message(f"File updated: {source_item} → {replica_item} (size or timestamp mismatch)")
                shutil.copy2(source_item, replica_item)

    # Remove items from replica that are not in source
    for item in os.listdir(replica):
        source_item = os.path.join(source, item)
        replica_item = os.path.join(replica, item)

        if not os.path.exists(source_item):
            if os.path.isdir(replica_item):
                log_message(f"Folder removed: {replica_item} (not present in source)")
                shutil.rmtree(replica_item)
            else:
                log_message(f"File removed: {replica_item} (not present in source)")
                os.remove(replica_item)


def main(source, replica, log_file, interval):
    "main sync function"
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    log_message("Starting folder synchronization.")
    log_message(f"Source folder: {source}")
    log_message(f"Replica folder: {replica}")
    log_message(f"Synchronization interval: {interval} seconds")

    try:
        while True:
            log_message("Performing synchronization...")
            sync_folders(source, replica)
            log_message("Synchronization completed.")
            time.sleep(interval)
    except KeyboardInterrupt:
        log_message("Synchronization stopped by user.")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Optimized Folder Synchronization Script")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("log_file", help="Path to the log file")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")

    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(args.source, args.replica, args.log_file, args.interval)
