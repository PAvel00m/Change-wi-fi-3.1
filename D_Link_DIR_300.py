# -*- coding: utf-8 -*-

import random
import datetime
import requests

import MAIN_program


def DIR_300():
    data_conf, error = MAIN_program.search_and_read_file_config()
    ssid_err = ''
    pasw_err = 'ERROR'
    now = datetime.datetime.now() #Текущая дата
    date = str(now.year) + '.' + str(now.month) + '.' + str(now.day) + '.' + str(now.hour) + '.' + str(now.minute) + '.' + str(now.second)
    log_f = open('log.txt', 'a+')
    if error == '':
        try:
            #авторизация на роутере (POST запрос)
            rec_ses = requests.session()
            data_aut = {
                'ACTION_POST': 'LOGIN',
                'FILECODE': '',
                'VERIFICATION_CODE': '',
                'LOGIN_USER': data_conf[1],       #логин считаный из файла
                'LOGIN_PASSWD': data_conf[2],     #пароль считаный из файла
                'login': ' Авторизоваться',
                'VER_CODE': ''
            }

            try:
                ex_con = rec_ses.post('http://' + data_conf[0], data=data_aut)
            except requests.exceptions.MissingSchema:
                log_f.write(date + ' Вы ввели 1-ой строкой в файле config.txt некорректный URL-адрес сервера\n')
                log_f.close()
                return ssid_err, pasw_err
            except requests.exceptions.ConnectionError :
                log_f.write(date + ' Сервер расположеный по адресу http://' + data_conf[0]+' не найден\n')
                log_f.close()
                return ssid_err, pasw_err
            else:
                if ex_con.status_code == 200:
                    rec_ses.cookies
                    #Изменение пароля f_wpa_psk на роутере (POST запрос)
                    pasw = random.randint(12345678, 99999999) #для генерации пароля
                    data_pas = {
                        'ACTION_POST': 'final',
                        'f_enable': 1,
                        'f_wps_enable': 1,
                        'f_ssid': data_conf[3],
                        'f_channel': 6,
                        'f_auto_channel': 0,
                        'f_super_g': '',
                        'f_xr': '',
                        'f_txrate': 0,
                        'f_wmm_enable': 0,
                        'f_ap_hidden': 0,
                        'f_authentication': 5,
                        'f_cipher': 2,
                        'f_wep_len': '',
                        'f_wep_format': '',
                        'f_wep_def_key': '',
                        'f_wep': '',
                        'f_wpa_psk_type': 1,
                        'f_wpa_psk': pasw,
                        'f_radius_ip1': '',
                        'f_radius_port1': '',
                        'f_radius_secret1': ''
                    }
                    rec_ses.post('http://' + data_conf[0] + '/bsc_wlan.php', data=data_pas)

                    #отправка get запроса на применение настроек
                    ex_change_settings = requests.get('http://' + data_conf[0] + '/bsc_wlan.xgi?random_num=' + date + '&exeshell=submit%20COMMIT&exeshell=submit%20WLAN')
                    if ex_change_settings.status_code == 200:
                        log_f.write(date + ' Проль для сети ' + data_conf[3] + ' успешно изменен\n')
                        log_f.close()
                        requests.get('http://' + data_conf[0] + '/sys_cfg_valid.xgi?&exeshell=submit%20REBOOT')
                        return data_conf[3], pasw
                    elif ex_change_settings.status_code == 404:
                        log_f.write(date + ' Подключение к серверу http://' + data_conf[0] + ' окончено с ошибкой\n')
                        log_f.write('\tОшибка доступа! Несоответствие запрос <--> устройство\n')
                        log_f.close()
                        return ssid_err, pasw_err
                    elif ex_change_settings.status_code == 401:
                        log_f.write(date + ' Сервер http://' + data_conf[0] + ' ожидает повторного подтверждения\n')
                        ex_recon = rec_ses.post('http://' + data_conf[0], data=data_aut)
                        rec_ses.post('http://' + data_conf[0] + '/bsc_wlan.php', data=data_pas)
                        ex_change_settings_recon = requests.get('http://' + data_conf[0] + '/bsc_wlan.xgi?random_num=' + date + '&exeshell=submit%20COMMIT&exeshell=submit%20WLAN')
                        if (ex_recon.status_code == 200) and (ex_change_settings_recon.status_code == 200):
                            log_f.write(date + ' Проль для сети ' + data_conf[3] + ' успешно изменен\n')
                            log_f.close()
                            requests.get('http://' + data_conf[0] + '/sys_cfg_valid.xgi?&exeshell=submit%20REBOOT')
                            return data_conf[3], pasw
                        elif (ex_recon.status_code == 401) or (ex_change_settings_recon.status_code == 401):
                            log_f.write(date + ' Введен не верный логин или пароль\n')
                            log_f.close()
                            return ssid_err, pasw_err
                        else:
                            log_f.write(date + ' Ошибка при повторной отправки запроса на применение настроек\n')
                            log_f.write('\tex_recon = ' + str(ex_recon.status_code) +
                                        ' ex_change_settings_recon = ' + str(ex_change_settings_recon.status_code) +'\n')
                            log_f.close()
                            return ssid_err, pasw_err
                    else:
                        log_f.write(date + ' Неизвестная ошибка при изменении настроек ex_change_settings = ' + str(ex_change_settings.status_code) + '\n')
                        log_f.close()
                        return ssid_err, pasw_err
                elif ex_con.status_code == 401:
                    log_f.write(date + ' Подключение к серверу http://' + data_conf[0] + ' окончено с ошибкой\n')
                    log_f.write('\tОшибка доступа! Несоответствие запрос <--> устройство\n')
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

