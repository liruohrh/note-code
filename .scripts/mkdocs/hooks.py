import re
from pathlib import Path

TAG_PATTERN = re.compile(r'(?<!\\)#([^\s#]+)')


def on_page_markdown(markdown, page, **kwargs):
    def repl(match):
        tag = match.group(1)
        return "\\#"+tag

    markdown = TAG_PATTERN.sub(repl, markdown)

    markdown = re.sub(r'^(#+) (.+)(\s*)$', r'#\1 \2\3', markdown, flags=re.M)
    return markdown


def on_page_context(context, **kwargs):
    # 在 on_template_context后执行，抛出 icon 属性错误后，都不会执行到此处
    # page = kwargs["page"]
    # if page.meta:
    #     page.meta.pop("icon", None)
    #     page.meta.pop("cssclass", None)
    #     page.meta.pop("cssclasses", None)
    return context


def on_template_context(context, **kwargs):
    """处理 404.html 等主题模板，清掉所有导航项里的 icon"""

    def strip(items):
        for item in items:
            if hasattr(item, "meta") and isinstance(item.meta, dict):
                item.meta.pop("icon", None)
            if hasattr(item, "children") and item.children:
                strip(item.children)

    if "nav" in context and context["nav"]:
        strip(context["nav"].items)
    return context


def build_nav(dir_path: Path, base=""):
    nav = []

    for item in sorted(dir_path.iterdir(), key=lambda p: (p.is_dir(), p.name.lower())):
        if item.name.startswith("."):
            continue

        if item.is_dir():
            children = build_nav(item, f"{base}{item.name}/")

            if children:
                nav.append({item.name: children})

        elif item.suffix == ".md":
            # if item.name == "index.md":
            #     continue

            nav.append({item.stem: f"{base}{item.name}"})

    return nav


def on_config(config):
    config["nav"] = build_nav(Path(config.docs_dir))
    return config
