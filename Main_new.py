from typing import Dict

from CLI_Scripts.ALU.ALU_ADI_up_file import alu_adi_up_file
from CLI_Scripts.Juniper.JunOS_BW_update import junos_bw_update_file2
from CLI_Scripts.Juniper.JunOS_IPVPN_up_file import junos_ipvpn_up_file2
from Init.files_manager import init_do_files

import xlrd
workbook = xlrd.open_workbook('/home/martin/Downloads/do.xlsx')
worksheet = workbook.sheet_by_name('VARS')

"""
Datos iniciales necesarios para generar la estructura de archivos de la Dokuorder
"""
# Estas variables cambian entre ordenes TODO: "Sacar de Excel"

# Parametros administrativos TODO: Hay que ver como hacer para que estos parametros se obtengan solos, incluye partes gráficas

customer = {
    'id'   : 1238,
    'name' : 'BROADNET'
}

customer['id'] = int(worksheet.cell_value(1,1))
customer['name'] = worksheet.cell_value(2, 1)

work = {
    'do_number'     : 7415942,
    'work_type'     : 'DOWNGRADE',
    'service_type'  : 'IPVPN'
    }
work['do_number'] = int(worksheet.cell_value(5,1))
work['work_type'] = worksheet.cell_value(6, 1)
work['service_type'] = worksheet.cell_value(7, 1)

circuit = {
    'country'       : 'ECUADOR',
    'cid_number'    : 500073072,
    'cid_location'  : 'TLP GYE',
    'ies_id'        : 28715,
    'siebel_id'     : ''
}
circuit['country'] = worksheet.cell_value(10, 1)
circuit['cid_number'] = int(worksheet.cell_value(11, 1))
circuit['cid_location'] = worksheet.cell_value(12, 1)
circuit['ies_id'] = int(worksheet.cell_value(13, 1))
circuit['siebel_id'] = worksheet.cell_value(14, 1)

pe_device = {
    'vendor'    : 'JUNIPER',
    'hostname'  : '',
    'iface_name': 'ae10',
    'subiface'  : '45632'
    }
pe_device['vendor'] = worksheet.cell_value(17, 1)
pe_device['hostname'] = worksheet.cell_value(18, 1)
pe_device['iface_name'] = worksheet.cell_value(19, 1)
pe_device['subiface'] = int(worksheet.cell_value(20, 1))

pe_l2 = {
    'cvlan_id' : 4219,
    'svlan_id' : 25
    }
pe_l2['cvlan_id']  = int(worksheet.cell_value(23, 1))
pe_l2['svlan_id']  = int(worksheet.cell_value(24, 1))

ipv4_iface = {
    'local_address'    : '200.32.69.45',
    'neighbor_address' :  '200.32.69.46',
    'netmask_lenght'   :  30,
    'lan_net'          :  ""
}
ipv4_iface['lan_net'] = worksheet.cell_value(27, 1)

ipv6_iface = {
    'local_address'    : '',
    'neighbor_address' : '2001:13B0:E000:1DC::2',
    'netmask_lenght'   : 64,
    'lan_net'          : '2000::8/64'
}
ipv6_iface['lan_net'] = worksheet.cell_value(30, 1)
routing_instance = {
    'name'      : '',
    'exists'    : '',
    'rt_import' : ['',''],
    'rt_export' : ['',''],
    'rd'        : '',
    'rid'       :''
}
routing_instance['name'] = worksheet.cell_value(33, 1)
routing_instance['exists'] = worksheet.cell_value(34, 1)
routing_instance['rt_import'] = worksheet.cell_value(35, 1)
routing_instance['rt_export'] = worksheet.cell_value(36, 1)
routing_instance['rd'] = worksheet.cell_value(37, 1)
routing_instance['rid'] = worksheet.cell_value(38, 1)

cpe = {
    'rfs': '',
    'iface_ipv4_address'  : '',
    'loopback_ipv4_address': '',
}
cpe['rfs'] = int(worksheet.cell_value(41, 1))
cpe['loopback_ipv4_address'] = worksheet.cell_value(42, 1)

nid = {
    'rfs': '',
    'ipv4_address'  : ''
}
nid['rfs'] = int(worksheet.cell_value(45, 1))
nid['ipv4_address'] = worksheet.cell_value(46, 1)

