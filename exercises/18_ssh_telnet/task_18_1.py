# -*- coding: utf-8 -*-
"""
Задание 18.1

Создать функцию send_show_command.

Функция подключается по SSH (с помощью netmiko) к ОДНОМУ устройству
и выполняет указанную команду.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* command - команда, которую надо выполнить

Функция возвращает строку с выводом команды.

Скрипт должен отправлять команду command на все устройства из файла devices.yaml
с помощью функции send_show_command (эта часть кода написана).

"""
import yaml
from netmiko import (ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException)

def send_show_command(device, command):
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            output = ssh.send_command(command)
        return output
    except (NetMikoTimeoutException, NetMikoAuthenticationException) as error:
        print(error)

if __name__ == "__main__":
    command = "disp ip int br"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        print(send_show_command(dev, command))
