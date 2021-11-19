import os
import shutil
import frontmatter
import json
from pathlib import Path
from shutil import copy2
from markdown2 import Markdown

# 기존 파일 삭제
shutil.rmtree("./stories/writing", ignore_errors=True)
shutil.rmtree("./stories/til", ignore_errors=True)

markdowner = Markdown()
root_path = Path(__file__).parent.parent

f = open(os.path.join(root_path, "gen/template/writing/post.html"), "r")
writing_post_template = f.read()
f.close()
f = open(os.path.join(root_path, "gen/template/writing/row.html"), "r")
writing_row_template = f.read()
f.close()
f = open(os.path.join(root_path, "gen/template/writing/list.html"), "r")
writing_list_template = f.read()
f.close()
f = open(os.path.join(root_path, "gen/template/til/list.html"), "r")
til_list_template = f.read()
f.close()
f = open(os.path.join(root_path, "gen/template/til/post.html"), "r")
til_post_template = f.read()
f.close()
f = open(os.path.join(root_path, "gen/template/til/row.html"), "r")
til_row_template = f.read()
f.close()
f = open(os.path.join(root_path, "gen/template/til/time_table.html"), "r")
til_time_table_template = f.read()
f.close()


def generate_post(src_path, dst_path, transform, key=None):
    writing_src_file_names = list(
        filter(lambda x: x[0] != ".", os.listdir(os.path.join(root_path, src_path)))
    )
    if key != None:
        writing_src_file_names.sort(key=date_of_story, reverse=True)

    for writing_src_file_name in writing_src_file_names:
        story_src_path = os.path.join(root_path, src_path, writing_src_file_name)
        story_dst_path = os.path.join(root_path, dst_path, writing_src_file_name)
        Path(story_dst_path).mkdir(parents=True, exist_ok=False)
        # 특정 글에 속한 모든 파일을 순회
        for writing_src_component_file_name in os.listdir(story_src_path):
            writing_src_component_file_path = os.path.join(
                story_src_path, writing_src_component_file_name
            )
            if writing_src_component_file_name == "content.md":
                with open(
                    os.path.join(writing_src_component_file_path), "r"
                ) as markdown_with_yaml:
                    markdown_with_yaml_divided = frontmatter.load(markdown_with_yaml)
                    writing_post = transform(
                        markdown_with_yaml_divided, writing_src_file_name
                    )
                    with open(os.path.join(story_dst_path, "index.html"), "w") as f:
                        f.write(writing_post)
            else:
                copy2(writing_src_component_file_path, story_dst_path)


writing_rows = ""


def writing_transform(markdown_with_yaml_divided, writing_src_file_name):
    title = markdown_with_yaml_divided["title"]
    date = markdown_with_yaml_divided["date"]
    markdown_converted = markdowner.convert(markdown_with_yaml_divided.content)
    writing_post = writing_post_template.format(
        title=title, date=date, content=markdown_converted
    )
    global writing_rows
    writing_rows += writing_row_template.format(
        link=f"/stories/writing/{writing_src_file_name}",
        title=title,
        date=str(date),
    )
    return writing_post


# 스토리 파일명 날짜순으로 정리
def date_of_story(path):
    p = os.path.join("./src/writing", path, "content.md")
    with open(p, "r+") as f:
        post = frontmatter.load(f)
        return post["date"]


generate_post("src/writing", "stories/writing", writing_transform, date_of_story)

with open(os.path.join("./stories/index.html"), "w") as f:
    f.write(writing_list_template.format(rows=writing_rows))

til_rows = ""


def til_transform(markdown_with_yaml_divided, writing_src_file_name):
    date = markdown_with_yaml_divided["date"]
    list = markdown_with_yaml_divided["list"]
    time_table = ""
    for time_table_title in list:
        time_table += til_time_table_template.format(
            title=time_table_title, time=list[time_table_title]
        )
    markdown_converted = markdowner.convert(markdown_with_yaml_divided.content)
    inner_title = "\n".join(date.split("-"))
    writing_post = til_post_template.format(
        date=inner_title, time_table=time_table, content=markdown_converted
    )
    global til_rows
    til_rows += til_row_template.format(link=f"{writing_src_file_name}", date=str(date))
    return writing_post


generate_post("src/til", "stories/til", til_transform)

with open(os.path.join("./stories/til/index.html"), "w") as f:
    f.write(til_list_template.format(rows=til_rows))
