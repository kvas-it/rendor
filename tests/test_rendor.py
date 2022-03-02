import os

from rendor import main


def expect_html(title, body):
    return f'''\
<html>
  <head>
    <title>{title}</title>
  </head>
  <body>
{body}
  </body>
</html>'''


def test_one_page(tmpdir):
    os.chdir(str(tmpdir))
    infile = tmpdir.join('index.md')
    infile.write('# Foo')
    outdir = tmpdir.join('html')
    main([str(infile)])
    outfile = outdir.join('index.html')
    assert outfile.read() == expect_html('Foo', '<h1>Foo</h1>')


def test_static(tmpdir):
    os.chdir(str(tmpdir))
    infile = tmpdir.join('index.html')
    infile.write('Foo')
    outdir = tmpdir.join('out')
    main(['-o', str(outdir), str(infile)])
    outfile = outdir.join('index.html')
    assert outfile.read() == 'Foo'


def test_template(tmpdir):
    os.chdir(str(tmpdir))
    infile = tmpdir.join('index.j2')
    infile.write('{{ 1 + 1 }}')
    outdir = tmpdir.join('out')
    main(['-o', str(outdir), str(infile)])
    outfile = outdir.join('index.html')
    assert outfile.read() == '2'


def test_alt_template(tmpdir):
    os.chdir(str(tmpdir))
    in1 = tmpdir.join('template.j2')
    in1.write('foo {{ title }}')
    in2 = tmpdir.join('index.md')
    in2.write('# bar')
    outdir = tmpdir.join('out')
    main(['-o', str(outdir), '-t', str(in1), str(in2)])
    outfile = outdir.join('index.html')
    assert outfile.read() == 'foo bar'


def test_subdirs(tmpdir):
    os.chdir(str(tmpdir))
    in1 = tmpdir.mkdir('foo').join('index.md')
    in1.write('# Foo')
    in2 = tmpdir.mkdir('bar').join('index.html')
    in2.write('Bar')
    outdir = tmpdir.join('html')
    main([str(in1), str(in2)])
    out1 = outdir.join('foo', 'index.html')
    assert out1.read() == expect_html('Foo', '<h1>Foo</h1>')
    out2 = outdir.join('bar', 'index.html')
    assert out2.read() == 'Bar'
