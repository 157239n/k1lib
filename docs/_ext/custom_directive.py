
from k1lib.imports import *

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.docutils import SphinxDirective

import pygments; from pygments.lexers import PythonLexer, JavascriptLexer; from pygments.formatters import HtmlFormatter

g = {**globals()}
ctxD = defaultdict(lambda: g)

class pyexec(SphinxDirective):
    """Executes random Python code.
Example::

    .. pyexec:: pre True some_header

        s = "abc "
        s * 10
    
This will execute the cell and displays the result in a <pre> tag

:param mode: "pre" (display the output as-is. If it's not a string then use repr(content))
    or "html" (assumes output is a html string or an object that implements _repr_html_())
:param displaySource: (optional) if True, displays the source code before the output
:param header: (optional) Header of the segment (can't use spaces, replace them with underscore instead)
"""
    has_content = True
    required_arguments = 1
    optional_arguments = 2

    def run(self):
        docname = self.env.temp_data["docname"]
        src = pygments.highlight("\n".join(self.content), PythonLexer(), HtmlFormatter())
        exec("\n".join(self.content[:-1]), ctxD[docname])
        # print(self.content)
        res = eval(self.content[-1], ctxD[docname])
        _type = self.arguments[0]
        _htm = lambda s: [nodes.raw('', s, format='html')]
        def htm(s):
            ans = ""; header = self.arguments[2].replace("_", " ") if len(self.arguments) > 2 else None
            if len(self.arguments) > 1:
                if eval(self.arguments[1]): # displays source code
                    header = header or "Result"
                    ans += f"<h4>Source code</h4>{src}"
            if header: ans += f"<h4>{header}</h4>"
            ans += s; return _htm(f"<div style='margin-left: 30px'>{ans}</div>")
        if _type == "pre": # grab string ussing repr() and returns <pre>
            return htm(f"<pre style='overflow-x: auto'>{html.escape(res if isinstance(res, str) else repr(res))}</pre>")
        if _type == "js": # formatted js code
            return htm(pygments.highlight(res, JavascriptLexer(), HtmlFormatter()))
        elif _type == "html": # grab html string using _repr_html_(), or just itself if it's a string already
            if isinstance(res, str): return htm(res)
            return htm(res | toHtml())
        else: raise Exception(f"pyexec doesn't know about the tag type {_type}. Only 'pre' and 'html' are allowed")

def setup(app):
    print("---------- custom setup")
    app.add_directive("pyexec", pyexec)

    return {
        'version': '0.1',
    }

