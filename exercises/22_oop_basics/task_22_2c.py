# -*- coding: utf-8 -*-

"""
Задание 22.2c

Скопировать класс CiscoTelnet из задания 22.2b и изменить метод send_config_commands
добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать
  исключение ValueError (значение по умолчанию)
* strict=False значит, что при обнаружении ошибки, надо только вывести
  на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set
у netmiko (пример вывода ниже). Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_22_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "a" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "a"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

"""
import telnetlib
import time
from textfsm import clitable


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.ip = ip
        self.telnet = telnetlib.Telnet(ip)
        self.telnet.read_until(b'Username:')
        self._write_line(username)
        self.telnet.read_until(b'Password:')
        self._write_line(password)
        self.telnet.read_until(b'>')
        #self._write_line('enable')
        #self._write_line(secret)
        #self.telnet.read_until(b'#')
        #self._write_line('terminal length 0')
        self._write_line('screen-length 0 temporary') # huawei
        time.sleep(1)
        self.telnet.read_very_eager()

    def _write_line(self, line):
        self.telnet.write(line.encode("utf-8") + b"\r\n")

    def wrt_ln(self, line):
        return self.telnet.write(line.encode("utf-8") + b"\r\n")

    def send_show_command(self, show, parse=True, templates='templates', index='index'):
        self._write_line(show)
        output = self.telnet.read_until(b'#', timeout=3).decode('utf-8')
        if parse:
            cli_table = clitable.CliTable(index, templates)
            result = cli_table.ParseCmd(output, {'Command': show})
            return result
        else:
            return output

    def send_config_commands(self, commands, strict=True):
        output = self.send_show_command('system-view', parse=False)
        error = 'При выполнении команды "{}" на устройстве {} возникла ошибка -> {}'
        if type(commands) == list:
            for command in commands:
                out = self.send_show_command(command, parse=False)
                if 'Error:' in out:
                    if strict:
                        raise ValueError(error.format(command, self.ip, out))
                    else:
                        print(error.format(command, self.ip, out))
                else:
                    output += out
        elif type(commands) == str:
            out = self.send_show_command(commands, parse=False)
            if 'Error:' in out:
                if strict:
                    raise ValueError(error.format(commands, self.ip, out))
                else:
                    print(error.format(commands, self.ip, out))
            else:
                output += out
        output += self.send_show_command('return', parse=False)

        return output

if __name__ == '__main__':
    r1_params = {
        'ip': '192.168.100.1',
        'username': 'admin',
        'password': 'admin',
        'secret': 'admin'}
    # 'username': 'cisco',
    # 'password': 'cisco',
    # 'secret': 'cisco'}
    commands_with_errors = ['infoce 0255.255.1', 'info-center', 'a']
    correct_commands = ['info-center loghost 10.10.10.10', 'ip route-static 172.19.40.0 24 10.20.30.40']
    commands = commands_with_errors + correct_commands
    sw1 = CiscoTelnet(**r1_params)
    print(sw1.send_config_commands(commands))