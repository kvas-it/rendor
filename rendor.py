"""Rendor -- convert markdown files to HTML."""

import argparse
import os
import shutil
import sys
from typing import List

import markdown


def rendor(inputs: List[str], outdir: str):
    """Render all `inputs` to `outdir`."""
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
                    out_fp.write(markdown.markdown(in_fp.read()))
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
    args = parser.parse_args(args)
    print(args)
    rendor(args.inputs, args.outdir)


if __name__ == '__main__':
    main()
