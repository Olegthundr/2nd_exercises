# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
vlan_input = int(input('Enter VLAN number: '))
with open('CAM_table.txt') as cam_table:
    result = []
    for line in cam_table:
        piece = line.split()
        if len(piece) > 1 and piece[1][0] in '0123456789abcdef':
            piece.pop(2)
            piece[0] = int(piece[0])
            result.append(piece)
    for iteration in sorted(result):
        if vlan_input == iteration[0]:
            vlan = iteration[0]
            mac = iteration[1]
            interface = iteration[2]
            print('{:<9}{:<20}{}'.format(vlan, mac, interface))
