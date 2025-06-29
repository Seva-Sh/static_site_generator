import re

from enum import Enum
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    output_list = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            output_list.append(node)
            continue

        split_list = node.text.split(delimiter, 2)
        
        for item in split_list:
            if split_list.index(item) == 1:
                match delimiter:
                    case "`":
                        output_list.append(TextNode(item, TextType.CODE))
                    case "**":
                        output_list.append(TextNode(item, TextType.BOLD))
                    case "_":
                        output_list.append(TextNode(item, TextType.ITALIC))
            else:
                output_list.append(TextNode(item, TextType.TEXT))

    return output_list

def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
     
def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    delimiter_phrase = "_img_"
    delimiter = "_"
    output_list = []

    for node in old_nodes:
        extracted_images = extract_markdown_images(node.text)
        extracted_images_idx = 0
        text_without_img = re.sub(r"\!\[(.*?)\]\((.*?)\)", delimiter_phrase, node.text) 
        split_list = text_without_img.split(delimiter)

        if len(split_list) == 1:
            output_list.append(node)
            continue

        for item in split_list:
            if item == "img":
                current_img = extracted_images[extracted_images_idx]
                output_list.append(TextNode(current_img[0], TextType.IMAGE, current_img[1]))
                extracted_images_idx += 1
            elif item == "":
                continue
            else:
                output_list.append(TextNode(item, TextType.TEXT))

    
    return output_list

def split_nodes_link(old_nodes):
    delimiter_phrase = "_link_"
    delimiter = "_"
    output_list = []

    for node in old_nodes:
        extracted_links = extract_markdown_links(node.text)
        extracted_links_idx = 0
        text_without_links = re.sub(r"\[(.*?)\]\((.*?)\)", delimiter_phrase, node.text)
        split_list = text_without_links.split(delimiter)

        if len(split_list) == 1:
            output_list.append(node)
            continue

        for item in split_list:
            if item == "link":
                current_link = extracted_links[extracted_links_idx]
                output_list.append(TextNode(current_link[0], TextType.LINK, current_link[1]))
                extracted_links_idx += 1
            elif item == "":
                continue
            else:
                output_list.append(TextNode(item, TextType.TEXT))
    
    return output_list

def split_check(output, test):
    condition = True

    while condition:
        if test == "**":
            new_output = split_nodes_delimiter(output, "**", TextType.BOLD)
        elif test == "`":
            new_output = split_nodes_delimiter(output, "`", TextType.CODE)
        elif test == "_":
            new_output = split_nodes_delimiter(output, "_", TextType.ITALIC)
        elif test == "img":
            new_output = split_nodes_image(output)
        elif test == "link":
            new_output = split_nodes_link(output)

        if new_output == output:
            condition = False
        output = new_output
    
    return output


def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    output = [text_node]
    split_tests = ["**", "`", "_", "img", "link"]

    for test in split_tests:
        output = split_check(output, test)

    # while condition:
    #     new_output = split_nodes_delimiter(output, "**", TextType.BOLD)
    #     if new_output == output:
    #         condition = False
    #     output = new_output


    # output = split_nodes_delimiter(output, "**", TextType.BOLD)
    # output = split_nodes_delimiter(output, "`", TextType.CODE)
    # output = split_nodes_delimiter(output, "_", TextType.ITALIC)
 
    # output = split_nodes_image(output)
    # output = split_nodes_link(output)

    return output

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        if block == "":
            continue
        else:
            stripped_blocks.append(block.strip())
    
    return stripped_blocks

# Block Type Code Implementation

class BlockType(Enum):
    P = "paragraph"
    H = "heading"
    C = "code"
    Q = "quote"
    UL = "unordered_list"
    OL = "ordered_list"

def check_headings(block):
    if " " in block:
        split_block = block.split(" ")
        hash_count = split_block[0].count("#")
        if hash_count > 0 and hash_count < 7:
            return True

    return False

def check_code(block):
    if block[:3] == "```" and block[-3:] == "```":
        return True
    return False

def check_quote(block):
    if "\n" in block or block[0] == ">":
        split_lines = block.split("\n")
        split_lines = list(filter(None, split_lines))
        return all(line[0] == ">" for line in split_lines)
    
    return False
    
