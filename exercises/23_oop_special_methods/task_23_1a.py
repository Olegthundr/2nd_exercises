# -*- coding: utf-8 -*-

"""
Задание 23.1a

Скопировать и изменить класс IPAddress из задания 23.1.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

"""
import re


class IPAddress:
    def __init__(self, prefix):
        self.prefix = prefix
        self.ip, self.mask = prefix.split('/')
        self.mask = int(self.mask)
        regexp = r'(((25[0-5])|(2[0-4]\d)|(1\d{2})|(\d{1,2}))\.){3}(((25[0-5])|(2[0-4]\d)|(1\d{2})|(\d{1,2})))'
        if not re.search(regexp, self.ip):
            raise ValueError('Incorrect IPv4 address')
        elif 8 > self.mask or self.mask > 32:
            raise ValueError('Incorrect mask')

    def __str__(self):
        return f'IP address {self.prefix}'

    def __repr__(self):
        return f"IPAddress('{self.prefix}')"


if __name__ == '__main__':
    ip1 = IPAddress('10.1.1.1/24')
    print(str(ip1))
