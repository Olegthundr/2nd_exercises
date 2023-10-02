# -*- coding: utf-8 -*-
"""
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом,
чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1': ('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2': ('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""
import re


def get_ip_from_cfg(config_file):
    with open(config_file) as config:
        addresses_dict = {}
        for line in config:
            match_intf = re.search(r'interface (?P<intf>\S+$)', line)
            match_ip = re.search(r'ip address (?P<ip_add>[\d.]+) (?P<mask>[\d.]+)', line)
            if match_intf:
                intf = match_intf.group('intf')
            elif match_ip:
                addresses_dict[intf] = match_ip.groups()
    return addresses_dict


if name == 'main':
    print(get_ip_from_cfg('config_r2.txt'))
