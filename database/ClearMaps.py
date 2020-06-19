#coding: utf-8
import os, sqlite3

db_dir = "Maps.db"

#reset db tables
db = sqlite3.connect(db_dir, check_same_thread=True)
dbc = db.cursor()

commands = {
    "DELETE FROM %s":["Name", "Code", "XML", "YesVotes", "NoVotes", "Perma", "Del", "TopTime", "TopTimeNick", "Updated"],
	 }
for commands, tables in commands.items():
    for table in tables:
        dbc.execute(commands % table)
db.commit()
