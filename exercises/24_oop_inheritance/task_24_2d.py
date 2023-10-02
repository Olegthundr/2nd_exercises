# -*- coding: utf-8 -*-

"""
Задание 24.2d

Скопировать класс MyNetmiko из задания 24.2c или задания 24.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен
работать точно так же как метод send_config_set в netmiko.
Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_24_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."
"""
from netmiko.cisco.cisco_ios import CiscoIosSSH
import re


class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """


device_params = {
    "device_type": "huawei",
    "ip": "192.168.100.1",
    "username": "admin",
    "password": "admin",
    "secret": "admin",
}


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

    def send_command(self, command, ignore_errors=False, *args, **kwargs):
        send = super().send_command(command, *args, **kwargs)
        if not ignore_errors:
            self._check_error_in_command(command, send)
        return send

    def send_config_set(self, commands, ignore_errors=False, *args, **kwargs):
        send_set = ''
        if type(commands) == str:
            send_set = super().send_config_set(commands, *args, **kwargs)
            if not ignore_errors:
                self._check_error_in_command(commands, send_set)
            return send_set
        elif type(commands) == list:
            for command in commands:
                send = self.send_command(command, exit_config_mode=False, *args, **kwargs)
                if not ignore_errors:
                    self._check_error_in_command(command, send)
                send_set += send
            super().exit_config_mode()
            return send_set


if __name__ == '__main__':
    r1 = MyNetmiko(**device_params)
    print(r1.send_config_set('sh ip int br'))
    print(r1.send_config_set(['sh ip int br', 'sh ip int br', 'sow ip int br']))