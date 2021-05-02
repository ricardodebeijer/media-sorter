# media-sorter
Sort documents, photo's & video's on NAS using small python script.

Sorts from SRC into DEST, using YEAR/MONTH folder structure.

Separate top level folders for:
-  Documents (pdf,docx,pptx etc)
-  Media (jpg,png,mp4 etc)



Example use for Documents:
Src folder: `Z:/SourceTest/` (forward slash will be added if not provided)
Dest folder: `Z:/DestTest/Documents/` (forward slash will be added if not provided)
Extensions to move: `.pdf .docx .doc .pptx .xlsx .xls .txt`

Full command:
`python sortfiles.py "Z:/SourceTest/" "Z:/DestTest/Documents/" --extensions .pdf .docx .doc .pptx .xlsx .xls .txt`


For media (photos and videos):
Src folder: `Z:/SourceTest/` (forward slash will be added if not provided)
Dest folder: `Z:/DestTest/Media/` (forward slash will be added if not provided)
Extensions to move: `.png .jpg .jpeg`

Full command:
`python sortfiles.py "Z:/SourceTest/" "Z:/DestTest/Media/" --extensions .png .jpg .jpeg`