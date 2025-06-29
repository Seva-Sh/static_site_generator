from textnode import TextNode
from helper_func import markdown_to_html_node
import shutil
import os

def copy_source_to_destination(dest_path, source_path, cleaned=False):
    public_path = dest_path

    if cleaned == False and os.path.exists("public"):
        shutil.rmtree("public")
        os.mkdir("public")
    elif os.path.exists("public") == False:
        os.mkdir("public")

    static_list = os.listdir(source_path)
    static_path = source_path

    for item in static_list:
        if os.path.isfile(os.path.join(static_path, item)):
            shutil.copy(os.path.join(static_path, item), os.path.join(public_path, item))
        else:
            os.mkdir(os.path.join(public_path, item))
            copy_source_to_destination(os.path.join(public_path, item), os.path.join(static_path, item), True)

def extract_title(markdown):
    split_md = markdown.split("\n")
    for line in split_md:
        if line.split(" ")[0] == "#":
            return " ".join(line.split(" ")[1:])
    raise Exception

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_md = open(from_path).read()
    template_html = open(template_path).read()
    dest_file = open(dest_path, "x")

    header = extract_title(from_md)
    from_md_to_html = markdown_to_html_node(from_md).to_html()

    template_html = template_html.replace("{{ Title }}", header)
    template_html = template_html.replace("{{ Content }}", from_md_to_html)
    dest_file.write(template_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    public_path = dest_dir_path
    content_path = dir_path_content

    content_list = os.listdir(dir_path_content)

    for item in content_list:
        if os.path.isfile(os.path.join(content_path, item)):
            generate_page(os.path.join(content_path, item), template_path, os.path.join(public_path, item.replace("md", "html")))
        else:
            os.mkdir(os.path.join(public_path, item))
            generate_pages_recursive(os.path.join(content_path, item), template_path, os.path.join(public_path, item))




def main():
    text_node = TextNode("Anchor text", "link", "https://www.boot.dev")
    # Copy all static files from static to public
    copy_source_to_destination("public", "static")
    # Generate a page from context/index.md using template.md and write to public/index.html
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")
main()

