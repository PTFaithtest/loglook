# TO DO 
# make single search function (prevent duplication of same code in current "both searches" function)


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
downloaded = []


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


def both_searches(status, source):   
    with ZipFile(source, 'r') as zipObj:
        list_of_fileNames = zipObj.namelist()
        if status:
            while True:
                more = input('Do you want to search more? (y = "yes", n = "no")\n')
                more = more.lower()
                if more == 'n':
                    return
                elif more == 'y':
                    lower = True
                    diy_search = input('Enter your search term.  For a case sensitive search, prefix cs: to the search term, without adding a space, using lower case.\n')
                    diy_search = re.escape(diy_search)
                    # automatically escapes any special regex included in user's request
                    if diy_search.startswith('cs:'):
                        lower = False
                        diy_search = diy_search.replace('cs:', '')
                    if lower:
                        diy_search = diy_search.lower()
                    print(f'Your search term: {diy_search}')
                    # search_funct('file_name', list_of_fileNames, custom_search('file_name', diy_search))
                    for file_name in list_of_fileNames:
                        if file_name.endswith('.log') or file_name.endswith('.txt'):
                            print(file_name)
                            zipObj.extract(file_name)
                            # custom_search(file_name, diy_search) 
                            with open(file_name, 'r', encoding='latin-1') as current_log:
                                for line in current_log:
                                    if lower:
                                        line = line.lower()
                                    if search(f'{diy_search}', line):
                                        print(line)                    
                else:
                    print('Entry invalid.  Please try again')                    
        else:
            for file_name in list_of_fileNames:
                if file_name.endswith('.log') or file_name.endswith('.txt'):
                    print(file_name)
                    zipObj.extract(file_name)
                    tally = get_info(file_name)
            organize_results(tally)


def unzip_iter():
    # based on code given in https://thispointer.com/python-how-to-unzip-a-file-extract-single-multiple-or-all-files-from-a-zip-archive/
    logzip = findzip()
    zip_file = zip_folder.joinpath(logzip)
    # searchreq = None
    tallydone = False
    both_searches(tallydone, zip_file) 
    tallydone = True
    # cust_resp = search_ask()
    # if cust_resp is not None:
    both_searches(tallydone, zip_file) 
    Path(zip_file).rename(finished.joinpath(logzip))
    print(f'Moving {logzip} to {finished}.  It will be deleted the next time this script is run.')    
    
   

def add_if_new(item, item_list):
    if item == 'anonymous':
        item = 'Anonymous'
    if item not in item_list:
        item_list.append(item)
        return item_list


def custom_search(each_iter_file, search_term):
    with open(each_iter_file, 'r', encoding='latin-1') as current_log:
        for line in current_log:
            lower_line = line.lower()
            if search(f'{search_term}', lower_line):
                print(line)


