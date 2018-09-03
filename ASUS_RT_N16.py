# -*- coding: utf-8 -*-
import datetime
import random
import requests

import MAIN_program


def RT_N16():
    data_conf, error = MAIN_program.search_and_read_file_config()
    ssid_err = ''
    pasw_err = 'ERROR'
    now = datetime.datetime.now()  # Текущая дата
    date = str(now.year) + '.' + str(now.month) + '.' + str(now.day) + '.' + str(now.hour) + '.' + str(now.minute) + '.' + str(now.second)
    log_f = open('log.txt', 'a+')
    if error == '':
        try:
            try:
                ex_con = requests.get('http://' + data_conf[0], auth=(data_conf[1], data_conf[2]))
            except requests.exceptions.MissingSchema:
                log_f.write(date + ' Вы ввели 1-ой строкой в файле config.txt некорректный URL-адрес сервера\n')
                log_f.close()
                return ssid_err, pasw_err
            except requests.exceptions.ConnectionError:
                log_f.write(date + ' Сервер расположеный по адресу http://' + data_conf[0] + ' не найден\n')
                log_f.close()
                return ssid_err, pasw_err
            else:
                if ex_con.status_code == 200:
                    rec_ses = requests.session()
                    #Изменение пароля f_wpa_psk на роутере (POST запрос)
                    pasw = random.randint(12345678, 99999999) #для генерации пароля
                    data_pas = {
                        'current_page': '',
                        'next_page': '/',
                        'sid_list': 'WLANConfig11b;',
                        'group_id': '',
                        'action_mode': 'Apply',
                        'productid': 'RT-N16',
                        'wl_key1_org': '',
                        'wl_key2_org': '',
                        'wl_key3_org': '',
                        'wl_key4_org': '',
                        'wps_mode': 'enabled',
                        'wps_config_state': '1',
                        'wl_wpa_mode': '2',
                        'wl_key1': '',
                        'wl_key2': '',
                        'wl_key3': '',
                        'wl_key4': '',
                        'wl_gmode': '0',
                        'ssid_acsii': data_conf[3],
                        'wl_ssid': data_conf[3],
                        'wl_auth_mode': 'psk',
                        'wl_wep_x': '0',
                        'wl_key': '2',
                        'wl_asuskey1': '',
                        'wl_crypto': 'aes',
                        'wl_wpa_psk': pasw,
                        'wl_radio_x': '1'
                    }
                    try:
                        ex_change_settings = rec_ses.post('http://' + data_conf[0] + '/start_apply2.htm', data=data_pas, auth=(data_conf[1], data_conf[2]))
                    except requests.exceptions.ConnectionError :
                        log_f.write(date + ' Ошибка доступа! Несоответствие запрос <--> устройство\n')
                        log_f.close()
                        return ssid_err, pasw_err
                    if ex_change_settings.status_code == 200:
                        log_f.write(date + ' Проль для сети ' + data_conf[3] + ' успешно изменен\n')
                        log_f.close()
                        return data_conf[3], pasw
                    elif ex_change_settings.status_code == 501 or ex_change_settings.status_code == 404:
                        log_f.write(date + ' Подключение к серверу http://' + data_conf[0] + ' окончено с ошибкой\n')
                        log_f.write('\tСервер понял запрос, но не смог найти соответствующий URL\n')
                        log_f.write('\tОшибка доступа! Несоответствие запрос <--> устройство\n')
                        log_f.close()
                        return ssid_err, pasw_err
                    else:
                        log_f.write(date + ' Неизвестная ошибка при изменении настроек ex_change_settings = ' + str(ex_change_settings.status_code) + '\n')
                        log_f.close()
                        return ssid_err, pasw_err
                elif ex_con.status_code == 404:
                    log_f.write(date + ' Подключение к серверу http://' + data_conf[0] + ' окончено с ошибкой\n')
                    log_f.write('\tОшибка доступа! Несоответствие запрос <--> устройство\n')
                    log_f.close()
                    return ssid_err, pasw_err
                elif ex_con.status_code == 401:
                    log_f.write(date + ' Введен неверный логин или пароль\n')
                    log_f.close()
                    return ssid_err, pasw_err
                else:
                    log_f.write(date + ' Неизвестная ошибка в подключении ex_con = ' + str(ex_con.status_code) + '\n')
                    log_f.close()
                    return ssid_err, pasw_err

        except IndexError:
            log_f.write(date + ' Файл config.txt пуст или в нем меньше четырех строк\n'
                        '\t1 - адрес роутера\n\t2 - логин\n\t3 - пароль\n\t4 - имя сети')
            log_f.close()
            return ssid_err, pasw_err
    else:
        log_f.write(date + ' ' + error + '\n')
        log_f.close()
        return ssid_err, pasw_err

