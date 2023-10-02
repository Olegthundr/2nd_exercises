# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
def get_int_vlan_map(config_filename):
    with open(config_filename) as config:
    #with open('config_sw1.txt') as config:
        intf_and_vlan_access = {}
        intf_and_vlan_trunk = {}
        interfaces = (intf_and_vlan_access, intf_and_vlan_trunk)
        for line in config:
            if line.startswith('interface F'):
                interface = line.split()[-1]
            elif 'mode access' in line:
                intf_and_vlan_access[interface] = 1
            elif 'access vlan' in line:
                intf_and_vlan_access[interface] = int(line.split()[-1])
            elif 'allowed vlan' in line:
                vlans = line.split()[-1].split(',')
                intf_and_vlan_trunk[interface] = [int(vlan) for vlan in vlans]
    return interfaces

print(get_int_vlan_map('config_sw2.txt'))