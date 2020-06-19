#coding: utf-8
import os, sqlite3

db_dir = "Users.db"

#reset db tables
db = sqlite3.connect(db_dir, check_same_thread=True)
dbc = db.cursor()

commands = {
    "DELETE FROM %s":["Account", "BanLog", "Chats", "DDoS", "Election", "IPPermaBan", "Tribe", "UserPermaBan", "UserTempBan", "UserTempMute", "Users"],
    "DELETE FROM sqlite_sequence WHERE name = '%s'":["Account", "BanLog", "Chats", "DDoS", "Election", "IPPermaBan", "Tribe", "UserPermaBan", "UserTempBan", "UserTempMute", "Users"]
	}
for commands, tables in commands.items():
    for table in tables:
        dbc.execute(commands % table)
db.commit()
