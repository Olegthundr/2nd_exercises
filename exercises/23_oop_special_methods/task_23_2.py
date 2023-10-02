# -*- coding: utf-8 -*-

"""
Задание 23.2

Скопировать класс CiscoTelnet из задания 22.2 и добавить классу поддержку
работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_23_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка

Тест проверяет подключение с параметрами из файла devices.yaml. Там должны быть
указаны доступные устройства.
"""
import telnetlib
import time


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.telnet = telnetlib.Telnet(ip)
        self.telnet.read_until(b'Username:')
        self._write_line(username)
        self.telnet.read_until(b'Password:')
        self._write_line(password)
        self.telnet.read_until(b'>')

    def _write_line(self, line):
        self.telnet.write(line.encode("utf-8") + b"\n")

    def send_show_command(self, show):
        self._write_line(show)
        output = self.telnet.read_until(b'>', timeout=5).decode('utf-8')
        return output

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.telnet.close()


if __name__ == '__main__':
    r1_params = {
        'ip': '192.168.100.1',
        'username': 'admin',
        'password': 'admin',
        'secret': 'admin'}
    with CiscoTelnet(**r1_params) as sw1:
        print(sw1.send_show_command('disp ip int br'))