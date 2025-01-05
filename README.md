# Duplicate File Finder and Remover

## Overview
This Python script scans directories to identify and optionally remove **duplicate files** based on their **name and size**. It is designed to work on **local drives**, **network-attached storage (NAS)**, and **mounted shares**.

The tool generates detailed CSV reports for review before performing any deletions and logs all operations, ensuring safety and transparency.

---

## Features
- **Duplicate Detection:** Scans all subdirectories to find duplicate files by matching filenames and sizes.
- **CSV Reporting:** Outputs a list of duplicates along with potential space savings.
- **Selective Deletion:** Removes duplicates while retaining the first instance of each file.
- **Error Handling:** Logs permission issues and errors encountered during processing.
- **Large File Support:** Handles large directories and files by dynamically adjusting CSV limits.

---

## Requirements
- Python 3.x

### Dependencies
No additional libraries are required beyond Python's standard library.

---

## Usage
### 1. Listing Duplicates
To scan the current directory and generate a report of duplicates:
```bash
python duplicate_finder.py -l
```
- Generates a CSV file (e.g., `duplicates_YYYYMMDD_HHMMSS.csv`) in the current directory.
- Estimates potential space savings based on duplicate sizes.

### 2. Removing Duplicates
To remove duplicates based on the most recent CSV file:
```bash
python duplicate_finder.py -r
```
- Prompts for confirmation before deleting files.
- Retains the first instance of each duplicate and deletes the rest.
- Logs detailed results, including retained and deleted files, errors, and space savings.

---

## Example Workflow
1. Scan for duplicates:
   ```bash
   python duplicate_finder.py -l
   ```
2. Review the CSV file to verify duplicates.
3. Remove duplicates safely:
   ```bash
   python duplicate_finder.py -r
   ```
4. Review logs for details:
   - `removal_log_YYYYMMDD_HHMMSS.txt`

---

## Notes
- **Scope:** Operates within the current directory and its subdirectories.
- **Safety:** Files are only deleted after explicit confirmation in removal mode.
- **Compatibility:** Works with NAS and network shares as long as they are mounted.
- **Permissions:** May fail to process files owned or managed by other users, such as system files, local admin files, or backups like File History.

---

## Error Handling
- Permission errors and inaccessible files are logged without interrupting processing.
- Malformed CSV entries during removal are skipped and logged.

---

## License
This project is licensed under the MIT License. See LICENSE for details.

---

## Disclaimer
Use this tool at your own risk. Review all reports and logs carefully before proceeding with deletions. The authors are not responsible for accidental data loss.