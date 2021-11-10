import os, frontmatter, shutil
from postHtmlSrc import postHtmlSrc
from postRowHtmlSrc import postListHtmlSrc, postRowHtmlSrc
from markdown2 import Markdown
from pathlib import Path
from shutil import copy2

sourcePath = "./src/post/"
htmlPath = "./stories/post/"

sourceFolderList = list(filter(lambda x: x[0] != ".", os.listdir(sourcePath)))

folder = "./stories/post"
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print("Failed to delete %s. Reason: %s" % (file_path, e))

# Add postnumber to js
with open(os.path.join("./js/ui.js"), "r+") as f:
    src = f.read()
    equalIdx = src.find("=")
    semicolonIdx = src.find(";")
    src = src[: equalIdx + 1] + " " + str(len(sourceFolderList)) + src[semicolonIdx:]
    f.seek(0)
    f.write(src)
    f.truncate()


def findNextIdx(html, selector):
    return html.find(selector) + len(selector)


postTitleIdx = findNextIdx(postHtmlSrc, "<h2>")
postDateIdx = findNextIdx(postHtmlSrc, "<h3>")
contentIdx = findNextIdx(postHtmlSrc, '<div id="post-content">')

postListContentIdx = findNextIdx(postListHtmlSrc, '<ol id="post-list">')
postListHtml = postListHtmlSrc[:postListContentIdx]

postRowTitleIdx = findNextIdx(postRowHtmlSrc, "<h2>")
postRowDateIdx = findNextIdx(postRowHtmlSrc, '"post-row__date">')
postRowAIdx = findNextIdx(postRowHtmlSrc, 'href="')

markdowner = Markdown()
for folderName in sourceFolderList:
    Path(htmlPath + folderName).mkdir(parents=True, exist_ok=True)
    sourceFolderPath = sourcePath + folderName
    for filename in os.listdir(sourceFolderPath):
        with open(os.path.join(sourceFolderPath, filename), "r") as f:
            if filename == "content.md":
                # Making post html
                post = frontmatter.load(f)
                converted = (
                    postHtmlSrc[:postTitleIdx]
                    + post["title"]
                    + postHtmlSrc[postTitleIdx:postDateIdx]
                    + str(post["date"])
                    + postHtmlSrc[postDateIdx:contentIdx]
                    + markdowner.convert(post.content)
                    + postHtmlSrc[contentIdx:]
                )
                with open(
                    os.path.join(htmlPath, folderName, "index.html"), "w"
                ) as file1:
                    file1.write(converted)
                # Making post row html
                postListHtml += (
                    postRowHtmlSrc[:postRowAIdx]
                    + "post/"
                    + folderName
                    + postRowHtmlSrc[postRowAIdx:postRowTitleIdx]
                    + post["title"]
                    + postRowHtmlSrc[postRowTitleIdx:postRowDateIdx]
                    + str(post["date"])
                    + postRowHtmlSrc[postRowDateIdx:]
                )
            else:
                copy2(sourceFolderPath + "/" + filename, htmlPath + folderName)

postListHtml += postListHtmlSrc[postListContentIdx:]
with open(os.path.join("./stories/index.html"), "w") as f:
    f.seek(0)
    f.write(postListHtml)
    f.truncate()
