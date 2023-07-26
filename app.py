#!/bin/env python3

from flask import Flask, request, render_template,make_response
from flask_sqlalchemy import SQLAlchemy
from db import database
from db import sqldb
import base64
import json
import html
#from jinja2 import Markup
from collections import namedtuple
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///system_info.db'  # Change the database URL as per your requirement
db = database.initialize_sqldb(app)




@app.route('/systeminfo/<machinename>', methods=['POST'])
def store_system_info(machinename):
       
    system_info = database.SystemInfo.query.filter_by(machine_name=machinename).first()
    data = request.get_json()

    #Determine if the item exists
    if system_info:
        #Update the item with newly received data
    
        SystemInfoTuple = namedtuple('SystemInfoTuple', data.keys())

        # # Convert the JSON data to a named tuple
        system_info_tuple = SystemInfoTuple(**data)

        # # Convert the named tuple to an object
    
        siTmp = database.SystemInfo()
        siTmp.__dict__ = system_info_tuple._asdict()

        system_info.operating_system = siTmp.operating_system
        system_info.version = siTmp.version
        system_info.manufacturer = siTmp.manufacturer
        system_info.model = siTmp.model
        system_info.total_memory = siTmp.total_memory
        system_info.disks = json.dumps(data['disks'])
        system_info.system_type = siTmp.system_type
        system_info.hostname = siTmp.hostname
        system_info.python_version = siTmp.python_version
        system_info.processor_type = siTmp.processor_type
        system_info.processor_cores = siTmp.processor_cores
        system_info.processor_threads = siTmp.processor_threads
        system_info.network_adapters = json.dumps(siTmp.network_adapters)
        system_info.dell_service_tag = siTmp.dell_service_tag



        


    else:
        #Create new Item
        system = database.SystemInfo(
            machine_name=machinename,
            operating_system=data['operating_system'],
            version=data['version'],
            manufacturer=data['manufacturer'],
            model=data['model'],
            total_memory=data['total_memory'],
            disks=data['disks'],
            system_type=data['system_type'],
            hostname=data['hostname'],
            python_version=data['python_version'],
            processor_type=data['processor_type'],
            processor_cores=data['processor_cores'],
            processor_threads=data['processor_threads'],
            network_adapters=data['network_adapters'],
            dell_service_tag=data['dell_service_tag']
        )
        sqldb.session.add(system)
    sqldb.session.commit()

    return 'System information stored successfully.'
###Build wrapper if the SH version is called
@app.route('/sysinfo.sh')
def sysinfo_bash():
    app_url = request.host_url
    sysinfo_content = render_template('sysinfo.py', app_url=app_url)

    wrapper_content = render_template('sysinfo.sh', python_script=base64.b64encode(sysinfo_content.encode()).decode())
    response = make_response(wrapper_content)

    response.headers['Content-Disposition'] = 'attachment; filename=sysinfo.bash'
    response.headers['Content-Type'] = 'text/plain'

    return response

### Send the python file and update with the API location
@app.route('/sysinfo.py')
def sysinfo_python():
    app_url = request.host_url
    sysinfo_content = render_template('sysinfo.py', app_url=app_url)

    response = make_response(sysinfo_content)

    response.headers['Content-Disposition'] = 'attachment; filename=sysinfo.py'
    response.headers['Content-Type'] = 'text/plain'

    return response

@app.route('/sysinfo.ps1')
def sysinfo_powershell():
    app_url = request.host_url
    sysinfo_content = render_template('sysinfo.ps1', app_url=app_url)

    response = make_response(sysinfo_content)

    response.headers['Content-Disposition'] = 'attachment; filename=sysinfo.ps1'
    response.headers['Content-Type'] = 'text/plain'

    return response

@app.route('/')
def index():
    machines = database.SystemInfo.query.all()
    return render_template('index.html', machines=machines)

@app.route('/machine/<int:machine_id>')
def machine_details(machine_id):
    system_info = database.SystemInfo.query.get(machine_id)
    network = html.unescape(system_info.network_adapters)
    disks= html.unescape(system_info.disks)
    return render_template('machine.html', system_info=system_info, network=network,disks=disks)

if __name__ == '__main__':

   
    app.run()
