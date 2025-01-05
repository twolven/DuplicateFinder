import os
from collections import defaultdict
import csv
from datetime import datetime
import glob
import sys

# Increase CSV field size limit
maxInt = sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

def find_duplicates():
    """
    Scan current directory and find duplicate files based on name and size
    Returns a dictionary with (filename, size) as key and list of full paths as value
    """
    print("Scanning files...")
    file_dict = defaultdict(list)
    file_count = 0
    
    # Walk through current directory
    for root, _, files in os.walk('.'):
        for filename in files:
            # Skip the script itself and its output files
            if filename.endswith('.py') or filename.startswith('duplicates_') or filename.startswith('removal_log_'):
                continue
                
            full_path = os.path.join(root, filename)
            try:
                # Get file size
                file_size = os.path.getsize(full_path)
                # Use filename and size as key
                file_dict[(filename, file_size)].append(full_path)
                file_count += 1
                if file_count % 100 == 0:
                    print(f"Processed {file_count} files...", end='\r')
            except (OSError, PermissionError) as e:
                print(f"\nError accessing {full_path}: {e}")
                continue
    
    print(f"\nFinished scanning {file_count} files.")
    
    # Filter to keep only duplicates
    return {k: v for k, v in file_dict.items() if len(v) > 1}

def list_mode():
    """Just list the duplicates"""
    print("\nStarting duplicate file scan in current directory...")
    duplicates = find_duplicates()
    if not duplicates:
        print("No duplicates found.")
        return
    
    # Save to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"duplicates_{timestamp}.csv"
    
    print("\nSaving duplicate list...")
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Filename', 'Size (MB)', 'Paths'])
        
        total_space = 0
        for (filename, size), paths in duplicates.items():
            writer.writerow([filename, f"{size/1024/1024:.2f}", '|'.join(paths)])
            total_space += size * (len(paths) - 1)
    
    print(f"\nResults:")
    print(f"- Found {len(duplicates)} sets of duplicate files")
    print(f"- Potential space savings: {total_space/1024/1024:.2f} MB")
    print(f"- Full list saved to: {output_file}")
    print("\nReview the CSV file before running removal!")

def remove_mode():
    """Remove duplicate files using the most recent CSV file"""
    # Find the most recent duplicates CSV file
    csv_files = glob.glob('duplicates_*.csv')
    if not csv_files:
        print("No duplicate list found! Please run with -l first to generate the list.")
        return
    
    latest_csv = max(csv_files, key=os.path.getctime)
    print(f"\nUsing duplicate list from: {latest_csv}")
    
    # Confirm before proceeding
    print("\nWARNING: This will remove duplicate files, keeping only the first copy of each.")
    response = input("Are you sure you want to proceed? (yes/no): ")
    if response.lower() != 'yes':
        print("Operation cancelled.")
        return
    
    removed_files = []
    saved_space = 0
    error_files = []
    kept_files = []
    
    try:
        with open(latest_csv, 'r', encoding='utf-8') as f:
            # Count total lines first
            total_sets = sum(1 for _ in f) - 1  # Subtract header
            f.seek(0)  # Reset to start of file
            
            reader = csv.reader(f)
            next(reader)  # Skip header
            
            print(f"\nProcessing {total_sets} sets of duplicate files...")
            
            for i, row in enumerate(reader, 1):
                if len(row) < 3:
                    print(f"\nSkipping malformed row {i}")
                    continue
                
                filename, size_mb, paths = row
                paths = paths.split('|')
                
                if not paths:
                    continue
                
                # Verify we have at least 2 paths (original + duplicates)
                if len(paths) < 2:
                    continue
                
                # Keep track of which file we're keeping
                original_path = paths[0]
                if os.path.exists(original_path):
                    kept_files.append(original_path)
                    print(f"\nSet {i}/{total_sets}:")
                    print(f"Keeping: {original_path}")
                    
                    # Remove duplicates
                    for dup_path in paths[1:]:
                        if os.path.exists(dup_path):
                            try:
                                print(f"Removing: {dup_path}")
                                os.remove(dup_path)
                                removed_files.append(dup_path)
                                saved_space += float(size_mb)
                            except (OSError, PermissionError) as e:
                                error_msg = f"Error removing {dup_path}: {str(e)}"
                                print(error_msg)
                                error_files.append(error_msg)
        
        # Save detailed log
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"removal_log_{timestamp}.txt"
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("Files kept (originals):\n")
            f.write("\n".join(kept_files))
            f.write("\n\nFiles removed (duplicates):\n")
            f.write("\n".join(removed_files))
            if error_files:
                f.write("\n\nErrors encountered:\n")
                f.write("\n".join(error_files))
        
        print(f"\n\nOperation Complete:")
        print(f"- Kept {len(kept_files)} original files")
        print(f"- Removed {len(removed_files)} duplicate files")
        print(f"- Saved approximately {saved_space:.2f} MB of space")
        if error_files:
            print(f"- Encountered {len(error_files)} errors (see log file)")
        print(f"- Full log saved to: {log_file}")
            
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        return

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2 or sys.argv[1] not in ['-l', '-r']:
        print("Usage:")
        print("  To list duplicates:  python duplicate_finder.py -l")
        print("  To remove duplicates: python duplicate_finder.py -r")
        sys.exit(1)
    
    print("Duplicate File Finder")
    print("Current directory:", os.path.abspath('.'))
    
    if sys.argv[1] == '-l':
        list_mode()
    else:
        remove_mode()