qos = {
    'qos_profile_id'                : 146,
    'total_bandwidth'               : 1024, # TODO: Sacarlo
    'old_bandwidth'                 : 3072,
    'new_bandwidth'                 : 1536,
    'new_burst_size'                : '',
    'new_bandwidth_ef_percent'      : 10,
    'new_bandwidth_ef'              : '',
    'new_burst_size_ef'             : '',
    'new_bandwidth_ef_de_percent'   : 30,
    'new_bandwidth_ef_de'           : '',
    'new_burst_size_ef_de'          : ''
}
qos['qos_profile_id'] = int(worksheet.cell_value(49, 1))
qos['old_bandwidth'] = int(worksheet.cell_value(50, 1))
qos['new_bandwidth'] = int(worksheet.cell_value(51, 1))
qos['new_bandwidth_ef_percent'] = int(worksheet.cell_value(52, 1))
qos['new_bandwidth_ef_de_percent'] = int(worksheet.cell_value(53, 1))
qos['new_burst_size'] = int(qos['new_bandwidth'] * 0.0375)
qos['new_bandwidth_ef'] = int(qos['new_bandwidth'] * qos['new_bandwidth_ef_percent'] / 100)
qos['new_burst_size_ef'] = int(qos['new_bandwidth_ef'] * 0.0375)
qos['new_bandwidth_ef_de'] = int(qos['new_bandwidth'] * qos['new_bandwidth_ef_de_percent'] / 100)
qos['new_burst_size_ef_de'] = int(qos['new_bandwidth_ef_de'] * 0.0375)

# Genera estaticas a la loopback del CPE, y a la LAN
static_routing = {
    'enabled'    : False,
    'tag'               : '10'
}
static_routing['enabled'] = worksheet.cell_value(56, 1)
static_routing['tag'] = int(worksheet.cell_value(57, 1))

bgp_routing = {
    'enabled'               : True,
    'peer_as_number'            : 10753,
    'ipv4_received_prefixes'    : [
        ('190.216.103.53/32', 32),
        ('190.216.103.54/32', 32),
        ('201.234.202.160/29', 29)
    ],
    'ipv6_received_prefixes'    : [
        ('2803:c2c0::/32', 48)
    ],
# TODO: Agregar flags (override,remove_private, etc)
    'send_full_table':  False
}
bgp_routing['enabled'] = worksheet.cell_value(60, 1)
bgp_routing['peer_as_number'] = int(worksheet.cell_value(61, 1))
# TODO no se como hacerlo
#bgp_routing['ipv4_received_prefixes']
#bgp_routing['ipv6_received_prefixes']
bgp_routing['send_full_table'] = worksheet.cell_value(64, 1)

# Crea la estructura de directorios y archivos

init_do_files(work['do_number'], work['work_type'], circuit['country'])


if pe_device['vendor'] == "NOKIA":
    if work['service_type'] == "ADI" or work['service_type'] == "DIA":
        """alu_adi_up(cid_number, customer_id, customer_name, cid_location, service_type, ies_id, iface_name, cvlan_id, svlan_id,
        ipv4_local_address, ipv4_neighbor_address, ipv4_netmask_lenght, ipv6_local_address, ipv6_neighbor_address,
        ipv6_netmask_lenght, qos_profile_id, total_bandwidth, peer_as_number, ipv4_received_prefixes,
        ipv6_received_prefixes, send_full_table, ipv4_lan_net, cpe_ipv4_address, ipv6_lan_net, static_routing, bgp_routing)"""
        alu_adi_up_file(do_number, country, work_type,cid_number, customer_id, customer_name, cid_location, service_type, ies_id, iface_name, cvlan_id, svlan_id,
        ipv4_local_address, ipv4_neighbor_address, ipv4_netmask_lenght, ipv6_local_address, ipv6_neighbor_address,
        ipv6_netmask_lenght, qos_profile_id, total_bandwidth, peer_as_number, ipv4_received_prefixes,
        ipv6_received_prefixes, send_full_table, ipv4_lan_net, cpe_ipv4_address, ipv6_lan_net, static_routing, bgp_routing)
    else:
        print("Solo esta hecho ADI para NOKIA")
elif pe_device['vendor'] == "JUNIPER":
    if work['service_type'] == "IPVPN" and work['work_type'] == "ALTA":
        """junos_ipvpn_up_file(do_number, country, work_type,cid_number, customer_id, customer_name, cid_location, service_type, ies_id, iface_name, cvlan_id, svlan_id,
        ipv4_local_address, ipv4_neighbor_address, ipv4_netmask_lenght, ipv6_local_address, ipv6_neighbor_address,
        ipv6_netmask_lenght, qos_profile_id, total_bandwidth, peer_as_number, ipv4_received_prefixes,
        ipv6_received_prefixes, send_full_table, ipv4_lan_net, cpe_ipv4_address, ipv6_lan_net, static_routing, bgp_routing)"""
        print("Work in progess...")
        junos_ipvpn_up_file2(
            customer, work, circuit, pe_device, pe_l2, ipv4_iface,
            ipv6_iface, cpe, nid, qos, static_routing, bgp_routing, routing_instance)

    elif work['work_type'] == "DOWNGRADE" or work['work_type'] == "UPGRADE":
        junos_bw_update_file2(pe_device, qos)
    else:
        print("Solo esta hecho IPVPN UP, y BW_UPDATE para JUNIPER")
else:
    print("Eso todavía no esta hecho...")