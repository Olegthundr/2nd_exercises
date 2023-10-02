# -*- coding: utf-8 -*-

"""
Задание 24.2c

Скопировать класс MyNetmiko из задания 24.2b.
Проверить, что метод send_command кроме команду, принимает еще и дополнительные
аргументы, например, strip_command.

Если возникает ошибка, переделать метод таким образом, чтобы он принимал
любые аргументы, которые поддерживает netmiko.


In [2]: from task_24_2c import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_command('sh ip int br', strip_command=False)
Out[4]: 'sh ip int br\nInterface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

In [5]: r1.send_command('sh ip int br', strip_command=True)
Out[5]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

"""
from netmiko.cisco.cisco_ios import CiscoIosSSH
import re


class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """


device_params = {
    "device_type": "cisco_ios",
    "ip": "192.168.100.1",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}


class MyNetmiko(CiscoIosSSH):
    def __init__(self, **device_params):
        super().__init__(**device_params)
        super().enable()

    def _check_error_in_command(self, command, output):
        regexp = r'% (?P<error>.+)'
        answer = 'При выполнении команды "{}" на устройстве {} возникла ошибка "{}"'
        err = re.search(regexp, output)
        if err:
            raise ErrorInCommand(answer.format(command, self.host, err.group('error')))

    def send_command(self, command, *args, **kwargs):
        send = super().send_command(command, *args, **kwargs)
        self._check_error_in_command(command, send)
        return send

    def send_config_set(self, commands, *args, **kwargs):
        send_set = ''
        if type(commands) == str:
            send_set = super().send_config_set(commands, *args, **kwargs)
            self._check_error_in_command(commands, send_set)
            return send_set
        elif type(commands) == list:
            for command in commands:
                send = self.send_command(command, exit_config_mode=False, *args, **kwargs)
                self._check_error_in_command(command, send)
                send_set += send
            super().exit_config_mode()
            return send_set


if __name__ == '__main__':
    r1 = MyNetmiko(**device_params)
    print(r1.send_config_set('sh ip int br'))
    print(r1.send_config_set(['sh ip int br', 'sh ip int br', 'sow ip int br']))