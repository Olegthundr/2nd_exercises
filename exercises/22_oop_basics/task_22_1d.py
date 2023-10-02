# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Соединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Соединение с одним из портов существует


"""
from pprint import pprint

topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, topology_dict):
        self.topologys = {}
        for loc_intf, rem_intf in topology_dict.items():
            if rem_intf not in self.topologys.keys():
                self.topologys.update({loc_intf: rem_intf})
        return self.topologys

    def delete_link(self, loc_intf, rem_intf):
        if loc_intf in self.topology.keys() and rem_intf == self.topology[loc_intf]:
            del self.topology[loc_intf]
        elif rem_intf in self.topology.keys() and loc_intf == self.topology[rem_intf]:
            del self.topology[rem_intf]
        else:
            return print('Такого соединения нет')

    def delete_node(self, node):
        old_topology = self.topology.copy()
        was_here = False
        for local, remote in old_topology.items():
            if node == local[0] or node == remote[0]:
                was_here = True
                del self.topology[local]
        if not was_here:
            return print('Такого устройства нет')

    def add_link(self, new_local, new_remote):
        was_here = False
        for local, remote in self.topology.items():
            list_of_intf = [local, remote]
            if new_local in list_of_intf and new_remote in list_of_intf:
                was_here = True
                return print('Такое соединение существует')
            elif new_local in list_of_intf or new_remote in list_of_intf:
                was_here = True
                return print('Соединение с одним из портов существует')
        if not was_here:
            self.topology.update({new_local: new_remote})


if __name__ == '__main__':
    top = Topology(topology_example)
    pprint(top.topology)
    top.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
    top.add_link(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))
    pprint(top.topology)