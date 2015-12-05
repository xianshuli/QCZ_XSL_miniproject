__author__ = 'Qingchuan'

import channel_server

def update_match():
    update_item1 = {
        "client_ID": ,
        "num_of_match": 1,
    }

    # send out notifications
    channel_server.notifiyclient(update_item1["client_ID"], update_item1["num_of_match"])

