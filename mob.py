# TO DO 
# look for indications of poor bandwidth or offline use
# ask if user wants to search


from zipfile import ZipFile
from re import search
from pathlib import Path
import os
import shutil
import re
from sys import exit


zip_folder = Path.home().joinpath('loglook')
finished = Path(zip_folder).joinpath('done')
app_name = []
app_v = []
device = []
os_name = []
os_v = []
lang = []
user_id = []
preferred = []
android_reading_plans = []
crash = []
failure = []
fatal = []

def delete_prev_files(which_dir):
    # taken from https://www.techiedelight.com/delete-all-files-directory-python/
    for files in os.listdir(which_dir):
        path = os.path.join(which_dir, files)
        if path != os.path.join(which_dir, '.placeholder'):
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)


def findzip():
    delete_prev_files(finished)
    file_list = os.listdir(zip_folder)
    zip_list = []
    for file in file_list:
        if file.endswith('.zip'):
            zip_list.append(file)
        else:
            continue
    if len(zip_list) > 1:
        print('More than one zipped file available in the loglook folder, try again after making sure that there is only one.')
        exit()
    elif len(zip_list) < 1:
        print('No zipped files available, try again after putting a zipped file in the loglook folder.') 
        exit()
    else:
        file_name = zip_list[0]
        print(f'\nPlease be patient, this process is usually quick, but sometimes takes a while.\n\nZipped File: {file_name}\n\nLog Files:')
        return file_name


def unzip_iter():
    # based on code given in https://thispointer.com/python-how-to-unzip-a-file-extract-single-multiple-or-all-files-from-a-zip-archive/
    logzip = findzip()
    zip_file = zip_folder.joinpath(logzip)
    with ZipFile(zip_file, 'r') as zipObj:
        list_of_fileNames = zipObj.namelist()
        for file_name in list_of_fileNames:
            if file_name.endswith('.log') or file_name.endswith('.txt'):
                print(file_name)
                zipObj.extract(file_name)
                tally = get_info(file_name)
    organize_results(tally)
    Path(zip_file).rename(finished.joinpath(logzip))
    print(f'Moving {logzip} to {finished}.  It will be deleted the next time this script is run.')
    
   

def add_if_new(item, item_list):
    if item not in item_list:
        item_list.append(item)
        return item_list


