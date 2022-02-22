# Rendor

Rendor is a simple static site generator that can turn a folder with markdown
files into a website.

    $ rendor [-o OUTDIR] [-t TEMPLATE] INPUT [INPUT ...]

All `.md` files will be converted to HTML (extension will be changed to
`.html`). All other files will be copied verbatim.

If `TEMPLATE` is specified, it must be a Jijnja2 template that will be used for
all markdown pages. It will be passed `title` and `body` variables where
`title` is the content of the first `<h1>` in the rendered markdown and `body`
is all of it.
