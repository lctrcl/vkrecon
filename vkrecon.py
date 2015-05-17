from __future__ import absolute_import
from __future__ import print_function
#!/usr/bin/python
# -*- coding: utf8 -*-
import vk_api
import sys
import itertools
from termcolor import colored
from six.moves import input

# TODO: optimize api calls

__author__ = "Igor Ivanov, @lctrcl"
__license__ = "GPL"
__banner__ = 'VK Recon Tool'
__version__ = '0.4.0'

print((colored(__banner__ + ' ' + __version__ + '\n', 'blue')))

login = ''
password = ''

mutual_friends = {}
mutual_friends_set = []
company = ''
users = []
employees = []

try:
    import config  # where we define login/password/company
    login = config.login
    password = config.password
    company = config.company
except:
    pass

print(' -[*] VK API conection is establishing')
try:
    vk = vk_api.VkApi(login, password)
    print(' -[+] OK')
except Exception as e:
    print((colored(' -[-] Auth problems', 'red')))
    print("Exception: %s" % str(e), file=sys.stderr)
    sys.exit(1)


def get_mutual_pairs():   # get from list 'users'
    mutual_friends_pairs = itertools.combinations(users, 2)
    for m in mutual_friends_pairs:
        user1 = vk.method('users.get', {'user_ids': m[0][u'id'], 'fields': 'contacts, screen_name'})
        user2 = vk.method('users.get', {'user_ids': m[1][u'id'], 'fields': 'contacts, screen_name'})
        print(('\t-[] Finding common friends between {} and {}'). \
            format(get_printable_user(user1[0], 'white'),
                   get_printable_user(user2[0], 'white')))
        find_common_friends(user1, user2)
    return


def find_common_friends(user1, user2):
    mfp1 = set(vk.method('friends.get', {'user_id': user1[0][u'id']})['items'])
    mfp2 = set(vk.method('friends.get', {'user_id': user2[0][u'id']})['items'])
    mfp = list(mfp1.intersection(mfp2))
    for m2 in mfp:
        if m2:
            u2 = vk.method('users.get', {'user_ids': m2, 'fields': 'contacts, screen_name'})[0]
            if u2 not in users:
                users.append(u2)
                print('\t\t' + colored(get_printable_user(u2), 'green'))
            else:
                print('\t\t' + get_printable_user(u2, 'yellow') \
                    + ' | already in the base')

    return


def get_printable_user(user, color='green'):
    string = colored(user[u'first_name'] + ' ' + user[u'last_name']
                   + ' |id ' + str(user[u'id']), color).encode('utf-8')
    if 'mobile_phone' in user:
        string += ' Mobile phone: ' + user[u'mobile_phone'].encode('utf-8')
    if 'screen_name' in user:
        string += ' Screen name: ' + user[u'screen_name'].encode('utf-8')
    return string



def search_newsfeed():
    search = vk.method('newsfeed.search', {'q': company})
    print(search)
    return


def get_user_wall(userid):
    search = vk.method(
        'wall.get', {'owner_id': userid, 'count': 3, 'filter': 'owner'})
    for r in search.get('items'):
        print(r[u'text'])
    return


def get_users_nearby(userid):
    search = vk.method(
        'users.getNearby',
        {'latitude': 55.803742, 'longitude': 37.551469, 'radius': 1})
    print(search)


def main():
    print(('\n ' + '-' * 65))
    print((' -[*] Searching for all users with company ' +
          colored("{}", 'red') + ' in theirs profiles:\n').format(company))
    rs = vk.method('users.search', {'company': company, 'fields': 'contacts, screen_name'})
    for user in rs.get('items'):
        print(get_printable_user(user))
        mutual_friends[user[u'id']] = vk.method(
            'friends.get', {'user_id': user[u'id']})
        users.append(user)
        employees.append(user)

    print(('\n ' + '-' * 65))
    print(' -[*] Searching for all mutual friends between these employees:\n')

    for key in list(mutual_friends.keys()):
        if mutual_friends[key]['count'] > 0:
            mutual_friends_set.append(set(mutual_friends[key]['items']))

    u = list(set.intersection(*mutual_friends_set))

    if u:
        for z in u:
            user = vk.method('users.get', {'user_ids': z, 'fields': 'contacts, screen_name'})
            print(get_printable_user(user[0]))
    else:
        print(colored(' -[x] None common friends found', 'red'))

    print('\n -[*] Searching for mutual friends between pairs of employees:\n')

    shall = True
    while shall:
        shall = input("%s (y/N) " %
                          'Do you want to go deeper?').lower() == 'y'
        if shall:
            print((colored('\n -[*] Digging deeper:\n', 'yellow')))
            get_mutual_pairs()

    print('\n -[*] Final list\n')
    print(('\n -[-] Employees of {}:\n').format(company))

    for u in employees:
        print(get_printable_user(u))
    print('\n -[-] Secondary connections:\n')
    for u in users:
        if u not in employees:
            print(get_printable_user(u, 'yellow'))

main()
