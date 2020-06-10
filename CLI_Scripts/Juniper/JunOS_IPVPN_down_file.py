from Init.files_manager import *
from jinja2 import Environment, FileSystemLoader

def junos_ipvpn_down_file(customer, work, circuit, pe_device, pe_l2, ipv4_iface,
            ipv6_iface, cpe, nid, qos, static_routing, bgp_routing, routing_instance):

    environment = {
        'CID': circuit['cid_number'],
        'CUSTOMER_NAME': customer['name'],
        'CID_LOCATION': circuit['cid_location'],
        'SERVICE_TYPE': work['service_type'],
        'IES_ID': circuit['ies_id'],

        'IFACE_NAME': pe_device['iface_name'],
        'DATA_UNIT': pe_device['subiface'],

        'IPV4_LOCAL_ADDRESS': ipv4_iface['local_address'],
        'IPV4_NEIGHBOR_ADDRESS': ipv4_iface['neighbor_address'],
        'IPV4_NETMASK_LENGHT': ipv4_iface['netmask_length'],
        'IPV4_LAN_NET': static_routing['ipv4_lan'],

        'IPV6_LOCAL_ADDRESS': ipv6_iface['local_address'],
        'IPV6_NEIGHBOR_ADDRESS': ipv6_iface['neighbor_address'],
        'IPV6_LAN_NET': static_routing['ipv6_lan'],
        'IPV6_NETMASK_LENGHT': ipv6_iface['netmask_length'],

        'TOTAL_BW': qos['new_bandwidth'],

        'BGP_ROUTING': bgp_routing['enabled'],
        'PEER_AS_NUMBER': bgp_routing['peer_as_number'],
        'IPV4_RECEIVED_PREFIXES': bgp_routing['ipv4_received_prefixes'],
        'IPV4_RECEIVED_THROUGH': bgp_routing['ipv4_received_prefixes_through'],
        'IPV6_RECEIVED_PREFIXES': bgp_routing['ipv6_received_prefixes'],
        'IPV6_RECEIVED_THROUGH': bgp_routing['ipv6_received_prefixes_through'],
        'SEND_FULL_TABLE': bgp_routing['send_full_table'],

        'STATIC_ROUTING': static_routing['enabled'],
        'CPE_IPV4_ADDRESS': cpe['loopback_ipv4_address'][0],

        'DATA_VRF': routing_instance['name'],
        'DATA_VRF_EXIST': routing_instance['exists'],
        'DATA_VRF_TARGET_IMPORT': routing_instance['rt_import'],
        'DATA_VRF_TARGET_EXPORT': routing_instance['rt_export'],
        'DATA_VRF_RD': routing_instance['rd'],
        'DATA_VRF_RID': routing_instance['rid']
    }


    file = get_pe_script(work['do_number'], work['work_type'], circuit['country'])

    loader = FileSystemLoader("/home/martin/PycharmProjects/CL_IPSA_Automation/Jinja_Templates")
    env = Environment(loader = loader, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('junos_ipvpn_down.j2')

    result = template.render(environment)

    with open(file.name, 'a') as pe_script:
        pe_script.write(result)