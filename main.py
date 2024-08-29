# This script can be used to perform different osint actions on instagram.
#       1. Find out which insta ids are tagged in particular user's story.
#       2. Find Common accounts followed by two accounts that user follows.
# This can be useful to dox someone as one can easily hide tags in story.
import os
import sys
import instagrapi.exceptions
from instagrapi import Client
from dotenv import load_dotenv


def changeLogin():
    os.remove('.env')
    print('[*] Setting new account to be used.....')
    nu = input('[*] Enter your Username--> ')
    np = input('[*] Enter your password--> ')
    ncontent = f"USER={nu}\nPASSWORD={np}"
    nfile = open('.env', 'x')
    nfile.write(ncontent)
    nfile.close()
    print('[*] Program Exiting..... Please re-run to login with new account.')
    sys.exit()


def commonFollowing():
    print('[*]---------- Find the accounts followed by 2 accounts! ----------[*]')
    acc1 = input('[*] Enter 1st insta id--> ')
    acc2 = input('[*] Enter 2nd insta id--> ')
    uid1 = str(cl.user_id_from_username(acc1))
    uid2 = str(cl.user_id_from_username(acc2))
    acc1Followings = cl.user_following_v1(user_id=uid1)
    acc2Followings = cl.user_following_v1(user_id=uid2)
    i = 1
    acc1Dic = {}
    for element in acc1Followings:
        temp = str(element)
        prnt = temp.split("' ")
        uname = prnt[1]
        fname = prnt[2]
        acc1Dic[uname] = fname
        i += 1

    j = 1
    acc2Dic = {}
    for element in acc2Followings:
        temp = str(element)
        prnt = temp.split("' ")
        uname = prnt[1]
        fname = prnt[2]
        acc2Dic[uname] = fname
        j += 1

    k = 0
    for i in acc2Dic:
        for j in acc1Dic:
            if i == j:
                k += 1
                print('[', k, '] ', i, '\n  ', acc2Dic[i])
            else:
                pass
    menu()


def menu():
    print('\n[*]---------- Menu ----------[*]')
    print('[1] Find Hidden tags in story.')
    print('[2] Find Common Followings.')
    print('[3] Change saved insta account.')
    print('[4] Exit')
    choice = input('\nEnter your choice--> ')
    if choice == '1':
        hiddenTags()
    elif choice == '2':
        commonFollowing()
    elif choice == '3':
        changeLogin()
    elif choice == '4':
        print('[*] Exiting the program.....!')
        cl.logout()
        sys.exit()
    else:
        print('Invalid Input!')


def hiddenTags():
    print('\n[*]---------- Find the hidden tags in someones story! ----------[*]')
    while True:
        # Getting target from user.
        target = input('\nEnter the insta id of target (to return to main menu type back)--> ')
        if target == "back":
            break
        else:
            try:
                uid = int(cl.user_id_from_username(target))  # Getting user id of the target.
                print('[*] User id: ', uid)
                story = str(cl.user_stories(user_id=uid))  # Getting story of the user.
                # Printing some info about user.
                print('[*] Username: ', target)
                # print('[*] info: ', bio)
                # Checking if there are any mentions in story.
                if story.__contains__('StoryMention'):  # Just a matcher to check if someone is mentioned.
                    men = story.split(
                        'StoryMention')  # Splitting the response from 'StoryMention' and storing in list men[]
                    length = men.__len__()  # Finding number of mentions in story.
                    print('[*] There are total ', length - 1, ' people tagged in story.')
                    i = 1  # Counter for iterating through mentions.
                    for items in men:
                        rep = "(user=UserShort(pk='1', "  # String to replace
                        temp = str(men[i])  # Storing mentions in temp variable in string format
                        prnt = temp.split(" stories=[]", 1)  # Removing useless data from ' stories=[]' to end.
                        print('[', i, '] ', prnt[0].replace(rep, ''))  # Printing the refined data
                        i += 1  # Increment to iterate through list
                        if i == length:  # To prevent IndexOutOfBound error in 'temp = str(men[i])'
                            break
                else:
                    print('[*] No mentions found!')  # If no-one is mentioned.
            except instagrapi.exceptions.UserNotFound:
                print('[*] Invalid user name please check and try again')
            except IndexError:
                print('[*] Please ensure that user has uploaded the story and try again!')
    menu()


if __name__ == '__main__':
    f = os.path.exists('.env')
    if not f:
        print('[*] Config file not found.....!')
        print('[*] Creating one.....')
        u = input('[*] Enter your Username--> ')
        p = input('[*] Enter your password--> ')
        content = f"USER={u}\nPASSWORD={p}"
        file = open('.env', 'x')
        file.write(content)
        file.close()
    # Fetching USERNAME and PASSWORD from .env file.
    load_dotenv()
    uname = os.getenv('USER')
    passwd = os.getenv('PASSWORD')
    print('[*] Logging in as ', uname)
    # Logging in instagram using USERNAME and PASSWORD.
    cl = Client()
    cl.login(username=uname, password=passwd)
    menu()
