from re import search

date_time_rx ='([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]:[0-9][0-9][0-9])'
launched_rx = '.+Application launched \(([\w]+)/([.\d]+)\s\(([\w]+);.+CPU\s([\w]+)\s([.\d]+).+\s([\w]+)\)\s/\s([0-9]+)\)$'
user1_rx = 'userId=\s([0-9]+)&'
# need to get another speciman to see what correct regex will be, it might start with time date ^^^
user2_rx = 'UserID=([0-9]+)"'
# need to get another speciman to see what correct regex will be, it might start with time date ^^^
user_sup_rx = '\sSupport/Users/([0-9]+)/'
user_lls_rx = 'new items: \[{\s([0-9]+)/LLS:'
android_user_lls_rx = '[{\s([0-9]+)/LLS:'
# needs further refinement ^^^


print('Hello logs!\n')
with open('iOSlog.log', 'r') as current_log:
    for line in current_log:
        if search(f'^{date_time_rx}{launched_rx}', line):
            multi = search(f'^{date_time_rx}{launched_rx}', line) 
            # multi = search(f'^{date_time_rx}.+Application launched \(([\w]+)/([.\d]+)\s\(([\w]+);.+CPU\s([\w]+)\s([.\d]+).+\s([\w]+)\)\s/\s([0-9]+)\)$', line)
            # multi = search('^([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]:[0-9][0-9][0-9]).+Application launched \(([\w]+)/([.\d]+)\s\(([\w]+);.+CPU\s([\w]+)\s([.\d]+).+\s([\w]+)\)\s/\s([0-9]+)\)$', line)
            # multi = search('Application launched \(([\w]+)/([.\d]+)\s\(([\w]+);.+CPU\s([\w]+)\s([.\d]+).+\s([\w]+)\)\s/\s([0-9]+)\)$', line)
            # multi = search('Application launched \(([\w]+)/([.\d]+)\s\(([\w]+);.+CPU\s([\w]+)\s([.\d]+).+\)\s/\s([0-9]+)\)$', line)
            # multi = search('Application launched \(([\w]+)/([.\d]+)\s\(([\w]+);.+CPU\s([\w]+)\s.+\)\s/\s([0-9]+)\)$', line)
            # multi = search('Application launched \(([\w]+)/([.\d]+)\s\(([\w]+);.+\)\s/\s([0-9]+)\)$', line)
            # multi = search('Application launched \(([\w]+)/([.\d]+)\s\(.+\)\s/\s([0-9]+)\)$', line)
            # multi = search('Application launched \(([\w]+).+\s/\s([0-9]+)\)$', line)
            # multi = search('Application launched \(.+\s/\s([0-9]+)\)$', line)
            # multi = search('Application launched \(([\w]+)/.+\)\s\(.*\)\s/\s([0-9]+)\)$', line)
            print(multi.groups())
        # elif search('userId=\s(([0-9]+))&', line):
        elif search(f'{user1_rx}', line):
            user_equals1 = search(f'{user1_rx}', line)
            print(user_equals1.group(1))
            print(f'EMAIL THIS TO JOE:\n{line}')
        elif search(f'{user2_rx}', line):
            user_equals2 = search(f'{user2_rx}', line)
            # user_equals2 = search('UserID=([0-9]+)"', line)
            print(user_equals2.group(1))
            print(f'EMAIL THIS TO JOE:\n{line}')
        elif search(f'{user_sup_rx}', line):
            user_sup = search(f'{user_sup_rx}', line)
            print(user_sup.group(1))
        elif search(f'{user_lls_rx}', line):
            user_lls = search(f'{user_lls_rx}', line)
            print(user_lls.group(1))
            print(f'EMAIL THIS TO JOE:\n{line}')
        elif search(f'{user_lls_rx}', line):
            user_lls = search(f'{user_lls_rx}', line)
            print(user_lls.group(1))
            print(f'EMAIL THIS TO JOE:\n{line}')
        elif search('anonymous', line):
            print(f'EMAIL THIS TO JOE:\n{line}')
        # elif search('users', line) or search('Users', line):
            # print(line)
print('\nGoodbye logs!')
