from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children 
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        str = ""
        if self.props == None:
            return str

        for key in self.props.keys():
            str += f" {key}=\"{self.props[key]}\""
        return str
    
    def __repr__(self):
        return f"HTMLNode object {self.tag}, {self.value}, {self.children}, {self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        elif self.tag == None:
            return str(self.value)
        else:
            opening_tag = f"<{self.tag}"
            closing_tag = f"</{self.tag}>"
            if self.props == None:
                opening_tag += ">"
            else:
                opening_tag += self.props_to_html() + ">"

            return opening_tag + self.value + closing_tag

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("The tag is missing")
        elif self.children == None:
            raise ValueError("Children nodes are missing")
        else:
            val = ""
            opening_tag = f"<{self.tag}>"
            closing_tag = f"</{self.tag}>"

            for child in self.children:
                val += child.to_html()

            return opening_tag + val + closing_tag



