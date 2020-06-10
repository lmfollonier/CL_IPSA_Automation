from Init.files_manager import *
from jinja2 import Environment, FileSystemLoader

def alu_adi_bw_update(work, pe_device, pe_l2, circuit, qos):

    environment = {
        'IES_ID': circuit['ies_id'],
        'IFACE_NAME': pe_device['iface_name'],
        'DATA_UNIT': pe_device['subiface'],
        'CVLAN_ID': pe_l2['cvlan_id'],
        'SVLAN_ID': pe_l2['svlan_id'],

        'QOS_ID': qos['qos_profile_id'],
        'NEW_QOS_ID': qos['new_qos_profile_id'],
        'QOS_PROFILE_DESCRIPTION': qos['qos_profile_description'],
        'TOTAL_BW': qos['new_bandwidth'],
    }


    file = get_pe_script(work['do_number'], work['work_type'], circuit['country'])

    loader = FileSystemLoader("/home/martin/PycharmProjects/CL_IPSA_Automation/Jinja_Templates")
    env = Environment(loader = loader, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('alu_bw_update.j2')
    result = template.render(environment)
    print(result)

    with open(file.name, 'a') as pe_script:
        pe_script.write(result)