from Init.files_manager import *
from jinja2 import Environment, FileSystemLoader


def junos_bw_update_file(do_number,
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
                         bgp_routing,
                         old_bandwidth,
                         new_bandwidth,
                         new_bandwidth_ef_percent,
                         new_bandwidth_ef_de_percent):


    new_burst_size: int = int(new_bandwidth * 0.0375)
    new_bandwidth_ef: int = int(new_bandwidth * new_bandwidth_ef_percent / 100)
    new_burst_size_ef: int = int(new_bandwidth_ef * 0.0375)
    new_bandwidth_ef_de: int = int(new_bandwidth * new_bandwidth_ef_de_percent / 100)
    new_burst_size_ef_de: int = int(new_bandwidth_ef_de * 0.0375)

    environment = {"OLD_BW": old_bandwidth, "NEW_BW": new_bandwidth, "NEW_BS": new_burst_size, "DATA_IFACE": iface_name,
                   "DATA_UNIT": cvlan_id, "NEW_EF_BW": new_bandwidth_ef, "NEW_EF_BS": new_burst_size_ef,
                   "NEW_EF_DE_BW": new_bandwidth_ef_de, "NEW_EF_DE_BS": new_burst_size_ef_de}

    # file = get_pe_script(do_number, work_type, country)

    loader = FileSystemLoader("/home/martin/PycharmProjects/CL_IPSA_Automation/Jinja_Templates")
    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('junos_bw_update.j2')

    result = template.render(environment)

    print(result)

    # with open(file.name, 'w') as pe_script:
    #    pe_script.write(result)

def junos_bw_update_file2(pe_device_data, qos_data, work, circuit):

    environment = {
        "OLD_BW"        : qos_data['old_bandwidth'],
        "NEW_BW"        : qos_data['new_bandwidth'],
        "NEW_BS"        : qos_data['new_burst_size'],
        "NEW_EF_BW"     : qos_data['new_bandwidth_ef'],
        "NEW_EF_BS"     : qos_data['new_burst_size_ef'],
        "NEW_EF_DE_BW"  : qos_data['new_bandwidth_ef_de'],
        "NEW_EF_DE_BS"  : qos_data['new_burst_size_ef_de'],
        'AF_BW'         : qos_data['new_bandwidth_af'],
        'AF_BS'         : qos_data['new_burst_size_af'],
        'AF_DE_BW'      : qos_data['new_bandwidth_af_de'],
        'AF_DE_BS'      : qos_data['new_burst_size_af_de'],
        'VPN_BE_BW'     : qos_data['new_bandwidth_vpn_be'],
        'VPN_BE_BS'     : qos_data['new_burst_size_vpn_be'],
        "DATA_IFACE"    : pe_device_data['iface_name'],
        "DATA_UNIT"     : pe_device_data['subiface']
    }

    file = get_pe_script(work['do_number'], work['work_type'], circuit['country'])

    loader = FileSystemLoader("/home/martin/PycharmProjects/CL_IPSA_Automation/Jinja_Templates")
    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('junos_bw_update.j2')

    result = template.render(environment)

    print(result)

    with open(file.name, 'w') as pe_script:
        pe_script.write(result)