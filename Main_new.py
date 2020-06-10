import sys
from ipaddress import ip_network


from CLI_Scripts.ALU.ALU_ADI_up_file import alu_adi_up_file, alu_adi_up_file2
from CLI_Scripts.ALU.ALU_BW_update_file import alu_adi_bw_update
from CLI_Scripts.Juniper.JunOS_BW_update import junos_bw_update_file2
from CLI_Scripts.Juniper.JunOS_IPVPN_down_file import junos_ipvpn_down_file
from CLI_Scripts.Juniper.JunOS_IPVPN_up_file import junos_ipvpn_up_file2
from Init.files_manager import init_do_files
import xlrd, xlsxwriter

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

if pe_device['vendor'] == "NOKIA":
    ies_worksheet_name = pe_device['hostname'] + "-ies-table"
    ies_worksheet = workbook.sheet_by_name(ies_worksheet_name)

    for row_num in range(0, ies_worksheet.nrows):
        row_value = ies_worksheet.cell_value(row_num,1)
        if row_value == (pe_device['iface_name'] + ":" + str(pe_l2['svlan_id']) + "." + str(pe_l2['cvlan_id']) ):
            print(int(ies_worksheet.cell_value(row_num,0)))
            circuit['ies_id'] = int(ies_worksheet.cell_value(row_num, 0))
            break
        else:
            circuit['ies_id'] = "no existe"
            #circuit['new_ies_profile_id'] = int(ies_worksheet.cell_value(row_num, 0)) + 1

    if circuit['ies_id'] == "no existe":
        print('verificar ies con: admin display-config | match context all ' + pe_device['iface_name'] + ":" + str(pe_l2['svlan_id']) + "." + str(pe_l2['cvlan_id']))
        sys.exit()


ipv4_iface = {
    'wan_net'           : '',
    'netmask_length'    : 30,
    'local_address'     : '',
    'lan_net'           : '3.3.3.0/10',
    'neighbor_address'  : ''
}
ipv4_iface['wan_net'] = ip_network(worksheet.cell_value(27, 1))
ipv4_iface['local_address'] = (ipv4_iface['wan_net'].network_address + 1).compressed
ipv4_iface['neighbor_address'] = (ipv4_iface['wan_net'].network_address + 2).compressed
ipv4_iface['netmask_length'] = ipv4_iface['wan_net'].prefixlen

ipv6_iface = {
    'wan_net'           : '',
    'netmask_length'    : 30,
    'local_address'     : '',
    'lan_net'           : '20005::0/10',
    'neighbor_address'  :  '',
}
if worksheet.cell_value(30, 1):
    ipv6_iface['wan_net'] = ip_network(worksheet.cell_value(30, 1))
    ipv6_iface['local_address'] = (ipv6_iface['wan_net'].network_address + 1).compressed
    ipv6_iface['neighbor_address'] = (ipv6_iface['wan_net'].network_address + 2).compressed
    ipv6_iface['netmask_length'] = ipv6_iface['wan_net'].prefixlen

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
cpe['loopback_ipv4_address'] = worksheet.cell_value(42, 1).split('/')

nid = {
    'rfs': '',
    'ipv4_address'  : ''
}
nid['rfs'] = int(worksheet.cell_value(45, 1))
nid['ipv4_address'] = worksheet.cell_value(46, 1)

