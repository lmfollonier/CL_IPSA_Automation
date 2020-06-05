
def alu_adi_up(cid_number,
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

    iface_description: str = customer_name + " [" + cid_location + ", CID:" + str(cid_number) + "]"
    iface_full: str = "\"" + iface_name + ":" + str(cvlan_id) + "." + str(svlan_id) + "\""

    # Pongo la jerarquia acá para que el comando no quede tan largo:
    ies_path: str = "/configure service ies " + ies_id + " "

    # TODO: Creación del cliente

    # Creación del IES
    print(ies_path + "customer " + customer_id + " create")
    print(ies_path + "no shutdown")
    print("")

    # Configuracion de Interfaz
    print(ies_path + "interface " + iface_full + " create")
    print(ies_path + "interface " + iface_full + " no shutdown")
    print(ies_path + "interface " + iface_full + " description \"CUSTOMER: IMPS-CLI: " + iface_description + " " + service_type + "@" + str(int(total_bandwidth/1000)) + "Mbps")
    print(ies_path + "interface " + iface_full + " enable-ingress-stats")
    print(ies_path + "interface " + iface_full + " urpf-check mode loose")
    print(ies_path + "interface " + iface_full + " tos-marking-state trusted")
    print(ies_path + "interface " + iface_full + " cflowd-parameters sampling unicast type interface")
    print(ies_path + "interface " + iface_full + " address " + ipv4_local_address + "/" + str(ipv4_netmask_lenght))
    if ipv6_local_address:
        print(ies_path + "interface " + iface_full + " ipv6 address " + ipv6_local_address + "/" + str(ipv6_netmask_lenght))
    print("")

    # Configuración de SAP
    print(ies_path + "interface " + iface_full + " sap " + iface_full + " create")
    print(ies_path + "interface " + iface_full + " sap " + iface_full + " ingress qos " + str(qos_profile_id))
    print(ies_path + "interface " + iface_full + " sap " + iface_full + " egress agg-rate rate " + str(total_bandwidth))
    print("")

    # Configuracion de BGP
    # IPv4
    ipv4_prefixlist_path: str = "/configure router policy-options prefix-list \"CUSTOMER:AS" + str(peer_as_number) + "\" prefix "
    ipv4_policy_path: str = "/configure router policy-options policy-statement \"CUSTOMER:AS" + str(peer_as_number) + "\""
    ipv4_bgp_group_path: str = "/configure router bgp group \"AS" + str(peer_as_number) + "\""
    ipv4_bgp_neighbor_path: str = "/configure router bgp group \"AS" + str(peer_as_number) + "\" neighbor " + ipv4_neighbor_address

    # Definicion de politica
    print("/configure router policy-options abort")
    print("/configure router policy-options begin")

    # Definición de Prefix List
    for prefix in ipv4_received_prefixes:
        print(ipv4_prefixlist_path + prefix)
    print("")

    print(ipv4_policy_path + " entry 5 description \"AS" + str(peer_as_number) + "-PREFIXES\"")
    print(ipv4_policy_path + " entry 5 from prefix-list \"CUSTOMER:AS" + str(peer_as_number) + "\"")
    print(ipv4_policy_path + " entry 5 action next-policy")
    print(ipv4_policy_path + " default-action reject")
    print("/configure router policy-options commit")
    print("")

    # Sesión
    print(ipv4_bgp_group_path + " type external")
    print(ipv4_bgp_group_path + " peer-as " + str(peer_as_number))
    print(ipv4_bgp_neighbor_path + " description \"" + iface_description + "\"")
    print(ipv4_bgp_neighbor_path + " remove-private")
    print(ipv4_bgp_neighbor_path + " family ipv4")
    print(ipv4_bgp_neighbor_path + " import \"CUSTOMER:AS" + str(peer_as_number) + "\" \"transit-customer-map\"")
    if send_full_table:
        print(ipv4_bgp_neighbor_path + " export \"send-default\" \"rfc1918\" \"global-routes\"")
    else:
        print(ipv4_bgp_neighbor_path + " export \"send-default\" \"none\"")
    print(ipv4_bgp_neighbor_path + " prefix-limit ipv4 5000 threshold 90")
    print("")
    # Actualiza la prefix list para que se pueda establecer la sesion
    print("/configure filter match-list ip-prefix-list \"cust-bgp\" prefix " + ipv4_neighbor_address + "/32")
    print("")

    if ipv6_local_address:
        # IPv6
        ipv6_prefixlist_path: str = "/configure router policy-options prefix-list \"CUSTOMER:AS" + str(peer_as_number) + "-IPV6\" prefix "
        ipv6_policy_path: str = "/configure router policy-options policy-statement \"CUSTOMER:AS" + str(peer_as_number) + "-IPV6\""
        ipv6_bgp_group_path: str = "/configure router bgp group \"AS" + str(peer_as_number) + "-IPV6\""
        ipv6_bgp_neighbor_path: str = "/configure router bgp group \"AS" + str(peer_as_number) + "-IPV6\" neighbor " + ipv6_neighbor_address

        # Definicion de politica
        print("/configure router policy-options abort")
        print("/configure router policy-options begin")

        # Definición de Prefix List
        for prefix in ipv6_received_prefixes:
            print(ipv6_prefixlist_path + prefix)
        print("")

        print(ipv6_policy_path + " entry 5 description \"AS" + str(peer_as_number) + "-PREFIXES-IPV6\"")
        print(ipv6_policy_path + " entry 5 from prefix-list \"CUSTOMER:AS" + str(peer_as_number) + "-IPV6\"")
        print(ipv6_policy_path + " entry 5 action next-policy")
        print(ipv6_policy_path + " default-action reject")
        print("/configure router policy-options commit")
        print("")

        # Sesión
        print(ipv6_bgp_group_path + " family ipv6")
        print(ipv6_bgp_group_path + " type external")
        print(ipv6_bgp_group_path + " peer-as " + str(peer_as_number))
        print(ipv6_bgp_neighbor_path + " description \"" + iface_description + "\"")
        print(ipv6_bgp_neighbor_path + " remove-private")
        print(ipv6_bgp_neighbor_path + " family ipv6")
        print(ipv6_bgp_neighbor_path + " import \"CUSTOMER:AS" + str(peer_as_number) + "-IPV6\"")
        if send_full_table:
            print(ipv6_bgp_neighbor_path + " export \"send-default\" \"rfc1918\" \"global-routes\"")
        else:
            print(ipv6_bgp_neighbor_path + " export \"default-originate-ipv6\"")
        print(ipv6_bgp_neighbor_path + " prefix-limit ipv6 2000 threshold 90")
        print("")
        # Actualiza la prefix list para que se pueda establecer la sesion
        print("/configure filter match-list ipv6-prefix-list \"cust-bgp-ipv6\" prefix " + ipv6_neighbor_address + "/128")
