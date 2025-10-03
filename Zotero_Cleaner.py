import os
import shutil
import os
import argparse
from pathlib import Path
from pyzotero import zotero
from dotenv import load_dotenv

def main():
    # Argument parser for configurable items
    parser = argparse.ArgumentParser(description="Move Zotero attachments and update links.")
    parser.add_argument("--batch-size", default=100, type=int, help="Maximum number of items to process per request")
    parser.add_argument("--library-id", type=str, help="Zotero library ID")
    parser.add_argument("--library-type", type=str, default="user", help="Zotero library type (user or group)")
    parser.add_argument("--zotero-key", type=str, help="Zotero API key")
    parser.add_argument("--zotero-storage-path", type=str, help="Path to Zotero storage")
    parser.add_argument("--dest-folder", type=str, help="Destination folder for exported files")
    args = parser.parse_args()

    # Load environment variables from .env file
    load_dotenv()

    # Configuration (use argparse values if provided, else fallback to env or default)
    LIBRARY_ID = args.library_id or os.getenv("LIBRARY_ID")         # Zotero library ID
    LIBRARY_TYPE = args.library_type or os.getenv("LIBRARY_TYPE", "user") # Use 'group' for group libraries
    ZOTERO_KEY = args.zotero_key or os.getenv("ZOTERO_KEY")         # API key
    ZOTERO_STORAGE_PATH = Path(args.zotero_storage_path or os.getenv("ZOTERO_STORAGE_PATH", "zotero_storage")) # Path to store attachments
    DEST_FOLDER = Path(args.dest_folder or os.getenv("DEST_FOLDER", "zotero_export")) # Path to store exported files

    # Initialize Zotero API
    zot = zotero.Zotero(LIBRARY_ID, LIBRARY_TYPE, ZOTERO_KEY)

    # Retrieve all items in the Zotero library efficiently
    def fetch_all_items(zot, batch_size):
        all_items = []
        start = 0
        while True:
            items = zot.items(start=start, limit=batch_size)
            if not items:
                break
            all_items.extend(items)
            start += batch_size
        return all_items

    all_items = fetch_all_items(zot, args.batch_size)
    print(f"Total items retrieved: {len(all_items)}")

    # Move local files to specified new storage and delete the original file
    for item in all_items:

        # Check if the attachment is a PDF and stored locally
        if item['data'].get('linkMode') != 'imported_file' or not item['data']['filename'].endswith('.pdf'):
            continue

        # Get attachment details
        key = item['key']
        parent_key = item['data'].get('parentItem')  # Use .get() to handle missing parentItem
        title = item['data']['title']
        file_name = item['data']['filename']
        storage_path = os.path.join(ZOTERO_STORAGE_PATH, key)

        # Skip if the storage folder does not exist
        if not os.path.exists(storage_path):
            print(f"Storage path not found for attachment key {key}")
            continue

        # Identify the file to move
        files = [f for f in os.listdir(storage_path) if os.path.isfile(os.path.join(storage_path, f))]
        
        # Filter to get the PDF file
        try:
            pdf_file = [f for f in files if f.endswith('.pdf')][0]
        except Exception as e:
            print(f"No PDF file found in {storage_path} for attachment key {key}")
            continue
        
        if not files:
            print(f"No files found in {storage_path}")
            continue

        file_path = os.path.join(storage_path, pdf_file)
        dest_path = os.path.join(DEST_FOLDER, key, pdf_file)
        
        
        # Check if there is a .zotero-reader-state file and move it as well
        reader_state_file = [f for f in files if f == '.zotero-reader-state']

        if reader_state_file:
            reader_state_file_path = os.path.join(storage_path, reader_state_file[0])
            reader_state_dest_path = os.path.join(DEST_FOLDER, key, reader_state_file[0])
            try:
                if not os.path.exists(os.path.dirname(reader_state_dest_path)):
                    os.makedirs(os.path.dirname(reader_state_dest_path))
                shutil.move(reader_state_file_path, reader_state_dest_path)
                print(f"Moved {reader_state_file[0]} to {reader_state_dest_path}")
            except Exception as e:
                print(f"Error moving {reader_state_file[0]}: {e}")

        # Move the file to destination folder
        try:
            if not os.path.exists(os.path.dirname(dest_path)):
                os.makedirs(os.path.dirname(dest_path))
            shutil.move(file_path, dest_path)
            print(f"Moved {pdf_file} to {dest_path}")
        except Exception as e:
            print(f"Error moving {pdf_file}: {e}")
            continue

        # Create the linked file path
        linked_file_path = os.path.abspath(dest_path)

        # Create a new linked file attachment
        try:
            new_attachment = {
                'itemType': 'attachment',
                'parentItem': parent_key,  # Can be None for standalone attachments
                'linkMode': 'linked_file',
                'title': title,
                'path': linked_file_path,  # Path to the linked file
                'contentType': 'application/pdf',  # Specify the content type for PDFs
            }
            zot.create_items([new_attachment])
            print(f"Created new linked file attachment for {pdf_file} at {linked_file_path}")
        except Exception as e:
            print(f"Error creating linked file attachment for {pdf_file}: {e}")
            continue

        # Delete the original Zotero item
        try:
            zot.delete_item(item)
            print(f"Deleted original attachment with key {key}")
        except Exception as e:
            print(f"Error deleting Zotero item {key}: {e}")

if __name__ == "__main__":
    main()