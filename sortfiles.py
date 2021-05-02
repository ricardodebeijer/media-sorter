#!/usr/bin/python3
import os, time, shutil, sys
from pathlib import Path

def main():
    # Do end with /
    srcDir = 'Z:/SourceTest/'
    # Dont end with /
    destDir = 'Z:/DestTest/Documenten/'
    extensions = ('.pdf','.docx','.doc','.pptx','.rtf','.xlsx','.xls','.txt','.dwg')
    # List all files in SRC
    for f in os.listdir(srcDir):
        srcPath = srcDir + f
        # Check if its a file
        if os.path.isfile(srcPath):
            # Check if its in the extension list
            if f.lower().endswith(extensions):
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

                # Log
                print('"',srcPath, '" modified at:', time.strftime('%Y-%m-%d', ftime),'moved to: "', destPath,'"')

if __name__ == "__main__":
    main()
