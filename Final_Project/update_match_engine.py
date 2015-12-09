__author__ = 'Qingchuan'

import management
import Person
import channel_server
import update_chattarget_engine


def update_match(usr_login):

    print("Updating "+usr_login+" match list")

    num_NewMatch = updateMutualMatches(usr_login)

    usr_personal_info = Person.Person.query(
            ancestor=management.person_key(usr_login)).fetch(1)[0]

    if num_NewMatch > 0:
        usr_personal_info.usr_notification = num_NewMatch
        usr_personal_info.usr_viewed_updates = False

        usr_personal_info.put()

        # send my self notification
        channel_server.notifiyclient(usr_login)


# worst case O(kn) k is the number of matching attributes, n is the number of accounts
def updateMutualMatches(usr_login):

    new_match = 0

    # Step1 get current usr information
    usr_personal_info = Person.Person.query(
            ancestor=management.person_key(usr_login)).fetch(1)[0]
    usr_current_matches = usr_personal_info.current_matches
    usr_school = usr_personal_info.person_school
    print("Usr_school is "+usr_school)

    # Step2 go over current match list, remove unmatched items according to some threshold setting
    for usr_i in usr_current_matches:
        usr_i_info =  Person.Person.query(
            ancestor=management.person_key(usr_i)).fetch(1)[0]
        usr_i_school = usr_i_info.person_school
        print("Usr_i_school= "+usr_i_school+" Usr_school = "+usr_school)
        if usr_i_school != usr_school:
            usr_current_matches.remove(usr_i)

    # Step3 go over the database to add any new matches to the list
    all_usrs = Person.Person.query().fetch()
    for usr_i in all_usrs:
        usr_i_account = usr_i.person_account
        if usr_i_account != str(usr_login):
            # see if it is not in the current match list
            in_list_already = find_in_list(usr_current_matches, usr_i_account)

            # a POTENTIAL candidate
            if not in_list_already:
                usr_i_info = Person.Person.query(
                    ancestor=management.person_key(usr_i_account)).fetch(1)[0]
                usr_i_school = usr_i_info.person_school
                if usr_i_school == usr_school:
                    print("Going to append "+usr_i_account+" to "+(str(usr_login)))
                    usr_current_matches.append(usr_i_account)

                    # try to test and add this potential new match to chat list
                    update_chattarget_engine.updateMutualMatches(usr_login, usr_i_account)

                    new_match = new_match + 1
                usr_i_info.put()

    # Step4 go over other accounts to see if current usr can be a candidate or should be removed, can be combined into Step3 for concise
    all_usrs = Person.Person.query().fetch()
    for usr_i in all_usrs:
        usr_i_account = usr_i.person_account
        print(str(usr_i_account) == str(usr_login))
        if str(usr_i_account) != str(usr_login):
            usr_i_has_new_noti = False
            we_match_and_i_dont_have_you = doWeMatch(usr_i_account, str(usr_login))
            # add this usr, update usr_i info, send usr_i notification
            if we_match_and_i_dont_have_you:
                usr_i_info = Person.Person.query(
                    ancestor=management.person_key(usr_i_account)).fetch(1)[0]
                usr_i_match_list = usr_i_info.current_matches
                usr_i_notification = usr_i_info.usr_notification
                print("Going to append "+(str(usr_login))+" to "+usr_i_account)
                usr_i_match_list.append(str(usr_login))

                # try to test and add this potential new match to chat list
                update_chattarget_engine.updateMutualMatches(usr_i_account, usr_login)

                usr_i_info.usr_notification = usr_i_notification + 1
                usr_i_info.usr_viewed_updates = False
                usr_i_has_new_noti = True

            should_i_delete_you = deleteYou(usr_i_account, str(usr_login))
            # delete this usr
            if should_i_delete_you:
                usr_i_info = Person.Person.query(
                    ancestor=management.person_key(usr_i_account)).fetch(1)[0]
                usr_i_match_list = usr_i_info.current_matches
                print("Going to remove "+(str(usr_login))+" from "+usr_i_account)
                usr_i_match_list.remove(str(usr_login))

            usr_i_info.put()
            if usr_i_has_new_noti:
                print("I will notify him")
                channel_server.notifiyclient(usr_i_account)

    # Step5 return number of new matches
    usr_personal_info.put()
    return new_match


def find_in_list(usr_current_matches, usr_i_account):
    for account in usr_current_matches:
        if usr_i_account == account:
            return True
    return False


def doWeMatch(usr_i_account, usr_login):
    usr_i_info = Person.Person.query(
                    ancestor=management.person_key(usr_i_account)).fetch(1)[0]

    usr_info = Person.Person.query(
                    ancestor=management.person_key(usr_login)).fetch(1)[0]

    usr_i_match_list = usr_i_info.current_matches

    for in_list in usr_i_match_list:
        if in_list == usr_login:
            return False

    if usr_i_info.person_school == usr_info.person_school:
        return True

    return False


def deleteYou(usr_i_account, usr_login):
    usr_i_info = Person.Person.query(
                    ancestor=management.person_key(usr_i_account)).fetch(1)[0]

    usr_info = Person.Person.query(
                    ancestor=management.person_key(usr_login)).fetch(1)[0]

    usr_i_match_list = usr_i_info.current_matches

    for in_list in usr_i_match_list:
        if in_list == usr_login:
            # I am in his old list and now no longer qualified
            if usr_i_info.person_school != usr_info.person_school:
                return True
    return False
