from __future__ import absolute_import
from __future__ import unicode_literals
import os
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
import warnings
from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_lexer_for_filename, guess_lexer, TextLexer
from pygments.formatters import HtmlFormatter


# ------------------ The Markdown Extension -------------------------------
class CodeBlockProTreeprocessor(Treeprocessor):
    """ Highlight source code in code blocks. """

    def run(self, root):
        """ Find code blocks and store in htmlStash. """
        blocks = root.getiterator('pre')
        for block in blocks:
            children = block.getchildren()
            if len(children) == 1 and children[0].tag == 'code':
                code = CodeBlockHilit(source_code = children[0].text,
                                    code_path = self.config["code_path"],
                                    linenos=self.config["linenos"],
                                    title_bar=self.config["title_bar"])
                c = code.hilit()
                if c:
                    placeholder = self.markdown.htmlStash.store(c,safe=True)
                    # Clear codeblock in etree instance
                    block.clear()
                    # Change to div element which will later
                    # be removed when inserting raw html
                    block.tag = 'div'
                    block.set('class', 'codeblock')
                    block.text = placeholder



class CodeBlockProExtension(Extension):
    """ Add source code hilighting to markdown codeblocks. """

    def __init__(self, configs):
        # define default configs
        self.config = {
            "code_path" : ["", "This is code file path which is default search path."],
            "linenos" : ["True",""],
            "title_bar" : ["header",""],
            }
        # Override defaults with user settings
        for key, value in configs.iteritems():
            # convert strings to booleans
            if value == 'True': value = True
            if value == 'False': value = False
            if value == 'None': value = None


            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        """ Add CodeBlockProcessor to Markdown instance. """
        codeblockpro = CodeBlockProTreeprocessor(md)
        codeblockpro.config = self.getConfigs()
        md.treeprocessors.add("codeblockpro", codeblockpro, "<inline")

        md.registerExtension(self)


def makeExtension(configs={}):
  return CodeBlockProExtension(configs=configs)

#--------------------Main CodeBlock Highlight Class----------------------
class CodeBlockHilit(object):

    TITLE_BAR = '<div class="title_bar %s"><span style="width: 20%%;">%s</span><span style="margin:0 auto;">%s</span><span style="width: 20%%; text-align:right;"><a href="%s">%s</a></span></div>'

    BLOCK_BODY = '<div class="block_body">%s</div>'
    
    def __init__(self, source_code=None, code_path="", linenos=True, title_bar = "header"):
        self.source_code = source_code
        self.code_path = code_path
        self.linenos = linenos
        self.lang = None
        self.hl_lines = []
        self.title = ""
        self.title_bar = title_bar
        self.src = ""

    def hilit(self):
        """
        Use pygments to highlight codeblock of Markdown
        returns : A string of html.
        """
        if not self.__parse_header():
            return None
        else:
            try:
                lexer = get_lexer_by_name(self.lang)
            except ValueError:
                lexer = TextLexer()
            formatter = HtmlFormatter(linenos=self.linenos,hl_lines=self.hl_lines)
            def get_codeblock_html(title):
                titleBar = self.TITLE_BAR % (title, self.lang, self.title, self.src, bool(self.src) * "view raw")
                blockBody = self.BLOCK_BODY % highlight(self.source_code, lexer, formatter)
                return titleBar,blockBody

            if "header" == self.title_bar:
                titleBar, blockBody = get_codeblock_html("title_bar_header")
                return titleBar + blockBody
            else:
                titleBar, blockBody = get_codeblock_html("title_bar_footer")
                return blockBody + titleBar

                

    def __parse_header(self):
        """
            Parse codeblock header, like this:

                :[lang=python]
                print "hello, world!"

            the string ":[lang=python]" will be parsed.
            self.lang = "python"

            return: Booleans.
                    True: successful parsing
                    False: failed parsing
        """
        lines = self.source_code.split("\n")
        header = lines.pop(0)

        import re
        reg1 = r"^:\[(?P<attr>.*)\]\((?P<src>.*)\)"
        reg2 = r"^:\[(?P<attr>.*)\]"
        src = ''
        attr = ''
        m = re.search(reg1,header)
        if m:
            attr = m.group('attr')
            src = m.group('src')
        else:
            m = re.search(reg2,header)
            if m:
                attr = m.group('attr')
            else:
                lines.insert(0,header)
                self.linenos = False
                return False

        if attr:
            try:
                self.lang = re.findall(r"lang=([^,]+)", attr)[0]
            except IndexError:
                pass

            try:
                cmd = "self.hl_lines = " + re.findall(r"hl_lines=(\[[\d,]+\])",attr)[0]
                exec(cmd)
            except IndexError:
                pass 

            try:
                self.title = re.findall(r"title=\"([^\"]+)", attr)[0]
            except IndexError:
                pass

            try:
                cmd = "self.linenos = " + re.findall(r"linenos=([^,]+)", attr)[0]
                exec(cmd)
            except IndexError:
                pass  

            try:
                self.title_bar = re.findall(r"title_bar=([^,]+)", attr)[0]
            except IndexError:
                pass

        
        if src :
            source_code = self.__load_file(src)
            if source_code:
                self.source_code = source_code
                self.src = src
        else:
            self.source_code = "\n".join(lines).strip("\n")
        return True

    def __load_file(self, src):
        """
        Load code file.
        return: A string of code.
        """
        if os.path.exists(src):
            filePath = src
        else:
            filePath = self.code_path + src

        if os.path.exists(filePath):
            f = open(filePath, "r")
            source_code = f.read()
            f.close()
            return source_code
        else:
            return None
