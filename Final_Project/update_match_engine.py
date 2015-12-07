__author__ = 'Qingchuan'

import management
import Person


def update_match(usr_login):

    print("Updating "+usr_login+" match list")

    num_NewMatch = updateMutualMatches(usr_login)

    usr_personal_info = Person.Person.query(
            ancestor=management.person_key(usr_login)).fetch(1)[0]

    usr_personal_info.usr_notification = num_NewMatch
    usr_personal_info.usr_viewed_updates = False

    usr_personal_info.put()


def updateMutualMatches(usr_login):

    return 2
