from Init.files_manager import *
from jinja2 import Environment, FileSystemLoader

def alu_adi_down(work, circuit, pe_device, pe_l2, ipv4_iface,
            ipv6_iface, cpe, static_routing, bgp_routing):

    environment = {
        'DO_NUMBER': work['do_number'],
        'COUNTRY': circuit['country'],
        'WORK_TYPE': work['work_type'],
        'CID': circuit['cid_number'],
        'CID_LOCATION': circuit['cid_location'],
        'SERVICE_TYPE': work['service_type'],
        'IES_ID': circuit['ies_id'],

        'PE_HOSTNAME': pe_device['hostname'],
        'IFACE_NAME': pe_device['iface_name'],
        'DATA_UNIT': pe_device['subiface'],
        'CVLAN_ID': pe_l2['cvlan_id'],
        'SVLAN_ID': pe_l2['svlan_id'],

        'IPV4_LOCAL_NET': ipv4_iface['wan_net'],
        'IPV4_LOCAL_ADDR': ipv4_iface['local_address'],
        'IPV4_NEIGHBOR_ADDR': ipv4_iface['neighbor_address'],
        'IPV4_NETMASK_LENGTH': ipv4_iface['netmask_length'],
        'IPV4_LAN_NET': static_routing['ipv4_lan'],

        'IPV6_LOCAL_ADDRESS': ipv6_iface['local_address'],
        'IPV6_NEIGHBOR_ADDRESS': ipv6_iface['neighbor_address'],
        'IPV6_LAN_NET': static_routing['ipv6_lan'],
        'IPV6_NETMASK_LENGHT': ipv6_iface['netmask_length'],

        'BGP_ROUTING': bgp_routing['enabled'],
        'PEER_AS_NUMBER': bgp_routing['peer_as_number'],
        'IPV4_RECEIVED_PREFIXES': bgp_routing['ipv4_received_prefixes'],
        'IPV4_RECEIVED_THROUGH': bgp_routing['ipv4_received_prefixes_through'],
        'IPV6_RECEIVED_PREFIXES': bgp_routing['ipv6_received_prefixes'],
        'IPV6_RECEIVED_THROUGH': bgp_routing['ipv6_received_prefixes_through'],
        'SEND_FULL_TABLE': bgp_routing['send_full_table'],

        'STATIC_ROUTING': static_routing['enabled'],
        'STATIC_TAG': static_routing['tag'],
        'CPE_IPV4_ADDRESS': cpe['loopback_ipv4_address'][0],
    }

    loader = FileSystemLoader("/home/martin/PycharmProjects/CL_IPSA_Automation/Jinja_Templates")
    env = Environment(loader = loader, trim_blocks=True, lstrip_blocks=True)

    # Genera el PE-PRETASK
    file = get_pe_pretask_oper(work['do_number'], work['work_type'], circuit['country'])
    template = env.get_template('alu_adi_pre_down.j2')
    result = template.render(environment)
    with open(file.name, 'w') as pe_script:
        pe_script.write(result)
    # Genera el PE-SCRIPT
    file = get_pe_script(work['do_number'], work['work_type'], circuit['country'])
    template = env.get_template('alu_adi_down.j2')
    result = template.render(environment)
    with open(file.name, 'w') as pe_script:
        pe_script.write(result)
    # Genera el PE-POSTASK
    file = get_pe_postask_oper(work['do_number'], work['work_type'], circuit['country'])
    template = env.get_template('alu_adi_post_down.j2')
    result = template.render(environment)
    with open(file.name, 'w') as pe_script:
        pe_script.write(result)
    # Genera el INFO-CIERRE
    file = get_do_cierre(work['do_number'], work['work_type'], circuit['country'])
    template = env.get_template('alu_adi_down_cierre.j2')
    result = template.render(environment)
    with open(file.name, 'w') as pe_script:
        pe_script.write(result)



