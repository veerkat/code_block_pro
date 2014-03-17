code_block_pro
==============

A Highlight Code Block Extension of Python-Markdown.

### How to use


    import markdown
    from code_block_pro import CodeBlockProExtension
    markdown.markdown(some_text, extensions=[CodeBlockProExtension({})])
  
`{}` is a dict of configs.

configs:

   `"code_path"` default: "", code file path.
     
   `"linenos"` default: "True", value is "True" or "False", add line number to code.
     
   `"title_bar"` default: "header", value is "header" or "footer", show the title bar of CodeBlock.
    
### Markdown Syntax

    like this
        :[lang=python]
        print "hello, world."
    
    
the `:[]` is mark of highlighting code block.
