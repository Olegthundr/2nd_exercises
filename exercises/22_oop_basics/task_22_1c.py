# -*- coding: utf-8 -*-

"""
Задание 22.1c

Изменить класс Topology из задания 22.1b.

Добавить метод delete_node, который удаляет все соединения с указаным устройством.

Если такого устройства нет, выводится сообщение "Такого устройства нет".

Создание топологии
In [1]: t = Topology(topology_example)

In [2]: t.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление устройства:
In [3]: t.delete_node('SW1')

In [4]: t.topology
Out[4]:
{('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Если такого устройства нет, выводится сообщение:
In [5]: t.delete_node('SW1')
Такого устройства нет

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


if __name__ == '__main__':
    top = Topology(topology_example)
    pprint(top.topology)
    top.delete_node('R5')
    pprint(top.topology)