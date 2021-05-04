# add in regex for Android and Bep
# regex for Fire OS and Android- date time format is different, examples of diff syntax in fire.zip and android.zip
# TO DO Piar all results with date stamps
# get rid of print statemtnets that call out which regex found this result
# In Android, the "launched" info is spread out over several different lines
# Consolidate rx for iOS date time and BEP iOS date time
# make allowance for Android message beginning of crash with the actual crash on the next line


from zipfile import ZipFile
from re import search
from pathlib import Path
from os import listdir
from sys import exit


app_name = []
app_v = []
device = []
os_name = []
os_v = []
lang = []
user_id = []
preferred = []
reading_plans = []


def findzip():
    folder = 'loglook'
    zip_folder = Path.home().joinpath(folder)
    file_list = listdir(zip_folder)
    zip_list = []
    for file in file_list:
        if file.endswith('.zip'):
            zip_list.append(file)
        else:
            continue
    print(file_list)
    print(zip_list)  
    if len(zip_list) > 1:
        print('More than one zipped file available in the loglook folder, try again after making sure that there is only one.')
        exit()
    elif len(zip_list) < 1:
        print('No zipped files available, try again after putting a zipped file in the loglook folder.') 
        exit()
    else:
        file_name = zip_list[0]
        zip_file = Path.home().joinpath(folder, file_name)
        print(zip_file)
        return zip_file


