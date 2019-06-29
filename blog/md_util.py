import markdown

exts = [
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',
    'markdown.extensions.tables'
]


def md2html(md):
    return markdown.markdown(md, extensions=exts)
