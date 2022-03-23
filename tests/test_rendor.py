import os

import pytest

from rendor import main


@pytest.fixture
def srcdir(tmpdir):
    os.chdir(str(tmpdir))
    return tmpdir


def expect_html(title, body):
    return f'''\
<html>
  <head>
    <meta charset="utf-8">
    <title>{title}</title>
  </head>
  <body>
{body}
  </body>
</html>'''


def test_one_page(srcdir):
    infile = srcdir.join('index.md')
    infile.write('# Foo')
    outdir = srcdir.join('html')
    main([str(infile)])
    outfile = outdir.join('index.html')
    assert outfile.read() == expect_html('Foo', '<h1>Foo</h1>')


def test_static(srcdir):
    infile = srcdir.join('index.html')
    infile.write('Foo')
    outdir = srcdir.join('out')
    main(['-o', str(outdir), str(infile)])
    outfile = outdir.join('index.html')
    assert outfile.read() == 'Foo'


def test_template(srcdir):
    infile = srcdir.join('index.j2')
    infile.write('{{ 1 + 1 }}')
    outdir = srcdir.join('out')
    main(['-o', str(outdir), str(infile)])
    outfile = outdir.join('index.html')
    assert outfile.read() == '2'


def test_links(srcdir):
    infile = srcdir.join('index.md')
    infile.write('[Foo](foo.md)')
    outdir = srcdir.join('html')
    main([str(infile)])
    outfile = outdir.join('index.html')
    exp = expect_html('index', '<p><a href="foo.html">Foo</a></p>')
    assert outfile.read() == exp


def test_alt_template(srcdir):
    in1 = srcdir.join('template.j2')
    in1.write('foo {{ title }}')
    in2 = srcdir.join('index.md')
    in2.write('# bar')
    outdir = srcdir.join('out')
    main(['-o', str(outdir), '-t', str(in1), str(in2)])
    outfile = outdir.join('index.html')
    assert outfile.read() == 'foo bar'


def test_subdirs(srcdir):
    in1 = srcdir.mkdir('foo').join('index.md')
    in1.write('# Foo')
    in2 = srcdir.mkdir('bar').join('index.html')
    in2.write('Bar')
    outdir = srcdir.join('html')
    main([str(in1), str(in2)])
    out1 = outdir.join('foo', 'index.html')
    assert out1.read() == expect_html('Foo', '<h1>Foo</h1>')
    out2 = outdir.join('bar', 'index.html')
    assert out2.read() == 'Bar'


def test_extension(srcdir):
    # We employ a shortcut here: check that whatever we pass via -x gets to
    # markdown.markdown() and that it tries to import it. The rest should be
    # done by the markdown engine, which we assume works.
    infile = srcdir.join('index.md')
    infile.write('# Foo')
    with pytest.raises(ModuleNotFoundError) as err:
        main(['-x', 'foo_bar', str(infile)])
    assert err.type == ModuleNotFoundError
    assert str(err.value) == "No module named 'foo_bar'"
