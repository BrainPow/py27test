#coding: utf-8
import re, time as _time, struct

# Modules
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers
from twisted.internet import reactor

# Library
from collections import deque

class Tribulle:    
    def __init__(this, player, server):
        this.client = player
        this.server = player.server
        this.Cursor = player.Cursor

        #Boolean
        this.SILENCE = False
        this.tribeOpen = False
        this.friendOpen = False
        this.tribeChanged = False
        this.friendChanged = False
        #String
        this.SILENCE_MESSAGE = ""
        this.tribeRanks = ""
        this.tribeData = ""
        this.friendData = ""
        #Interger
        this.tribulleID = 0                
        this.firstByteValue = 0
        this.secondByteValue = 0
        #List
        this.tribeMembers = []

    def getTime(this):
        return int(_time.time() / 60)    

    def parseTribulleCode(this, code, packet):
        if code == 52: #Cochicho.
            this.whisperMessage(packet)
        elif code == 60: #Silence.
            this.disableWhispers(packet)
        elif code == 10: #Mudar Sexo Do Rato.
            this.changeGender(packet)
        elif code == 108: #Abrir Tribo No Botão.
            this.openTribe(packet)
        elif code == 110: #Fechar Tribo.
            this.closeTribe(packet)
        elif code == 84: #Criar Tribo.
            this.newTribe(packet)
        elif code == 102: #Mudar Codigo Cafofo.
       	    this.changeHouseCode(packet)
       	elif code == 98: #Mudar Mensagem Da Tribo.
       	    this.changeTribeMessage(packet)
       	elif code == 50: #Mandar Mensagem Para Tribo.
            this.messageTribeChat(packet)
        elif code == 78: #Recrutar Jogador.
            this.invitePlayerTribe(packet)
        elif code == 80: #Aceitar Recusar Tribo.
            this.resultInvitePlayerTribe(packet)
        elif code == 132: #Historico Da Tribo.
            this.tribeHistorique(packet)
        elif code == 82: #Sair Da Tribo.
            this.leaveTribe(packet)
        elif code == 114: #Alterar Priv Tribo.
            this.changePrivTribe(packet)
        elif code == 118: #Criar Cargo Tribo.
            this.createRankTribe(packet)
        elif code == 120: #Deletar Cargo Tribo.
            this.deleteRankTribe(packet)
        elif code == 116: #Renomear Cargo Tribo.
            this.renameRankTribe(packet)
        elif code == 122: #Subir Ou Descer Cargo Tribo.
            this.changePosRankTribe(packet)
        elif code == 112: #Trocar Rank Do Jogador Na Tribo.
            this.changePlayerRankTribe(packet)
        elif code == 104: #Expulsar Jogador Da Tribo.
            this.kickPlayerTribe(packet)
        elif code == 126: #Dar Lider Na Tribo.
            this.giveOwnerTribe(packet)
        elif code == 128: #Extinguir Tribo.
            this.deleteTribe(packet)
        elif code == 28: #Abrir Lista De Amigo Botão.
            this.openFriendList(packet)
        elif code == 30: #Fechar Lista De Amigo.
            this.closeFriendList(packet)
        elif code == 18: #Adicionar Player Lista De Amigo.
            this.addPlayerFriendList(packet)
        elif code == 20: #Remover Da Lista De Amigo.
            this.deletePlayerFriendList(packet)
        elif code == 46: #Lista De Ignorados.
            this.sendIgnoredList(packet)
        elif code == 44: #Remover Da Lista De Ignorados.
            this.removePlayerIgnoredList(packet)
        elif code == 42: #Adicionar Na Lista De Ignorados.
            this.addPlayerIgnoredList(packet)
        elif code == 22: #Pedir Em Casamento.
            this.invitePlayerMarriage(packet)
        elif code == 24: #Resposta Pedido De Casamento.
            this.resultInviteMarriage(packet)
        elif code == 26: #Divorciar-se.
            this.divorceMarriage(packet)
        elif code == 54: #Criar Canal.
            this.createChannel(packet)
        elif code == 48: #Mandar Mensagem No Canal.
            this.sendMessageChannel(packet)
        elif code == 58: #Players Do Canal.
            this.listPlayersChannel(packet)
        elif code == 56: #Sair Do Canal.
            this.leaveChannel(packet)
        
    def checkExistingTribe(this, tribeName):
        this.Cursor.execute("select 1 from Tribe where Name = ?", [tribeName])
        return this.Cursor.fetchone() != None

    def getTribeMemberInfo(this, arg, playerName):
        if arg == 0:            
            this.Cursor.execute("select Gender, LastOn, TribeCode, TribeRank, Avatar from Users where Username = ?",  [str(playerName)])
            for rs in this.Cursor.fetchall():
                this.Cursor.execute("select tribeRanks from tribe where Code = ?", [rs["TribeCode"]])
                tribeRanks = this.Cursor.fetchone()
                if tribeRanks in ["None", None, ""]:
                    tribeRanks = "${trad#TG_0}-1-1-1-1-1-1-1-1-1|0|0/${trad#TG_1}-1-1-1-1-1-1-1-1-1|0|0/${trad#TG_2}-1-1-1-1-1-1-1-1-1|0|0/${trad#TG_3}-1-1-1-1-1-1-1-1-1|0|0/${trad#TG_4}-1-1-1-1-1-1-1-1-1|0|32/${trad#TG_5}-1-1-1-1-1-1-1-1-1|0|160/Estagiário-1-1-1-1-1-1-1-1-1|1|160/${trad#TG_7}-1-1-1-1-1-1-1-1-1|3|164/${trad#TG_8}-1-1-1-1-1-1-1-1-1|7|252/${trad#TG_9}-0-0-0-0-0-0-0-0-0|7|254')"
                else: tribeRanks = str(tribeRanks[0])
                return [rs["Gender"], rs["LastOn"], rs["TribeRank"], str(tribeRanks), rs["Avatar"]]
        elif arg == 1:
            for player in this.server.players.values():
                if player.playerName == str(playerName):
                    return [str(player.playerName), int(player.gender), str(player.langue), str(player.roomName), str(player.tribulle.tribeRanks), str(player.tribeRank), int(this.client.server.getplayerAvatar(str(player.playerName)))]

    def getTribeMembers(this, tribeCode):
        this.tribeMembers = []
        this.Cursor.execute("select Members from tribe where Code = ?", [this.client.tribeCode])
        members = str(this.Cursor.fetchone()[0]).split("#")
        for membro in members:
            this.Cursor.execute("select TribeCode from Users where Username = ?", [this.client.playerName])
            tribeCode = int(this.Cursor.fetchone()[0])
            if int(tribeCode) == int(this.client.tribeCode):
                this.tribeMembers.append(str(membro))
        return len(set(list(this.tribeMembers)))

    def checkConnectedTribeMembers(this, playerName):
        found = False
        for player in this.server.players.values():
            if player.playerName == str(playerName):
                found = True
        return found

    def plataformAuthentication(this, status):
        this.client.sendPacket([60, 4], struct.pack("!?", status))        

    #Whisper/Silence

    def getWhisperErrors(this, tribulleID, error):
        errors = {"offline": 11, "silence": 23}
        return struct.pack("!hibh", 53, tribulleID, errors[str(error)], 0)        

    def whisperMessage(this, packet):
        tribulleID, playerName, message = packet.readInt(), Utils.parsePlayerName(packet.readUTF()), packet.readUTF().replace("\n", "").replace("&amp;#", "&#").replace("<", "&lt;")
        if message in ["\n"] or message in ["\r"] or message in ["\x02"] or message in ["<BR>"]:
            if message in ["\n", "\r"]:
                this.server.sendModMessage(7, "<font color='#00C0FF'>[ANTI-BOT] - Suspect BOT - IP: [</font><J>"+str(this.client.ipAddress)+"<font color='#00C0FF'>]</font>")
            this.client.transport.loseConnection()
            message = ""
        if message == this.client.lastMessage and this.client.privLevel < 6:
            message = ""
        if message in [" "] >= 1 or len(message) >= 200:
            message = ""
            this.client.sendMessage("Atenção! Digite uma mensagem com menos de 200 letras!")
        isCheck = this.server.checkMessage(this.client, message)
        langue = {"EN": 1, "FR": 2, "RU": 3, "BR": 4, "ES": 5, "CN": 6, "TR": 7, "VK": 8, "PL": 9, "HU": 10, "NL": 11, "RO": 12, "ID": 13, "DE": 14, "E2": 15, "AR": 16, "PH": 17, "LT": 18, "JP": 19, "CH": 20, "FI": 21, "CZ": 22, "HR": 23, "CZ": 24, "SK": 25, "HR": 26, "BG": 27, "LV": 28, "HE": 29, "IT": 30, "ET": 31, "AZ": 32, "PT": 33}
        data = ""
        if not this.client.isGuest:
            if this.client.cheeseCount >= 0:
                if this.server.players.has_key(playerName):                
                    data = struct.pack("!hh", 66, len(this.client.playerName.lower())) + this.client.playerName.lower() + struct.pack("!i", langue[str(this.client.langue)]) + struct.pack("!h", len(playerName.lower())) + playerName.lower() + struct.pack("!h", len(message)) + message
                    player = this.server.players.get(playerName)
                    if not player.tribulle.SILENCE:
                        if not this.client.isMute:
                            if not player.playerName in [None, ""] and not player.playerName.startswith("*") and not player.playerName == this.client.playerName:
                                ignoredList = str(player.ignoredsList).split("#")
                                if not str(this.client.playerName) in ignoredList:
                                    if isCheck == False:
                                        player.sendPacket([60, 3], data)
                            this.client.sendPacket([60, 3], data)
                            bMessage = "<CH>%s <N>cochichou com <CH>%s <N>a seguinte mensagem: <CH>%s" % (str(this.client.playerName), str(playerName), str(message))
                            for admins in this.server.players.values():
                                if admins.privLevel >= 7:
                                    if not str(this.client.playerName) in ["Danshweger", "Rhaella"]:
                                        admins.sendPacket([60, 3], struct.pack("!hh", 64, len("!")) + "!" + struct.pack("!i", int(langue[str(this.client.langue)])) + struct.pack("!h", len("Whisper")) + str("Whisper") + struct.pack("!h", len(bMessage)) + str(bMessage))
                        else: this.client.sendMessage("<ROSE>Você foi mutado por um moderador e não poderá falar.")
                    else: this.client.sendPacket([60, 3], this.getWhisperErrors(tribulleID, "silence"))
                else: this.client.sendPacket([60, 3], this.getWhisperErrors(tribulleID, "offline"))
            else: this.client.sendMessage("<ROSE>Por favor, colete 2 queijos para liberar o chat e conversar com outros jogadores.")
        else: this.client.sendLangueMessage("", "$Créer_Compte_Parler")

    def disableWhispers(this, packet):
        tribulleID, type, message = packet.readInt(), packet.readByte(), packet.readUTF()
        this.client.sendPacket([60, 3], struct.pack("!hib", 61, tribulleID, 1))
        if type == 1: this.SILENCE = True
        else: this.SILENCE = False

    #Gender

    def changeGender(this, packet):
        tribulleID, gender = packet.readInt(), packet.readByte()
        this.client.gender = gender
        this.friendChanged = True
        for player in this.server.players.values():
            if int(player.tribeCode) == int(this.client.tribeCode):
                player.tribulle.tribeChanged = True
                if player.tribulle.tribeOpen == True:
                    player.tribulle.interfaceTribe()
        for player in this.server.players.values():
            friendList = str(player.friendsList).split("#")
            if str(this.client.playerName) in friendList:
                player.tribulle.friendChanged = True                
                if player.tribulle.friendOpen == True:
                    player.tribulle.loadFriendList()

    #Tribe

    def getTribeWarn(this, tribulleID, error):
        errors = {"exist": 8, "noCheeses": 13, "sucess": 0}
        return struct.pack("!hib", 85, tribulleID, errors[str(error)])

    def closeTribe(this, packet):
    	tribulleID = packet.readInt()
    	this.tribeOpen = False

    def openTribe(this, packet):
        tribulleID, type = packet.readInt(), packet.readByte()
        this.tribulleID = int(tribulleID)
        this.interfaceTribe()

    def interfaceTribe(this):
    	langue = {"EN": 1, "FR": 2, "RU": 3, "BR": 4, "ES": 5, "CN": 6, "TR": 7, "VK": 8, "PL": 9, "HU": 10, "NL": 11, "RO": 12, "ID": 13, "DE": 14, "E2": 15, "AR": 16, "PH": 17, "LT": 18, "JP": 19, "CH": 20, "FI": 21, "CZ": 22, "HR": 23, "CZ": 24, "SK": 25, "HR": 26, "BG": 27, "LV": 28, "HE": 29, "IT": 30, "ET": 31, "AZ": 32, "PT": 33}    	
        if this.client.tribeName in ["", None, "None"]:
            this.client.sendPacket([60, 3], struct.pack("!hib", 109, this.tribulleID, 17))
        else:
            this.tribeOpen = True
            if this.tribeChanged == True:
                this.Cursor.execute("select tribeRanks from tribe where Code = ?", [this.client.tribeCode])
                this.tribeRanks = str(this.Cursor.fetchone()[0])
                onlinesData = ""
                offlineData = ""
                data = struct.pack("!h", 130) + struct.pack("!i", this.client.tribeCode) + struct.pack("!h", len(this.client.tribeName)) + this.client.tribeName
                data += struct.pack("!h", len(this.client.tribeMessage)) + this.client.tribeMessage + struct.pack("!I", this.client.tribeHouse) + struct.pack("!h", this.getTribeMembers(this.client.tribeCode))
                for selected in set(list(this.tribeMembers)):
                    connected = this.checkConnectedTribeMembers(str(selected))
                    if connected == True:
                        rankID = 0
                        info = this.getTribeMemberInfo(1, str(selected))                    
                        for a, b in enumerate(str(info[4]).split("/")):
                            b = str(b).split("-")                        
                            if str(b[0]) == str(info[5]):
                                rankID = int(a)
                        onlinesData += struct.pack("!i", int(info[6])) + struct.pack("!h", len(info[0])) + str(info[0]) + struct.pack("!b", int(info[1])) + struct.pack("!i", int(info[6])) + struct.pack("!i", 0) + struct.pack("!B", int(rankID)) + "\x00\x00\x00" + struct.pack("!b", langue[str(info[2])]) + struct.pack("!h", len(info[3])) + str(info[3])
                    else:
                        info = this.getTribeMemberInfo(0, str(selected))
                        rankID = 0
                        for a, b in enumerate(str(info[3]).split("/")):
                            b = str(b).split("-")
                            if str(b[0]) == str(info[2]):
                                rankID = int(a)
                        offlineData += struct.pack("!i", int(info[4])) + struct.pack("!h", len(selected)) + str(selected) + struct.pack("!b", int(info[0])) + struct.pack("!i", int(info[4])) + struct.pack("!i", int(info[1])) + struct.pack("!B", int(rankID)) + "\x00\x00\x00" + struct.pack("!b", 1) + struct.pack("!h", 0)
                data += str(onlinesData) + str(offlineData)
                data += struct.pack("!h", len(this.tribeRanks.split("/")))
                for rank in this.tribeRanks.split("/"):
                    rankInfo = str(rank).split("-")
                    calculationRanks = str(rankInfo[len(rankInfo) - 1]).split("|")
                    data += struct.pack("!h", len(rankInfo[0])) + str(rankInfo[0]) + struct.pack("!h", 0)
                    data += struct.pack("!B", int(calculationRanks[1])) + struct.pack("!B", int(calculationRanks[2]))
                this.tribeData = data
                this.tribeChanged = False
            else:
                data = this.tribeData
            this.client.sendPacket([60, 3], data)    

    def sendTribe(this):
        this.Cursor.execute("select tribeRanks from tribe where Code = ?", [this.client.tribeCode])
        this.tribeRanks = str(this.Cursor.fetchone()[0])
        firstValue = 0; secondValue = 0
        for rank in this.tribeRanks.split("/"):
            rank = str(rank).split("-")
            if str(rank[0]) == str(this.client.tribeRank):
                rank = str(rank).split("|")
                firstValue = int(rank[1]); secondValue = int(str(rank[2]).replace("']", ""))
   	data = struct.pack("!hh", 89, len(this.client.tribeName)) + this.client.tribeName + struct.pack("!i", this.client.tribeCode)
   	data += struct.pack("!h", len(this.client.tribeMessage)) + this.client.tribeMessage + "\x00\x00\x00\x00\x00" + struct.pack("!h", len(this.client.tribeRank)) + str(this.client.tribeRank) + struct.pack("!h", 0) + struct.pack("!BB", int(firstValue), int(secondValue))
   	this.client.sendPacket([60, 3], data)   		

    def newTribe(this, packet):
        tribulleID, tribeName = packet.readInt(), packet.readUTF()
        if not this.checkExistingTribe(tribeName) or tribeName == "":
            if this.client.shopCheeses >= 500:
                #Settings
                this.server.lastChatID += 1
                createTime = this.getTime()                
                this.Cursor.execute("insert into Tribe values (null, ?, 'Hosgeldin ^^', '0', '', ?, ?, '${trad#TG_0}-1-1-1-1-1-1-1-1-1|0|0/${trad#TG_1}-1-1-1-1-1-1-1-1-1|0|0/${trad#TG_2}-1-1-1-1-1-1-1-1-1|0|0/${trad#TG_3}-1-1-1-1-1-1-1-1-1|0|0/${trad#TG_4}-1-1-1-1-1-0-1-1-1|0|32/${trad#TG_5}-1-1-1-0-1-0-1-1-1|0|160/Estagiário-1-1-0-0-1-0-1-1-1|1|160/${trad#TG_7}-1-0-0-0-1-0-1-1-0|3|164/${trad#TG_8}-0-0-0-0-0-0-0-0-0|7|252/${trad#TG_9}-0-0-0-0-0-0-0-0-0|7|254', 0)", [tribeName, this.client.playerName, this.server.lastChatID])
                this.client.shopCheeses -= 500
                this.client.tribeCode = this.Cursor.lastrowid
                this.client.tribeJoined = createTime
                this.client.tribeName = tribeName
                this.client.tribeChat = this.server.lastChatID
                this.client.tribeMessage = "Welcome ^^"
                this.client.tribeHouse = 0
                this.Cursor.execute('update Users set TribeCode = ? where Username = ?', [this.client.tribeCode, this.client.playerName])
                this.Cursor.execute('update Users set TribeRank = ? where Username = ?', ["${trad#TG_9}", this.client.playerName])
                this.client.tribeRank = "${trad#TG_9}"

                this.tribeChanged = True
                this.sendTribe()

                this.insertHistorique(1, str(tribeName), str(this.client.playerName))
                    
                this.client.sendPacket([60, 3], this.getTribeWarn(tribulleID, "sucess"))
            else:
                this.client.sendPacket([60, 3], this.getTribeWarn(tribulleID, "noCheeses"))
        else:
            this.client.sendPacket([60, 3], this.getTribeWarn(tribulleID, "exist"))

    def changeHouseCode(this, packet):
    	tribulleID, houseCode = packet.readInt(), packet.readInt()    	
        this.Cursor.execute('UPDATE tribe set House = ? where Code = ?', [int(houseCode), this.client.tribeCode])
        this.client.room.CursorMaps.execute('select Code from maps where Code = ?', [int(houseCode)])
        mapInfo = this.client.room.CursorMaps.fetchone()
        if not mapInfo in ["", None, "None"]:
            for player in this.server.players.values():
                if int(player.tribeCode) == int(this.client.tribeCode):
                    player.tribeHouse = int(houseCode)
            this.insertHistorique(8, str(houseCode), str(this.client.playerName))
            this.interfaceTribe()
        else:
            this.client.sendPacket([16, 4], ["16"])

    def changeTribeMessage(this, packet):
    	tribulleID, message = packet.readInt(), packet.readUTF()
    	this.Cursor.execute('UPDATE tribe set Message = ? where Code = ?', [str(message), this.client.tribeCode])
    	for player in this.server.players.values():
            if int(player.tribeCode) == int(this.client.tribeCode):
        	player.tribeMessage = str(message)
        	player.sendPacket([60, 3], struct.pack("!hh", 125, len(this.client.playerName.lower())) + this.client.playerName.lower() + struct.pack("!h", len(message)) + message)
        	player.tribulle.tribeChanged = True
        this.insertHistorique(6, str(message), str(this.client.playerName))
        this.interfaceTribe()

    def messageTribeChat(this, packet):
        tribulleID, message = packet.readInt(), packet.readUTF()
        if not this.client.tribeName in ["", None, "None"] and not this.client.tribeCode in [0, None, "None", ""]:
            for player in this.server.players.values():
                if int(player.tribeCode) == int(this.client.tribeCode):
                    player.sendPacket([60, 3], struct.pack("!hh", 65, len(this.client.playerName.lower())) + this.client.playerName.lower() + struct.pack("!h", len(message)) + message)

    def invitePlayerError(this, tribulleID, error):
        errors = {"offline": 10, "haveTribe": 17, "sucess": 0}
        return struct.pack("!hib", 79, tribulleID, errors[str(error)])

    def invitePlayerTribe(this, packet):
        tribulleID, playerName = packet.readInt(), packet.readUTF()
        found = False
        for player in this.server.players.values():
            if player.playerName == str(playerName):
                found = True
                if player.tribeCode in [0, None, "None", ""]:
                    this.client.sendPacket([60, 3], this.invitePlayerError(tribulleID, "sucess"))
                    player.sendPacket([60, 3], struct.pack("!hh", 86, len(this.client.playerName.lower())) + this.client.playerName.lower() + struct.pack("!h", len(this.client.tribeName)) + this.client.tribeName)
                else:
                    this.client.sendPacket([60, 3], this.invitePlayerError(tribulleID, "haveTribe"))
        if found == False: this.client.sendPacket([60, 3], this.invitePlayerError(tribulleID, "offline"))

    def resultInvitePlayerTribe(this, packet):
        tribulleID, playerName, result = packet.readInt(), packet.readUTF(), packet.readByte()
        myRank = ""
        if result in [1]: #Accept
            for player in this.server.players.values():
                if player.playerName == str(playerName):
                    player.sendPacket([60, 3], struct.pack("!hh", 91, len(this.client.playerName.lower())) + this.client.playerName.lower() + struct.pack("!?", True))
                    player.sendPacket([60, 3], struct.pack("!hh", 87, len(this.client.playerName.lower())) + this.client.playerName.lower() + struct.pack("!b", result))
                    this.Cursor.execute('update Users set TribeCode = ? where Username = ?', [player.tribeCode, this.client.playerName])
                    this.Cursor.execute("select Members from tribe where Code = ?", [player.tribeCode])
                    allPlayers = str(this.Cursor.fetchone()[0]) + "#" + str(this.client.playerName)
                    this.Cursor.execute('update tribe set Members = ? where Code = ?', [str(allPlayers), player.tribeCode])
                    this.client.tribeName = player.tribeName
                    this.client.tribeCode = player.tribeCode
                    this.client.tribeChat = player.tribeChat
                    this.client.tribeMessage = player.tribeMessage
                    this.client.tribeHouse = player.tribeHouse
                    for a, b in enumerate(player.tribulle.tribeRanks.split("/")):
                        b = str(b).split("-")
                        if a == 0:
                            myRank = str(b[0])
                    this.Cursor.execute('update Users set TribeRank = ? where Username = ?', [str(myRank), this.client.playerName])
                    this.client.tribeRank = str(myRank)
                    reactor.callLater(0.5, this.sendTribe)
                    this.insertHistorique(2, str(this.client.playerName), str(playerName))
                if int(player.tribeCode) == int(this.client.tribeCode):
                    player.sendPacket([60, 3], struct.pack("!hh", 93, len(this.client.playerName.lower())) + this.client.playerName.lower())
            for player in this.server.players.values():
                if int(player.tribeCode) == int(this.client.tribeCode):
                    player.tribulle.tribeChanged = True
                    if player.tribulle.tribeOpen == True:
                        player.tribulle.interfaceTribe()
                    
        elif result in [0]: #Decline
            for player in this.server.players.values():
                if player.playerName == str(playerName):
                    player.sendPacket([60, 3], struct.pack("!hh", 87, len(this.client.playerName.lower())) + this.client.playerName.lower() + struct.pack("!b", result))

    def tribeHistorique(this, packet):                
        tribulleID = packet.readInt()        
        this.Cursor.execute("select Historique from tribe where Code = ?", [this.client.tribeCode])        
        historique = str(this.Cursor.fetchall()[0][0])
        dictSplit = historique.split("#")
        dictResult = historique.replace("{", "").replace('"', "").replace("}", "").replace(",", ":").split("#")
        data = struct.pack("!hi", 133, tribulleID) + struct.pack("!h", len(dictSplit))
        for dictType in dictResult:   
            type = dictType.split(":")
            if str(type[0]) != "cible":
                time = this.getTime()
                for selected in type:
                    if selected.isdigit():
                        time = int(selected)
                filtro = {"membreExclu": 3, "membreParti": 4, "membreAjoute": 2, "code": 8, "message": 6, "tribu": 1}
                string = '{"'+str(type[0])+'":"'+str(type[1])+'","'+str(type[2])+'":"'+str(type[3])+'"}'
                data += struct.pack("!i", int(time)) + struct.pack("!i", filtro[str(type[0])]) + struct.pack("!h", len(string)) + string
            if str(type[0]) == "cible":
                string = '{"'+str(type[0])+'":"'+str(type[1])+'","'+str(type[2])+'":"'+str(type[3])+'","'+str(type[4])+'":"'+str(type[5].replace("|", "#").replace(">", "}").replace("<", "{"))+'","'+str(type[6])+'":"'+str(type[7])+'"}'
                data += struct.pack("!i", int(type[8])) + struct.pack("!i", 5) + struct.pack("!h", len(string)) + string
        data += struct.pack("!i", len(dictSplit))
        this.client.sendPacket([60, 3], data)

    def insertRankHistorique(this, arg0, arg1, arg2, arg3):
        this.Cursor.execute("select Historique from tribe where Code = ?", [this.client.tribeCode])        
        historique = str(this.Cursor.fetchall()[0][0])        
        if not historique in ["", None, "None"]:            
            string = '{"cible":"'+str(arg0)+'","ordreRang":"'+str(arg1)+'","rang":"'+str(arg2)+'","auteur":"'+str(arg3)+'":'+str(this.getTime())+'}#' + str(historique)
        this.Cursor.execute('update tribe set Historique = ? where Code = ?', [str(string), this.client.tribeCode])

    def insertHistorique(this, value, arg, arg1):
        this.Cursor.execute("select Historique from tribe where Code = ?", [this.client.tribeCode])        
        historique = str(this.Cursor.fetchall()[0][0])
        filtro = {3: "membreExclu", 4: "membreParti", 2: "membreAjoute", 8: "code", 6: "message", 1: "tribu"}        
        if historique in ["", None, "None"]:
            string = '{"'+str(filtro[value])+'":"'+str(arg)+'","auteur":'+str(arg1)+'":'+str(this.getTime())+'}'
        else:
            string = '{"'+str(filtro[value])+'":"'+str(arg)+'","auteur":'+str(arg1)+'":'+str(this.getTime())+'}#' + str(historique)
        this.Cursor.execute('update tribe set Historique = ? where Code = ?', [str(string), this.client.tribeCode])        

    def leaveTribe(this, packet):        
        tribulleID = packet.readInt()        
        deleteTribe = False
        deleted = False
        exitSucess = False   	
        this.Cursor.execute("select Members from tribe where Code = ?", [this.client.tribeCode])
        players = str(this.Cursor.fetchone()[0])
        allPlayers = players.split("#")
        if len(allPlayers) == 1:
            deleteTribe = True

        if deleteTribe != True:
            ranksCount = len(this.tribeRanks.split("/")) - 1
            rankID = 0
            for c, d in enumerate(this.tribeRanks.split("/")):
                d = str(d).split("-")
                if str(d[0]) == str(this.client.tribeRank):
                    rankID = int(c)
            if int(rankID) != int(ranksCount):
                num = None
                for a, b in enumerate(allPlayers):
                    if str(b) == str(this.client.playerName):
                        num = a
                del allPlayers[num]
                allPlayers = '#'.join(allPlayers)
                this.Cursor.execute('update tribe set Members = ? where Code = ?', [str(allPlayers), this.client.tribeCode])
                this.insertHistorique(4, str(this.client.playerName), str(this.client.playerName))
                for player in this.server.players.values():
                    if int(player.tribeCode) == int(this.client.tribeCode):
                        player.sendPacket([60, 3], struct.pack("!hh", 92, len(this.client.playerName.lower())) + this.client.playerName.lower())
                        player.tribulle.tribeChanged = True                        
                exitSucess = True
            else:
                this.client.sendPacket([60, 3], struct.pack("!hib", 83, tribulleID, 3))
            
        if deleteTribe == True:            
            this.Cursor.execute("delete from tribe where Code = ?", [this.client.tribeCode])
            this.Cursor.execute('update Users set TribeCode = ? where Username = ?', [0, this.client.playerName])        
            this.client.tribeName = ""        
            this.client.tribeCode = 0
            this.client.tribeMessage = ""
            this.client.tribeHouse = 0
            deleted = True
            
        if deleted == True:
            this.client.sendPacket([60, 3], struct.pack("!hh", 92, len(this.client.playerName.lower())) + this.client.playerName.lower())
            this.Cursor.execute('update Users set TribeCode = ? where TribeCode = ?', [0, this.client.tribeCode])
            
        if exitSucess == True:                        
            this.Cursor.execute('update Users set TribeCode = ? where Username = ?', [0, this.client.playerName])        
            this.client.tribeName = ""        
            this.client.tribeCode = 0
            this.client.tribeMessage = ""
            this.client.tribeHouse = 0

    def changePrivTribe(this, packet):
        tribulleID, rankID, changeColum, status = packet.readInt(), packet.readByte(), packet.readInt(), packet.readByte()
        this.firstByteValue = 0
        this.secondByteValue = 0
        this.Cursor.execute("select tribeRanks from tribe where Code = ?", [this.client.tribeCode])
        this.tribeRanks = str(this.Cursor.fetchone()[0])
        rankStatus = {10: "adminForum", 9: "loadNP", 8: "changeHouse", 7: "playMusic", 6: "kickPlayer", 5: "invitePlayer", 4: "changeRank", 3: "editRank", 2: "changeMessage"}        
        for a, b in enumerate(this.tribeRanks.split("/")):
            rankInfo = str(b).split("-")
            if a == int(rankID):
                adminForum = rankInfo[1]; loadNP = rankInfo[2]; changeHouse = rankInfo[3]; playMusic = rankInfo[4]
                kickPlayer = rankInfo[5]; invitePlayer = rankInfo[6]; changeRank = rankInfo[7]; editRank = rankInfo[8]; changeMessage = rankInfo[9]
                if rankStatus[int(changeColum)] == "adminForum":                    
                    adminForum = int(status)                    
                elif rankStatus[int(changeColum)] == "loadNP":                    
                    loadNP = int(status)                                        
                elif rankStatus[int(changeColum)] == "changeHouse":                    
                    changeHouse = int(status)                                            
                elif rankStatus[int(changeColum)] == "playMusic":                    
                    playMusic = int(status)                                        
                elif rankStatus[int(changeColum)] == "kickPlayer":                    
                    kickPlayer = int(status)                                        
                elif rankStatus[int(changeColum)] == "invitePlayer":                    
                    invitePlayer = int(status)                                    
                elif rankStatus[int(changeColum)] == "changeRank":
                    changeRank = int(status)                                
                elif rankStatus[int(changeColum)] == "editRank":                    
                    editRank = int(status)                    
                elif rankStatus[int(changeColum)] == "changeMessage":                    
                    changeMessage = int(status)                    
                        
                if int(adminForum) == 0:
                    this.firstByteValue += 4
                if int(loadNP) == 0:
                    this.firstByteValue += 2
                if int(changeHouse) == 0:
                    this.firstByteValue += 1
                if int(playMusic) == 0:
                    this.secondByteValue += 128
                if int(kickPlayer) == 0:
                    this.secondByteValue += 64
                if int(invitePlayer) == 0:
                    this.secondByteValue += 32
                if int(changeRank) == 0:
                    this.secondByteValue += 16
                if int(editRank) == 0:
                    this.secondByteValue += 8
                if int(str(changeMessage)[0]) == 0:
                    this.secondByteValue += 4

                newRank = [int(adminForum), int(loadNP), int(changeHouse), int(playMusic), int(kickPlayer), int(invitePlayer), int(changeRank), int(editRank), int(str(changeMessage)[0])]
                newRank = [str(x) for x in newRank]
                newRank = '-'.join(newRank)
                rankEdit = str(b.split("-")[0]) + "-" + str(newRank) + "|"+str(this.firstByteValue)+"|"+str(this.secondByteValue)+""
                replace = this.tribeRanks.split("/"); replace[int(a)] = str(rankEdit); replace = '/'.join(replace)
                this.tribeRanks = str(replace)
                this.Cursor.execute('update tribe set tribeRanks = ? where Code = ?', [str(replace), this.client.tribeCode])
                for player in this.server.players.values():
                    player.tribulle.tribeChanged = True
                    if player.tribulle.tribeOpen == True:
                        player.tribulle.interfaceTribe()
                
    def createRankTribe(this, packet):
        tribulleID, rankName = packet.readInt(), packet.readUTF()
        if re.match("^[ a-zA-Z0-9]*$", rankName):
            tribeRanks = this.tribeRanks.split("/")
            newTribeRanks = '/'.join(tribeRanks[1:])
            newRank = str(rankName) + "-1-1-1-1-1-1-1-1-1|0|0/"
            newRank = str(tribeRanks[0]) + "/" + str(newRank) + str(newTribeRanks)
            this.Cursor.execute('update tribe set tribeRanks = ? where Code = ?', [newRank, this.client.tribeCode])
            for player in this.server.players.values():
                if int(player.tribeCode) == int(this.client.tribeCode):
                    player.tribulle.tribeChanged = True
                    if player.tribulle.tribeOpen == True:
                        player.tribulle.interfaceTribe()
        else:
            this.client.sendPacket([60, 3], struct.pack("!hib", 117, tribulleID, 7))

    def deleteRankTribe(this, packet):
        tribulleID, rankID = packet.readInt(), packet.readByte()
        num = None
        tribeRanks = this.tribeRanks.split("/")
        for a, b in enumerate(tribeRanks):
            if int(a) == int(rankID):
                num = int(a)
        del tribeRanks[num]
        newRank = '/'.join(tribeRanks)
        this.Cursor.execute('update tribe set tribeRanks = ? where Code = ?', [newRank, this.client.tribeCode])
        for player in this.server.players.values():
            if int(player.tribeCode) == int(this.client.tribeCode):
                player.tribulle.tribeChanged = True
                if player.tribulle.tribeOpen == True:
                    player.tribulle.interfaceTribe()

    def renameRankTribe(this, packet):
        tribulleID, rankID, rankName = packet.readInt(), packet.readByte(), packet.readUTF()
        if rankID == 9:
            this.client.sendMessage("No momento, não é possível alterar o nome do rank Lider Espiritual.")
        else:
            tribeRanks = this.tribeRanks.split("/")
            newRank = ""
            num = None
            for a, b in enumerate(tribeRanks):
                b = str(b).split("-")
                if int(a) == int(rankID):
                    num = int(a)
                    b[0] = str(rankName)                
                    newRank = '-'.join(b)
            tribeRanks[int(num)] = str(newRank)
            newRank = '/'.join(tribeRanks)        
            this.Cursor.execute('update tribe set tribeRanks = ? where Code = ?', [newRank, this.client.tribeCode])
            for player in this.server.players.values():
                if int(player.tribeCode) == int(this.client.tribeCode):
                    player.tribulle.tribeChanged = True
                    if player.tribulle.tribeOpen == True:
                        player.tribulle.interfaceTribe()
                    
    def updateTribeData(this):
        for player in this.server.players.values():
            if player.tribeCode == this.client.tribeCode:
                player.tribeHouse = this.client.tribeHouse
                player.tribeMessage = this.client.tribeMessage
                player.tribeRanks = this.tribeRanks

    def changePosRankTribe(this, packet):
        tribulleID, old, new = packet.readInt(), packet.readByte(), packet.readByte()
        tribeRanks = this.tribeRanks.split("/")
        oldRank = ""
        newRank = ""
        for a, b in enumerate(tribeRanks):
            if int(a) == int(old):
                oldRank = str(b)
            if int(a) == int(new):
                newRank = str(b)
        tribeRanks[int(old)] = str(newRank)
        tribeRanks[int(new)] = str(oldRank)
        newRank = '/'.join(tribeRanks)
        this.Cursor.execute('update tribe set tribeRanks = ? where Code = ?', [newRank, this.client.tribeCode])
        for player in this.server.players.values():
            if int(player.tribeCode) == int(this.client.tribeCode):
                player.tribulle.tribeChanged = True
                if player.tribulle.tribeOpen == True:
                    player.tribulle.interfaceTribe()                

    def changePlayerRankTribe(this, packet):
        tribulleID, playerName, rankID = packet.readInt(), packet.readUTF(), packet.readByte()
        rankChange = str(this.client.tribeRank)
        for a, b in enumerate(this.tribeRanks.split("/")):
            b = str(b).split("-")
            if int(a) == int(rankID):
                rankChange = str(b[0])
        this.Cursor.execute('update Users set TribeRank = ? where Username = ?', [str(rankChange), str(playerName)])        
        for player in this.server.players.values():
            if str(player.playerName) == str(playerName):
                player.tribeRank = str(rankChange)
        this.insertRankHistorique(str(playerName.lower()), str(rankID), str(rankChange).replace("#", "|").replace("{", "<").replace("}", ">"), str(this.client.playerName.lower()))
        found = False
        for player in this.server.players.values():
            if int(player.tribeCode) == int(this.client.tribeCode):
                player.sendPacket([60, 3], struct.pack("!hh", 124, len(this.client.playerName.lower())) + str(this.client.playerName.lower()) + struct.pack("!h", len(playerName.lower())) + str(playerName.lower()) + struct.pack("!h", len(rankChange)) + str(rankChange))
                player.tribulle.tribeChanged = True
                if player.tribulle.tribeOpen == True:
                    player.tribulle.interfaceTribe()                

    def kickPlayerTribe(this, packet):
        tribulleID, playerName = packet.readInt(), packet.readUTF()        
        this.Cursor.execute("select Members from tribe where Code = ?", [this.client.tribeCode])
        players = str(this.Cursor.fetchone()[0])
        allPlayers = players.split("#")
        num = None
        for a, b in enumerate(allPlayers):
            if str(b) == str(playerName):
                num = a
        del allPlayers[num]
        allPlayers = '#'.join(allPlayers)
        this.Cursor.execute('update tribe set Members = ? where Code = ?', [str(allPlayers), this.client.tribeCode])
        this.Cursor.execute('update Users set TribeRank = ? where Username = ?', ["", str(playerName)])
        this.Cursor.execute('update Users set TribeCode = ? where Username = ?', [0, str(playerName)])
        this.insertHistorique(3, str(playerName), str(this.client.playerName))
        for player in this.server.players.values():
            if int(player.tribeCode) == int(this.client.tribeCode):
                player.sendPacket([60, 3], struct.pack("!hh", 93, len(playerName.lower())) + str(playerName.lower()) + struct.pack("!h", len(this.client.playerName.lower())) + str(this.client.playerName.lower()))
            if str(player.playerName) == str(playerName):
                player.tribeName = ""        
                player.tribeCode = 0
                player.tribeMessage = ""
                player.tribeHouse = 0
            if int(player.tribeCode) == int(this.client.tribeCode):
                player.tribulle.tribeChanged = True
                if player.tribulle.tribeOpen == True:
                    player.tribulle.interfaceTribe()                

    def giveOwnerTribe(this, packet):
        tribulleID, playerName = packet.readInt(), packet.readUTF()
        countRanks = len(this.tribeRanks.split("/"))
        playerRank = ""
        playerID = 0
        myRank = ""
        for a, b in enumerate(this.tribeRanks.split("/")):
            b = str(b).split("-")
            if int(a) == int(countRanks) - 1:
                playerRank = str(b[0])
                playerID = int(a)
            if int(a) == int(countRanks) - 2:
                myRank = str(b[0])
        this.insertRankHistorique(str(playerName.lower()), str(playerID), str(playerRank).replace("#", "|").replace("{", "<").replace("}", ">"), str(this.client.playerName.lower()))
        this.Cursor.execute('update Users set TribeRank = ? where Username = ?', [str(myRank), str(this.client.playerName)])
        this.client.tribeRank = str(myRank)
        this.Cursor.execute('update Users set TribeRank = ? where Username = ?', [str(playerRank), str(playerName)])
        for player in this.server.players.values():
            if str(player.playerName) == str(playerName):
                player.tribeRank = str(playerRank)
        for player in this.server.players.values():
            if int(player.tribeCode) == int(this.client.tribeCode):
                player.tribulle.tribeChanged = True
                if player.tribulle.tribeOpen == True:
                    player.tribulle.interfaceTribe()

    def resetTribeSettings(this, playerName):
        for player in this.server.players.values():
            if int(player.tribeCode) == int(this.client.tribeCode):
                player.sendPacket([60, 3], struct.pack("!hh", 93, len(playerName.lower())) + str(playerName.lower()) + struct.pack("!h", len(this.client.playerName.lower())) + str(this.client.playerName.lower()))
            if str(player.playerName) == str(playerName):
                player.tribeName = ""        
                player.tribeCode = 0
                player.tribeMessage = ""
                player.tribeHouse = 0                
            
    def deleteTribe(this, packet):
        tribulleID = packet.readInt()
        totalRanks = len(this.tribeRanks.split("/")) - 1
        lastRank = ""
        myRank = str(this.client.tribeRank)
        for a, b in enumerate(this.tribeRanks.split("/")):
            b = str(b).split("-")
            if a == int(totalRanks):
                lastRank =  str(b[0])
        if str(myRank) == str(lastRank):
            this.Cursor.execute("select Members from tribe where Code = ?", [this.client.tribeCode])
            players = str(this.Cursor.fetchone()[0]).split("#")
            for player in players:
                if str(player) != str(this.client.playerName):
                    this.Cursor.execute('update Users set TribeRank = ? where Username = ?', ["", str(player)])
                    this.Cursor.execute('update Users set TribeCode = ? where Username = ?', [0, str(player)])
                    this.resetTribeSettings(str(player))
            this.Cursor.execute('update Users set TribeRank = ? where Username = ?', ["", str(this.client.playerName)])
            this.Cursor.execute('update Users set TribeCode = ? where Username = ?', [0, str(this.client.playerName)])
            this.Cursor.execute("delete from tribe where Code = ?", [this.client.tribeCode])
            this.resetTribeSettings(str(this.client.playerName))
            this.client.sendPacket([60, 3], struct.pack("!hh", 93, len(this.client.playerName.lower())) + str(this.client.playerName.lower()) + struct.pack("!h", len(this.client.playerName.lower())) + str(this.client.playerName.lower()))
            this.client.sendPacket([60, 3], struct.pack("!hib", 127, tribulleID, 0))            

    #FriendList

    def checkConnectedFriendList(this, playerName):
        found = False
        for player in this.server.players.values():
            if player.playerName == str(playerName):
                found = True
        return found

    def getFriendListInfo(this, arg, playerName):
        if arg == 0:            
            this.Cursor.execute("select Gender, LastOn, FriendsList, Avatar from Users where Username = ?",  [str(playerName)])
            for rs in this.Cursor.fetchall():                
                return [rs["Gender"], rs["LastOn"], str(rs["FriendsList"]), rs["Avatar"]]
        elif arg == 1:
            for player in this.server.players.values():
                if player.playerName == str(playerName):
                    return [int(player.gender), str(player.langue), str(player.roomName), int(player.lastOn), str(player.friendsList), int(this.client.server.getplayerAvatar(str(player.playerName)))]                 

    def sendFriendList(this):
        this.client.sendPacket([60, 3], "\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x8e\xf9N\x00\nratatoller\x00\x00\x8e\xf9N\x01\x00\x00\x00\x00\x01\x00\x00\x01z%\x82\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

    def openFriendList(this, packet):
        tribulleID = packet.readInt()
        this.tribulleID = tribulleID
        this.loadFriendList()

    def closeFriendList(this, packet):
        tribulleID = packet.readInt()
        this.friendOpen = False
    
    def loadFriendList(this):        
        langue = {"EN": 1, "FR": 2, "RU": 3, "BR": 4, "ES": 5, "CN": 6, "TR": 7, "VK": 8, "PL": 9, "HU": 10, "NL": 11, "RO": 12, "ID": 13, "DE": 14, "E2": 15, "AR": 16, "PH": 17, "LT": 18, "JP": 19, "CH": 20, "FI": 21, "CZ": 22, "HR": 23, "CZ": 24, "SK": 25, "HR": 26, "BG": 27, "LV": 28, "HE": 29, "IT": 30, "ET": 31, "AZ": 32, "PT": 33}    	
        friends = str(this.client.friendsList).split("#")
        marriageFound = False
        friendList = []
        this.friendOpen = True
        for playerName in friends:
            playerName = str(playerName.replace(" ", ""))
            if playerName != "":
                friendList.append(playerName)
        marriageData = ""
        onlinesData = ""
        offlinesData = ""        
        if this.client.marriage == "":
            data = struct.pack("!hiiiibih", 34, 0, 0, 0, 0, 1, 0, 0) + struct.pack("!h", len(friendList))
        else:
            data = struct.pack("!h", 34)
        if str(this.client.marriage) != "":
            if not str(this.client.marriage) in friendList:
                friendList.append(this.client.marriage)
        if this.friendChanged == True:
            for playerName in friendList:
                connected = this.checkConnectedTribeMembers(str(playerName))
                if str(playerName) != str(this.client.marriage):
                    if connected == True:
                        info = this.getFriendListInfo(1, str(playerName))
                        if str(this.client.playerName) in str(info[4]).split("#"):                    
                            onlinesData += struct.pack("!i", int(info[5])) + struct.pack("!h", len(playerName.lower())) + str(playerName.lower()) + struct.pack("!b", int(info[0])) + struct.pack("!i", int(info[5])) + '\x01' + struct.pack("!?", connected) + struct.pack("!i", int(langue[str(info[1])])) + struct.pack("!h", len(info[2])) + str(info[2]) + struct.pack("!i", int(info[3]))
                        else: onlinesData += struct.pack("!i", int(info[5])) + struct.pack("!h", len(playerName.lower())) + str(playerName.lower()) + struct.pack("!b", int(info[0])) + struct.pack("!i", int(info[5])) + '\x01' + struct.pack("!?", connected) + struct.pack("!i", 0) + struct.pack("!h", 0) + struct.pack("!i", 0)
                    else:
                        info = this.getFriendListInfo(0, str(playerName))
                        if this.server.checkExistingUser(playerName):
                            if str(this.client.playerName) in str(info[2]).split("#"):
                                offlinesData += struct.pack("!i", int(info[3])) + struct.pack("!h", len(playerName.lower())) + str(playerName.lower()) + struct.pack("!b", int(info[0])) + struct.pack("!i", int(info[3])) + '\x01' + struct.pack("!?", connected) + struct.pack("!i", 1) + struct.pack("!h", 0) + struct.pack("!i", int(info[1]))
                            else: offlinesData += struct.pack("!i", int(info[3])) + struct.pack("!h", len(playerName.lower())) + str(playerName.lower()) + struct.pack("!b", int(info[0])) + struct.pack("!i", int(info[3])) + '\x01' + struct.pack("!?", connected) + struct.pack("!i", 0) + struct.pack("!h", 0) + struct.pack("!i", 0)
                        else:
                            friendList = str(this.client.friendsList).split("#")
                            num = None
                            if str(playerName) in friendList:
                                for a, b in enumerate(friendList):
                                    if str(b) == str(playerName):
                                        num = int(a)
                                del friendList[int(num)]
                                friendList = '#'.join(friendList)
                                this.Cursor.execute('update Users set FriendsList = ? where Username = ?', [str(friendList), str(this.client.playerName)])
                                this.client.friendsList = str(friendList)
                                this.friendChanged = True
                                if this.friendOpen == True:
                                    this.loadFriendList()
                                try: 
                                    if str(this.client.playerName) in str(info[2]).split("#"):
                                        offlinesData += struct.pack("!i", int(info[3])) + struct.pack("!h", len(playerName.lower())) + str(playerName.lower()) + struct.pack("!b", int(info[0])) + struct.pack("!i", int(info[3])) + '\x01' + struct.pack("!?", connected) + struct.pack("!i", 1) + struct.pack("!h", 0) + struct.pack("!i", int(info[1]))
                                    else: offlinesData += struct.pack("!i", int(info[3])) + struct.pack("!h", len(playerName.lower())) + str(playerName.lower()) + struct.pack("!b", int(info[0])) + struct.pack("!i", int(info[3])) + '\x01' + struct.pack("!?", connected) + struct.pack("!i", 0) + struct.pack("!h", 0) + struct.pack("!i", 0)
                                except: return
                else:
                    if str(this.client.marriage) != "":
                        if connected == True:                                                                                                                                                                                                                                        
                            info = this.getFriendListInfo(1, str(playerName))
                            marriageData += struct.pack("!i", int(info[5])) + struct.pack("!h", len(playerName.lower())) + str(playerName.lower()) + struct.pack("!b", int(info[0])) + struct.pack("!i", int(info[5])) + "\x01" + struct.pack("!?", connected) + struct.pack("!i", int(langue[str(info[1])])) + struct.pack("!h", len(info[2])) + str(info[2]) + struct.pack("!i", int(info[3])) + struct.pack("!h", len(friendList)) + struct.pack("!i", int(info[5])) + struct.pack("!h", len(playerName.lower())) + str(playerName.lower()) + struct.pack("!b", int(info[0])) + struct.pack("!i", int(info[5])) + "\x01" + struct.pack("!?", connected) + struct.pack("!i", int(langue[str(info[1])])) + struct.pack("!h", len(info[2])) + str(info[2]) + struct.pack("!i", int(info[3]))
                        else:
                            info = this.getFriendListInfo(0, str(playerName))
                            marriageData += struct.pack("!i", int(info[3])) + struct.pack("!h", len(playerName.lower())) + str(playerName.lower()) + struct.pack("!b", int(info[0])) + struct.pack("!i", int(info[3])) + "\x01" + struct.pack("!?", connected) + struct.pack("!i", 1) + struct.pack("!h", 0) + struct.pack("!i", int(info[1])) + struct.pack("!h", len(friendList)) + struct.pack("!i", int(info[3])) + struct.pack("!h", len(playerName.lower())) + str(playerName.lower()) + struct.pack("!b", int(info[0])) + struct.pack("!i", int(info[3])) + "\x01" + struct.pack("!?", connected) + struct.pack("!i", 1) + struct.pack("!h", 0) + struct.pack("!i", int(info[1]))
                        
            data += str(marriageData) + str(onlinesData) + str(offlinesData)
            this.friendData = data
            this.friendChanged = False
        else: data = this.friendData
        this.client.sendPacket([60, 3], data)

    def addPlayerFriendList(this, packet):
        tribulleID, playerName = packet.readInt(), packet.readUTF()
        friendList = str(this.client.friendsList).split("#")
        if not len(friendList) >= 200:
            if this.server.checkExistingUser(playerName):
                if not str(playerName) in friendList:
                    friendList.append(str(playerName))
                    friendList = '#'.join(friendList)
                    this.Cursor.execute('update Users set IgnoredsList = ? where Username = ?', [str(friendList), str(this.client.playerName)])
                    this.client.friendsList = str(friendList)
                    this.client.sendPacket([60, 3], struct.pack("!hib", 19, tribulleID, 0))
                    this.friendChanged = True
                    if this.friendOpen == True:                        
                        this.loadFriendList()
                    for player in this.server.players.values():
                        if str(player.playerName) == str(playerName):
                            player.tribulle.friendChanged = True
                            if player.tribulle.friendOpen == True:
                                player.tribulle.loadFriendList()
            else:
                this.client.sendPacket([60, 3], struct.pack("!hib", 19, tribulleID, 11))
        else:
            this.client.sendPacket([60, 3], struct.pack("!hib", 19, tribulleID, 6))

    def deletePlayerFriendList(this, packet):
        tribulleID, playerName = packet.readInt(), packet.readUTF()
        friendList = str(this.client.friendsList).split("#")
        num = None
        if str(playerName) in friendList:
            for a, b in enumerate(friendList):
                if str(b) == str(playerName):
                    num = int(a)
            del friendList[int(num)]
            friendList = '#'.join(friendList)
            this.Cursor.execute('update Users set FriendsList = ? where Username = ?', [str(friendList), str(this.client.playerName)])
            this.client.friendsList = str(friendList)
            this.client.sendPacket([60, 3], struct.pack("!hib", 21, tribulleID, 0))
            this.friendChanged = True
            if this.friendOpen == True:
                this.loadFriendList()            
            for player in this.server.players.values():
                if str(player.playerName) == str(playerName):
                    player.tribulle.friendChanged = True
                    if player.tribulle.friendOpen == True:
                        player.tribulle.loadFriendList()

    def invitePlayerMarriage(this, packet):
        tribulleID, playerName = packet.readInt(), packet.readUTF()
        found = False
        if str(this.client.marriage) == "":
            for player in this.server.players.values():
                if str(player.playerName) == str(playerName):
                    found = True
                    if str(player.marriage) == "":
                        this.client.sendPacket([60, 3], struct.pack("!hib", 23, tribulleID, 0))
                        player.sendPacket([60, 3], struct.pack("!hh", 38, len(this.client.playerName.lower())) + str(this.client.playerName.lower()))
                    else:
                        this.client.sendPacket([60, 3], struct.pack("!hib", 23, tribulleID, 14))
            if found == False:
                this.client.sendPacket([60, 3], struct.pack("!hib", 23, tribulleID, 10))
        else:
            this.client.sendPacket([60, 3], struct.pack("!hib", 23, tribulleID, 14))            

    def resultInviteMarriage(this, packet):
        tribulleID, playerName, result = packet.readInt(), packet.readUTF(), packet.readByte()
        if result == 0:
            for player in this.server.players.values():
                if str(player.playerName) == str(playerName):
                    player.sendPacket([60, 3], struct.pack("!hh", 40, len(this.client.playerName.lower())) + str(this.client.playerName.lower()))
        elif result == 1:
            for player in this.server.players.values():
                if str(player.playerName) == str(playerName):                    
                    this.Cursor.execute('update Users set Marriage = ? where Username = ?', [str(this.client.playerName), str(playerName)])
                    player.marriage = str(this.client.playerName)
                    player.sendPacket([60, 3], struct.pack("!hh", 39, len(this.client.playerName.lower())) + str(this.client.playerName.lower()))
                    player.tribulle.friendChanged = True
                    if player.tribulle.friendOpen == True:
                        player.tribulle.loadFriendList()
            this.Cursor.execute('update Users set Marriage = ? where Username = ?', [str(playerName), str(this.client.playerName)])
            this.client.marriage = str(playerName)
            this.client.sendPacket([60, 3], struct.pack("!hh", 39, len(playerName.lower())) + str(playerName.lower()))
            this.friendChanged = True
            if this.friendOpen == True:
                this.loadFriendList()

    def divorceMarriage(this, packet):
        tribulleID = packet.readInt()
        found = False        
        if this.client.marriage != "":
            for player in this.server.players.values():                
                if str(player.playerName) == str(this.client.marriage):
                    found = True
                    this.Cursor.execute('update Users set Marriage = ? where Username = ?', ["", str(player.playerName)])
                    player.marriage = ""
                    player.sendPacket([60, 3], struct.pack("!hh", 41, len(this.client.playerName.lower())) + str(this.client.playerName.lower()) + struct.pack("!b", 0))
                    player.tribulle.friendChanged = True
                    if player.tribulle.friendOpen == True:
                        player.tribulle.loadFriendList()
            if found == False:                
                this.Cursor.execute('update Users set Marriage = ? where Username = ?', ["", str(this.client.marriage)])
            this.client.sendPacket([60, 3], struct.pack("!hh", 41, len(this.client.marriage.lower())) + str(this.client.marriage.lower()) + struct.pack("!b", 1))
            this.Cursor.execute('update Users set Marriage = ? where Username = ?', ["", str(this.client.playerName)])
            this.client.marriage = ""
            this.friendChanged = True
            if this.friendOpen == True:
                this.loadFriendList()
            
    #IgnoredList

    def sendIgnoredList(this, packet):
        tribulleID = packet.readInt()
        ignoredList = this.client.ignoredsList.split("#")
        data = struct.pack("!hih", 47, tribulleID, len(ignoredList))
        for playerName in ignoredList:
            data += struct.pack("!h", len(playerName.lower())) + str(playerName.lower())
        this.client.sendPacket([60, 3], data)
    
    def addPlayerIgnoredList(this, packet):        
        tribulleID, playerName = packet.readInt(), packet.readUTF()
        ignoredList = str(this.client.ignoredsList).split("#")
        if this.server.checkExistingUser(playerName):
            if not str(playerName) in ignoredList:
                if not str(playerName) == str(this.client.playerName):
                    ignoredList.append(str(playerName))
                    ignoredList = '#'.join(ignoredList)
                    this.Cursor.execute('update Users set IgnoredsList = ? where Username = ?', [str(ignoredList), str(this.client.playerName)])
                    this.client.ignoredsList = str(ignoredList)
                    this.client.sendPacket([60, 3], struct.pack("!hib", 43, tribulleID, 0))
        else:
            this.client.sendPacket([60, 3], struct.pack("!hib", 43, tribulleID, 11))

    def removePlayerIgnoredList(this, packet):
        tribulleID, playerName = packet.readInt(), packet.readUTF()
        ignoredList = str(this.client.ignoredsList).split("#")
        num = None
        if str(playerName) in ignoredList:
            for a, b in enumerate(ignoredList):
                if str(b) == str(playerName):
                    num = int(a)
            del ignoredList[int(num)]
            ignoredList = '#'.join(ignoredList)
            this.Cursor.execute('update Users set IgnoredsList = ? where Username = ?', [str(ignoredList), str(this.client.playerName)])
            this.client.ignoredsList = str(ignoredList)
            this.client.sendPacket([60, 3], struct.pack("!hib", 45, tribulleID, 0))

    #Channels

    def getChannelErrors(this, tribulleID, error):
        errors = {"invalidName": 7}
        return struct.pack("!hib", 55, tribulleID, int(errors[str(error)]))

    def checkExistingChat(this, chatName):
        this.Cursor.execute("select 1 from chats where Name = ?", [chatName])
        return this.Cursor.fetchone() != None
    
    def createChannel(this, packet):
        tribulleID, channelName = packet.readInt(), packet.readUTF()
        players = ""
        if re.match("^[ a-zA-Z0-9]*$", channelName):
            if this.checkExistingChat(str(channelName)) == True:
                this.Cursor.execute("select Members from chats where Name = ?",  [str(channelName)])
                players = str(this.Cursor.fetchone()[0])
                if not str(this.client.playerName) in players:
                    players += "#" + str(this.client.playerName)
                    this.Cursor.execute('update chats set Members = ? where Name = ?', [str(players), str(channelName)])
            if this.checkExistingChat(str(channelName)) == False:
                this.Cursor.execute("insert into chats values (null, ?, ?)", [str(channelName), str(this.client.playerName)])
            if not str(channelName) in this.client.chats:
                this.client.chats.append(str(channelName))
            this.client.sendPacket([60, 3], struct.pack("!hh", 62, len(channelName)) + str(channelName))
        else:
            this.client.sendPacket([60, 3], this.getChannelErrors(tribulleID, "invalidName"))

    def sendMessageChannel(this, packet):
        tribulleID, channelName, message = packet.readInt(), packet.readUTF(), packet.readUTF()
        langue = {"EN": 1, "FR": 2, "RU": 3, "BR": 4, "ES": 5, "CN": 6, "TR": 7, "VK": 8, "PL": 9, "HU": 10, "NL": 11, "RO": 12, "ID": 13, "DE": 14, "E2": 15, "AR": 16, "PH": 17, "LT": 18, "JP": 19, "CH": 20, "FI": 21, "CZ": 22, "HR": 23, "CZ": 24, "SK": 25, "HR": 26, "BG": 27, "LV": 28, "HE": 29, "IT": 30, "ET": 31, "AZ": 32, "PT": 33}    	
        this.Cursor.execute("select Members from chats where Name = ?",  [str(channelName)])        
        players = str(this.Cursor.fetchone()[0])
        if "#" in str(players):
            players = str(players).split("#")
        if "list" in str(type(players)):
            for selected in players:
                for player in this.server.players.values():
                    if str(player.playerName) == str(selected):
                        player.sendPacket([60, 3], struct.pack("!hh", 64, len(this.client.playerName.lower())) + str(this.client.playerName.lower()) + struct.pack("!i", int(langue[str(this.client.langue)])) + struct.pack("!h", len(channelName)) + str(channelName) + struct.pack("!h", len(message)) + str(message))
        elif "str" in str(type(players)):
            this.client.sendPacket([60, 3], struct.pack("!hh", 64, len(this.client.playerName.lower())) + str(this.client.playerName.lower()) + struct.pack("!i", int(langue[str(this.client.langue)])) + struct.pack("!h", len(channelName)) + str(channelName) + struct.pack("!h", len(message)) + str(message))

    def listPlayersChannel(this, packet):
        try:
            tribulleID, channelName = packet.readInt(), packet.readUTF()
            this.Cursor.execute("select Members from chats where Name = ?",  [str(channelName)])        
            players = str(this.Cursor.fetchone()[0])
            allPlayers = ""
            lenPlayers = 0
            if "#" in str(players):
                players = str(players).split("#")
            if "list" in str(type(players)):
                data = ""
                lenPlayers = len(players)
                for selected in players:
                    data += struct.pack("!h", len(selected.lower())) + str(selected.lower())
                this.client.sendPacket([60, 3], struct.pack("!hibh", 59, tribulleID, 0, int(lenPlayers)) + data)
            elif "str" in str(type(players)):
                lenPlayers = 1
                allPlayers = str(players)
                data = struct.pack("!h", len(allPlayers.lower())) + str(allPlayers.lower())
                this.client.sendPacket([60, 3], struct.pack("!hibh", 59, tribulleID, 0, int(lenPlayers)) + data)
        except:
            pass

    def leaveChannel(this, packet):
        tribulleID, channelName = packet.readInt(), packet.readUTF()
        try:
            this.Cursor.execute("select Members from chats where Name = ?",  [str(channelName)])        
            players = str(this.Cursor.fetchone()[0])
            num = None
            secondNum = None
            if not "#" in players:
                this.Cursor.execute("delete from chats where Name = ?", [str(channelName)])
                for a, b in enumerate(this.client.chats):
                    if str(b) == str(channelName):
                        num = int(a)
                del this.client.chats[int(num)]
            elif "#" in players:
                for a, b in enumerate(this.client.chats):
                    if str(b) == str(channelName):
                        num = int(a)
                del this.client.chats[int(num)]
                players = str(players).split("#")
                for c, d in enumerate(players):
                    if str(d) == str(this.client.playerName):
                        secondNum = int(c)
                del players[int(secondNum)]
                players = '#'.join(players)
                this.Cursor.execute('update chats set Members = ? where Name = ?', [str(players), str(channelName)])
        except:
            pass
