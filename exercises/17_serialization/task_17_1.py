# -*- coding: utf-8 -*-
"""
Задание 17.1

Создать функцию write_dhcp_snooping_to_csv, которая обрабатывает вывод
команды show dhcp snooping binding из разных файлов и записывает обработанные
данные в csv файл.

Аргументы функции:
* filenames - список с именами файлов с выводом show dhcp snooping binding
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Например, если как аргумент был передан список с одним файлом sw3_dhcp_snooping.txt:
MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
------------------  ---------------  ----------  -------------  ----  --------------------
00:E9:BC:3F:A6:50   100.1.1.6        76260       dhcp-snooping   3    FastEthernet0/20
00:E9:22:11:A6:50   100.1.1.7        76260       dhcp-snooping   3    FastEthernet0/21
Total number of bindings: 2

В итоговом csv файле должно быть такое содержимое:
switch,mac,ip,vlan,interface
sw3,00:E9:BC:3F:A6:50,100.1.1.6,3,FastEthernet0/20
sw3,00:E9:22:11:A6:50,100.1.1.7,3,FastEthernet0/21

Первый столбец в csv файле имя коммутатора надо получить из имени файла,
остальные - из содержимого в файлах.

Проверить работу функции на содержимом файлов sw1_dhcp_snooping.txt,
sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt.

"""
import csv
import re
from pprint import pprint

def write_dhcp_snooping_to_csv(filenames, output):
    with open(output, 'w', newline='') as result_file:
        writer = csv.writer(result_file)
        writer.writerow(['switch','mac','ip','vlan','interface'])
        regex = re.compile(r'(\S+) +([\d.]+) +\w+ +\S+ +(\d+) +(\S+)', re.DOTALL)
        list_of_tuples = []
        for file in filenames:
            with open(file) as f:
                switch = re.search(r'(^\S+?)_', file).group(1)
                for line in regex.findall(f.read()):
                    #list_of_tuples.
                    list_of_line = list(line)
                    list_of_line.insert(0, switch)
                    list_of_tuples.append(list_of_line)
        for row in list_of_tuples:
            writer.writerow(row)


if __name__ == '__main__':
    files = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']
    pprint(write_dhcp_snooping_to_csv(files, 'result.txt'))
    with open('result.txt') as out:
        print(out.read())