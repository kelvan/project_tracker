from os.path import join
import subprocess
import codecs

from settings import *

from jinja2 import Environment


def get_environment():
    # The environment
    latex_jinja_env = Environment(block_start_string='\BLOCK{',
                                  block_end_string='}',
                                  variable_start_string='\VAR{',
                                  variable_end_string='}',
                                  comment_start_string='\#{',
                                  comment_end_string='}',
                                  line_statement_prefix='%-',
                                  line_comment_prefix='%#',
                                  trim_blocks=True,
                                  autoescape=False)
    return latex_jinja_env


def compile_latex(no, content):
    texfile = join(texdir, '%s.tex' % no)
    with codecs.open(texfile, encoding='utf-8', mode='w') as f:
        f.write(content)

    subprocess.call(['pdflatex', '-output-directory', pdfdir, texfile],
                    stdout=subprocess.PIPE)
    return join(pdfdir, '%s.pdf' % no)


def get_template():
    env = get_environment()
    with open(join(invoicedirectory, templatefile), 'r') as f:
        t = f.read()
    return env.from_string(t)


def pdflatex(invoice):
    return compile_latex(invoice.number,
                         get_template().render(invoice=invoice))
