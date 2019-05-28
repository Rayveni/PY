from flask import render_template,flash,request
from . import admin_bp
from json import load,dump
from os.path import isfile
import sys
#import os
#print(os.path.abspath(r'src/utils'))
sys.path.insert(0, r'src/utils')
from   myutils import exception 
config_fields=('db_name','assets','operations','host','port','user','user_pswd')
config_path='config.json'
error_msg_len=256

@admin_bp.route("/admin")
def index():
    config_exists = isfile(config_path)
    
    if config_exists:
        err,data=read_config(config_path)
    else:
        err,data=create_config(config_path)
    if not err[0]:
        flash(err[1],'error')  #success info error 
    data={k:('' if v is None else v ) for (k,v) in data.items() }
    return render_template('admin.html', data=data)

@admin_bp.route("/upload_mongo_form",methods=["POST"])#,methods=["POST"]
def upload_mongo_form():
    form_data=request.form.to_dict(flat=False)

    err,res=update_config(config_path,form_data)

    if not err[0]:
        flash(err[1],'error')  #success info error  
    elif not res[0]:
        flash(res[1],'error')  #success info error
    else:
        flash('Config updated','success')  #success info error  
    return render_template('admin.html',data=res[1])




@exception
def read_config(conf_path:str)->dict:
    with open(conf_path) as json_file:  
        data = load(json_file)
    return data

@exception    
def create_config(conf_path:str)->bool:
    data={'driver':'mongo'}
    for el in config_fields:
        data[el]=None
        
    with open(conf_path, 'w') as outfile:  
         dump(data, outfile)
    return data

@exception
def update_config(conf_path:str,form_data)->tuple:
    err,data=read_config(conf_path) 	
    if not err[0]:
        return (False,err[1])
    
    for param in config_fields:
        data[param]=form_data[f'mongo_{param}'][0]

    with open(conf_path, 'w') as outfile:  
        dump(data, outfile)

    return (True,data)

