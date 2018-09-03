# -*- coding: utf-8 -*-

import random
import paramiko
import datetime

import MAIN_program

#смена парол на роутере с прошивкой Openwrt через SSH

def TL_WA801ND():

    data_conf, error = MAIN_program.search_and_read_file_config()
    ssid_err = ''
    pasw_err = 'ERROR'
    now = datetime.datetime.now()  # Текущая дата
    date = str(now.year) + '.' + str(now.month) + '.' + str(now.day) + '.' + str(now.hour) + '.' + str(now.minute) + '.' + str(now.second)
    log_f = open('log.txt', 'a+')
    if error == '':
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(hostname=data_conf[0], username=data_conf[1], password=data_conf[2], port=22)
            except paramiko.ssh_exception.AuthenticationException:
                log_f.write(date + ' Введен не верный логин или пароль\n')
                log_f.close()
                return ssid_err, pasw_err
            except paramiko.ssh_exception.NoValidConnectionsError:
                log_f.write(date + ' Устройство не поддерживает SSH протокол\n'
                                   '\tОшибка доступа! Несоответствие запрос <--> устройство\n')
                log_f.close()
                return ssid_err, pasw_err
            except TimeoutError:
                log_f.write(date + ' Сервер расположеный по адресу ' + data_conf[0] + ' не найден\n')
                log_f.close()
                return ssid_err, pasw_err

            pasw = random.randint(12345678, 99999999)  # для генерации пароля
            stdin, stdout, stderr = client.exec_command('uci set wireless.@wifi-iface[0].ssid=\''+ data_conf[3] + '\'')
            stdin, stdout, stderr = client.exec_command('uci set wireless.@wifi-iface[0].key=\'' + str(pasw) + '\'')
            stdin, stdout, stderr = client.exec_command('uci commit wireless; wifi')
            client.close()
            log_f.write(date + ' Проль для сети ' + data_conf[3] + ' успешно изменен\n')
            log_f.close()
            return data_conf[3], pasw

        except IndexError:
            log_f.write(date + ' Файл config.txt пуст или в нем меньше четырех строк\n'
                        '\t1 - адрес роутера\n\t2 - логин\n\t3 - пароль\n\t4 - имя сети')
            log_f.close()
            return ssid_err, pasw_err
    else:
        log_f.write(date + ' ' + error + '\n')
        log_f.close()
        return ssid_err, pasw_err

