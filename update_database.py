from create_database import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from datetime import date, timedelta


class Filler:
    def __init__(self):
        self.engine = create_engine(
        "postgresql://postgres:hog55555@localhost:5432/teamspeak"
        )
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.warning_afk = 1800 * 1000
        self.marked_afk = 2700 * 1000
        Base.metadata.create_all(self.engine, checkfirst=True)

    # Updates the table of users

    def set_users_offline(self):
        online_users = self.usersOnline = self.session.query(UserInfo).filter(
            UserInfo.online == True).all()
        for y in online_users:
            y.online = False
        self.session.commit()


    def update_all_users(self, allusers, server, afkid):
        online_users = self.usersOnline = self.session.query(UserInfo).filter(
            UserInfo.online == True).all()


        # Appends all clients id's who are connected to the server currently
        all_client_ids = []
        for x in allusers:
            # if str(x['clientDatabaseId']) not in all_client_ids:
            all_client_ids.append(x['client_database_id'])
        client_infos = {}

        # Searches through all online users to either update their afk/idle time or set them offline if they left
        for y in online_users:
            # If they are still connected
            if str(y.client_database_id) in all_client_ids:
                for x in allusers:
                    if y.username == x['username']:
                        # should check for success
                        client_infos[x['clid']] = server.clientinfo(clid=x['clid'])
                        break
                y.end_time = datetime.datetime.now()
                y.total_time = (y.end_time - y.start_time).total_seconds()
                client_info = client_infos[x['clid']]
                y.idle_time = int(client_info[0]['client_idle_time'])

                #if x.idleTime >= self.marked_afk:
                #    x.online = False
                #    x.endTime = x.endTime - datetime.timedelta(minutes=15)
                #    x.idleTime = x.idleTime - (15 * 60)

                # update to not send_commands

                # if (int(client_info[0]['client_idle_time']) >= self.warning_afk) and (y.messege_sent == False):
                #     server.send_command('sendtextmessage', keys={'targetmode': 1, 'target': x['clid'], 'msg':
                #         'If you are not afk, respond to this messege. You will be marked afk in 15 minutes.'})
                #     y.messege_sent = True
                #     print(x['username']+ 'lol1')
                # elif (int(client_info[0]['client_idle_time']) >= self.marked_afk) and (y.messege_Sent == True):
                #     server.send_command('clientmove', keys={'clid': x['clid'], 'cid': afkid})
                #     print(x['username'] + 'lol2')
                #     x['online'] = False
                #     y.messege_sent = False

                if (int(client_info[0]['client_idle_time']) >= self.marked_afk):
                    # server.send_command('clientmove', keys={'clid': x['clid'], 'cid': afkid})
                    # print(x['username'] + 'lol2')
                    # x['online'] = False
                    y.end_time = datetime.datetime.now() - timedelta(milliseconds=y.idle_time)
                    y.total_time = (y.end_time - y.start_time).total_seconds()
                    y.idle_time = 0
                    y.online = False


                for x in allusers:
                    if x['client_database_id'] == str(y.client_database_id):
                        allusers.remove(x)
                        break
            # If they were found to be offline
            else:
                y.end_time = datetime.datetime.now() - timedelta(milliseconds=y.idle_time)
                y.total_time = (y.end_time - y.start_time).total_seconds()
                y.idle_time = 0
                y.online = False

        # For any users that are still online but weren't online before (adding new users)
        for x in allusers:
            if x['clid'] in client_infos.keys():
                client_info = client_infos[x['clid']]
            else:
                # should test if success
                # test = server.clientinfo(clid= x['clid'])
                # if test.is_successful:
                #     client_info = test
                client_info = server.clientinfo(clid=x['clid'])

            # if user is idle for above afk time and a messege hasnt been sent, send one

            # afkmsg = 'If you are not afk, respond to this messege. You will be marked afk in 15 minutes.'
            # if (int(client_info[0]['client_idle_time']) >= self.warning_afk) and (x['messege_sent'] == False):
            #     server.sendtextmessage(targetmode=1, target=x['clid'], msg=afkmsg)
            #     x['messege_sent'] == True
            x.pop('clid', None)
            self.session.add(UserInfo(**x))
        self.session.commit()
