from Init.files_manager import *
from jinja2 import Environment, FileSystemLoader

def junos_ipvpn_up_file(do_number,
               country,
               work_type,
               cid_number,
               customer_id,
               customer_name,
               cid_location,
               service_type,
               ies_id, iface_name,
               cvlan_id, svlan_id,
               ipv4_local_address,
               ipv4_neighbor_address,
               ipv4_netmask_lenght,
               ipv6_local_address,
               ipv6_neighbor_address,
               ipv6_netmask_lenght,
               qos_profile_id,
               total_bandwidth,
               peer_as_number,
               ipv4_received_prefixes,
               ipv6_received_prefixes,
               send_full_table,
               ipv4_lan_net,
               cpe_ipv4_address,
               ipv6_lan_net,
               static_routing,
               bgp_routing):

    environment = {'DO_NUMBER': do_number,
        'COUNTRY': country,
        'WORK_TYPE': work_type,
        'CID': cid_number,
        'CUSTOMER_ID': customer_id,
        'CUSTOMER_NAME': customer_name,
        'CID_LOCATION': cid_location,
        'SERVICE_TYPE': service_type,
        'IES_ID': ies_id,
        'IFACE_NAME': iface_name,
        'CVLAN_ID': cvlan_id,
        'SVLAN_ID': svlan_id,
        'IPV4_LOCAL_ADDRESS': ipv4_local_address,
        'IPV4_NEIGHBOR_ADDRESS': ipv4_neighbor_address,
        'IPV4_netmask_LENGHT': ipv4_netmask_lenght,
        'IPV6_LOCAL_ADDRESS': ipv6_local_address,
        'IPV6_NEIGHBOR_ADDRESS': ipv6_neighbor_address,
        'IPV6_NETMASK_LENGHT': ipv6_netmask_lenght,
        'QOS_PROFILE_ID': qos_profile_id,
        'TOTAL_BW': total_bandwidth,
        'PEER_AS_NUMBER': peer_as_number,
        'IPV4_RECEIVED_PREFIXES': ipv4_received_prefixes,
        'IPV6_RECEIVED_PREFIXES': ipv6_received_prefixes,
        'SEND_FULL_TABLE': send_full_table,
        'IPV4_LAN_NET': ipv4_lan_net,
        'CPE_IPV4_ADDRESS': cpe_ipv4_address,
        'IPV6_LAN_NET': ipv6_lan_net,
        'STATIC_ROUTING': static_routing,
        'BGP_ROUTING': bgp_routing,
        'DATA_UNIT': '1200',
        'DATA_VRF': 'pepito',
        'DATA_VRF_EXIST': False,
        'EF_BW': '',
        'TOTAL_BS': '1234',
        'EF_BS': '4321',
        'DATA_VRF_TARGET': '65400:79564',
        'DATA_VRF_RD': "",
        'DATA_VRF_RID': ""}

    file = get_pe_script(do_number, work_type, country)

    loader = FileSystemLoader("/home/martin/PycharmProjects/CL_IPSA_Automation/Jinja_Templates")
    env = Environment(loader = loader, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('junos_ipvpn_up.j2')

    result = template.render(environment)

    with open(file.name, 'w') as pe_script:
        pe_script.write(result)


def junos_ipvpn_up_file2(customer, work, circuit, pe_device, pe_l2, ipv4_iface,
            ipv6_iface, cpe, nid, qos, static_routing, bgp_routing, routing_instance):

    environment = {
        'DO_NUMBER': work['do_number'],
        'COUNTRY': circuit['country'],
        'WORK_TYPE': work['work_type'],
        'CID': circuit['cid_number'],
        'CUSTOMER_ID': customer['id'],
        'CUSTOMER_NAME': customer['name'],
        'CID_LOCATION': circuit['cid_location'],
        'SERVICE_TYPE': work['service_type'],
        'IES_ID': circuit['ies_id'],

        'IFACE_NAME': pe_device['iface_name'],
        'DATA_UNIT': pe_device['subiface'],
        'CVLAN_ID': pe_l2['cvlan_id'],
        'SVLAN_ID': pe_l2['svlan_id'],

        'IPV4_LOCAL_ADDRESS': ipv4_iface['local_address'],
        'IPV4_NEIGHBOR_ADDRESS': ipv4_iface['neighbor_address'],
        'IPV4_NETMASK_LENGHT': ipv4_iface['netmask_length'],
        'IPV4_LAN_NET': static_routing['ipv4_lan'],

        'IPV6_LOCAL_ADDRESS': ipv6_iface['local_address'],
        'IPV6_NEIGHBOR_ADDRESS': ipv6_iface['neighbor_address'],
        'IPV6_LAN_NET': static_routing['ipv6_lan'],
        'IPV6_NETMASK_LENGHT': ipv6_iface['netmask_length'],

        'QOS_PROFILE_ID': qos['qos_profile_id'],
        'TOTAL_BW': qos['new_bandwidth'],
        'TOTAL_BS': qos['new_burst_size'],
        'EF_BW': qos['new_bandwidth_ef'],
        'EF_BS': qos['new_burst_size_ef'],
        'EF_DE_BW': qos['new_bandwidth_ef_de'],
        'EF_DE_BS': qos['new_burst_size_ef_de'],

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
    template = env.get_template('junos_ipvpn_up.j2')

    result = template.render(environment)

    with open(file.name, 'a') as pe_script:
        pe_script.write(result)