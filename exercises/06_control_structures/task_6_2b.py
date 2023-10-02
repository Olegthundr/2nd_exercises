# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'
Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
ip_correct = False
while not ip_correct:
    ip = input('Введите IP-адрес: ')
    check = 0
    if len(ip.split('.')) == 4:
        if '.'.join(ip.split('.')) == ip:
            i = 0
            for i in range(len(ip.split('.'))):
                if ip.split('.')[i].isdigit():
                    if 0 <= int(ip.split('.')[i]) <= 255:
                        check += 1
    if check == 4:
        ip_correct = True
        if 1 <= int(ip.split('.')[0]) <= 223:
            print('unicast')
        elif 224 <= int(ip.split('.')[0]) <= 239:
            print('multicast')
        elif ip == '255.255.255.255':
            print('local broadcast')
        elif ip == '0.0.0.0':
            print('unassigned')
        else:
            print('unused')
    else:
        print('Неправильный IP-адрес')
        continue
