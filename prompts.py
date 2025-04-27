from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape()
)

def script(args):
    return env.get_template('daily.prompt.jinja').render(args)

def voicing(args):
    return env.get_template('voicing.prompt.jinja').render(args)

