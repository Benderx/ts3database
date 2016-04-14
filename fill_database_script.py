import time
from filler import Filler
import config
import ts3
import datetime
import logging
import logging.handlers

logger = logging.getLogger('TS3bot')
logger.setLevel(logging.INFO)
timed_log = logging.handlers.TimedRotatingFileHandler('fill.log', when='D', interval=1)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
timed_log.setFormatter(formatter)
logger.addHandler(timed_log)

# Outer loop running through all challenger teams (dataM)
#server.send_command('servernotifyregister', keys={'event': 'textprivate'})


def fill_database(ts3conn):
    filler = Filler()
    start = time.time()

    allClients = ts3conn.clientlist()
    clientList = []

    channels = ts3conn.channellist()


    afk_cid = ''

    for x in channels:
        print(type(x))
        if x['channel_name'] == 'AFK':
            afk_cid = x['cid']

    for x in allClients:
        if (int(x['client_type']) == 0) and (str(x['cid']) != str(afk_cid)):
            clientList.append(x)
            continue

    for x in clientList:
        x['username'] = x['client_nickname']
        x['start_time'] = datetime.datetime.now()
        x['end_time'] = datetime.datetime.now()
        x['total_time'] = 0
        x['idle_time'] = 0
        x['messege_sent'] = False
        x['online'] = True

        x.pop("cid", None)
        x.pop("client_type", None)
        x.pop("client_nickname", None)

    filler.update_all_users(clientList, ts3conn, afk_cid)

    print(time.time() - start)



if __name__ == "__main__":
    # USER, PASS, HOST, ...
    HOST = 'www.quinnspeak.com'
    PORT = 10011
    SID = 1
    USER = str(config.username)
    PASS = str(config.password)

    with ts3.query.TS3Connection(HOST, PORT) as ts3conn:
        ts3conn.login(client_login_name=USER, client_login_password=PASS)
        ts3conn.use(sid=SID)
        # hi = ts3conn.clientlist()
        # print(type(hi))
        # for client in ts3conn.clientlist():
        #     if client["client_nickname"] == 'Ryan':
        #         msg = "Hi {}".format(client["client_nickname"])
        #         ts3conn.clientpoke(clid=client["clid"], msg=msg)

        try:
            fill_database(ts3conn)
        except:
            logger.exception('Error Raised')

        # while True:
        #     try:
        #         fill_database(ts3conn)
        #     except:
        #         logger.exception('Error Raised')
        #         break
        #     time.sleep(15)