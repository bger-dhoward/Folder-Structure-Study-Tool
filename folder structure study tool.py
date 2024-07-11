import os
import tkinter as tk
from tkinter import filedialog
import csv
import time

os.system('color')

class bcolors: 
    # from https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal 
    # per comments at above, make sure to import os, then set os.system('color') to get these to work!
    HEADER = '\x1b[95m' 
    OKBLUE = '\x1b[94m'
    OKCYAN = '\x1b[96m'
    OKGREEN = '\x1b[92m'
    WARNING = '\x1b[93m'
    FAIL = '\x1b[91m'
    ENDC = '\x1b[0m'
    BOLD = '\x1b[1m'
    UNDERLINE = '\x1b[4m'

def proceed_or_quit():
    response = input(f'Press {bcolors.WARNING}Enter{bcolors.ENDC} to proceed, or {bcolors.WARNING}Q{bcolors.ENDC} to quit: ')
    if response.upper() == "Q":
        print('Thanks for stopping by!')
        time.sleep(3)
        quit()
    elif len(response) > 0:
        print(f'Invalid response: {response}')
        proceed_or_quit()


def print_size_format(size):
    bytes = size
    kb = bytes / 1024
    mb = kb / 1024
    gb = mb / 1024
    
    if gb > 1:
        print(f"Size: {round(gb, 2)} gb")
        return
    if mb > 1:
        print(f"Size: {round(mb, 2)} mb")
        return
    if kb > 1:
        print(f"Size: {round(kb, 2)} kb")
        return
    else:
        print(f"Size: {bytes} bytes")
        return

def convert_size(size):
    bytes = size
    kb = bytes / 1024
    mb = kb / 1024
    gb = mb / 1024
    
    if size == 0:
        return ""
    
    if gb > 1:
        return f"{round(gb,2)} gb"
    if mb > 1:
        return f"{round(mb,2)} mb"
    if kb > 1:
        return f"{round(kb,2)} kb"
    else:
        return f"{round(bytes,2)} bytes"

def get_dir_size(dir_path):
    size = 0
    num_files = 0
    num_dirs = 0
    for path, dirs, files in os.walk(dir_path):
        num_files += len(files)
        num_dirs += len(dirs)
        #print(path)
        #print(f"Num of Files: {len(files)}")
        #print(f"Num of SubDirectories: {len(dirs)}")
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)
        #print(f"Running Subtotal Size: {print_size_format(size)}")
    #print(f"Num Files: {num_files}\nNum Directories: {num_dirs}")
    #print_size_format(size)
    return size, num_files


def survey_folder(dir_path, data_structure, depth=0):
    time.sleep(0.05)
    print('.', end='', flush=True)
    data_i = len(data_structure)
    data_structure.append([])
    size = 0
    num_files = 0
    if depth == 3:
        dir_size, dir_files = get_dir_size(dir_path)
        size += dir_size
        num_files += dir_files
        # print(f"depth 3! {dir_path}\nSize: {size}\nFiles: {num_files}\n")
    else:
        try:
            for direntry in os.scandir(dir_path):
                if direntry.is_dir(follow_symlinks=False):
                    dir_size, dir_files = survey_folder(direntry, data_structure, depth=depth+1)
                    size += dir_size
                    num_files += dir_files
                else:
                    size += os.path.getsize(direntry)
                    num_files +=1
        except PermissionError as e:
            print('\n')
            print(e)
    
    data_row = ["" for i in range(depth + 3)]
    data_row[0] = size
    data_row[1] = num_files
    
    data_path = ""
    if type(dir_path) == str:
        data_path = dir_path.split('/')[-1]
    else:
        data_path = dir_path.name
    data_row[-1] = data_path
    
    data_structure[data_i] = data_row
    return size, num_files

starting_text = f"""{bcolors.OKGREEN}
#####################################
#    Folder Structure Study Tool    #
##################################### {bcolors.ENDC}

This tool will scan the selected directory and 3 levels of subdirectories, and report 
the total size and number of files at each level.

{bcolors.OKGREEN}Instructions:{bcolors.ENDC}
1. Select Directory to be scanned.
2. Tool will scan all permissible files and subdirectories.
    - Note: this may take a long time for directories with many subdirectories and files.
3. When scan is complete, save the results .CSV file to your preferred location.
4. Press Enter to select another directory, or Q to quit.

{bcolors.OKGREEN}Using the results file:{bcolors.ENDC}
1. Open the results .csv file in Excel.
2. Each level of directory will report the total size and number of folders for itself
   and all of its subdirectories.
3. Subdirectory paths are indented one column for each level of nesting.
3. Enjoy your data.

For questions or troubleshooting, contact Dan Howard (dhoward@ballinger.com)

Ready? Let's go!

"""

if __name__ == "__main__":
    print(starting_text)
    while True:
        proceed_or_quit()
        root = tk.Tk()
        root.withdraw()  
        directory = filedialog.askdirectory(title='Select Directory to be scanned')
        root.destroy()
        
        out_data = []
        
        total_size, total_files = survey_folder(directory, out_data)
        
        print(f"\n\nScan complete. Total size: {convert_size(total_size)}  Total files: {total_files}\nSave results?")
        proceed_or_quit()

        dir_name = directory.split('/')[-1]
        init_filename = f"{dir_name} Structure.csv"
        root = tk.Tk()
        root.withdraw()  
        filename =  filedialog.asksaveasfilename(
            title="Save Results File", 
            initialfile=init_filename, 
            defaultextension='.csv',
            )
        root.destroy()
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([directory])
            writer.writerow([])
            writer.writerow(['Size', 'Num Files', 'Path'])
            for row in out_data:
                row[0] = convert_size(row[0])
                writer.writerow(row)
                #print(row)

        print(f'\nResults file saved at: {filename}\n')
        print('Repeat with another directory?')
        
        #input('we good?')