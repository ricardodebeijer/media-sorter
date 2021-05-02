#!/usr/bin/python3
import os, time, shutil, sys
from pathlib import Path

def sortFiles(
    srcDir,
    destDir,
    extensions
):
    print('Moving files matching', extensions, 'from', srcDir , 'to', destDir);
    # Check if srcDir exists
    if not os.path.exists(srcDir):
        raise Exception("Source directory does not exist")
    
    # Add forward slash to srcDir if not existing
    if not srcDir.endswith('/'):
        srcDir = srcDir + '/'
        print('Forward slash added to srcDir')
    # Add forward slash to destDir if not existing
    if not destDir.endswith('/'):
        destDir = srcDir + '/'
        print('Forward slash added to destDir')

    nothingMoved = True;
    # List all files in SRC
    for f in os.listdir(srcDir):
        srcPath = srcDir + f
        # Check if its a file
        if os.path.isfile(srcPath):
            # Check if its in the extension list
            if f.lower().endswith(tuple(extensions)):
                # Get modified time
                ftime = time.gmtime(os.path.getmtime(srcPath))

                # Create dest directory if not existing
                if not os.path.isdir(destDir):
                    os.mkdir(destDir)

                # Create dest year directory if not existing
                yearDir = destDir + str(ftime.tm_year)
                if not os.path.isdir(yearDir):
                    os.mkdir(yearDir)

                # Create dest month directory if not existing
                monthDir = yearDir + '/' + str(ftime.tm_mon).zfill(2)
                if not os.path.isdir(monthDir):
                    os.mkdir(monthDir)

                destPath = monthDir + '/' + f;
                # Move file to destPath
                shutil.move(srcPath, destPath);

                # Set flag something was moved
                nothingMoved = False
                # Log
                print('"',srcPath, '" modified at:', time.strftime('%Y-%m-%d', ftime),'moved to: "', destPath,'"')

    if nothingMoved:
        print('Nothing was matches/moved.')
def main():
    import argparse
    # setup command line parsing
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Sort files into folders by date",
    )
    parser.add_argument("src_dir", type=str, help="source directory")
    parser.add_argument("dest_dir", type=str, help="destination directory")
    # parser.add_argument("-r", "--recursive", action="store_true", help="search src_dir recursively")
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
    )

if __name__ == "__main__":
    main()
