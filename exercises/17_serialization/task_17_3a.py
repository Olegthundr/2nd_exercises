# -*- coding: utf-8 -*-
"""
Задание 17.3a

Создать функцию generate_topology_from_cdp, которая обрабатывает вывод
команды show cdp neighbor из нескольких файлов и записывает итоговую
топологию в один словарь.

Функция generate_topology_from_cdp должна быть создана с параметрами:
* list_of_files - список файлов из которых надо считать вывод команды sh cdp neighbor
* save_to_filename - имя файла в формате YAML, в который сохранится топология.
 * значение по умолчанию - None. По умолчанию, топология не сохраняется в файл
 * топология сохраняется только, если save_to_filename как аргумент указано имя файла

Функция должна возвращать словарь, который описывает соединения между устройствами,
независимо от того сохраняется ли топология в файл.

Структура словаря должна быть такой:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}},
 'R5': {'Fa 0/1': {'R4': 'Fa 0/1'}},
 'R6': {'Fa 0/0': {'R4': 'Fa 0/2'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.

Проверить работу функции generate_topology_from_cdp на списке файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt
* sh_cdp_n_r4.txt
* sh_cdp_n_r5.txt
* sh_cdp_n_r6.txt

Проверить работу параметра save_to_filename и записать итоговый словарь
в файл topology.yaml. Он понадобится в следующем задании.

"""
import glob
import re

import yaml


def generate_topology_from_cdp(list_of_files, save_to_filename=None):
    out_dict = {}
    for file in list_of_files:
        with open(file) as f:
            sh_cdp_nei = f.read()
            host = re.search(r'(\S+)>.+', sh_cdp_nei).group(1)
            regex = re.compile(r'(\S+) +(Eth \S+).+(Eth \S+)')
            out_dict[host] = {}
            for nei, loc_intf, remote_intf in regex.findall(sh_cdp_nei):
                out_dict[host][loc_intf] = {nei: remote_intf}
    if save_to_filename:
        with open(save_to_filename, 'w', newline='') as wr_file:
            yaml.dump(out_dict, wr_file)
    return out_dict

if __name__ == '__main__':
    sh_cdp_files = glob.glob("sh_cdp_*")
    print(generate_topology_from_cdp(sh_cdp_files, 'topology.yaml'))