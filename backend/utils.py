import os

def load_template(template_name=""):
    template_dir = os.path.dirname(__file__)+'/templates/'
    f = open(template_dir+template_name+'.html')
    _template = f.read()
    f.close()
    return _template 
