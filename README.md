# Zotero Cleaner Notebook

This repository contains a **Jupyter Notebook** that helps clean and migrate **PDF attachments** from Zotero’s local storage to an external folder (e.g., OneDrive, Dropbox, Google Drive).
The notebook also updates your Zotero library: imported file attachments are replaced with **linked file attachments** pointing to the new location.

This workflow is especially useful if you want to:

* Reduce your Zotero storage footprint.
* Sync all PDFs via a cloud service.
* Keep your reading progress (`.zotero-reader-state` files).

---

## Features

* Connects to Zotero using the [pyzotero](https://github.com/urschrei/pyzotero) library.
* Fetches all items from your Zotero library in batches.
* Moves local **PDF attachments** (and `.zotero-reader-state` files) to a specified folder.
* Creates **linked file entries** in Zotero pointing to the new files.
* Deletes the old Zotero-stored attachments.
* Uses `.env` for configuration (no hard-coded credentials).

---

## Requirements

* Python 3.7+
* Jupyter Notebook / JupyterLab
* Dependencies:

  ```bash
  pip install pyzotero python-dotenv
  ```

---

## Configuration

Create a `.env` file in the repository root with the following variables:

```ini
LIBRARY_ID=your_zotero_library_id   # Zotero user or group ID
LIBRARY_TYPE=user                   # or "group"
ZOTERO_KEY=your_zotero_api_key      # Zotero API key
ZOTERO_STORAGE_PATH=/path/to/zotero/storage
DEST_FOLDER=/path/to/export/folder
```

💡 *You can find your Zotero API key under: `Zotero.org → Settings → Feeds/API → Create new private key`*

---

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/zotero-cleaner-notebook.git
   cd zotero-cleaner-notebook
   ```

2. Create and edit the `.env` file as described above.

3. Start Jupyter:

   ```bash
   jupyter notebook
   ```

4. Open the notebook (`zotero_cleaner.ipynb`) and run the cells step by step:

   * **Load configuration** (reads `.env`)
   * **Fetch Zotero items**
   * **Clean and migrate PDFs**

---

## Example Output

```text
Total items retrieved: 1520
Moved paper123.pdf to /OneDrive/ZoteroPapers/ABCD123/paper123.pdf
Created new linked file attachment for paper123.pdf
Deleted original attachment with key ABCD123
```

---

## Notes & Limitations

* The notebook **does not move annotations** stored in Zotero’s database. Only `.zotero-reader-state` (reading position, open tabs) is preserved.
* Run on a **small test library** before migrating your entire collection.
* The process is **destructive** (old attachments are deleted after linking). Ensure your destination folder is backed up.

---

## License

MIT License – feel free to use, adapt, and improve.

---

## Disclaimer

This project is an **unofficial tool** for managing Zotero libraries. It is not affiliated with or endorsed by Zotero or the Corporation for Digital Scholarship.

* Use at your own risk.
* Always **back up your Zotero data** before running the notebook, as the process deletes and recreates attachments.
* The authors of this repository are **not responsible for data loss, misconfiguration, or any unintended effects**.
* Zotero® is a registered trademark of the Corporation for Digital Scholarship.

---
