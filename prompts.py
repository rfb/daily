from template import template

def mkprompt(args):
    return template('daily.prompt.jinja').render(args)

def mkvoicing(args):
    return template('voicing.prompt.jinja').render(args)

