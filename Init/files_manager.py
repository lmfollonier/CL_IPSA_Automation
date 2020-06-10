def init_do_files(do_number, work_type, country):
    from os import mkdir, popen

    # Definimos los directorios de trabajo. TODO: ver que onda ese Path de Feli
    base_dir = '/home/martin/Proyectos/Iquall/CenturyLink/DOs/'
    # Agrego "S" al final de la orden, esto tranquilamente se podría hacer desde las variables
    work_type += 'S'
    working_dir = base_dir + work_type + "/" + country + "/" + str(do_number) + '/'
    backups_dir = working_dir + '01-BACKUPS/'
    pe_backup_file = backups_dir + str(do_number) + '-PE-BACKUP.txt'
    um_backup_file = backups_dir + str(do_number) + '-UM-BACKUP.txt'
    pretask_dir = working_dir + '02-PRETASK/'
    pe_pretask_conf = pretask_dir + str(do_number) + '-PE-PRETASK-CONFIG.txt'
    pe_pretask_oper = pretask_dir + str(do_number) + '-PE-PRETASK-OPER.txt'
    um_pretask_conf = pretask_dir + str(do_number) + '-UM-PRETASK-CONFIG.txt'
    um_pretask_oper = pretask_dir + str(do_number) + '-UM-PRETAST-OPER.txt'
    scripts_dir = working_dir + '03-SCRIPTS/'
    pe_script = scripts_dir + str(do_number) + '-PE-SCRIPT.txt'
    um_script = scripts_dir + str(do_number) + '-UM-SCRIPT.txt'
    postask_dir = working_dir + '04-POSTASK/'
    pe_postask_conf = postask_dir + str(do_number) + '-PE-POSTASK-CONFIG.txt'
    pe_postask_oper = postask_dir + str(do_number) + '-PE-POSTASK-OPER.txt'
    um_postask_conf = postask_dir + str(do_number) + '-UM-POSTASK-CONFIG.txt'
    um_postask_oper = postask_dir + str(do_number) + '-UM-POSTASK-OPER.txt'
    diff_dir = working_dir + '05-DIFF/'
    pe_diff = diff_dir + str(do_number) + '-PE-DIFF.txt'
    um_diff = diff_dir + str(do_number) + '-UM-DIFF.txt'
    do_info_file = working_dir + str(do_number) + '-DO-INFO.txt'
    do_close_file = working_dir + str(do_number) + '-INFO-CIERRE.txt'

    if do_number and work_type and country:
        print('todo bien')
        print(do_number, work_type, country)
        try:
            mkdir(working_dir)
        except OSError as error:
            print(error)
        try:
            mkdir(backups_dir)
        except OSError as error:
            print(error)
        try:
            mkdir(pretask_dir)
        except OSError as error:
            print(error)
        try:
            mkdir(scripts_dir)
        except OSError as error:
            print(error)
        try:
            mkdir(postask_dir)
        except OSError as error:
            print(error)
        try:
            mkdir(diff_dir)
        except OSError as error:
            print(error)

        open(pe_backup_file, 'a')
        open(um_backup_file, 'a')
        open(pe_pretask_conf, 'a')
        open(pe_pretask_oper, 'a')
        open(um_pretask_conf, 'a')
        open(um_pretask_oper, 'a')
        open(pe_script, 'a')
        open(um_script, 'a')
        open(pe_postask_conf, 'a')
        open(pe_postask_oper, 'a')
        open(um_postask_conf, 'a')
        open(um_postask_oper, 'a')
        open(pe_diff, 'a')
        open(um_diff, 'a')
        open(do_info_file, 'a')
        open(do_close_file, 'a')
        popen('subl %s' % working_dir)

    else:
        print('todo mal')
        print(do_number, work_type, country)
        print('No se crea nada')

    return


def get_pe_script(do_number, work_type, country):
    # Definimos los directorios de trabajo. TODO: ver que onda ese Path de Feli
    base_dir = '/home/martin/Proyectos/Iquall/CenturyLink/DOs/'
    # Agrego "S" al final de la orden, esto tranquilamente se podría hacer desde las variables
    work_type += 'S'
    working_dir = base_dir + work_type + "/" + country + "/" + str(do_number) + '/'
    scripts_dir = working_dir + '03-SCRIPTS/'
    pe_script = scripts_dir + str(do_number) + '-PE-SCRIPT.txt'
    file = open(pe_script, 'w')
    #file.write('############################################################################')
    return (file)