def unzip_iter():
    # based on code given in https://thispointer.com/python-how-to-unzip-a-file-extract-single-multiple-or-all-files-from-a-zip-archive/
    logzip = findzip()
    with ZipFile(logzip, 'r') as zipObj:
        list_of_fileNames = zipObj.namelist()
        print(list_of_fileNames)
        print('STARTING\n\n')
        for file_name in list_of_fileNames:
            if file_name.endswith('.log') or file_name.endswith('.txt'):
                zipObj.extract(file_name)
                print(f'\nCurrent Log: {file_name}\n')
                tally = get_info(file_name)
    print(tally)
    print('\n\nFINISHED')

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
    # need to get another speciman to see what correct regex will be, it might start with time date ^^^
    user_sup_rx = '.+\sSupport/Users/([0-9]+)/'
    # lls1_rx = '.+new items:\s\[{\s([0-9]+)/.+'
    lls1_rx = '.+items?:\s\[?\{?\s?([0-9]+)/.+'
    lls2_rx = '.+synced:\s([0-9]+)/.+'
    # android_lls_rx = '\s([0-9]+)/LLS:'
    # needs further refinement ^^^
    # android_mod_rx = '.+state\(Modified\)'
    android_mod_rx = '.+state\(Modified\):\s([0-9]+)/'
    fire_items_rx = '.+items:\s\[\{"id":"([0-9]+)/'
    anon_rx = '.+User\sis\s(anonymous)'
    bep_id_rx = '.+User:\s([0-9]+)'
    bep_android_specs_rx = 'I/DeveloperSendLogsEmail\([0-9]+\):\s(.+)$'
    bep_ios_specs_rx = '.+I/DeveloperSendLogsEmail:\s(.+)$'
    bep_appsup_rx = '.+/Library/Application Support/([0-9]+)/'
    android_lang_rx = '.+DeviceLanguage:([\w]+)$'
    pref_bib_rx = '.+preferredBible\?resourceId=LLS%3A([.\w]+)$'

    with open(each_iter_file, 'r', encoding='latin-1') as current_log:
        for line in current_log:
            if search(f'{ios_date_time_rx}{ios_launched1_rx}', line):
                multi1 = search(f'{ios_date_time_rx}{ios_launched1_rx}', line) 
                # print(multi1.groups())
                add_if_new(multi1.group(2), app_name)
                add_if_new(multi1.group(3), app_v)
                add_if_new(multi1.group(4), device)
                add_if_new(multi1.group(5), os_name)
                add_if_new(multi1.group(6), os_v)
                add_if_new(multi1.group(7), lang)
                add_if_new(multi1.group(8), user_id)
                # print(f'multi ONE {app_name}')
            elif search(f'{ios_date_time_rx}{ios_launched2_rx}', line):
                multi2 = search(f'{ios_date_time_rx}{ios_launched2_rx}', line) 
                # print(multi2.group(1, 2, 3, 9, 6, 7, 8))
                add_if_new(multi2.group(2), app_name)
                add_if_new(multi2.group(3), app_v)
                add_if_new(multi2.group(9), device)
                add_if_new(multi2.group(5), os_name)
                add_if_new(multi2.group(6), os_v)
                add_if_new(multi2.group(7), lang)
                add_if_new(multi2.group(8), user_id)
                # print(f'multi TWO {app_name}')
            elif search(f'{android_date_time_rx}{android_launched_rx}', line):
                android_launched = search(f'{android_date_time_rx}{android_launched_rx}', line)
                # print(android_launched.groups())
                add_if_new('Android', os_name)
                add_if_new(android_launched.group(2), user_id)
                # print(user_id)
            elif search(f'{ios_date_time_rx}.+{user1_rx}', line):
                user_equals1 = search(f'{ios_date_time_rx}.+{user1_rx}', line)
                # print('\n\nUSER1\n\n')
                # print(user_equals1.groups())
                add_if_new('iOS', os_name)
                add_if_new(user_equals1.group(2), user_id)
            elif search(f'{user2_rx}', line):
                user_equals2 = search(f'{user2_rx}', line)
                print(f'\n\nENDS IN ":\n\n{line}')
                print(user_equals2.group(1))
            elif search(f'{ios_date_time_rx}{user_sup_rx}', line):
                user_sup = search(f'{ios_date_time_rx}{user_sup_rx}', line)
                # print(f'\n\niOS Sup\n\n{user_sup.groups()}')
                add_if_new('iOS', os_name)
                add_if_new(user_sup.group(2), user_id)
            elif search(f'{ios_date_time_rx}{lls1_rx}', line):
                lls1 = search(f'{ios_date_time_rx}{lls1_rx}', line)
                # print('\n\nLLS1\n\n')
                # print(lls1.groups())
                add_if_new('iOS', os_name)
                add_if_new(lls1.group(2), user_id)
            elif search(f'{android_date_time_rx}{lls2_rx}', line):
                android_lls2 = search(f'{android_date_time_rx}{lls2_rx}', line)
                print('\n\nANDROID LLS2\n\n')
                print(android_lls2.groups())
                add_if_new('Android', os_name)
                add_if_new(android_lls2.group(2), user_id)
                print(user_id)
            elif search(f'{android_date_time_rx}{lls1_rx}', line):
                lls_fire = search(f'{android_date_time_rx}{lls1_rx}', line)
                print('\n\nLLS ANDROID\n\n')
                print(lls_fire.groups())
            elif search(f'{android_date_time_rx}{android_mod_rx}', line):
                mod_file = search(f'{android_date_time_rx}{android_mod_rx}', line)
                print('\n\nMOD ANDROID\n\n')
                # print(line)
                print(mod_file.groups())
                add_if_new('Android', os_name)
                add_if_new(mod_file.group(2), user_id)
                # print(user_id)
            elif search(f'{android_date_time_rx}{fire_items_rx}', line):
                items_fire = search(f'{android_date_time_rx}{fire_items_rx}', line)
                print('\n\nITEMS ANDROID\n\n')
                print(items_fire.groups())
            # elif search(f'{android_lls_rx}', line):
                # android_lls = search(f'{android_lls_rx}', line)
                # print(android_lls.group(1))
                # print(f'PROBABLY ANDROID LLS:\n{line}')
            elif search(f'{ios_date_time_rx}{anon_rx}', line):
                anon_user = search(f'{ios_date_time_rx}{anon_rx}', line)
                # print(f'ANON USER:\n{line}')
                # print(anon_user.groups())
                add_if_new('iOS', os_name)
                add_if_new(anon_user.group(2), user_id)
            # elif search('users', line) or search('Users', line):
                # print(line)
            elif search(f'{android_date_time_rx}{bep_id_rx}', line):
                android_bep_id = search(f'{android_date_time_rx}{bep_id_rx}', line)
                print('\n\nANDROID BEP ID\n\n')
                print(android_bep_id.groups())
                add_if_new('Android', os_name)
                add_if_new('Bible Engagement Project', app_name)
                add_if_new(android_bep_id.group(2), user_id)
            elif search(f'{bep_ios_date_time_rx}{bep_id_rx}', line):
                ios_bep_id = search(f'{bep_ios_date_time_rx}{bep_id_rx}', line)
                print('\n\nIOS BEP ID\n\n')
                print(ios_bep_id.groups())
                add_if_new('iOS', os_name)
                add_if_new('Bible Engagement Project', app_name)
                add_if_new(ios_bep_id.group(2), user_id)
            elif search(f'{android_date_time_rx}{bep_android_specs_rx}', line):
                android_bep_specs = search(f'{android_date_time_rx}{bep_android_specs_rx}', line)
                print(android_bep_specs.groups())
            elif search(f'{bep_ios_date_time_rx}{bep_ios_specs_rx}', line):
                ios_bep_specs = search(f'{bep_ios_date_time_rx}{bep_ios_specs_rx}', line)
                print(ios_bep_specs.groups())
            elif line.startswith('iP'):
                print(line)
                add_if_new(line, device)
            elif search(f'{bep_ios_date_time_rx}{bep_appsup_rx}', line):
                bep_appsup = search(f'{bep_ios_date_time_rx}{bep_appsup_rx}', line)
                print(bep_appsup.groups())
            elif 'crash detected' in line or 'beginning of crash' in line:
                print('CRASH DETECTED\n\n')
                print(line)
            elif 'readingPlanTitle=' in line:
                print('READING PLAN\n\n')
                print(line)
            elif search(f'{android_date_time_rx}{android_lang_rx}', line):
                android_lang = search(f'{android_date_time_rx}{android_lang_rx}', line)
                add_if_new('Android', os_name)
                add_if_new(android_lang.group(2), lang)
            elif search(f'{ios_date_time_rx}{pref_bib_rx}', line):
                ios_pref_bib = search(f'{ios_date_time_rx}{pref_bib_rx}', line)
                add_if_new('iOS', os_name)
                add_if_new(f'LLS:{ios_pref_bib.group(2)}', preferred)





    if len(device) > 1:
        longest = max(device, key=len)
        for varient in device:
            if varient != longest:
                device.remove(varient)
    # git statusprint(device)  
    group_sum = f'OS: {os_name} {os_v}\nApp: {app_name} {app_v}\nDevice: {device}\nLanguage: {lang}\nUser ID: {user_id}\nPreferred Bible(s): {preferred}'
    # print(group_sum)
    return group_sum

unzip_iter()    



