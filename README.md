code_block_pro
==============

A Highlight Code Block Extension of Python-Markdown Using Pygments.

How To Use
----------

    import markdown
    from code_block_pro import CodeBlockProExtension
    markdown.markdown(some_text, extensions=[CodeBlockProExtension({})])
  
`{}` is a dict of configs.

Configs:

* `"code_path"`  default: "", code file path.
* `"linenos"`  default: "True", value is "True" or "False", add line number to code.
* `"title_bar"`  default: "header", value is "header" or "footer", show the title bar of CodeBlock.
    
Note: if you use the extension, please include `codeblockui.css` and `pygments.css` in html file, `codeblockui.css` provides a ui style and `pygments.css` provides a code highlight style, you can also alter them that you like.

Markdown Syntax
---------------

    like this
        
        :[lang=python,title="Python Test"]
        print "hello, world."
    
    sometext...
    
    
It will look like this:

![img](https://github.com/veerkat/code_block_pro/raw/master/preview/preview.png)

`:[]` is mark of highlighting code block. You can set some configs in `[]`,

such as `:[lang=python,title="python test", linenos=False, title_bar=footer]`.

All configs in markdown syntax:

* `lang`: set language of code.
* `title`: set title of code block.
* `linenos`: set whether to show line number. default: True.
* `title_bar`: set title bar show head or foot of code block. default: header.

Highlight a code file:

    like this
    
        :[lang=python](your_codefile_path/file.py)
        
    if you set code_path=your_codefile_path, like this
    
        :[lang=python](file.py)
        
    sometext...
    

