#!/usr/bin/python3
import os, time, shutil, sys
from pathlib import Path
import ntpath

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def run_fast_scandir(dir, ext):    # dir: str, ext: list
    subfolders, files = [], []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                files.append(f.path)


    for dir in list(subfolders):
        sf, f = run_fast_scandir(dir, ext)
        subfolders.extend(sf)
        files.extend(f)
    return subfolders, files

def sortFiles(
    srcDir,
    destDir,
    extensions,
    clearEmptyFolders,
    dryRun
):
    print('Moving files matching', extensions, 'from', srcDir , 'to', destDir, 'clearEmptyFolders',clearEmptyFolders,'dryRun',dryRun);
    # Check if srcDir exists
    if not os.path.exists(srcDir):
        raise Exception("Source directory does not exist")
    
    # Add forward slash to srcDir if not existing
    if not srcDir.endswith(('/','\\')):
        srcDir = srcDir + '/'
        print('Forward slash added to srcDir')
    # Add forward slash to destDir if not existing
    if not destDir.endswith(('/','\\')):
        destDir = destDir + '/'
        print('Forward slash added to destDir')

    nothingMoved = True;
    # Get all subfolders and files in srcDir matching the given extensions 
    subfolders, files = run_fast_scandir(srcDir, extensions)

    # List all files in SRC
    for srcPath in files:
        # Get modified time
        ftime = time.gmtime(os.path.getmtime(srcPath))

        # Create dest directory if not existing
        if not os.path.isdir(destDir):
            os.mkdir(destDir)

        # Create dest year directory if not existing
        yearDir = os.path.join(destDir, str(ftime.tm_year))
        if not os.path.isdir(yearDir):
            os.mkdir(yearDir)

        # Create dest month directory if not existing
        monthDir = os.path.join(yearDir, str(ftime.tm_mon).zfill(2))
        if not os.path.isdir(monthDir):
            os.mkdir(monthDir)

        destPath = os.path.join(monthDir, path_leaf(srcPath))

        # Check if the file already exists
        if os.path.exists(destPath):
            duplicateDir = os.path.join(destDir, 'DUPLICATES')
            # Create DUPLICATES directory if not existing
            if not os.path.isdir(duplicateDir):
                os.mkdir(duplicateDir)

            # Create dest year directory if not existing
            yearDir = os.path.join(duplicateDir, str(ftime.tm_year))
            if not os.path.isdir(yearDir):
                os.mkdir(yearDir)

            # Create dest month directory if not existing
            monthDir = os.path.join(yearDir, str(ftime.tm_mon).zfill(2))
            if not os.path.isdir(monthDir):
                os.mkdir(monthDir)

            duplicatePath = os.path.join(monthDir, path_leaf(srcPath))
            if not dryRun:
                # Move file to DUPLICATE folder
                shutil.move(srcPath, duplicatePath);
                # Set flag something was moved
                nothingMoved = False
            print(f"{bcolors.WARNING}'{srcPath}' Duplicate file '{duplicatePath}'{bcolors.ENDC}")
        else:
            # Check if not dry run
            if not dryRun:
                # Move file to destPath
                shutil.move(srcPath, destPath);
                # Set flag something was moved
                nothingMoved = False
            # Always log move
            print(os.path.join(srcPath), 'modified at:', time.strftime('%Y-%m-%d', ftime),'moved to:', destPath)
       
    # Log if no files were moved/matched
    if nothingMoved:
        print('Nothing was matches/moved.')

    # Check if delete empty folders is enabled
    if clearEmptyFolders:
        print('Clearing empty folders is enabled')
        # Loop trough all folders
        for folder in subfolders:
            # Check if its empty
            if len(os.listdir(folder)) == 0:
                print(folder, "is empty, removing")
                # Remove it if we are not doing a dry run
                if not dryRun:
                    os.rmdir(folder)

   
def main():
    import argparse
    # setup command line parsing
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Sort files into folders by date",
    )
    parser.add_argument("src_dir", type=str, help="source directory")
    parser.add_argument("dest_dir", type=str, help="destination directory")
    parser.add_argument("-c", "--clear-empty-folders", action="store_true", help="Clear empty folders", default=False)
    parser.add_argument("-t", "--test", action="store_true", help="Test run", default=False)

    parser.add_argument(
        "--extensions",
        type=str,
        nargs="+",
        default=[],
        help="a list of extensions to match",
    )

    # parse command line arguments
    args = parser.parse_args()

    sortFiles(
        args.src_dir,
        args.dest_dir,
        args.extensions,
        args.clear_empty_folders,
        args.test
    )

if __name__ == "__main__":
    main()
