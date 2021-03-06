# TO DO 
# get rid of print statements that call out which regex found this result
# Consolidate rx for iOS date time and BEP iOS date time
# add BEP crash
# Printing the results should be improved
# Preferred Bible regex needs refinement
# regex needs to be added for problems downloading books


from zipfile import ZipFile
from re import search
from pathlib import Path
from os import listdir
from sys import exit

doc_num = 0

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

rez = (
        f'Os: {os_name} {os_v}\nApp: {app_name} {app_v}\nDevice: {device}\nLanguage: {lang}\nUser ID: {user_id}\n'
        f'Preferred Bible(s): {preferred}\nDetected Reading Plans: \n{android_reading_plans}\n'
        f'{len(crash)} Crash(es):\n{crash}'
        ) 


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
    # print(file_list)
    # print(zip_list)  
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


def unzip_iter(dox):
    # based on code given in https://thispointer.com/python-how-to-unzip-a-file-extract-single-multiple-or-all-files-from-a-zip-archive/
    logzip = findzip()
    with ZipFile(logzip, 'r') as zipObj:
        list_of_fileNames = zipObj.namelist()
        print(list_of_fileNames)
        for file_name in list_of_fileNames:
            if file_name.endswith('.log') or file_name.endswith('.txt'):
                zipObj.extract(file_name)
                # print(f'\nCurrent Log: {file_name}\n')
                dox += 1
                tally = get_info(file_name, dox)
    organize_results(tally)

def add_if_new(item, item_list):
    if item not in item_list:
        item_list.append(item)
        return item_list


def get_info(each_iter_file, dox):
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
    bep_ios_specs_rx = '.+I/DeveloperSendLogsEmail:\s(.+)$'
    bep_appsup_rx = '.+/Library/Application Support/([0-9]+)/'
    android_crash_rx = '.+beginning\sof\scrash$'
    ios_crash_rx = '.+Crash detected.+'
    android_lang_rx = '.+DeviceLanguage:([\w]+)$'
    ios_pref_bib_rx = '.+preferredBible\?resourceId=LLS%3A([.\w]+)$'
    android_pref_bib1_rx = '.+PreferredBible:LLS:([.\w]+)$'
    android_pref_bib2_rx = '.+preferredResourceId=LLS:([.\w]+)&dataTypeReference=bible'
    android_reading_plan_rx = '.+readingPlanTitle=([\s\w]+),\s.+'
    firebase_rx = '.+FirebaseInstanceId.+'

    with open(each_iter_file, 'r', encoding='latin-1') as current_log:
        detected = False
        # line_no = 1
        for line in current_log:
            # if line_no == 1:
                # print(dox, line_no, line)
            # elif line_no % 100 == 0:
                # print(dox, line_no, line)
            if detected:
                crash.append(line)
                detected = False
            elif search(f'{ios_date_time_rx}{ios_launched1_rx}', line):
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
                print(f'\n\nENDS IN ":\n\n{line}')
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
                print('\n\nITEMS ANDROID\n\n')
                print(items_fire.groups())
            elif search(f'{ios_date_time_rx}{anon_rx}', line):
                anon_user = search(f'{ios_date_time_rx}{anon_rx}', line)
                add_if_new('iOS', os_name)
                add_if_new(anon_user.group(2), user_id)
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
            elif search(f'{android_crash_rx}', line):
                add_if_new('Android', os_name)
                print(line)
                detected = True
            elif search(f'{ios_date_time_rx}{ios_crash_rx}', line):
                add_if_new('iOS', os_name)
                crash.append(line)
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
            # line_no += 1
        

    if len(device) > 1:
        longest = max(device, key=len)
        for varient in device:
            if varient != longest:
                device.remove(varient)
    if len(os_name) > 1 and 'Fire Os' in os_name:
        for name in os_name:
            if name != 'Fire Os':
                os_name.remove(name)

    group_sum = [os_name, os_v, app_name, app_v, device, lang, user_id, preferred, android_reading_plans, crash]   
    return group_sum

def organize_results(log_data):
    num = 0
    category = [
        '\nOs:', '\nOs version(s):', '\nApp:', '\nApp version(s):', '\nDevice:', '\nLanguage:', '\nUser ID(s):', '\nPreferred Bible(s):', '\nReading Plans:', '\nCrash(es):'
        ]
    for log in log_data:
        if len(log) > 0:
            log.sort()
            print(category[num])
            print(*log_data[num], sep = ', ')
        num += 1
    print('\n')


unzip_iter(doc_num)    



