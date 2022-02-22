"""Rendor -- convert markdown files to HTML."""

import argparse
import os
import re
import shutil
import sys
from typing import List, Optional

import jinja2
import markdown

DEFAULT_TEMPLATE = '''\
<html>
  <head>
    <title>{{ title }}</title>
  </head>
  <body>
{{ body }}
  </body>
</html>
'''
TITLE_RX = re.compile('<h1>(.*)</h1>')


class TemplateLoader(jinja2.FileSystemLoader):
    """A template loader that adds a special path: 'default'.

    It is mapped to either default or provided template.
    """

    def __init__(self, *args, **kw):
        self.default_path = kw.pop('default_path', None)
        super().__init__(*args, **kw)

    def get_source(self, environment, template):
        if template == 'default':
            if self.default_path is None:
                return DEFAULT_TEMPLATE, None, lambda: True
            template = self.default_path
        return super().get_source(environment, template)


def rendor(inputs: List[str], outdir: str, template: Optional[str]):
    """Render all `inputs` to `outdir`."""
    if template is not None:
        template = os.path.relpath(template)
    jinja_env = jinja2.Environment(
        loader=TemplateLoader(os.getcwd(), default_path=template),
        autoescape=jinja2.select_autoescape(),
    )

    for input in inputs:
        in_path = os.path.abspath(input)
        relative_path = os.path.relpath(in_path)
        out_path = os.path.join(outdir, relative_path)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        base, ext = os.path.splitext(out_path)
        if ext.lower() == '.md':
            out_path = base + '.html'
            with open(in_path, 'rt', encoding='utf-8') as in_fp:
                with open(
                    out_path,
                    'wt',
                    encoding='utf-8',
                    errors='xmlcharrefreplace',
                ) as out_fp:
                    rendored = markdown.markdown(in_fp.read())
                    if match := TITLE_RX.search(rendored):
                        title = match.group(1)
                    else:
                        title, _ = os.path.splitext(relative_path)
                    template = jinja_env.get_template('default')
                    out_fp.write(template.render(title=title, body=rendored))
        elif ext.lower() in {'.j2', '.jinja2'}:
            template = jinja_env.get_template(relative_path)
            out_path = base + '.html'
            with open(
                out_path,
                'wt',
                encoding='utf-8',
                errors='xmlcharrefreplace',
            ) as out_fp:
                out_fp.write(template.render())
        else:
            shutil.copy(in_path, out_path)


def main(args=None):
    """CLI."""
    args = args or sys.argv
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inputs', nargs='+', help='Input files')
    parser.add_argument(
        '--outdir',
        '-o',
        default='html',
        help='Output directory (will overwrite existing files)',
    )
    parser.add_argument(
        '--template',
        '-t',
        default=None,
        help='Page template (Jinja2)',
    )
    args = parser.parse_args(args)
    rendor(args.inputs, outdir=args.outdir, template=args.template)


if __name__ == '__main__':
    main()
