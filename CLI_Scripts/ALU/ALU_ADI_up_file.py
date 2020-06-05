from Init.files_manager import *


def alu_adi_up_file(do_number,
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
    import xlrd
    workbook = xlrd.open_workbook('/home/martin/Downloads/do.xlsx')
    worksheet = workbook.sheet_by_name('Sheet1')
    # TODO: esto quedó a medias
    #    ipv4_local_address = worksheet.cell(12,1)
    #    ipv4_neighbor_address = worksheet.cell(13, 1)
    #    ipv4_netmask_lenght = worksheet.cell(14, 1)

    # Abro el archivo
    file = get_pe_script(do_number, work_type, country)
    iface_description: str = customer_name + " [" + cid_location + ", CID:" + str(cid_number) + "]"
    iface_full: str = "\"" + iface_name + ":" + str(svlan_id) + "." + str(cvlan_id) + "\""

    # Pongo la jerarquia acá para que el comando no quede tan largo:
    ies_path: str = "/configure service ies " + ies_id + " "

    # TODO: Creación del cliente

    # Creación del IES
    print(ies_path + "customer " + customer_id + " create", file=file)
    print(ies_path + "no shutdown", file=file)
    print("", file=file)

    # Configuracion de Interfaz
    print(ies_path + "interface " + iface_full + " create", file=file)
    print(ies_path + "interface " + iface_full + " no shutdown", file=file)
    print(
        ies_path + "interface " + iface_full + " description \"CUSTOMER: IMPS-CLI: " + iface_description + " " + service_type + "@" + str(
            int(total_bandwidth / 1024)) + "Mbps\"", file=file)
    print(ies_path + "interface " + iface_full + " enable-ingress-stats", file=file)
    print(ies_path + "interface " + iface_full + " urpf-check mode loose", file=file)
    print(ies_path + "interface " + iface_full + " tos-marking-state trusted", file=file)
    print(ies_path + "interface " + iface_full + " cflowd-parameters sampling unicast type interface", file=file)
    print(ies_path + "interface " + iface_full + " address " + ipv4_local_address + "/" + str(ipv4_netmask_lenght),
          file=file)
    if ipv6_local_address:
        print(ies_path + "interface " + iface_full + " ipv6 address " + ipv6_local_address + "/" + str(
            ipv6_netmask_lenght), file=file)
    print("", file=file)

    # Configuración de SAP
    print(ies_path + "interface " + iface_full + " sap " + iface_full + " create", file=file)
    print(ies_path + "interface " + iface_full + " sap " + iface_full + " ingress qos " + str(qos_profile_id),
          file=file)
    print(ies_path + "interface " + iface_full + " sap " + iface_full + " egress agg-rate rate " + str(total_bandwidth),
          file=file)
    print("", file=file)

    # Static Routing
    if static_routing:
        print("/configure router static-route-entry " + cpe_ipv4_address + " next-hop " + ipv4_neighbor_address,
              file=file)
        print(
            "/configure router static-route-entry " + cpe_ipv4_address + " next-hop " + ipv4_neighbor_address + " no shutdown",
            file=file)
        print("/configure router static-route-entry " + ipv4_lan_net + " next-hop " + ipv4_neighbor_address, file=file)
        print(
            "/configure router static-route-entry " + ipv4_lan_net + " next-hop " + ipv4_neighbor_address + " no shutdown",
            file=file)
    # TODO: IPv6 Static

    if bgp_routing:
        # Configuracion de BGP
        # IPv4
        if peer_as_number == 10753:
            ipv4_prefixlist_path: str = "/configure router policy-options prefix-list \"CUSTOMER:AS" + str(
                peer_as_number) + "-" + customer_name + "\" prefix "
            ipv4_policy_path: str = "/configure router policy-options policy-statement \"CUSTOMER:AS" + str(
                peer_as_number) + "-" + customer_name + "\""
            ipv4_bgp_group_path: str = "/configure router bgp group \"AS" + str(
                peer_as_number) + "-" + customer_name + "\""
            ipv4_bgp_neighbor_path: str = "/configure router bgp group \"AS" + str(
                peer_as_number) + "-" + customer_name + "\" neighbor " + ipv4_neighbor_address
        else:
            ipv4_prefixlist_path: str = "/configure router policy-options prefix-list \"CUSTOMER:AS" + str(
                peer_as_number) + "\" prefix "
            ipv4_policy_path: str = "/configure router policy-options policy-statement \"CUSTOMER:AS" + str(
                peer_as_number) + "\""
            ipv4_bgp_group_path: str = "/configure router bgp group \"AS" + str(peer_as_number) + "\""
            ipv4_bgp_neighbor_path: str = "/configure router bgp group \"AS" + str(
                peer_as_number) + "\" neighbor " + ipv4_neighbor_address

        # Definicion de politica
        print("/configure router policy-options abort", file=file)
        print("/configure router policy-options begin", file=file)

        # Definición de Prefix List
        for prefix in ipv4_received_prefixes:
            print(ipv4_prefixlist_path + prefix, file=file)
        print("", file=file)

        if peer_as_number == 10753:
            print(ipv4_policy_path + " entry 5 description \"AS" + str(
                peer_as_number) + "-" + customer_name + "-PREFIXES\"", file=file)
            print(ipv4_policy_path + " entry 5 from prefix-list \"CUSTOMER:AS" + str(
                peer_as_number) + "-" + customer_name + "\"", file=file)
            print(ipv4_policy_path + " entry 5 action next-policy", file=file)
            print(ipv4_policy_path + " default-action reject", file=file)
            print("/configure router policy-options commit", file=file)
            print("", file=file)
        else:
            print(ipv4_policy_path + " entry 5 description \"AS" + str(peer_as_number) + "-PREFIXES\"", file=file)
            print(ipv4_policy_path + " entry 5 from prefix-list \"CUSTOMER:AS" + str(peer_as_number) + "\"", file=file)
            print(ipv4_policy_path + " entry 5 action next-policy", file=file)
            print(ipv4_policy_path + " default-action reject", file=file)
            print("/configure router policy-options commit", file=file)
            print("", file=file)

        # Sesión
        print(ipv4_bgp_group_path + " type external", file=file)
        print(ipv4_bgp_group_path + " peer-as " + str(peer_as_number), file=file)
        print(ipv4_bgp_neighbor_path + " description \"" + iface_description + "\"", file=file)
        print(ipv4_bgp_neighbor_path + " remove-private", file=file)
        print(ipv4_bgp_neighbor_path + " family ipv4", file=file)
        if peer_as_number == 10753:
            print(ipv4_bgp_neighbor_path + " import \"CUSTOMER:AS" + str(
                peer_as_number) + "-" + customer_name + "\" \"transit-customer-map\"", file=file)
        else:
            print(
                ipv4_bgp_neighbor_path + " import \"CUSTOMER:AS" + str(peer_as_number) + "\" \"transit-customer-map\"",
                file=file)
        if send_full_table:
            print(ipv4_bgp_neighbor_path + " export \"send-default\" \"rfc1918\" \"global-routes\"", file=file)
        else:
            print(ipv4_bgp_neighbor_path + " export \"send-default\" \"none\"", file=file)
        print(ipv4_bgp_neighbor_path + " prefix-limit ipv4 5000 threshold 90", file=file)
        print("", file=file)
        # Actualiza la prefix list para que se pueda establecer la sesion
        print("/configure filter match-list ip-prefix-list \"cust-bgp\" prefix " + ipv4_neighbor_address + "/32",
              file=file)
        print("", file=file)

        if ipv6_local_address:
            # IPv6
            ipv6_prefixlist_path: str = "/configure router policy-options prefix-list \"CUSTOMER:AS" + str(
                peer_as_number) + "-IPV6\" prefix "
            ipv6_policy_path: str = "/configure router policy-options policy-statement \"CUSTOMER:AS" + str(
                peer_as_number) + "-IPV6\""
            ipv6_bgp_group_path: str = "/configure router bgp group \"AS" + str(peer_as_number) + "-IPV6\""
            ipv6_bgp_neighbor_path: str = "/configure router bgp group \"AS" + str(
                peer_as_number) + "-IPV6\" neighbor " + ipv6_neighbor_address

            # Definicion de politica
            print("/configure router policy-options abort", file=file)
            print("/configure router policy-options begin", file=file)

            # Definición de Prefix List
            for prefix in ipv6_received_prefixes:
                print(ipv6_prefixlist_path + prefix, file=file)
            print("", file=file)

            print(ipv6_policy_path + " entry 5 description \"AS" + str(peer_as_number) + "-PREFIXES-IPV6\"", file=file)
            print(ipv6_policy_path + " entry 5 from prefix-list \"CUSTOMER:AS" + str(peer_as_number) + "-IPV6\"",
                  file=file)
            print(ipv6_policy_path + " entry 5 action next-policy", file=file)
            print(ipv6_policy_path + " default-action reject", file=file)
            print("/configure router policy-options commit", file=file)
            print("", file=file)

            # Sesión
            print(ipv6_bgp_group_path + " family ipv6", file=file)
            print(ipv6_bgp_group_path + " type external", file=file)
            print(ipv6_bgp_group_path + " peer-as " + str(peer_as_number), file=file)
            print(ipv6_bgp_neighbor_path + " description \"" + iface_description + "\"", file=file)
            print(ipv6_bgp_neighbor_path + " remove-private", file=file)
            print(ipv6_bgp_neighbor_path + " family ipv6", file=file)
            print(ipv6_bgp_neighbor_path + " import \"CUSTOMER:AS" + str(peer_as_number) + "-IPV6\"", file=file)
            if send_full_table:
                print(ipv6_bgp_neighbor_path + " export \"send-default\" \"rfc1918\" \"global-routes\"", file=file)
            else:
                print(ipv6_bgp_neighbor_path + " export \"default-originate-ipv6\"", file=file)
            print(ipv6_bgp_neighbor_path + " prefix-limit ipv6 2000 threshold 90", file=file)
            print("", file=file)
            # Actualiza la prefix list para que se pueda establecer la sesion
            print(
                "/configure filter match-list ipv6-prefix-list \"cust-bgp-ipv6\" prefix " + ipv6_neighbor_address + "/128",
                file=file)
