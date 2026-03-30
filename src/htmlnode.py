from __future__ import annotations


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("implement in child classes")

    def props_to_html(self):
        if not self.props:
            return ""
        prop_list = []
        for key, value in self.props.items():
            prop_list.append(f"{key}={value}")
        return " ".join(prop_list)

    def __eq__(self, value):
        if (
            self.tag == value.tag
            and self.value == value.value
            and self.children == value.children
            and self.props == value.props
        ):
            return True
        return False

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str, props: dict[str, str] | None = None
    ):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if not self.value:
            raise ValueError("must have a value")
        if not self.tag:
            return self.value
        props = self.props_to_html()
        props_str = f" {props}" if props else ""
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None
    ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("must have a tag")
        if not self.children:
            raise ValueError("must have children")
        out = ""
        for child in self.children:
            out += child.to_html()

        props = self.props_to_html()
        props_str = f" {props}" if props else ""
        return f"<{self.tag}{props_str}>{out}</{self.tag}>"