def check_ul(block):
    if "\n" in block:
        split_lines = block.split("\n")
        split_lines = list(filter(None, split_lines))
        return all(line.split(" ")[0] == "-" for line in split_lines)

    return False

def check_ol(block):
    if "\n" in block:
        split_lines = block.split("\n")
        split_lines = list(filter(None, split_lines))
        return all(line.split(" ")[0][1] == "." for line in split_lines)

    return False

def block_to_block_type(block):
    if check_headings(block):
        return BlockType.H
    elif check_code(block):
        return BlockType.C
    elif check_quote(block):
        return BlockType.Q
    elif check_ul(block):
        return BlockType.UL
    elif check_ol(block):
        return BlockType.OL
    else:
        return BlockType.P

# Block to HTML code implementation

class BlockType(Enum):
    P = "paragraph"
    H = "heading"
    C = "code"
    Q = "quote"
    UL = "unordered_list"
    OL = "ordered_list"


def markdown_paragraph_to_html_node(block_text):
    if "\n" in block_text:
        block_text = " ".join(block_text.split("\n"))
    children_list = list(map(lambda node: text_node_to_html_node(node), text_to_textnodes(block_text)))
    return ParentNode("p", children_list)

def markdown_header_to_html_node(block_text):
    split_block = block_text.split(" ")
    hash_count = split_block[0].count("#")

    children_list = list(map(lambda node: text_node_to_html_node(node), text_to_textnodes(" ".join(split_block[1:]))))

    return ParentNode(f"h{hash_count}", children_list)

def markdown_code_to_html_node(block_text):
    code_text = block_text.split("```")[1][1:]
    code_node = [LeafNode("code", code_text)]

    return ParentNode("pre", code_node)

def markdown_quote_to_html_node(block_text):
    split_lines = block_text.split("\n")
    split_lines = list(filter(None, split_lines))
    mapped_lines = list(map(lambda line: line[2:], split_lines))
    str = (" ".join(mapped_lines))

    children_list = list(map(lambda node: text_node_to_html_node(node), text_to_textnodes(str)))

    return ParentNode("blockquote", children_list)

def markdown_list_to_html_node(block_text, list_type):
    li_children = []
    split_lines = block_text.split("\n")
    split_lines_cleaned = list(filter(None, split_lines))

    for line in split_lines_cleaned:
        if list_type == "ul":
            children_list = list(map(lambda node: text_node_to_html_node(node), text_to_textnodes(line[2:])))
        else:
            children_list = list(map(lambda node: text_node_to_html_node(node), text_to_textnodes(line[3:])))
        li_children.append(ParentNode("li", children_list))
        # li_children.append(LeafNode("li", line[2:]))

    if list_type == "ul":
        return ParentNode("ul", li_children)
    else:
        return ParentNode("ol", li_children)

def block_node_to_html_node(block_type, block_text):
    match block_type:
        case BlockType.P:
            return markdown_paragraph_to_html_node(block_text)
        case BlockType.H:
            return markdown_header_to_html_node(block_text)
        case BlockType.C:
            return markdown_code_to_html_node(block_text)
        case BlockType.Q:
            return markdown_quote_to_html_node(block_text)
        case BlockType.UL:
            return markdown_list_to_html_node(block_text, "ul")
        case BlockType.OL:
            return markdown_list_to_html_node(block_text, "ol")
        case _:
            raise Exception

def markdown_to_html_node(markdown):
    children_blocks = []
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        children_blocks.append(block_node_to_html_node(block_type, block))

    return ParentNode("div", children_blocks)



md = """
# Why Glorfindel is More Impressive than Legolas

[< Back Home](/)

![Glorfindel image](/images/glorfindel.png)

> "The deeds of Glorfindel shine bright as the morning sun, whilst the feats of others are as the flickering of stars in the night sky."

In J.R.R. Tolkien's legendarium, characterized by its rich tapestry of noble heroes and epic deeds, two Elven luminaries stand out: **Glorfindel**, the stalwart warrior returned from the Halls of Mandos, and **Legolas**, abc
"""

print(markdown_to_html_node(md))