def get_info(each_iter_file):
    ios_date_time_rx ='([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]:[0-9][0-9][0-9])'
    bep_ios_date_time_rx = '([0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]\s[0-9][0-9]:[0-9][0-9]:[0-9][0-9]:[0-9][0-9][0-9])'
    android_date_time_rx = '([0-9][0-9]-[0-9][0-9]\s[0-9][0-9]:[0-9][0-9]:[0-9][0-9]\.[0-9][0-9][0-9]\s)'
    ios_launched1_rx = '.+Application launched \(([\w]+)/([.\d]+)\s\(([\w]+);.+CPU\s([\w]+)\s([.\d]+).+\s([\w]+)\)\s/\s([0-9]+)\)$'
    ios_launched2_rx = '.+Application launched \(([\w]+)/([.\d]+)\s\(([\w]+);.+CPU\s([\w]+)\s([.\d]+).+\s([\w]+)\)\s/\s([0-9]+)\s/\s(.+)\)$'
    android_launched_rx = '.+Application\slaunched\s/\s([0-9]+)$'
    user1_rx = 'userId=\s?([0-9]+)&'
    user2_rx = 'UserID=([0-9]+)"'
    user_sup_rx = '.+\sSupport/Users/([0-9]+)/'
    lls1_rx = '.+items?:\s\[?\{?\s?([0-9]+)/.+'
    lls2_rx = '.+synced:\s([0-9]+)/.+'
    android_mod_rx = '.+state\(Modified\):\s([0-9]+)/'
    fire_items_rx = '.+items:\s\[\{"id":"([0-9]+)/'
    anon_rx = '.+User\sis\s(anonymous)'
    bep_id_rx = '.+User:\s([0-9]+)'
    bep_android_specs_rx = 'I/DeveloperSendLogsEmail\([0-9]+\):\s(.+)$'
    bep_ios_specs_rx = '.+I/DeveloperSendLogsEmail:\s.+\((.+)\)$'
    bep_appsup_rx = '.+/Library/Application Support/([0-9]+)/'
    android_crash_rx = '.+beginning\sof\scrash$'
    ios_crash_rx = '.+Crash detected.+'
    ios_failure_rx = '.+= True'
    android_lang_rx = '.+DeviceLanguage:([\w]+)$'
    ios_pref_bib_rx = '.+preferredBible\?resourceId=LLS%3A([.\w]+)$'
    android_pref_bib1_rx = '.+PreferredBible:LLS:([.\w]+)$'
    android_pref_bib2_rx = '.+preferredResourceId=LLS:([.\w]+)&dataTypeReference=bible'
    android_reading_plan_rx = '.+readingPlanTitle=([\s\w]+),\s.+'
    firebase_rx = '.+FirebaseInstanceId.+'
    fatal_rx = '.+fatal.+'

    with open(each_iter_file, 'r', encoding='latin-1') as current_log:
        detected = False
        failed = False
        for line in current_log:
            if search(f'{ios_date_time_rx}{ios_launched1_rx}', line):
                multi1 = search(f'{ios_date_time_rx}{ios_launched1_rx}', line) 
                add_if_new(multi1.group(2), app_name)
                add_if_new(multi1.group(3), app_v)
                add_if_new(multi1.group(4), device)
                add_if_new(multi1.group(5), os_name)
                add_if_new(multi1.group(6), os_v)
                add_if_new(multi1.group(7), lang)
                add_if_new(multi1.group(8), user_id)
            elif search(f'{ios_date_time_rx}{ios_launched2_rx}', line):
                multi2 = search(f'{ios_date_time_rx}{ios_launched2_rx}', line) 
                add_if_new(multi2.group(2), app_name)
                add_if_new(multi2.group(3), app_v)
                add_if_new(multi2.group(9), device)
                add_if_new(multi2.group(5), os_name)
                add_if_new(multi2.group(6), os_v)
                add_if_new(multi2.group(7), lang)
                add_if_new(multi2.group(8), user_id)
            elif search(f'{android_date_time_rx}{android_launched_rx}', line):
                android_launched = search(f'{android_date_time_rx}{android_launched_rx}', line)
                add_if_new('Android', os_name)
                add_if_new(android_launched.group(2), user_id)
            elif search(f'{ios_date_time_rx}.+{user1_rx}', line):
                user_equals1 = search(f'{ios_date_time_rx}.+{user1_rx}', line)
                add_if_new('iOS', os_name)
                add_if_new(user_equals1.group(2), user_id)
            elif search(f'{user2_rx}', line):
                user_equals2 = search(f'{user2_rx}', line)
                print(user_equals2.group(1))
            elif search(f'{ios_date_time_rx}{user_sup_rx}', line):
                user_sup = search(f'{ios_date_time_rx}{user_sup_rx}', line)
                add_if_new('iOS', os_name)
                add_if_new(user_sup.group(2), user_id)
            elif search(f'{ios_date_time_rx}{lls1_rx}', line):
                lls1 = search(f'{ios_date_time_rx}{lls1_rx}', line)
                add_if_new('iOS', os_name)
                add_if_new(lls1.group(2), user_id)
            elif search(f'{android_date_time_rx}{lls2_rx}', line):
                android_lls2 = search(f'{android_date_time_rx}{lls2_rx}', line)
                add_if_new('Android', os_name)
                add_if_new(android_lls2.group(2), user_id)
            elif search(f'{android_date_time_rx}{lls1_rx}', line):
                lls_fire = search(f'{android_date_time_rx}{lls1_rx}', line)
                add_if_new('Android', os_name)
                add_if_new(lls_fire.group(2), user_id)
            elif search(f'{android_date_time_rx}{android_mod_rx}', line):
                mod_file = search(f'{android_date_time_rx}{android_mod_rx}', line)
                add_if_new('Android', os_name)
                add_if_new(mod_file.group(2), user_id)
            elif search(f'{android_date_time_rx}{fire_items_rx}', line):
                items_fire = search(f'{android_date_time_rx}{fire_items_rx}', line)
            elif search(f'{ios_date_time_rx}{anon_rx}', line):
                anon_user = search(f'{ios_date_time_rx}{anon_rx}', line)
                add_if_new('iOS', os_name)
                add_if_new(anon_user.group(2), user_id)
            elif search(f'{android_date_time_rx}{bep_id_rx}', line):
                android_bep_id = search(f'{android_date_time_rx}{bep_id_rx}', line)
                add_if_new('Android', os_name)
                add_if_new('Bible Engagement Project', app_name)
                add_if_new(android_bep_id.group(2), user_id)
            elif search(f'{bep_ios_date_time_rx}{bep_id_rx}', line):
                ios_bep_id = search(f'{bep_ios_date_time_rx}{bep_id_rx}', line)
                add_if_new('iOS', os_name)
                add_if_new('Bible Engagement Project', app_name)
                add_if_new(ios_bep_id.group(2), user_id)
            elif search(f'{android_date_time_rx}{bep_android_specs_rx}', line):
                android_bep_specs = search(f'{android_date_time_rx}{bep_android_specs_rx}', line)
                print(android_bep_specs.groups())
            elif search(f'{bep_ios_date_time_rx}{bep_ios_specs_rx}', line):
                ios_bep_specs = search(f'{bep_ios_date_time_rx}{bep_ios_specs_rx}', line)
                add_if_new('iOS', os_name)
                add_if_new('Bible Engagement Project', app_name)
                add_if_new(ios_bep_specs.group(2), app_v)
            elif line.startswith('iP'):
                # print(line)
                add_if_new(line, device)
            elif search(f'{bep_ios_date_time_rx}{bep_appsup_rx}', line):
                bep_appsup = search(f'{bep_ios_date_time_rx}{bep_appsup_rx}', line)
                add_if_new('iOS', os_name)
                add_if_new(bep_appsup.group(2), user_id)
            elif search(f'{android_crash_rx}', line):
                add_if_new('Android', os_name)
                crash.append(line)
            elif search(f'{ios_crash_rx}', line):
                add_if_new('iOS', os_name)
                crash.append(line)
            elif search(f'{ios_failure_rx}', line):
                add_if_new('iOS', os_name)
                failure.append(line)
            elif re.search(f'{fatal_rx}', line, re.IGNORECASE):
                fatal.append(line)
            elif search(f'{android_reading_plan_rx}', line):
                android_reading_plan = search(f'{android_reading_plan_rx}', line)
                add_if_new(android_reading_plan.group(1), android_reading_plans)
            elif search(f'{android_date_time_rx}{android_lang_rx}', line):
                android_lang = search(f'{android_date_time_rx}{android_lang_rx}', line)
                add_if_new('Android', os_name)
                add_if_new(android_lang.group(2), lang)
            elif search(f'{ios_date_time_rx}{ios_pref_bib_rx}', line):
                ios_pref_bib = search(f'{ios_date_time_rx}{ios_pref_bib_rx}', line)
                add_if_new('iOS', os_name)
                add_if_new(f'LLS:{ios_pref_bib.group(2)}', preferred)
            elif search(f'{android_pref_bib1_rx}', line):                
                android_pref_bib1 = search(f'{android_pref_bib1_rx}', line)
                add_if_new('Android', os_name)
                add_if_new(f'LLS:{android_pref_bib1.group(1)}', preferred)
            elif search(f'{android_pref_bib2_rx}', line):
                android_pref_bib2 = search(f'{android_pref_bib2_rx}', line)
                add_if_new('Android', os_name)
                add_if_new(f'LLS:{android_pref_bib2.group(1)}', preferred)
            elif search(firebase_rx, line):
                add_if_new('Android', os_name)
        

    if len(device) > 1:
        longest = max(device, key=len)
        for varient in device:
            if varient != longest:
                device.remove(varient)
    if len(os_name) > 1 and 'Fire Os' in os_name:
        for name in os_name:
            if name != 'Fire Os':
                os_name.remove(name)

    group_sum = [os_name, os_v, app_name, app_v, device, lang, user_id, preferred, android_reading_plans, crash, failure, fatal]   
    return group_sum


# def diy_search():
    # This function will allow user to search for string of their choice
        

def organize_results(log_data):
    num = 0
    category = [
        '\nOs:', '\nOs version(s):', '\nApp:', '\nApp version(s):', '\nDevice:', '\nLanguage:', '\nUser ID(s):', '\nPreferred Bible(s):', '\nReading Plans:', '\nCrash(es):', '\nOften but not always indicates failure:', '\nFatal Error:'
        ]
    for log in log_data:
        if len(log) > 0:
            log.sort()
            print(category[num])
            if num < 9:
                print(*log_data[num], sep = ', ')
            else:
                print(*log_data[num], sep = '\n')
        num += 1
    print('\n')


unzip_iter()    



