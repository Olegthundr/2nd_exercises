# -*- coding: utf-8 -*-
"""
Задание 18.1a

Скопировать функцию send_show_command из задания 18.1 и переделать ее таким образом,
чтобы обрабатывалось исключение, которое генерируется при ошибке аутентификации
на устройстве.

При возникновении ошибки, на стандартный поток вывода должно выводиться
сообщение исключения.

Для проверки измените пароль на устройстве или в файле devices.yaml.
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