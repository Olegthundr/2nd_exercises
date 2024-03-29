# -*- coding: utf-8 -*-
"""
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt.

"""
import re


def parse_sh_ip_int_br(show_ip_int_br):
    with open(show_ip_int_br) as interfaces:
        output_sh_ip_int_br = []
        for line in interfaces:
            #FastEthernet0/0            15.0.15.1       YES manual up                    up
            match = re.search(
                r"(?P<intf>\S+)\s+(?P<ip>[\d.]+|\w+) +\S+ +\S+ +(?P<status>\w+ \w+|\w+) +(?P<protocol>\w+)", line)
            if match:
                output_sh_ip_int_br.append(match.groups())
    return output_sh_ip_int_br

if name == 'main':
    print(parse_sh_ip_int_br('sh_ip_int_br.txt'))

