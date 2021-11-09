# 필요없는 파일도 카운트하는 버그 고치기

import os
import frontmatter
from postBlock import postSrc
from postListBlock import postListSrc
from postListBlock import postRowSrc
from markdown2 import Markdown
from pathlib import Path
from shutil import copy2

markdowner = Markdown()
titleIdx = postSrc.find('h2')+3
dateIdx = postSrc.find('h3')+3
contentIdx = postSrc.find('post-content')+14
sourcePath = "./stories/post/source/"
htmlPath = "./stories/post/"
postListHtml = postListSrc[:postListSrc.find("post-list")+11]
postRowTitleIdx = postRowSrc.find("h2")+3
postRowDateIdx = postRowSrc.find("post-row__date")+16
postRowAIdx = postRowSrc.find("href")+6

with open(os.path.join("./js/ui.js"), 'r+') as f: 
    src = f.read()
    equalIdx = src.find("=")
    semicolonIdx = src.find(";")
    src = src[:equalIdx+1] + str(len(os.listdir(sourcePath))) + src[semicolonIdx:]
    f.seek(0)
    f.write(src)
    f.truncate()
    
for postname in os.listdir(sourcePath):
    if postname == ".DS_Store":
        continue
    Path(htmlPath + "/" + postname).mkdir(parents=True, exist_ok=True)
    for filename in os.listdir(sourcePath + postname):
        with open(os.path.join(sourcePath, postname, filename), 'r') as f:
            if filename == "content.md":
                post = frontmatter.load(f)
                converted = postSrc[:titleIdx] + post["title"] + postSrc[titleIdx:dateIdx] + str(post["date"]) + postSrc[dateIdx:contentIdx] + markdowner.convert(post.content) + postSrc[contentIdx:]
                with open(os.path.join(htmlPath, postname, "index.html"), "w") as file1:
                    file1.write(converted)
                postListHtml += postRowSrc[:postRowAIdx] + "post/" + postname + postRowSrc[postRowAIdx:postRowTitleIdx] + post["title"] + postRowSrc[postRowTitleIdx:postRowDateIdx] + str(post["date"]) + postRowSrc[postRowDateIdx:]
            else:
                copy2(sourcePath+postname+"/"+filename, htmlPath+postname)
postListHtml += postListSrc[postListSrc.find("post-list")+11:]
with open(os.path.join("./stories/index.html"), 'w') as f: 
    f.seek(0)
    f.write(postListHtml)
    f.truncate()