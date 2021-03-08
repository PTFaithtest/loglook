# add in regex for ANdroid and Bep
# TO DO Piar all results with date stamps
# TO DO write function "findzip" whihc will find zipped file regardless of name

from zipfile import ZipFile
from re import search
from pathlib import Path

zipped_logs = Path.home().joinpath('loglook', 'info.zip')


def unzip_iter(logzip):
    # based on code given in https://thispointer.com/python-how-to-unzip-a-file-extract-single-multiple-or-all-files-from-a-zip-archive/
    with ZipFile(logzip, 'r') as zipObj:
        list_of_fileNames = zipObj.namelist()
        print(list_of_fileNames)
        print('STARTING\n\n')
        for file_name in list_of_fileNames:
            if file_name.endswith('.log'):
                zipObj.extract(file_name)
                print(f'\nCurrent Log: {file_name}\n')
                get_info(file_name)
        print('\n\nFINISHED')


def get_info(each_iter_file):
    date_time_rx ='([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]:[0-9][0-9][0-9])'
    launched1_rx = '.+Application launched \(([\w]+)/([.\d]+)\s\(([\w]+);.+CPU\s([\w]+)\s([.\d]+).+\s([\w]+)\)\s/\s([0-9]+)\)$'
    launched2_rx = '.+Application launched \(([\w]+)/([.\d]+)\s\([\w]+;.+CPU\s([\w]+)\s([.\d]+).+\s([\w]+)\)\s/\s([0-9]+)\s/\s(.+)\)$'
    user1_rx = 'userId=\s?([0-9]+)&'
    user2_rx = 'UserID=([0-9]+)"'
    # need to get another speciman to see what correct regex will be, it might start with time date ^^^
    user_sup_rx = '\sSupport/Users/([0-9]+)/'
    ios_lls_rx = '.+new items: \[{\s([0-9]+)/LLS:'
    android_lls_rx = '\s([0-9]+)/LLS:'
    # needs further refinement ^^^

    with open(each_iter_file, 'r') as current_log:
        for line in current_log:
            if search(f'{date_time_rx}{launched1_rx}', line):
                multi1 = search(f'{date_time_rx}{launched1_rx}', line) 
                print(multi1.groups()) 
            elif search(f'{date_time_rx}{launched2_rx}', line):
                multi2 = search(f'{date_time_rx}{launched2_rx}', line) 
                print(multi2.group(1, 2, 3, 8, 4, 5, 6, 7))     
            elif search(f'{date_time_rx}.+{user1_rx}', line):
                user_equals1 = search(f'{date_time_rx}.+{user1_rx}', line)
                print(user_equals1.groups())
            elif search(f'{user2_rx}', line):
                user_equals2 = search(f'{user2_rx}', line)
                print(f'\n\nENDS IN ":\n\n{line}')
                print(user_equals2.group(1))
            elif search(f'{user_sup_rx}', line):
                user_sup = search(f'{user_sup_rx}', line)
                print(user_sup.group(1))
            elif search(f'{date_time_rx}{ios_lls_rx}', line):
                ios_lls = search(f'{date_time_rx}{ios_lls_rx}', line)
                print(ios_lls.groups())
            elif search(f'{android_lls_rx}', line):
                android_lls = search(f'{android_lls_rx}', line)
                print(android_lls.group(1))
                print(f'PROBABLY ANDROID LLS:\n{line}')
            elif search('anonymous', line):
                print(f'ANON USER:\n{line}')
            # elif search('users', line) or search('Users', line):
                # print(line)

unzip_iter(zipped_logs)