def get_info(each_iter_file):
    ios_date_time_rx = r'([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9])'
    bep_ios_date_time_rx = r'([0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]:[0-9][0-9][0-9])'
    android_date_time_rx = r'([0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]\.[0-9][0-9][0-9] )'
    ios_launched1_rx = r'.*Application launched \(([\w]+)/([.\d]+) \(([\w]+);.+CPU ([\w]+) ([.\d]+).+ ([\w]+)\) / ([0-9]+)\)$'
    ios_launched2_rx = r'.*Application launched \(([\w]+)/([.\d]+) \(([\w]+);.+CPU ([\w]+) ([.\d]+).+ ([\w]+)\) / (.+) / (.+)\)$'
    # ios_launched2_rx = r'.*Application launched \(([\w]+)/([.\d]+) \(([\w]+);.+CPU ([\w]+) ([.\d]+).+ ([\w]+)\) / ([0-9]+) / (.+)\)$'
    android_launched_rx = r'.+Application launched / ([0-9]+)$'
    android_version_rx = r'.+/OurApp.+Version: (.+)'
    user1_rx = r'userId= ?([0-9]+)&'
    user2_rx = r'UserID=([0-9]+)"'
    user3_rx = r'.+"userId" : ([0-9]+)'
    user_sup_rx = r'.+ Support/Users/([0-9]+)/'
    lls1_rx = r'.+items?: \[?\{? ?([0-9]+)/.+'
    lls2_rx = r'.+synced: ([0-9]+)/.+'
    android_mod_rx = r'.+state\(Modified\): ([0-9]+)/'
    fire_items_rx = r'.+items: \[\{"id":"([0-9]+)/'
    anon_rx = r'.+User is (anonymous)'
    bep_id_rx = r'.+User: ([0-9]+)'
    bep_android_specs_rx = r'I/DeveloperSendLogsEmail\([0-9]+\): (.+)$'
    bep_ios_specs_rx = r'.+I/DeveloperSendLogsEmail: .+\((.+)\)$'
    bep_appsup_rx = r'.+/Library/Application Support/([0-9]+)/'
    android_crash_rx = r'.+beginning of crash$'
    ios_crash_rx = r'.+Crash detected.+'
    ios_failure_rx = r'.+= True'
    android_lang_rx = r'.+DeviceLanguage:([\w]+)$'
    ios_pref_bib_rx = r'.+preferredBible\?resourceId=LLS%3A([.\w]+)$'
    android_pref_bib1_rx = r'.+PreferredBible:LLS:([.\w]+)$'
    android_pref_bib2_rx = r'.+preferredResourceId=LLS:([.\w]+)&dataTypeReference=bible'
    android_reading_plan_rx = r'.+readingPlanTitle=([ \w]+), .+'
    firebase_rx = r'.+FirebaseInstanceId.+'
    fatal_rx = r'.+fatal.+'
    ios_local_rx = r'.+Resource (.+) is a local LogosResource'
    android_local_rx =r'.+\[resourceId=(.+), version=(.+), local=true\]'


    with open(each_iter_file, 'r', encoding='latin-1') as current_log:
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
                if multi2.group(8) == '(null)':
                    add_if_new('anonymous', user_id)
                else:
                    add_if_new(multi2.group(8), user_id)
            elif search(f'{android_version_rx}', line):
                android_version = search(f'{android_version_rx}', line)
                add_if_new(android_version.group(1), app_v)
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
                add_if_new(user_equals2.group(1), user_id)
            elif search(f'{user3_rx}', line):
                user_equals3 = search(f'{user3_rx}', line)
                add_if_new(user_equals3.group(1), user_id)
            elif search(f'{ios_date_time_rx}{user_sup_rx}', line):
                user_sup = search(f'{ios_date_time_rx}{user_sup_rx}', line)
                add_if_new('iOS', os_name)
                if user_sup.group(2) != '0':
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
            elif search(ios_local_rx, line):
                ios_local_res = search(ios_local_rx, line)
                add_if_new(ios_local_res.group(1), downloaded)
            elif search(android_local_rx, line):
                android_local_res = search(android_local_rx, line)
                add_if_new(android_local_res.group(1), downloaded)
    if len(device) > 1:
        longest = max(device, key=len)
        for varient in device:
            if varient != longest:
                device.remove(varient)
    if len(os_name) > 1 and 'Fire Os' in os_name:
        for name in os_name:
            if name != 'Fire Os':
                os_name.remove(name)
    group_sum = [os_name, os_v, app_name, app_v, device, lang, user_id, preferred, android_reading_plans, crash, failure, fatal, downloaded]   
    return group_sum
      

def organize_results(log_data):
    num = 0
    category = [
        '\nOs:', '\nOs version(s):', '\nApp:', '\nApp version(s):', '\nDevice:', '\nLanguage:', '\nUser ID(s):', '\nPreferred Bible(s):', '\nReading Plans:', '\nCrash(es):', '\nOften but not always indicates failure:', '\nFatal Error:', '\nDownloaded Books Mentioned:'
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



