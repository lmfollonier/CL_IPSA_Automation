from CLI_Scripts.ALU.ALU_ADI_up_file import alu_adi_up_file
from CLI_Scripts.Juniper.JunOS_BW_update import junos_bw_update_file
from CLI_Scripts.Juniper.JunOS_IPVPN_up_file import junos_ipvpn_up_file
from Init.files_manager import init_do_files

"""
Datos iniciales necesarios para generar la estructura de archivos de la Dokuorder
"""
# Estas variables cambian entre ordenes TODO: "Sacar de Excel"

do_number: int = 7415942
work_type: str = "DOWNGRADE"
country: str = "ECUADOR"


#init_do_files(do_number, work_type, country)

# TODO: Hay que ver como hacer para que estos parametros se obtengan solos, incluye partes gráficas
# Parametros administrativos
cid_number: int = 500073072
customer_id: str = "\"1238\""
customer_name: str = "BROADNET"
cid_location: str = "TLP GYE"
ies_id: str = "\"28715\""

# Parametros del equipo / fisico / L2
vendor: str = "JUNIPER"
iface_name: str = "ae10"
cvlan_id: int = 4219
svlan_id: int = 25

# Parametros de servicio
service_type: str = "IPVPN"

# IPv4
ipv4_local_address: str = "200.32.69.45"
ipv4_neighbor_address: str = "200.32.69.46"
ipv4_netmask_lenght: int = 30
ipv4_lan_net: str = ""

cpe_ipv4_address: str = ""


# IPv6
ipv6_local_address: str = ""
ipv6_neighbor_address: str = "2001:13B0:E000:1DC::2"
ipv6_netmask_lenght: int = 64
ipv6_lan_net:str = "2000::8/64"

# QoS
qos_profile_id: int = 146
total_bandwidth: int = 1024
old_bandwidth: int = 3072
new_bandwidth: int = 1536
new_bandwidth_ef_percent: int = 10
new_bandwidth_ef_de_percent: int = 30

# Static Routing
# Genera estaticas a la loopback del CPE, y a la LAN
static_routing: bool = False

# BGP
bgp_routing: bool = True
peer_as_number: int = 10753
ipv4_received_prefixes = ["190.216.103.53/32", "190.216.103.54/32", "201.234.202.160/29"]
ipv6_received_prefixes = ["2803:c2c0::/32 through 48"]
# TODO: Agregar flags (override,remove_private, etc)
send_full_table: bool = False

if vendor == "NOKIA":
    if service_type == "ADI" or service_type == "DIA":
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
elif vendor == "JUNIPER":
    if service_type == "IPVPN" and work_type == "ALTA":
        junos_ipvpn_up_file(do_number, country, work_type,cid_number, customer_id, customer_name, cid_location, service_type, ies_id, iface_name, cvlan_id, svlan_id,
        ipv4_local_address, ipv4_neighbor_address, ipv4_netmask_lenght, ipv6_local_address, ipv6_neighbor_address,
        ipv6_netmask_lenght, qos_profile_id, total_bandwidth, peer_as_number, ipv4_received_prefixes,
        ipv6_received_prefixes, send_full_table, ipv4_lan_net, cpe_ipv4_address, ipv6_lan_net, static_routing, bgp_routing)
        print("Work in progess...")
    elif work_type == "DOWNGRADE" or service_type == "UPGRADE":
        junos_bw_update_file(do_number, country, work_type, cid_number, customer_id, customer_name, cid_location,
                            service_type, ies_id, iface_name, cvlan_id, svlan_id,
                            ipv4_local_address, ipv4_neighbor_address, ipv4_netmask_lenght, ipv6_local_address,
                            ipv6_neighbor_address,
                            ipv6_netmask_lenght, qos_profile_id, total_bandwidth, peer_as_number,
                            ipv4_received_prefixes,
                            ipv6_received_prefixes, send_full_table, ipv4_lan_net, cpe_ipv4_address, ipv6_lan_net,
                            static_routing, bgp_routing, old_bandwidth, new_bandwidth, new_bandwidth_ef_percent, new_bandwidth_ef_de_percent)
    else:
        print("Solo esta hecho IPVPN UP, y BW_UPDATE para JUNIPER")
else:
    print("Eso todavía no esta hecho...")