qos = {
    'qos_profile_id'                : 146,
    'new_qos_profile_id'            : '',
    'qos_profile_description'       : '',
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

qos['old_bandwidth'] = int(worksheet.cell_value(50, 1))
qos['new_bandwidth'] = int(worksheet.cell_value(51, 1))
qos['new_bandwidth_ef_percent'] = int(worksheet.cell_value(52, 1))
qos['new_bandwidth_ef_de_percent'] = int(worksheet.cell_value(53, 1))
qos['new_burst_size'] = int(qos['new_bandwidth'] * 0.0375)
qos['new_bandwidth_ef'] = int(qos['new_bandwidth'] * qos['new_bandwidth_ef_percent'] / 100)
qos['new_burst_size_ef'] = int(qos['new_bandwidth_ef'] * 0.0375)
qos['new_bandwidth_ef_de'] = int(qos['new_bandwidth'] * qos['new_bandwidth_ef_de_percent'] / 100)
qos['new_burst_size_ef_de'] = int(qos['new_bandwidth_ef_de'] * 0.0375)

if pe_device['vendor'] == "NOKIA":
    qos_worksheet_name = pe_device['hostname'] + "-qos-table"
    qos_worksheet = workbook.sheet_by_name(qos_worksheet_name)

    for row_num in range(0, qos_worksheet.nrows):
        row_value = int(qos_worksheet.cell_value(row_num,2))
        if row_value == int(qos['new_bandwidth']):
            print(int(qos_worksheet.cell_value(row_num,0)))
            qos['qos_profile_id'] = int(qos_worksheet.cell_value(row_num, 0))
            break
        else:
            qos['qos_profile_id'] = "no existe"
            qos['new_qos_profile_id'] = int(qos_worksheet.cell_value(row_num, 0)) + 1

    if qos['qos_profile_id'] == "no existe":
        if qos['new_bandwidth'] >= 1000000:
            qos_desc_bw = round(qos['new_bandwidth']/1000000,1)
            qos_desc_post = str(qos_desc_bw) + "G"
            qos['qos_profile_description'] = 'CUSTOMER-' + qos_desc_post
        elif qos['new_bandwidth'] >= 1000:
            qos_desc_bw = int(qos['new_bandwidth'] / 1000)
            qos_desc_post = str(qos_desc_bw) + "M"
            qos['qos_profile_description'] = 'CUSTOMER-' + qos_desc_post
        else:
            qos_desc = str(qos['new_bandwidth']) + "K"
            qos['qos_profile_description'] = 'CUSTOMER-' + qos_desc_post
        print('No existe el qos_profile hay que crear el qos profile: ' + qos['qos_profile_description'] + ', id: ' + str(qos['new_qos_profile_id']) + " con el BW:" + str(qos['new_bandwidth']))
        sys.exit()

# Genera estaticas a la loopback del CPE, y a la LAN
static_routing = {
    'enabled'    : False,
    'ipv4_lan' : "",
    'ipv6_lan': "",
    'tag'               : '10'
}
static_routing['enabled'] = worksheet.cell_value(56, 1)
static_routing['ipv4_lan'] = worksheet.cell_value(57, 1)
static_routing['ipv6_lan'] = worksheet.cell_value(58, 1)
static_routing['tag'] = int(worksheet.cell_value(59, 1))

bgp_routing = {
    'enabled'               : True,
    'peer_as_number'            : 10753,
    'ipv4_received_prefixes'    : "",
    'ipv4_received_prefixes_through'    : "",
    'ipv6_received_prefixes'    : "",
    'ipv6_received_prefixes_through': "",
# TODO: Agregar flags (override,remove_private, etc)
    'send_full_table':  False
}
bgp_routing['enabled'] = worksheet.cell_value(62, 1)
bgp_routing['peer_as_number'] = int(worksheet.cell_value(63, 1))
# TODO no se como hacerlo
bgp_routing['ipv4_received_prefixes'] = worksheet.cell_value(64, 1).split(',')
bgp_routing['ipv4_received_prefixes_through'] = worksheet.cell_value(65, 1).split(',')
bgp_routing['ipv6_received_prefixes'] = worksheet.cell_value(66, 1).split(',')
bgp_routing['ipv6_received_prefixes_through'] = worksheet.cell_value(67, 1).split(',')
bgp_routing['send_full_table'] = worksheet.cell_value(68, 1)

# Crea la estructura de directorios y archivos

init_do_files(work['do_number'], work['work_type'], circuit['country'])


if pe_device['vendor'] == "NOKIA":
    if (work['service_type'] == "ADI" or work['service_type'] == "DIA") and work['work_type'] == "ALTA":
        """alu_adi_up(cid_number, customer_id, customer_name, cid_location, service_type, ies_id, iface_name, cvlan_id, svlan_id,
        ipv4_local_address, ipv4_neighbor_address, ipv4_netmask_lenght, ipv6_local_address, ipv6_neighbor_address,
        ipv6_netmask_lenght, qos_profile_id, total_bandwidth, peer_as_number, ipv4_received_prefixes,
        ipv6_received_prefixes, send_full_table, ipv4_lan_net, cpe_ipv4_address, ipv6_lan_net, static_routing, bgp_routing)"""
        """alu_adi_up_file(
            work['do_number'],
            circuit['country'],
            work['work_type'],
            circuit['cid_number'],
            customer['id'],
            customer['name'],
            circuit['cid_location'],
            work['service_type'],
            circuit['ies_id'],
            pe_device['iface_name'],
            pe_l2['cvlan_id'],
            pe_l2['svlan_id'],
            ipv4_iface['local_address'],
            ipv4_iface['neighbor_address'],
            ipv4_iface['netmask_length'],
            ipv6_iface['local_address'],
            ipv6_iface['neighbor_address'],
            ipv6_iface['netmask_length'],
            qos['qos_profile_id'],
            qos['new_bandwidth'],
            bgp_routing['peer_as_number'],
            bgp_routing['ipv4_received_prefixes'],
            bgp_routing['ipv6_received_prefixes'],
            bgp_routing['send_full_table'],
            # Esto es para la estatica de la LAN. Agregarlo al excel
            static_routing['ipv4_lan'],
            cpe['loopback_ipv4_address'],
            # Esto es para la estatica de la LAN. Agregarlo al excel
            static_routing['ipv6_lan'],
            static_routing['enabled'],
            bgp_routing['enabled'])
        """
        alu_adi_up_file2(
            customer,
            work,
            circuit,
            pe_device,
            pe_l2,
            ipv4_iface,
            ipv6_iface,
            cpe,
            nid,
            qos,
            static_routing,
            bgp_routing)
    elif work['work_type'] == "UPGRADE" or work['work_type'] == "DOWNGRADE":
        alu_adi_bw_update(work, pe_device, pe_l2, circuit, qos)
    else:
        print("Solo esta hecho ADI, y cambio de BW para NOKIA")
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
        junos_bw_update_file2(pe_device, qos, work, circuit)
    elif work['work_type'] == "BAJA":
        junos_ipvpn_down_file(
            customer, work, circuit, pe_device, pe_l2, ipv4_iface,
            ipv6_iface, cpe, nid, qos, static_routing, bgp_routing, routing_instance)
    else:
        print("Solo esta hecho IPVPN UP, BW_UPDATE y BAJA para JUNIPER")
else:
    print("Eso todavía no esta hecho...")