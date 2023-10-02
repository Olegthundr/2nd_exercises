# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
with open('ospf.txt') as output:
    for line in output:
        list_output = line.split()
        prefix = list_output[1]
        ad = list_output[2].strip('[]')
        next_hop = list_output[4].rstrip(',')
        last_update = list_output[5].rstrip(',')
        outbound_int = list_output[6]
        print("""Prefix                {0}
AD/Metric             {1}
Next-Hop              {2}
Last update           {3}
Outbound Interface    {4}""".format(prefix, ad, next_hop, last_update, outbound_int))
