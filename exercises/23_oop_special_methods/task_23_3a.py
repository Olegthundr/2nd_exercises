# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
"""

from pprint import pprint


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, topology_dict):
        topologys = {}
        for loc_intf, rem_intf in topology_dict.items():
            if rem_intf not in topologys.keys():
                topologys.update({loc_intf: rem_intf})
        return topologys

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

    def __add__(self, other):
        old_topo = self.topology.copy()
        old_topo.update(other.topology)
        return Topology(old_topo)

    def __getitem__(self, item):
        return tuple(self.topology.items())[item]


if __name__ == '__main__':
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
    for link in Topology(topology_example):
        print(link)
