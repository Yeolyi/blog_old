import glob
import os
from pathlib import Path, PurePath

root_path = Path(__file__).parent.parent
f = open(os.path.join(root_path, "gen/template/header.html"), "r")
header = f.read()
f.close()

for path in glob.iglob(str(root_path) + "/**/*.html", recursive=True):
    if PurePath(path).name == "header.html":
        continue
    with open(path, "r+") as f:
        content = f.read()
        startIdx = content.find("<header>")
        endIdx = content.find("</header>") + len("</header>")
        if startIdx != -1:
            new_content = content[:startIdx] + header + content[endIdx:]
            f.seek(0)
            f.write(new_content)
            f.truncate()
