import os
import shutil

TEST_DIR = "test_downloads"

if os.path.exists(TEST_DIR):
    shutil.rmtree(TEST_DIR)
os.makedirs(TEST_DIR)

files = [
    "document.pdf", "image.jpg", "song.mp3", "video.mp4", 
    "archive.zip", "code.py", "unknown.xyz", "presentation.pptx",
    "spreadsheet.xlsx", "installer.exe"
]

for f in files:
    with open(os.path.join(TEST_DIR, f), "w") as f_obj:
        f_obj.write("dummy content")

print(f"Created {len(files)} dummy files in {TEST_DIR}")
