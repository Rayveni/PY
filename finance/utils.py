def often_used_libs(matplotlib_magic='inline',show_all_pandas_columns=True):
    from importlib import import_module
    global np,pd,plt,sns

    np = import_module("numpy")
    print('imported numpy as np')
    pd=import_module("pandas")
    print('imported pandas as pd')
    sns=import_module("seaborn")
    print('imported seaborn as sns')
    if show_all_pandas_columns:pd.set_option('display.max_columns', None)

    if matplotlib_magic==None:
        pass
    else:
        from IPython import get_ipython	
        ipython = get_ipython()
        ipython.magic("matplotlib {}".format(matplotlib_magic))
        print('%matplotlib {}'.format(matplotlib_magic))





def jupyter_style(max_alight_left=True,dataftame_border=True,border_width_px=1,border_color='black'):
    from IPython.core.display import HTML
    css_expression=[]
    if max_alight_left:
        css_expression.append('.MathJax_Display {text-align: left !important;}')
    
    if dataftame_border:
        css_expression.append(
            """   .rendered_html table, .rendered_html th, .rendered_html tr, .rendered_html td {{
              border: {0}px  {1} solid !important;
              color: {1} !important;}}
            """ .format(border_width_px,border_color))
    
    css_expression='<style>'+'\n'.join(css_expression)+'</style>'
    return HTML(css_expression)