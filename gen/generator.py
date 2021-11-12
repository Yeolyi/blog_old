import os, frontmatter, shutil
from writingHtmlSrc import writingListSrc, writingPostSrc, writingRowSrc
from tilHtmlSrc import tilListSrc, tilRowSrc, tilPostSrc
from markdown2 import Markdown
from pathlib import Path
from shutil import copy2

writingSrcPath = "./src/writing/"
writingDstPath = "./stories/writing/"

shutil.rmtree("./stories", ignore_errors=True)

Path("./stories/writing").mkdir(parents=True, exist_ok=True)
Path("./stories/til").mkdir(parents=True, exist_ok=True)


def dateOfWriting(path):
    p = os.path.join(writingSrcPath, path, "content.md")
    with open(p, "r+") as f:
        post = frontmatter.load(f)
        return post["date"]


writingSrcFolderNames = list(filter(lambda x: x[0] != ".", os.listdir(writingSrcPath)))
writingSrcFolderNames.sort(key=dateOfWriting, reverse=True)


def replaceFile(path, converter):
    if os.path.isfile(path):
        with open(path, "r+") as f:
            converted = converter(f.read())
    else:
        converted = converter("")
    with open(path, "w+") as f:
        f.seek(0)
        f.write(converted)
        f.truncate()


# 스토리 수를 JS에 추가
def storyCntReplacer(js):
    equalIdx = js.find("=")
    semicolonIdx = js.find(";")
    return (
        js[: equalIdx + 1] + " " + str(len(writingSrcFolderNames)) + js[semicolonIdx:]
    )


replaceFile("./js/ui.js", storyCntReplacer)


def findIdxAfter(src, keyword):
    return src.find(keyword) + len(keyword)


def insertBtwHTML(htmlSrc, keywordContentList):
    converted = ""
    previousIdx = 0
    for keyword, content in keywordContentList.items():
        idx = findIdxAfter(htmlSrc, keyword)
        converted += htmlSrc[previousIdx:idx] + content
        previousIdx = idx
    converted += htmlSrc[previousIdx:]
    return converted


writingListContentIdx = findIdxAfter(writingListSrc, '<ol id="post-list">')
writingListHtml = writingListSrc[:writingListContentIdx]

markdowner = Markdown()

for folderName in writingSrcFolderNames:
    Path(writingDstPath + folderName).mkdir(parents=True, exist_ok=True)
    sourceFolderPath = os.path.join(writingSrcPath + folderName)
    for filename in os.listdir(sourceFolderPath):
        with open(os.path.join(sourceFolderPath, filename), "r") as storyFile:
            if filename == "content.md":
                # Making post html
                post = frontmatter.load(storyFile)
                converted = insertBtwHTML(
                    writingPostSrc,
                    {
                        "<h2>": post["title"],
                        "<h3>": str(post["date"]),
                        '<div id="post-content">': markdowner.convert(post.content),
                    },
                )
                writingPostPath = os.path.join(writingDstPath, folderName, "index.html")
                with open(writingPostPath, "w") as f:
                    f.write(converted)
                # Making post row html
                writingListHtml += insertBtwHTML(
                    writingRowSrc,
                    {
                        'href="': "writing/" + folderName,
                        "<h2>": post["title"],
                        '"post-row__date">': str(post["date"]),
                    },
                )
            else:
                copy2(sourceFolderPath + "/" + filename, writingDstPath + folderName)

writingListHtml += writingListSrc[writingListContentIdx:]
replaceFile(os.path.join("./stories/index.html"), lambda x: writingListHtml)

# ----------------------------------------------------------

sourcePath = "./src/til/"
htmlPath = "./stories/til/"

sourceFolderList = list(filter(lambda x: x[0] != ".", os.listdir(sourcePath)))

tilListContentIdx = findIdxAfter(tilListSrc, '"til-list">')
postListHtml = tilListSrc[:tilListContentIdx]


for fileName in sourceFolderList:
    with open(os.path.join(sourcePath, fileName), "r") as f:
        # Making post html
        post = frontmatter.load(f)
        postContent = markdowner.convert(post.content) + markdowner.convert(
            str(post["list"])
        )
        converted = insertBtwHTML(
            tilPostSrc, {"<h2>": post["date"], 'post-content">': postContent}
        )
        for key, val in post["list"].items():
            print(key, val)
        Path(htmlPath + post["date"]).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(htmlPath, post["date"], "index.html"), "w+") as file1:
            file1.write(converted)
        # Making post row html
        postListHtml += insertBtwHTML(
            tilRowSrc, {'href="': fileName[:-3], "<h2>": post["date"]}
        )

postListHtml += tilListSrc[tilListContentIdx:]
replaceFile(os.path.join("./stories/til/index.html"), lambda x: postListHtml)
