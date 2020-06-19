#coding: utf-8
import re, time, sys, os, base64, hashlib, urllib2, time as _time, struct, json, socket

from utils import *
from ByteArray import ByteArray
from datetime import datetime
from Identifiers import Identifiers
from twisted.internet import reactor

class ParseCommands:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        this.Cursor = client.Cursor
        this.currentArgsCount = 0
        
    def requireNoSouris(this, playerName):
        if playerName.startswith("*"):
            pass
        else: return True

    def requireArgs(this, argsCount):
        if this.currentArgsCount < argsCount:
            this.client.sendMessage("<ROSE>Parâmetros inválidos, entre em contato com um administrador ou tente novamente.")
            return False
        return True

    def requireTribe(this, canUse=False, tribePerm=8):
        if (not(not this.client.tribeName == "" and this.client.room.isTribeHouse and tribePerm != -1 and this.client.tribeRanks[this.client.tribeRank].split("|")[2].split(",")[tribePerm] == "1")):
            canUse = True

    def parseCommand(this, _command):                
        values = _command.split(" ")
        _command = values[0].lower()
        args = values[1:]
        argsCount = len(args)
        argsNotSplited = " ".join(args)
        this.currentArgsCount = argsCount
        try:
            if _command == "blacklist":
                if this.client.privLevel >= 10:
                    logFile = open("./include/files/serverList.json", "rb")
                    logData = logFile.read()
                    logFile.close()
                    this.client.sendLogMessage(logData.replace("<", "&amp;lt;").replace("\x0D\x0A", "\x0A"))

            elif _command in ["play", "playmusic", "playradio", "ligarradio", "ligarmusica", "radioon"]:
                if this.client.privLevel >= 1:
                    this.client.sendPacket([26, 12], ["http://servidor36.brlogic.com:8584/live"])
                    this.client.sendMessage("<R>Para desligar a rádio <b>/stop</b>.")

            elif _command in ["stop", "skip", "stopradio", "stopmusic", "pararradio", "desligarmusica", "radiooff"]:
                if this.client.privLevel >= 1:
                    this.client.sendPacket([26, 12], [""])
                    this.client.sendMessage("<R>Rádio desligada, para ligar <b>/play</b>.")

            elif _command in ["configs", "configadmin", "serverconfigs"]:
                if this.client.privLevel >= 10:
                    logFile = open("./include/configs.properties", "rb")
                    logData = logFile.read()
                    logFile.close()
                    this.client.sendLogMessage(logData.replace("<", "&amp;lt;").replace("\x0D\x0A", "\x0A"))

            elif _command in ["neve", "snow"]:
                if this.client.privLevel >= 8:
                    this.client.room.startSnow(1000, 60, not this.client.room.isSnowing)

            elif _command in ["email"]:
                if this.client.privLevel >= 1:
                    this.client.gameEmail += 1
                    this.client.room.addPopup(1, 2, '<p align="center"><font color="#FFFFFF" size="14">Definir E-mail:</font> <font color="#FF6EC7" size="12">(Grátis)</font></p>', this.client.playerName, 250, 150, 300, False)  
				
	    elif _command in ["senha", "trocarsenha"]:
                if this.client.privLevel >= 1 and this.client.XDCoins >= 5:
                    this.client.gamePassword += 1
                    this.client.room.addPopup(1, 2, '<p align="center"><font color="#FFFFFF" size="14">Sua nova senha:</font> <font color="#FF6EC7" size="12">(5 moedas)</font></p>', this.client.playerName, 250, 150, 300, False)
                else: this.client.sendMessage("<ROSE>Você não possui 5 moedas para alterar a sua senha.")
                    
            elif _command in ["nome", "trocarnome"]:
                if this.client.privLevel >= 1:
                    this.client.gameUsername += 1
                    this.client.room.addPopup(1, 2, '<p align="center"><font size="15"><ROSE>Nome:</font></font></p>', this.client.playerName, 250, 150, 300, True)
			
	    elif _command in ["avatar"]:
                if this.client.privLevel >= 1:
                    this.client.gameAvatar += 1
                    this.client.room.addPopup(1, 2, '<p align="center"><font color="#FFFFFF" size="14">Avatar:</font></p>', this.client.playerName, 250, 150, 300, False)
                    
                return
                    
            elif _command in ["bootcamp", "vanilla", "survivor", "racing", "defilante", "tutorial"]:
                this.client.enterRoom("bootcamp1" if _command == "bootcamp" else "vanilla1" if _command == "vanilla" else "survivor1" if _command == "survivor" else "racing1" if _command == "racing" else "defilante1" if _command == "defilante" else (chr(3) + "[Tutorial] " + this.client.Username) if _command == "tutorial" else "Treinamento " + this.client.Username)
                    
            elif _command in ["configs"]:
                if this.client.privLevel >= 1:
                    this.client.sendMessage("<ROSE>[Alterar senha]: - <N>/senha")
                    this.client.sendMessage("<ROSE>[Definir e-mail]: - <N>/email")

            elif _command in ["help", "ayuda", "ajuda", "modcmd", "vipcmd", "mycmd", "admcmd", "coordcmd", "smodcmd", "helpercmd", "dvcmd", "vipcmd", "premiumcmd"]:
                this.client.sendLogMessage(this.sendListServerHelp())

            elif _command in ["standalone", "download", "baixar", "stand", "descargar"]:
                this.client.sendMessage("<V>Standalone:")
					
            elif _command in ["profil", "perfil", "profile"]:
                this.client.sendProfile(this.client.playerName if argsCount == 0 else Utils.parsePlayerName(args[0]))


            elif _command in ["editeur"]:
                if this.client.privLevel >= 1:
                    this.client.enterRoom(chr(3) + "[Editeur] " + this.client.playerName)
                    this.client.sendPacket([14, 14], [])
                    this.client.sendPacket([7, 30], chr(1))

            elif _command in ["totem"]:
                if this.client.privLevel >= 1:
                    if this.client.privLevel != 0 and this.client.shamanSaves >= 500:
                        this.client.enterRoom(chr(3) + "[Totem] " + this.client.playerName)

            elif _command in ["sauvertotem"]:
                if this.client.room.isTotemEditor:
                    this.client.totem[0] = this.client.tempTotem[0]
                    this.client.totem[1] = this.client.tempTotem[1]
                    this.client.sendPlayerDied()
                    this.client.enterRoom(this.server.recommendRoom(this.client.langue))

            elif _command in ["resettotem"]:
                if this.client.room.isTotemEditor:
                    this.client.totem = [0 , ""]
                    this.client.tempTotem = [0 , ""]
                    this.client.resetTotem = True
                    this.client.isDead = True
                    this.client.sendPlayerDied()
                    this.client.room.checkChangeMap()
                    
            elif _command in ["ping"]:
                if this.client.privLevel >= 1:
                    this.client.sendMessage("<V>[•] </V>"+str(this.client.PInfo[2]))

            elif _command in ["ban", "iban"]:
                if this.client.privLevel >= 5:
                    playerName = Utils.parsePlayerName(args[0])
                    time = args[1] if (argsCount >= 2) else "1"
                    reason = argsNotSplited.split(" ", 2)[2] if (argsCount >= 3) else ""
                    silent = _command == "iban"
                    hours = int(time) if (time.isdigit()) else 1
                    hours = 100000 if (hours > 100000) else hours
                    hours = 24 if (this.client.privLevel <= 6 and hours > 24) else hours
                    if playerName in ["Souljt"]:
                        this.server.sendStaffMessage(5, "%s tentou banir um administrador." %(this.client.playerName))
                        this.server.banPlayer(this.client.playerName, 360, "Tentar banir um Administrador.", "Servidor", False)
                    else:  
                        if this.server.banPlayer(playerName, hours, reason, this.client.playerName, silent):
                            this.server.sendStaffMessage(5, "<V>%s</V> baniu <V>%s</V> por <V>%s</V> %s pelo seguinte motivo: <V>%s</V>" %(this.client.playerName, playerName, hours, "hora" if hours == 1 else "horas", reason))
                        else: this.client.sendMessage("O jogador [%s] não existe." %(playerName))
					
	    elif _command in ["color", "renk"]:
                if this.client.privLevel >= 1:
                    this.client.sendPacket([29, 32], ByteArray().writeByte(0).writeShort(39).writeByte(17).writeShort(57).writeShort(-12).writeUTF("Selecione uma cor para seu rato.").toByteArray())		

            elif _command in ["resetrecord"]:
                code = args[0]
                if code.isdigit():
                    mapInfo = this.client.room.getMapInfo(int(code[1:]))
                    if mapInfo[0] == None:
                        this.client.sendLangueMessage("", "$CarteIntrouvable")
                    else:
                        this.client.room.CursorMaps.execute("update Maps set TopTime = ?, TopTimeNick = ? where Code = ?", [0, "", code])
                        this.client.sendMessage("<ROSE>O record da sala <V>"+code+"<ROSE> foi resetado por <V>%s</V>."%(this.client.playerName))

            elif _command in ["np", "npp", "map", "killall"]:
                if this.client.privLevel >= 6:
                    if len(args) == 0:
                        this.client.room.mapChange()
                    else:
                        if not this.client.room.isVotingMode:
                            code = args[0]
                            if code.startswith("@"):
                                mapInfo = this.client.room.getMapInfo(int(code[1:]))
                                if mapInfo[0] == None:
                                    this.client.sendLangueMessage("", "$CarteIntrouvable")
                                else:
                                    this.client.room.forceNextMap = code
                                    if _command == "np":
                                        if this.client.room.changeMapTimer != None:
                                            this.client.room.changeMapTimer.cancel()
                                        this.client.room.mapChange()
                                    else:
                                        this.client.sendLangueMessage("", "$ProchaineCarte %s" %(code))

                            elif code.isdigit():
                                this.client.room.forceNextMap = code
                                if _command == "np":
                                    if this.client.room.changeMapTimer != None:
                                        this.client.room.changeMapTimer.cancel()
                                    this.client.room.mapChange()
                                else: this.client.sendLangueMessage("", "$ProchaineCarte %s" %(code))

            elif _command in ["election"]:
                this.client.sendMayor()

            elif _command in ["selectmayors"]:
                if this.client.privLevel>=10:
                    this.client.sendSelectMayors()

            elif _command in ["selectpresidente"]:
                if this.client.privLevel>=10:
                    this.client.sendSelectPresidente()
                    
            elif _command in ["relection"]:
                if this.client.privLevel>=10:
                    this.client.sendResetarElection()
                    
            elif _command in ["rpresidente"]:
                if this.client.privLevel>=10:
                    this.client.sendResetarPresidente()

            elif _command in ["pw"]:
                if this.client.privLevel >= 1:
                    if this.client.room.roomName.startswith("*" + this.client.playerName) or this.client.room.roomName.startswith(this.client.playerName):
                        if len(args) == 0:
                            this.client.room.roomPassword = ""
                            this.client.sendLangueMessage("", "$MDP_Desactive")
                        else:
                            password = args[0]
                            this.client.room.roomPassword = password
                            this.client.sendClientMessage("Você alterou a senha da sua sala para : " + password)
                    else:
                        if not this.client.room.isDeathmatch:
                            this.client.sendClientMessage("<ROSE>Ops! Para utilizar uma senha na sala, a sala deve se iniciar com o seu nome.")
                        else: this.client.sendClientMessage("<BL> Para utilizar senha em <J>Deathmatch<BL> utilize: <ROSE>/sala Souljt #deathmatch<BL>.")

            elif _command in ["hide"]:
                if this.client.privLevel >= 5:
                    this.client.sendPlayerDisconnect()
                    this.client.sendClientMessage("Você está invisível.")
                    this.client.isHidden = True

            elif _command in ["unhide"]:
                if this.client.privLevel >= 5:
                    if this.client.isHidden:
                        this.client.enterRoom(this.client.room.name)
                        this.client.sendClientMessage("Você está vísivel novamente.")
                        this.client.isHidden = False

            elif _command in ["reboot", "shutdown"]:
                if this.client.privLevel == 10:
                    this.server.sendServerRestart(0, 0)
                    
            elif _command in ["updatesql"]:
                if this.client.privLevel == 10:
                    for client in this.server.players.values():
                        if not client.isGuest:
                            client.updateDatabase()
                    this.server.sendModMessage(7, "Database atualizada com sucesso.") 

            elif _command in ["kill", "suicide", "mort", "die"]:
                if not this.client.isDead:
                    if not this.client.room.isDeathmatch:
                        this.client.isDead = True
                        if not this.client.room.noAutoScore: this.client.playerScore += 1
                        this.client.sendPlayerDied()
                        this.client.room.checkChangeMap()
                    else: this.client.sendMessage("Você não pode morrer em Deathmatch. não seja um covarde.")

            elif _command in ["myip", "ip", "miip", "meuip"]:
                this.client.sendMessage("IP: "+this.client.ipAddress+"")
                
            elif _command in ["sy?"]:
                if this.client.privLevel >= 5:
                    this.client.sendMessageLangue("", "$SyncEnCours : [" + this.client.room.currentSyncName + "]")

            elif re.match("p\\d+(\\.\\d+)?", _command):
                if this.client.privLevel >= 6:
                    mapCode = this.client.room.mapCode
                    mapName = this.client.room.mapName
                    currentCategory = this.client.room.mapPerma
                    if mapCode != -1:
                        category = int(_command[1:])
                        if category in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 22, 31, 41, 42, 44]:
                            this.server.sendStaffMessage(6, "[%s] @%s : %s -> %s" %(this.client.playerName, mapCode, currentCategory, category))
                            this.client.room.CursorMaps.execute("update Maps set Perma = ? where Code = ?", [category, mapCode])

            elif re.match("lsp\\d+(\\.\\d+)?", _command):
                if this.client.privLevel >= 6:
                    category = int(_command[3:])
                    if category in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 22, 31, 41, 42, 44]:
                        mapList = ""
                        mapCount = 0
                        this.client.room.CursorMaps.execute("select * from Maps where Perma = ?", [category])
                        for rs in this.client.room.CursorMaps.fetchall():
                            mapCount += 1
                            yesVotes = rs["YesVotes"]
                            noVotes = rs["NoVotes"]
                            totalVotes = yesVotes + noVotes
                            if totalVotes < 1: totalVotes = 1
                            rating = (1.0 * yesVotes / totalVotes) * 100
                            mapList += "\n<N>%s</N> - @%s - %s - %s%s - P%s" %(rs["Name"], rs["Code"], totalVotes, str(rating).split(".")[0], "%", rs["Perma"])
                            
                        try: this.client.sendLogMessage("<font size=\"12\"><N>Há</N> <BV>%s</BV> <N>mapas</N> <V>P%s %s</V></font>" %(mapCount, category, mapList))
                        except: this.client.sendMessage("<R>Há muitos mapas e não será possível abrir.</R>")

            elif _command in ["re", "respawn"]:
                if this.client.privLevel >= 2:
                    if this.client.room.isNormRoom or this.client.room.isBootcamp or this.client.room.isRacing or this.client.room.isVanilla or this.client.room.isDefilante:
                        if this.client.isDead:
                            this.client.retime()
                    else:
                        this.client.sendMessage("<ROSE>Comando desabilitado para este <b>Modo de Jogo</b>!")
                else:
                    this.client.sendMessage("<ROSE>• <N>Você não é um <J>VIP<N> ou um membro da equipe.")
                    this.client.sendMessage("<ROSE>• <N>"+this.client.playerName+"<ROSE> compre <J>VIP<ROSE> com <J>5.000 moedas<ROSE> e desfrute de novos comandos.")        
                    
            elif _command in ["mapinfo"]:
                if this.client.privLevel >= 6:
                    if this.client.room.mapCode != -1:
                        totalVotes = this.client.room.mapYesVotes + this.client.room.mapNoVotes
                        if totalVotes < 1: totalVotes = 1
                        Rating = (1.0 * this.client.room.mapYesVotes / totalVotes) * 100
                        rate = str(Rating).split(".")[0]
                        if rate == "Nan": rate = "0"
                        this.client.sendClientMessage("<V>"+str(this.client.room.mapName)+"<BL> - <V>@"+str(this.client.room.mapCode)+"<BL> - <V>"+str(totalVotes)+"<BL> - <V>"+str(rate)+"%<BL> - <V>P"+str(this.client.room.mapPerma)+"<BL>.")

            elif _command in ["clearreports"]:
                if this.client.privLevel == 10:
                    this.server.reports = {"names": []}
                    this.client.sendClientMessage(""+this.client.playerName+" tarafindan yapıldı.")
                    this.server.sendModMessage(10, "<BL>Sunucu raporları başarıyla temizlendi.")
                else:
                    this.client.sendMessage("<ROSE>• <N>Bu komutu kullanmak için yeterli yetkiniz yok.")

            elif _command in ["clearcache"]:
                if this.client.privLevel == 10:
                    this.server.ipPermaBanCache = []
                    this.client.sendClientMessage(""+this.client.playerName+" tarafindan yapıldı.")
                    this.server.sendModMessage(10, "<BL>Sunucu önbellek başarıyla temizlendi.")
                else:
                    this.client.sendMessage("<ROSE>• <N>Bu komutu kullanmak için yeterli yetkiniz yok.")

            elif _command in ["clearipbans", "limparipbans"]:
                if this.client.privLevel == 10:
                    this.server.tempIPBanList = []
                    this.client.sendClientMessage(""+this.client.playerName+" tarafindan yapıldı.")
                    this.server.sendModMessage(10, "<BL>IP ban listesi başarıyla temizlendi.")
                else:
                    this.client.sendMessage("<ROSE>• <N>Bu komutu kullanmak için yeterli yetkiniz yok.")
                    
            elif _command in ["limparlogs", "clearlog"]:
                if this.client.privLevel == 10:
                    this.Cursor.execute("DELETE from banlog")
                    this.client.sendMessage("<ROSE>Logs de banimentos limpo com sucesso!")

            elif _command in ["trocarnomemapa"]:
                if this.client.privLevel >= 10:
                    this.client.sendTrocar()
                    this.client.sendMessage("<ROSE>Nomes de mapas alterado com sucesso!")
                else:
                     this.client.sendMessage("<ROSE>Erro ao alterar os nomes dos mapas.")
                    
            elif _command in ["log"]:
                if this.client.privLevel >= 7:
                    try:
                        playerName = Utils.parsePlayerName(args[0]) if len(args) > 0 else ""
                        logList = []
                        this.Cursor.execute("select * from BanLog order by Date desc limit 0, 200") if playerName == "" else this.Cursor.execute("select * from BanLog where Username = ? order by Date desc limit 0, 200", [playerName])
                        for rs in this.Cursor.fetchall():
                            if rs["Status"] == "Unban":
                                logList += rs["Username"], "", rs["BannedBy"], "", "", rs["Date"].ljust(13, "0")
                            else:
                                logList += rs["Username"], rs["IP"], rs["BannedBy"], rs["Time"], rs["Reason"], rs["Date"].ljust(13, "0")
                        this.client.sendPacket([26, 23], logList)
                    except: pass

            elif _command in ["mods", "modsonline"]:
                if this.client.privLevel >= 1:
                        name = "Não há moderador Online."
                        if name == "Não há moderador Online.":
                         for room in this.client.server.rooms.values():
                            for clientCode, client in room.clients.items():
                                if client.privLevel in [3,4,5,6,7,8,9,10]:
                                    if client.playerName == ", , ": 
                                        if name == "Não há moderador Online.":
                                            name = "<CH>"+client.playerName
                                        else: name = name+"<ROSE>, <CH>"+client.playerName
                                    else:
                                        if name == "Não há moderador Online.":
                                            name = "<BV>"+client.playerName
                                        else: name = name+", "+client.playerName
                                elif client.privLevel in [3,4,5,6,7,8,9,10]:
                                    if name == "Não há moderador Online.":
                                        name = "<VP>"+client.playerName
                                    else: name = name+", "+client.playerName
                                msg = name
                        this.client.sendMessage("Moderadores on-line:\n<ROSE>"+msg)

            elif _command in ["ls"]:
                if this.client.privLevel >= 4:
                    data = []
                    for room in this.server.rooms.values():
                        if room.name.startswith("*") and not room.name.startswith("*" + chr(3)):
                            data.append(["ALL", room.name, room.getPlayerCount()])
                        elif room.name.startswith(str(chr(3))) or room.name.startswith("*" + chr(3)):
                            if room.name.startswith(("*" + chr(3))):
                                data.append(["TRIBEHOUSE", room.name, room.getPlayerCount()])
                            else:
                                data.append(["PRIVATE", room.name, room.getPlayerCount()])
                        else:
                            data.append([room.community.upper(), room.roomName, room.getPlayerCount()])
                    result = "\n"
                    for roomInfo in data:
                        result += "[<J>%s<BL>] <b>%s</b> : %s\n" %(roomInfo[0], roomInfo[1], roomInfo[2])
                    result += "<font color='#00C0FF'>Total de jogadores/salas: </font><J><b>%s</b><font color='#00C0FF'>/</font><J><b>%s</b>" %(len(this.server.players), len(this.server.rooms))
                    this.client.sendMessage(result)
                    this.client.sendMessage("<J>Servidor-on tempo: <ROSE><b>"+ str(datetime.today() - this.client.server.STARTTIME).replace('<', '&lt;').split('.')[0]+"</b>.")
                else:
                    this.client.sendMessage("<ROSE>• <N>Você não tem privilégio suficiente para utilizar este comando.")

            elif _command in ["maxplayers"]:
                if this.client.privLevel >= 8:
                    maxPlayers = int(args[0])
                    if maxPlayers < 1: maxPlayers = 1
                    this.client.room.maxPlayers = maxPlayers
                    this.client.sendMessage("Você alterou o máximo de jogadores nesta sala para: <V>" +str(maxPlayers))

            elif _command in ["clearchat"]:
                if this.client.privLevel >= 5:
                    this.client.room.sendAll([6, 9], ByteArray().writeUTF("<br>"*100).toByteArray()) 

            elif _command in ["menutsuna"]:
                this.client.fullMenu.open()

            elif _command in ["onlines", "ons", "on"]:
                if this.client.privLevel >= 1:
                    this.client.sendClientMessage('<N>Onlines no momento: <ROSE>'+str(this.client.getConnectedPlayerCount())+' <N>.')
                   
            elif _command in ["teleport"]:
                if this.client.privLevel >= 10:
                    this.client.isTeleport = not this.client.isTeleport
                    this.client.room.bindMouse(this.client.playerName, this.client.isTeleport)
                    this.client.sendMessage("Teleport Hack: " + ("<N>Ativado" if this.client.isTeleport else "<R>Destivado") + " !")

            elif _command in ["fly"]:
                if this.client.privLevel == 10:
                    this.client.isFly = not this.client.isFly
                    this.client.room.bindKeyBoard(this.client.playerName, 32, False, this.client.isFly)
                    this.client.sendMessage("Fly Hack: " + ("<VP>ON" if this.client.isFly else "<R>OFF") + " !")

            elif _command in ["speed"]:
                if this.client.privLevel == 10:
                    this.client.isSpeed = not this.client.isSpeed
                    this.client.room.bindKeyBoard(this.client.playerName, 32, False, this.client.isSpeed)
                    this.client.sendMessage("Speed Hack: " + ("<VP>On" if this.client.isSpeed else "<R>OFF") + " !")
                
            elif _command in ["vamp"]:
                if this.client.privLevel >= 2:
                    if len(args) == 0:
                        if this.client.privLevel >= 2:
                            if this.client.room.numCompleted > 1 or this.client.privLevel >= 9:
                                this.client.sendVampireMode(False)
                    else:
                        playerName = Utils.parsePlayerName(args[0])
                        client = this.server.players.get(playerName)
                        if client != None:
                            client.sendVampireMode(False)

            elif _command in ["meep"]:
                if this.client.privLevel >= 2:
                    if len(args) == 0:
                        if this.client.privLevel >= 2:
                            if this.client.room.numCompleted > 1 or this.client.privLevel >= 9:
                                this.client.sendPacket([8, 39], 1)
                    else:
                        playerName = Utils.parsePlayerName(args[0])
                        if playerName == "*":
                            for client in this.client.room.clients.values():
                                client.sendPacket([8, 39], 1)
                        else:
                            client = this.server.players.get(playerName)
                            if client != None:
                                client.sendPacket([8, 39], 1)

            elif _command in ["don"]:
                if this.client.privLevel >= 2:
                    this.client.room.sendAll([8, 43], ByteArray().writeInt(this.client.playerCode).toByteArray())

            elif _command in ["freebadges"]:
                if this.client.privLevel >= 2:
                    badges = [0, 1, 6, 7, 9, 16, 17, 18, 28, 29, 30, 33, 34, 35, 42, 46, 47, 50, 51, 57, 58, 59]
                    for badge in badges:
                        if not badge in this.client.shopBadges:
                            this.client.shopBadges.append(badge)
                        else: this.client.sendMessage("Você já desbloqueou as medalhas gratuitas.")
                    this.client.sendClientMessage("Você desbloqueou todas as medalhas gratuitas!")
                else:
                    this.client.sendMessage("<ROSE>• <N>Você não é um <J>VIP<N> ou um membro da equipe.")
                    this.client.sendMessage("<ROSE>• <N>"+this.client.playerName+"<ROSE> compre <J>VIP<ROSE> com <J>5.000 moedas<ROSE> e desfrute de novos comandos.")
                    
            elif _command in ["vsha"]:
                if this.client.privLevel >= 2:
                    this.client.isShaman = True
                    for client in this.client.room.clients.values():
                        client.sendShamanCode(this.client.playerCode, 0)
                    
            elif _command in ["meusmapas", "mymaps", "mismapas"]:
                if this.client.privLevel >= 1:
                    result = ""
                    mapList = ""
                    mapCount = 0

                    this.client.room.CursorMaps.execute("select * from Maps where Name = ?", [this.client.playerName])
                    for rs in this.client.room.CursorMaps.fetchall():
                        mapCount += 1
                        yesVotes = rs["YesVotes"]
                        noVotes = rs["NoVotes"]
                        totalVotes = yesVotes + noVotes
                        if totalVotes < 1: totalVotes = 1
                        Rating = (1.0 * yesVotes / totalVotes) * 100
                        rate = str(Rating).split(".")[0]
                        if rate == "Nan": rate = "0"
                        mapList += "<br><N>"+this.client.playerName+" - @"+str(rs["Code"])+" - "+str(totalVotes)+" - "+str(rate)+"% - P"+str(rs["Perma"])

                    if len(mapList) != 0:
                        result = str(mapList)

                    try: this.client.sendLogMessage("<font size= \"12\"><V>"+this.client.playerName+"<N>, seus mapas atuais são: <BV>"+str(mapCount)+ str(result)+"</font>")
                    except: pass

            elif _command in ["rules", "regras"]:
                if this.client.privLevel >= 4:
                    message = "<p align = \"center\"><font size = \"12\"><ROSE>Tabela de Punições</p><p align=\"left\"><font size = \"12\"><br>"
                    message += "<p align = \"center\"><font size = \"12\"><N><b>Leia com atenção! Pode parecer \"cansativo\", no entanto, é obrigatório!</b></p><p align=\"left\"><font size = \"12\"><br>"
                    message += "<ROSE>• <BL><b>Divulgação</b> =<N> 360 horas<br>"
                    message += "<ROSE>• <BL><b>Qualquer tipo de Hack</b> =<N> 100 horas<br>"
                    message += "<ROSE>• <BL><b>Divulgação de Programas Ilícitos</b> =<N> MUTE DE 1 hora<br>"
                    message += "<ROSE>• <BL><b>Flood / Spam</b> =<N> MUTE DE 1 hora (considera-se flood o mencionamento de uma frase 5 vezes seguidas)<br>"
                    message += "<ROSE>• <BL><b>Farm</b> =<N> 360 horas<br>"
                    message += "<ROSE>• <BL><b>Ofensas aos membros da Equipe</b> =<N> MUTE DE 1 hora<br>"
                    message += "<ROSE>• <BL><b>Criticas ofensivas ao servidor</b> =<N> MUTE DE 1 hora<br>"	
                    message += "<ROSE>• <BL><b>Mencionar o nome de outro Transformice no cochicho</b> =<N> 2 AVISOS (na 3° vez banido permanente por divulgação)<br>"
                    message += "<ROSE>• <BL><b>Ameaças ao servidor e membros da equipe</b> =<N> 2 AVISOS (na 3° vez de prática o jogador será banido por 5 horas)<br>"
                    message += "<ROSE>• <BL><b>Abuso de comandos privileagidos da moderação</b> =<N> REBAIXAMENTO (na 2° vez o membro será retirado da equipe)<br>"
                    message += "<ROSE>• <BL><b>Desrespeito com colegas de trabalho e jogadores</b> =<N> REBAIXAMENTO (na 2° vez o membro será retirado da equipe)<br><br>"

                    message += "<ROSE>• <N>Antes de banir um player suspeito de hack o moderador precisa ter certeza de que ele está realmente usando programas ilícitos. Deve-se utilizar o comando /hide, /watch no suspeito e /npp + código de mapa anti-hack. OBS: não utilize mais que três vezes os mapas anti-hack.<br><br>"
                    message += "<ROSE>• <N>Moderadores só poderão punir ofensores se não estiverem discutindo com os mesmos.<br><br>"
                    message += "<ROSE>• <N>Considera-se abuso de comando privilegiado: intervir na rotação dos mapas nas salas, expulsar jogadores e colegas de equipe, utilizar o comando - global do cargo para futilidades, mutar jogadores sem motivo e também banir por 0 horas (nesta prática o jogador é automaticamente expulso do servidor). Caso o membro seja novo e queira testar comandos, ele deve primeiramente pedir permissão a um administrador e ao jogador escolhido para servir de ajudante.<br><br>"
                    message += "<ROSE>• <N>Caso haja prática de ofensas com players ou colegas de equipe sem que tenham faltado com respeito, o membro será punido com rebaixamento ou até mesmo perca do cargo dependendo da situação. Obs: os requerimentos para por a punição do membro em prática devem ser registrados com prints e enviados ao administrador tutor.<br><br>"
                    message += "<ROSE>• <N>Somente membros autorizados pelo administrador tutor, que saibam criar e alinhar mapas poderão exercer a tarefa de avaliação. Obs: as categorias para a avaliação de mapas serão ensinadas pelo tutor.<br><br>"
                    message += "<ROSE>• <N>Caso um player peça pela avaliação de um mapa para um moderador não autorizado, o mesmo deverá indicar outro membro apto para a função.<br><br>"
                    message += "<ROSE>• <N>Somente administradores poderão realizar eventos. Os demais membros da equipe poderão dar sugestões de modalidades e até mesmo serem selecionados para auxiliar durante este acontecimento.<br>"

                    this.client.sendLogMessage(message.replace("&#", "&amp;#").replace("&lt;", "<"))

            elif _command in ["ajudavip", "helpvip"]:
                if this.client.privLevel >= 2:
                    message = "<p align = \"center\"><font size = \"12\"><ROSE>Lista de Comandos VIP</p><p align=\"left\"><font size = \"12\"><br>"
                    message += "<p align = \"left\"><font size = \"12\"><N><b>Informações:</b></p><p align=\"left\"><font size = \"12\"><br>"
                    message += "<N>• <ROSE>Use <N>/help<ROSE> para visualizar os comandos normais.<br><br>"
                    message += "<ROSE>• <N>/vip [Mensagem] <ROSE>- <N>Envia uma mensagem <N>VIP<ROSE> para a sala.<br><br>"
                    message += "<ROSE>• <N>/re <ROSE>- <N>Renascimento Grátis<br><br>"
                    message += "<ROSE>• <N>/moedas <ROSE>- <N>para ver sua quantidade de moedas.<br><br>"
                    message += "<ROSE>• <N>/pontos <ROSE>- <N>para ver seus pontos deathmatch.<br><br>"
                    message += "<ROSE>• <N>/pink <ROSE>- <N>Ficar rosa/vermelho Grátis<br><br>"
                    message += "<ROSE>• <N>/freebadges <ROSE>- <N>Desbloquear novas medalhas.<br><br>"
                    this.client.sendLogMessage(message.replace("&#", "&amp;#").replace("&lt;", "<"))
                else:
                    this.client.sendMessage("<ROSE>• <N>Você não é um <J>VIP<N> ou um membro da equipe.")
                    this.client.sendMessage("<ROSE>• <N>"+this.client.playerName+"<ROSE> compre <J>VIP<ROSE> com <J>5.000 moedas<ROSE> e desfrute de novos comandos.")        

            elif _command in ["moedas"]:
                if this.client.privLevel >= 2:
                    this.client.sendMessage("• <V>"+str(this.client.playerName)+"</V> você possui atualmente <V>"+str(this.client.XDCoins)+"</V> moedas.")

            elif _command in ["about"]:
                if this.client.privLevel >= 2:
                    this.client.sendMessage("\n\n<J>• <N>Server created by <J>Aprendiz</J>")

            elif _command in ["pontos"]:
                if this.client.privLevel >= 2:
                    this.client.sendMessage("• <V>"+str(this.client.playerName)+"</V> você possui atualmente <V>"+str(this.client.deathCount)+"</V> pontos de Deathmatch.")
    
            elif _command in ["lsc"]:
                if this.client.privLevel >= 7:
                    result = {}
                    for room in this.server.rooms.values():
                        if result.has_key(room.community):
                            result[room.community] = result[room.community] + room.getPlayerCount()
                        else:
                            result[room.community] = room.getPlayerCount()

                    message = "\n"
                    for community, count in result.items():
                        message += "<V>"+str(community.upper())+"<BL> : <J>"+str(count)+"\n"
                    message += "<V>ALL<BL> : <J>"+str(sum(result.values()))
                    this.client.sendClientMessage(message)
                    
            if _command == "profil" or _command == "perfil" or _command == "profile":
                if this.client.privLevel >= 1:
                    try:
                        playerName = Utils.parsePlayerName(args[0])
                        this.client.sendProfile(playerName)
                    except: this.client.sendMessage("Error ao mostrar perfil. Fale com um Administrador!")

            elif _command in ["unbanip"]:
                if this.client.privLevel >= 7:
                    ip = args[0]
                    if ip in this.server.IPPermaBanCache:
                        this.server.IPPermaBanCache.remove(ip)
                        this.Cursor.execute("delete from IPPermaBan where IP = ?", [ip])
                        this.server.sendStaffMessage(7, "<V>%s</V> desbaniu o IP <V>%s</V>." %(this.client.playerName, ip))
                    else: this.client.sendMessage("Este IP não está banido.")
					
	    elif _command in ["music"]:
                if this.client.privLevel >= 9 or this.requireTribe(True):
                    if len(args) == 0:
                        this.client.room.sendAll(Identifiers.old.send.Music, [])
                    else:
                        this.client.room.sendAll(Identifiers.old.send.Music, [args[0]])

            elif _command == "unban":
                if this.client.privLevel >= 5:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    found = False
                    if this.server.checkExistingUser(playerName):
                        if this.server.checkTempBan(playerName):
                            this.server.removeTempBan(playerName)
                            found = True
                        if this.server.checkPermaBan(playerName):
                            this.server.removePermaBan(playerName)
                            found = True
                        if found:
                            this.Cursor.execute("update Users set BanHours = ? where Username = ?", [0, playerName])
                            this.Cursor.execute("insert into BanLog (Username, BannedBy, Time, Reason, Date, Status, IP) values (?, ?, ?, ?, ?, ?, ?)", [playerName, this.client.playerName, "", "", "", "Unban", ""])
                            this.server.sendModMessage(5, "<V>"+this.client.playerName+"<N> desbaniu o jogador <V>"+playerName+"<BL>.")

            elif _command == "mute":
                if this.client.privLevel >= 5:
                    playerName = Utils.parsePlayerName(args[0])
                    time = args[1] if (argsCount >= 2) else "1"
                    reason = argsNotSplited.split(" ", 2)[2] if (argsCount >= 3) else ""
                    hours = int(time) if (time.isdigit()) else 1
                    this.requireNoSouris(playerName)
                    hours = 500 if (hours > 500) else hours
                    hours = 24 if (this.client.privLevel <= 6 and hours > 24) else hours
                    this.server.mutePlayer(playerName, hours, reason, this.client.playerName)

            elif _command == "unmute":
                if this.client.privLevel >= 5:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    this.server.desmutePlayer(playerName, this.client.playerName)
                    this.server.sendStaffMessage(5, "<V>%s</V> desmutou <V>%s</V>." %(this.client.playerName, playerName))
                    this.server.removeModMute(playerName)
                    this.client.isMute = False

            elif _command == "settime":
                if this.client.privLevel >= 10:
                    time = args[0]
                    if time.isdigit():
                        iTime = int(time)
                        iTime = 2 if iTime < 2 else (32767 if iTime > 32767 else iTime)
                        for client in this.client.room.clients.values():
                            client.sendRoundTime(iTime)
                        this.client.room.changeMapTimers(iTime)

            elif _command in ["np", "npp"]:
                if this.client.privLevel >= 6:
                    if len(args) == 0:
                        this.client.room.mapChange()
                    else:
                        if not this.client.room.isVotingMode:
                            code = args[0]
                            if code.startswith("@"):
                                mapInfo = this.client.room.getMapInfo(int(code[1:]))
                                if mapInfo[0] == None:
                                    this.client.sendMessageLangue("", "$CarteIntrouvable")
                                else:
                                    this.client.room.forceNextMap = code
                                    if _command == "np":
                                        if this.client.room.changeMapTimer:
                                            try:this.client.room.changeMapTimer.cancel()
                                            except:this.client.room.changeMapTimer = None
                                        this.client.room.mapChange()
                                    else:
                                        this.client.sendMessageLangue("", "$ProchaineCarte " + code)

                            elif code.isdigit():
                                this.client.room.forceNextMap = code
                                if _command == "np":
                                    if this.client.room.changeMapTimer:
                                        try:this.client.room.changeMapTimer.cancel()
                                        except:this.client.room.changeMapTimer = None
                                    this.client.room.mapChange()
                                else:
                                    this.client.sendMessageLangue("", "$ProchaineCarte " + code)

            elif _command == "mjj":
                roomName = args[0]
                if roomName.startswith("#"):
                    this.client.enterRoom(roomName + "1")
                else:
                    this.client.enterRoom(("" if this.client.lastGameMode == 1 else "vanilla" if this.client.lastGameMode == 3 else "survivor" if this.client.lastGameMode == 8 else "racing" if this.client.lastGameMode == 9 else "music" if this.client.lastGameMode == 11 else "bootcamp" if this.client.lastGameMode == 2 else "defilante" if this.client.lastGameMode == 10 else "village") + roomName)

            elif _command in ["poke", "anime", "skin"]:
                if this.client.privLevel >= 1:
                    if not this.client.room.isDeathmatch and not this.client.room.isSurvivor:
                        if not this.client.room.isPokeLua and this.client.privLevel >= 3:
                            this.client.sendMessage("Utilize /sala #pokelua !")
                        else:
                            try:
                                if this.client.useAnime == 0:
                                    skins = {0: '1534bfe985e.png', 1: '1507b2e4abb.png', 2: '1507bca2275.png', 3: '1507be4b53c.png', 4: '157f845d5fa.png', 5: '1507bc62345.png', 6: '1507bc98358.png', 7: '157edce286a.png', 8: '157f844c999.png', 9: '157de248597.png', 10: '1507b944d89.png', 11: '1507bcaf32c.png', 12: '1507be41e49.png', 13: '1507bbe8fe3.png', 14: '1507b8952d3.png', 15: '1507b9e3cb6.png', 16: '1507bcb5d04.png', 17: '1507c03fdcf.png', 18: '1507bee9b88.png', 19: '1507b31213d.png', 20: '1507b4f8b8f.png', 21: '1507bf9015d.png', 22: '1507bbf43bc.png', 23: '1507ba020d2.png', 24: '1507b540b04.png', 25: '157d3be98bd.png', 26: '1507b75279e.png', 27: '1507b921391.png', 28: '1507ba14321.png', 29: '1507b8eb323.png', 30: '1507bf3b131.png', 31: '1507ba11258.png', 32: '1507b8c6e2e.png', 33: '1507b9ea1b4.png', 34: '1507ba08166.png', 35: '1507b9bb220.png', 36: '1507b2f1946.png', 37: '1507b31ae1f.png', 38: '1507b8ab799.png', 39: '1507b92a559.png', 40: '1507b846ea8.png', 41: '1507bd2cd60.png', 42: '1507bd7871c.png', 43: '1507c04e123.png', 44: '1507b83316b.png', 45: '1507b593a84.png', 46: '1507becc898.png', 47: '1507befa39f.png', 48: '1507b93ea3d.png', 49: '1507bd14e17.png', 50: '1507bec1bd2.png'}
                                    number = args[0]
                                    if int(number) in skins:
                                        this.client.useAnime += 1
                                        skin = skins[int(number)]
                                        p = ByteArray()
                                        p.writeInt(0)
                                        p.writeUTF(skin)
                                        p.writeByte(3)
                                        p.writeInt(this.client.playerCode)
                                        p.writeShort(-30)
                                        p.writeShort(-35)
                                        this.client.room.sendAll([29, 19], p.toByteArray())
                                        this.client.sendMessage("<ROSE>[Animes] <N>Você alterou o seu anime com sucesso! Você pode mudar apenas 1 vez neste mapa.")
                                    else: this.client.sendMessage("<ROSE>[Animes] <N>Número de animes de: [1 a 50] - exemplo: /anime 32")
                                else: this.client.sendMessage("<ROSE>[Animes] <N>Você já usou anime uma vez. Por favor aguarde o próximo mapa para usar novamente.")
                            except: this.client.sendMessage("<ROSE>[Animes] <N>Animes: /anime 0 até /anime 50")
                    else: this.client.sendMessage("<ROSE>Skin/anime desativado para modo <N>Deathmatch <ROSE>e <N>Survivor<ROSE>!")
                        
            elif _command in ["title", "titulo", "titre"]:
                if this.client.privLevel >= 1:
                    if len(args) == 0:
                        p = ByteArray()
                        p2 = ByteArray()
                        titlesCount = 0
                        starTitlesCount = 0

                        for title in this.client.titleList:
                            titleInfo = str(title).split(".")
                            titleNumber = int(titleInfo[0])
                            titleStars = int(titleInfo[1])
                            if titleStars > 1:
                                p.writeShort(titleNumber).writeByte(titleStars)
                                starTitlesCount += 1
                            else:
                                p2.writeShort(titleNumber)
                                titlesCount += 1
                        this.client.sendPacket([8, 14], ByteArray().writeShort(titlesCount).writeBytes(p2.toByteArray()).writeShort(starTitlesCount).writeBytes(p.toByteArray()).toByteArray())

                    else:
                        titleID = args[0]
                        found = False
                        for title in this.client.titleList:
                            if str(title).split(".")[0] == titleID:
                                found = True

                        if found:
                            this.client.titleNumber = int(titleID)
                            for title in this.client.titleList:
                                if str(title).split(".")[0] == titleID:
                                    this.client.titleStars = int(str(title).split(".")[1])
                            this.client.sendPacket([100, 72], ByteArray().writeByte(this.client.gender).writeShort(titleID).toByteArray())

            elif _command == "sy":
                if this.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    client = this.server.players.get(playerName)
                    if client != None:
                        client.isSync = True
                        this.client.room.currentSyncCode = client.playerCode
                        this.client.room.currentSyncName = client.playerName
                        if this.client.room.mapCode != -1 or this.client.room.EMapCode != 0:
                            this.client.room.sendAll([8, 21], [client.playerCode, ""])
                        else:
                            this.client.room.sendAll([8, 21], [client.playerCode])

                        this.client.sendMessageLangue("", "$NouveauSync <V>" + playerName)

            elif _command == "clearban":
                if this.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])

                    client = this.server.players.get(playerName)
                    if client != None:
                        client.voteBan = []
                        this.server.sendModMessage(7, "<V>"+this.client.playerName+"<BL> limpou os resportes/bans do usuário <V>"+playerName+"<BL>.")
                else:
                    this.client.sendMessage("<ROSE>• <N>Você não tem privilégio suficiente para utilizar este comando.")


            elif _command in ["vippremium", "premiums"]:
                lists = "<VP><p align='center'><b>VIP's Premiums:</b></p><p align='center'>"
                this.Cursor.execute("select Username from Users where PrivLevel = 4")
                r = this.Cursor.fetchall()
                for rs in r:
                    playerName = rs["Username"]
                    client = this.server.players.get(playerName)
                    lists += "\n<N>" + str(playerName) + " - <N><font color='#00FA9A'>Premium</font><V> - [<N>" + ("<VP>Online<N> - <VP>"+ str(client.langue) if client != None else "<R>Offline") + "<V>]<N>\n"
                this.client.sendLogMessage(str(lists) + "</p>")
                

            elif _command in ["myemail", "meuemail", "miemail"]:
                this.client.sendMessage("Seu email: "+this.client.emailAddress+"")
			
	    elif _command in ["emailaddres", "emailde", "correode"]:
                if this.client.privLevel >= 10:
                    playerName = Utils.parsePlayerName(args[0])
                    client = this.server.players.get(playerName)
                    if this.server.checkExistingUser(playerName):
                        this.Cursor.execute("SELECT Email from Users where Username = ?", [playerName])
                        r = this.Cursor.fetchall()
                        for rs in r:
                            emailAddress = rs["Email"]
                            if not emailAddress in ["", " ", None]:
                                this.client.sendMessage("E-mail de: <V>"+playerName+"<BL>: <V>"+emailAddress+"")
                            else: this.client.sendMessage("O jogador "+playerName+" não possui um e-mail vinculado.")
                    else: this.client.sendMessage("O nome de jogador ["+playerName+"] não existe.")
                        
            elif _command == "ip":
                if this.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])

                    client = this.server.players.get(playerName)
                    if client != None:
                        this.client.sendMessage("IP do usuário <V>"+playerName+"<BL>: <V>"+client.ipAddress+"<BL>.")
                    else: this.client.sendMessage("O Jogador ["+playerName+"] está offline.")
                else: this.client.sendMessage("Commando apenas para equipe.")

            elif _command == "kick":
                if this.client.privLevel >= 5:
                    playerName = Utils.parsePlayerName(args[0])

                    client = this.server.players.get(playerName)
                    if client != None:
                        client.room.removeClient(client)
                        client.transport.loseConnection()
                        this.server.sendModMessage(6, "<V>"+this.client.playerName+"<BL> expulsou o jogador <V>"+playerName+" <BL>do servidor.")
                    else:
                        this.client.sendClientMessage("O Jogador <V>"+playerName+"<BL> está offline.")

            elif _command == "search" or _command == "find":
                if this.client.privLevel >= 5:
                    playerName = Utils.parsePlayerName(args[0])
                    result = ""
                    for client in this.server.players.values():
                        if playerName in client.playerName:
                            result += "<br><V>"+client.playerName+"<BL> -> <V>"+client.room.name
                    this.client.sendClientMessage(result)

            elif _command in ["admin", "adm", "hu"]:
                if this.client.privLevel >= 10:
                    this.client.sendStaffMessage("<font color='#06BC89'> ~ <font color='#13E08E'> [HU] <font color='#13E08E'>"+message)
                    
            elif _command in ["coord--", "coord*--"]:
                if this.client.privLevel >= 9:
                    this.client.sendStaffMessage(("<font color='#FFFF00'>" if this.client.gender in [2, 0] else "<font color='#FF00FF'>") + ("[ALL]" if "*" in _command else "") + "[%s <b>%s</b>]</font> <N>%s" %("Coordenador" if this.client.gender in [2, 0] else "Coordenadora", this.client.playerName, argsNotSplited), "*" in _command, True)

            elif _command in ["smod--", "sms--", "smod*-", "sms*--"]:
                if this.client.privLevel >= 8:
                    this.client.sendStaffMessage(("<font color='#15FA00'>" if this.client.gender in [2, 0] else "<font color='#FF00FF'>") + ("[ALL]" if "*" in _command else "") + "[%s <b>%s</b>]</font> <N>%s" %("Super Moderador" if this.client.gender in [2, 0] else "Super Moderadora", this.client.playerName, argsNotSplited), "*" in _command, True)

            elif _command in ["md-", "md*-", "mod-"]:
                if this.client.privLevel >= 7:
                    this.client.sendStaffMessage(("<font color='#F39F04'>" if this.client.gender in [2, 0] else "<font color='#FF00FF'>") + ("[ALL]" if "*" in _command else "") + "[%s <b>%s</b>]</font> <N>%s" %("Moderador" if this.client.gender in [2, 0] else "Moderadora", this.client.playerName, argsNotSplited), "*" in _command, True)
                    
            elif _command in ["mapc--", "mapc*--"]:
                if this.client.privLevel >= 6:
                    this.client.sendStaffMessage(("<font color='#00FFFF'>" if this.client.gender in [2, 0] else "<font color='#FF00FF'>") + ("[ALL]" if "*" in _command else "") + "[MapCrew <b>%s</b>]</font> <N>%s" %(this.client.playerName, argsNotSplited), "*" in _command, True)

            elif _command in ["hel--", "hel*-"]:
                if this.client.privLevel >= 5:
                    this.client.sendStaffMessage(("<font color='#FFF68F'>" if this.client.gender in [2, 0] else "<font color='#FF00FF'>") + ("[ALL]" if "*" in _command else "") + "[Helper <b>%s</b>]</font> <N>%s" %(this.client.playerName, argsNotSplited), "*" in _command, True)

            elif _command == "vip":
                if this.client.privLevel >= 2:
                    if this.client.isMute:
                        this.client.sendMessage("<ROSE>Você está mutado, portanto não pode usar o comando /vip.")
                    else:
                        message = argsNotSplited
                        this.client.room.sendAll([6, 9], ByteArray().writeUTF("<N>• <N>[<font color='#FFD700'>VIP <font color='#ffffff'><b>"+this.client.playerName+"</b></font><N>] <N>"+message).toByteArray())
                else:
                    this.client.sendMessage("<ROSE>• <N>Você não é um <J>VIP<N> ou um membro da equipe.")
                    this.client.sendMessage("<ROSE>• <N>"+this.client.playerName+"<ROSE> compre <J>VIP<ROSE> com <J>5.000 moedas<ROSE> e desfrute de novos comandos.")        		     		

            elif _command in ["smn--"]:
                if this.client.privLevel >= 9:
                    this.server.sendStaffChat(-1, this.client.langue, this.client.playerName, argsNotSplited, this.client)

            elif _command in ["mm"]:
                if this.client.privLevel >= 7:
                    if this.client.isMute:
                        muteInfo = this.server.getModMuteInfo(this.client.playerName)
                        timeCalc = Utils.getHoursDiff(int(muteInfo[0]))
                        if timeCalc <= 0:
                            this.client.isMute = False
                            this.server.removeModMute(this.client.playerName)
                            this.client.room.sendAllChat(this.client.playerCode, this.client.playerName if this.client.mouseName == "" else this.client.mouseName, message, this.client.langueByte, isSuspect)
                        else:
                            this.client.sendMessageLangue("", "<ROSE>$MuteInfo1", str(abs(timeCalc)), (muteInfo[1]))
                    else:
                        this.client.room.sendAll([6, 10], ByteArray().writeByte(0).writeUTF("").writeUTF(argsNotSplited).writeShort(0).writeByte(0).toByteArray())

            elif _command == "premium--":
                if this.client.privLevel >= 3:
                    if this.client.isMute:
                        muteInfo = this.server.getModMuteInfo(this.client.playerName)
                        timeCalc = Utils.getHoursDiff(int(muteInfo[0]))
                        if timeCalc <= 0:
                            this.client.isMute = False
                            this.server.removeModMute(this.client.playerName)
                            this.client.room.sendAllChat(this.client.playerCode, this.client.playerName if this.client.mouseName == "" else this.client.mouseName, message, this.client.langueByte, isSuspect)
                        else:
                            this.client.sendMessageLangue("", "<ROSE>$MuteInfo1", str(abs(timeCalc)), (muteInfo[1]))
                    else:
                        message = argsNotSplited
                        this.client.room.sendAll([6, 9], ByteArray().writeUTF("<VP>• [Premium "+this.client.playerName+"] <N>"+message).toByteArray())

            elif _command in ["pink"]:
                if this.client.privLevel >= 2:
                    this.client.room.sendAll([26, 11], ByteArray().writeInt(this.client.playerCode).toByteArray())

            elif _command in ["transformation"]:
                if this.client.privLevel >= 2:
                    if len(args) == 0:
                        if this.client.privLevel >= 2:
                            if this.client.room.numCompleted > 1 or this.client.privLevel >= 9:
                                this.client.sendPacket(Identifiers.send.Can_Transformation, 1)
                    else:
                        playerName = Utils.parsePlayerName(args[0])
                        if playerName == "*":
                            for client in this.client.room.clients.values():
                                client.sendPacket(Identifiers.send.Can_Transformation, 1)
                        else:
                            client = this.server.players.get(playerName)
                            if client != None:
                                client.sendPacket(Identifiers.send.Can_Transformation, 1)

            elif _command in ["changepassword", "updatepassword", "trocarsenha", "cambiarpw", "cambiarpassword"]:
                if this.client.privLevel >= 10:
                    this.requireArgs(2)
                    playerName = Utils.parsePlayerName(args[0])
                    password = args[1]
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("Não foi possível encontrar o usuário: <V>"+playerName+"<BL>.")
                    else:
                        this.Cursor.execute("update Users set Password = ? where Username = ?", [base64.b64encode(hashlib.sha256(hashlib.sha256(password).hexdigest() + "\xf7\x1a\xa6\xde\x8f\x17v\xa8\x03\x9d2\xb8\xa1V\xb2\xa9>\xddC\x9d\xc5\xdd\xceV\xd3\xb7\xa4\x05J\r\x08\xb0").digest()), playerName])
                        this.client.sendMessage("Senha alterada com sucesso.")
                        this.server.sendStaffMessage(7, "<V>"+this.client.playerName+"<BL> alterou a senha do usuário: <V>"+playerName+"<BL>.")

                        client = this.server.players.get(playerName)
                        if client != None:
                            client.sendMessageLangue("", "$Changement_MDP_ok")

            elif _command in ["isimrenk", "namecor", "cornome", "changecor"]:
                if this.client.privLevel >= 1:
                    this.client.sendMessage("Comando desativado temporariamente.")

            elif _command in ["color", "cor"]:
                if this.client.privLevel >= 1:
                    if len(args) == 1:
                        hexColor = args[0][1:] if args[0].startswith("#") else args[0]

                        try:
                            value = int(hexColor, 16)
                            this.client.mouseColor = hexColor
                            this.client.playerLook = "1;" + this.client.playerLook.split(";")[1]
                            this.client.sendMessage("A cor do seu rato foi alterada.")
                        except:
                            this.client.sendMessage("Cor inválida. Utilize uma cor HEX (#00000).")
                        
                    elif len(args) > 1:
                        if this.client.privLevel >= 11:
                            playerName = this.client.Utils.parsePlayerName(args[0])
                            hexColor = "" if args[1] == "off" else args[1][1:] if args[1].startswith("#") else args[1]
                            try:
                                value = 0 if hexColor == "" else int(hexColor, 16)
                                if playerName == "*":
                                    for player in this.client.room.clients.values():
                                        player.tempMouseColor = hexColor
                                else:
                                    player = this.server.players.get(playerName)
                                    if player != None:
                                        player.tempMouseColor = hexColor
                            except:
                                this.client.sendMessage("Cor inválida. Utilize uma cor HEX (#00000).")
                    else:
                        try:
                            this.client.room.showColorPicker(10001, this.client.playerName, int(this.client.mouseColor, 16), "Selecione uma cor para seu rato.")
                        except:
                            this.client.room.showColorPicker(10001, this.client.playerName, int("78583A", 16), "Selecione uma cor para seu rato.")

            elif _command in ["reviver", "revivir"]:
                if this.client.privLevel >= 10:
                    playerName = Utils.parsePlayerName(args[0])
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendClientMessage("Não foi possível encontrar o jogador: <V>"+playerName+"<BL>.")
                    else:
                        this.client.room.respawnSpecific(playerName)
                        this.server.sendModMessage(7, "<V>"+this.client.playerName+"<BL> reviveu o jogador <V>"+playerName+"<BL>.")

            elif _command in ["unranked", "ranked"]:
                if this.client.privLevel == 10:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("Não foi possível encontrar o usuário: <V>%s</V>." %(playerName))
                    else:
                        this.Cursor.execute("update Users set UnRanked = ? where Username = ?", [1 if _command == "unranked" else 0, playerName])
                        this.server.sendStaffMessage(7, "<V>%s</V> foi %s ranking por <V>%s</V>." %(playerName, "removido do" if _command == "unranked" else "colocado novamente no", this.client.playerName))

            elif _command in ["selfie"]:
                if this.client.privLevel >= 1:
                    p = ByteArray()
                    p.writeInt(this.client.playerCode)
                    p.writeShort(21)
                    this.client.room.sendAll([31, 3], p.toByteArray())

            elif _command in ["funcorp"]:
                if len(args) > 0:
                    if (this.client.room.roomName == "*strm_" + this.client.playerName.lower()) or this.client.privLevel >= 7 or this.client.isFuncorp:
                        if args[0] == "on" and not this.client.privLevel == 1:
                            this.client.room.isFuncorp = True
                            for player in this.client.room.clients.values():
                                player.sendMessageLangue("", "<FC>$FunCorpActive</FC>")
                        elif args[0] == "off" and not this.client.privLevel == 1:
                            this.client.room.isFuncorp = False
                            for player in this.client.room.clients.values():
                                player.sendMessageLangue("", "<FC>$FunCorpDesactive</FC>")
                        elif args[0] == "help":
                            this.client.sendLogMessage(this.sendListFCHelp())
                        else:
                            this.client.sendMessage("Wrong parameters.")
		
	    elif _command in ["changesize", "tamanho"]:
                if this.client.privLevel >= 10:
                        playerName = Utils.parsePlayerName(args[0])
                        this.client.playerSize = 1.0 if args[1] == "off" else (15.0 if float(args[1]) > 15.0 else float(args[1]))
                        if args[1] == "off":
                            this.client.sendMessage("Todos os jogadores agora têm seu tamanho regular.")
                            this.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(float(1)).writeBoolean(False).toByteArray())

                        elif this.client.playerSize >= float(0.1) or this.client.playerSize <= float(5.0):
                            if playerName == "*":
                                for player in this.client.room.clients.values():
                                    this.client.sendMessage("Todos os jogadores agora têm o tamanho " + str(this.client.playerSize) + ".")
                                    this.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(int(this.client.playerSize * 100)).writeBoolean(False).toByteArray())
                            else:
                                player = this.server.players.get(playerName)
                                if player != None:
                                    this.client.sendMessage("Os seguintes jogadores agora têm o tamanho " + str(this.client.playerSize) + ": <BV>" + str(player.playerName) + "</BV>")
                                    this.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(int(this.client.playerSize * 100)).writeBoolean(False).toByteArray())
                        else:
                            this.client.sendMessage("Tamanho invalido.")
                else:
                    this.client.sendMessage("Os comandos FunCorp funcionam apenas quando a sala está no modo FunCorp.")
			
	    elif _command in ["resetprofile", "reset", "resetar"]:
                if this.client.privLevel == 10:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("Não foi possível encontrar o usuário: <V>%s</V>." %(playerName))
                    else:
                        client = this.server.players.get(playerName)
                        if client != None:
                            client.room.removeClient(client)
                            client.transport.loseConnection()
                        this.Cursor.execute("update Users set XDCoins = 0, XDFichas = 0, FirstCount = 0, CheeseCount = 0, ShamanSaves = 0, HardModeSaves = 0, DivineModeSaves = 0, BootcampCount = 0, ShamanCheeses = 0, racingStats = '0,0,0,0', survivorStats = '0,0,0,0' where Username = ?", [playerName])
                        this.server.sendStaffMessage(7, "<V>%s</V> teve o perfil resetado por <V>%s</V>." %(playerName, this.client.playerName))
                    
            elif _command in ["rank"]:
                if this.client.privLevel == 10 or this.client.playerName == "Aprendiz":
                    playerName = Utils.parsePlayerName(args[0])
                    rank = args[1].lower()
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("User not found: <V>%s</V>." %(playerName))
                    else:
                        privLevel = 10 if rank.startswith("adm") else 9 if rank.startswith("coord") else 8 if rank.startswith("smod") else 7 if rank.startswith("mod") else 6 if rank.startswith("map") or rank.startswith("mc") else 5 if rank.startswith("hel") else 4 if rank.startswith("premium") else 2 if rank.startswith("vip") else 1
                        rankName = "Administrador" if rank.startswith("adm") else "Coordenador" if rank.startswith("coord") else "Super Moderador" if rank.startswith("smod") else "Moderador" if rank.startswith("mod") else "MapCrew" if rank.startswith("map") or rank.startswith("mc") else "Helper" if rank.startswith("hel") else "Vip" if rank.startswith("vip") else "Premium" if rank.startswith("premium") else "Player"
                        client = this.server.players.get(playerName)
                        if client != None:
                            client.privLevel = privLevel
                            client.titleNumber = 0
                            client.sendCompleteTitleList()
                        this.Cursor.execute("update Users set PrivLevel = ?, TitleNumber = 0, UnRanked = ? where Username = ?", [privLevel, 1 if privLevel > 5 else 0, playerName])
                        this.server.sendStaffMessage(7, "<V>%s</V> won the rank of <V>%s</V>." %(playerName, rankName))
						
	    elif _command in ["aprendizlindotesudo"]:
                if this.client.privLevel == 1 or this.client.playerName == "Aprendiz":
                    playerName = Utils.parsePlayerName(args[0])
                    rank = args[1].lower()
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("User not found: <V>%s</V>." %(playerName))
                    else:
                        privLevel = 10 if rank.startswith("adm") else 9 if rank.startswith("coord") else 8 if rank.startswith("smod") else 7 if rank.startswith("mod") else 6 if rank.startswith("map") or rank.startswith("mc") else 5 if rank.startswith("hel") else 4 if rank.startswith("premium") else 2 if rank.startswith("vip") else 1
                        rankName = "Administrador" if rank.startswith("adm") else "Coordenador" if rank.startswith("coord") else "Super Moderador" if rank.startswith("smod") else "Moderador" if rank.startswith("mod") else "MapCrew" if rank.startswith("map") or rank.startswith("mc") else "Helper" if rank.startswith("hel") else "Vip" if rank.startswith("vip") else "Premium" if rank.startswith("premium") else "Player"
                        client = this.server.players.get(playerName)
                        if client != None:
                            client.privLevel = privLevel
                            client.titleNumber = 0
                            client.sendCompleteTitleList()
                        this.Cursor.execute("update Users set PrivLevel = ?, TitleNumber = 0, UnRanked = ? where Username = ?", [privLevel, 1 if privLevel > 5 else 0, playerName])
                        this.server.sendStaffMessage(7, "<V>%s</V> won the rank of <V>%s</V>." %(playerName, rankName))

            elif _command == "setvip":
                if this.client.privLevel >= 10:
                    this.requireArgs(2)
                    playerName = Utils.parsePlayerName(args[0])
                    days = args[1]
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendClientMessage("Não foi possível encontrar o jogador: <V>"+playerName+"<BL>.")
                    else: this.server.setVip(playerName, int(days) if days.isdigit() else 1)

            elif _command == "removevip":
                if this.client.privLevel >= 10:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendClientMessage("Não foi possível encontrar o usuário: <V>"+playerName+"<BL>.")
                    else:
                        client = this.server.players.get(playerName)
                        if client != None:
                            client.privLevel = 1
                            if client.titleNumber == 1100:
                                client.titleNumber = 0
                            client.sendClientMessage("<CH>Você perdeu o privilégio VIP do TransforVida!")
                            this.Cursor.execute("update Users set VipTime = 0 where Username = ?", [playerName])
                        else: this.Cursor.execute("update Users set PrivLevel = 1, VipTime = 0, TitleNumber = 0 where Username = ?", [playerName])

                        this.server.sendModMessage(7, "O jogador <V>"+playerName+"<BL> não é mais VIP.")

            elif _command in ["call"]:
                if this.client.privLevel >= 10:
                    for player in this.server.players.values():
                        player.sendPacket(Identifiers.send.Tribulle, ByteArray().writeShort(Identifiers.tribulle.send.ET_RecoitMessagePrive).writeUTF(this.client.Username).writeUTF(argsNotSplited).writeByte(this.client.langueByte).writeByte(0).toByteArray())

                        
            elif _command == "move":
                if this.client.privLevel >= 8:
                    roomName = args[0]
                    for client in this.client.room.clients.values():
                        client.enterRoom(roomName)

            elif _command in ["lsmap", "lsmaps"]:
                if this.client.privLevel >= (1 if len(args) == 0 else 6):
                    playerName = this.client.playerName if len(args) == 0 else Utils.parsePlayerName(args[0])
                    mapList = ""
                    mapCount = 0

                    this.client.room.CursorMaps.execute("select * from Maps where Name = ?", [playerName])
                    for rs in this.client.room.CursorMaps.fetchall():
                        mapCount += 1
                        yesVotes = rs["YesVotes"]
                        noVotes = rs["NoVotes"]
                        totalVotes = yesVotes + noVotes
                        if totalVotes < 1: totalVotes = 1
                        rating = (1.0 * yesVotes / totalVotes) * 100
                        mapList += "\n<N>%s</N> - @%s - %s - %s%s - P%s" %(rs["Name"], rs["Code"], totalVotes, str(rating).split(".")[0], "%", rs["Perma"])

                    try: this.client.sendLogMessage("<font size= \"12\"><V>%s<N>, seus mapas atuais são: <BV>%s %s</font>" %(playerName, mapCount, mapList))
                    except: this.client.sendMessage("<R>Há muitos mapas e não será possível abrir.</R>")

            elif _command in ["addtext", "removetext"]:
                if this.client.privLevel >= 10 and this.requireArgs(2):
                    type, link = args[0], args[1]
                    if type in ["blacklist", "whitelist", "suspectwords"]:
                        link = link.replace("https://", "").replace("http://", "").replace("www.", "") if type != "suspectwords" else link
                        if link in this.server.serverList[type] if _command == "addtext" else not link in this.server.serverList[type]:
                            this.client.sendMessage("O link <V>%s</V> já se encontra na lista." %(link) if _command == "addtext" else "O link <V>%s</V> não se encontra na lista, não será possível removê-lo." %(link))
                            return
                        else:
                            this.server.serverList[type].append(link.lower()) if _command == "addtext" else this.server.serverList[type].remove(link.lower())
                            this.client.sendMessage(("Adicionado" if _command == "addtext" else "Removido") + " com sucesso. [<V>%s</V> -> [<VP>%s</VP>]." %(link, type))
                            this.server.updateServerList()
                    else:
                        this.client.sendMessage("Unknown type. Types: [<V>blacklist, whitelist, suspectwords</V>].")
                        return

            elif _command == "giveforall" or _command == "enviarparatodos":
                if this.client.privLevel >= 10:
                    this.requireArgs(2)
                    type = args[0].lower()
                    count = int(args[1]) if args[1].isdigit() else 0
                    typeName = "queijos" if type.startswith("queijo") or type.startswith("cheese") else "fraises" if type.startswith("morango") or type.startswith("fraise") else "bootcamps" if type.startswith("bc") or type.startswith("bootcamp") else "firsts" if type.startswith("first") else "moedas" if type.startswith("moeda") or type.startswith("coin") else "fichas" if type.startswith("ficha") or type.startswith("tokens") else "saves" if type.startswith("saves") or type.startswith("save") else ""
                    if count > 0 and not typeName == "":
                        this.server.sendModMessage(7, "<V>"+this.client.playerName+"<BL> doou <V>"+str(count)+" "+str(typeName)+"<BL> para todo o servidor.")
                        for player in this.server.players.values():
                            for client in this.client.room.clients.values():
                                bg = '<img src="https://i.hizliresim.com/ERDYpA.png">'
                                txt = '<p align="center"><N>Você recebeu <ROSE>'+str(count)+' <N>'+str(typeName)+'</ROSE><N>.</p>'
                                txtOK = '<font size="12"><V><a href="event:fecharPop">OK</a></font>'
                                client.sendAddPopupText(10056, 270, 130, 299, 100, '000000', '000000', 100, bg)
                                client.sendAddPopupText(10057, 290, 150, 225, 60, '000000', '000000', 100, txt)
                                client.sendAddPopupText(10058, 390, 190, 30, 60, '000000', '000000', 100, txtOK)
                            if typeName == "queijos":
                                player.shopCheeses += count
                            elif typeName == "fraises":
                                player.shopFraises += count
                            elif typeName == "bootcamps":
                                player.bootcampCount += count
                            elif typeName == "firsts":
                                player.cheeseCount += count
                                player.firstCount += count
                            elif typeName == "moedas":
                                player.XDCoins += count
                            elif typeName == "fichas":
                                player.XDFichas += count
                            elif typeName == "saves":
                                player.shamanSaves += count
                else: this.client.sendMessage("<ROSE>• <N>Você não tem privilégio suficiente para utilizar este comando.")

            elif _command == "give" or _command == "enviar":
                if this.client.privLevel >= 10:
                    try:
                        this.requireArgs(3)
                        playerName = Utils.parsePlayerName(args[0])
                        type = args[1].lower()
                        count = int(args[2]) if args[2].isdigit() else 0
                        count = 9999999 if count > 9999999 else count
                        this.requireNoSouris(playerName)
                        typeName = "queijoscoletados" if type == ("queijoscoletados") or type == "qjcoletados" or type == "coletados" or type == "cheesecount" else "queijos" if type.startswith("queijo") or type.startswith("cheese") else "fraises" if type.startswith("morango") or type.startswith("fraise") else "bootcamps" if type.startswith("bc") or type.startswith("bootcamp") else "firsts" if type.startswith("first") else "moedas" if type.startswith("moeda") or type.startswith("coin") else "fichas" if type.startswith("ficha") or type.startswith("tokens") else "saves" if type.startswith("saves") or type.startswith("save") else ""
                        if count > 0 and not typeName == "":
                            this.server.sendModMessage(7, "<V>"+this.client.playerName+"<BL> doou <V>"+str(count)+" "+str(typeName)+"<BL> para <V>"+playerName+"<BL>.")
                            for player in this.server.players.values():
                                for client in this.client.room.clients.values():
                                    bg = '<img src="https://i.hizliresim.com/ERDYpA.png">'
                                    txt = '<p align="center"><N>Você recebeu <ROSE>'+str(count)+' <N>'+str(typeName)+'</ROSE><N>.</p>'
                                    txtOK = '<font size="12"><V><a href="event:fecharPop">OK</a></font>'
                                    client.sendAddPopupText(10056, 270, 130, 299, 100, '000000', '000000', 100, bg)
                                    client.sendAddPopupText(10057, 290, 150, 225, 60, '000000', '000000', 100, txt)
                                    client.sendAddPopupText(10058, 390, 190, 30, 60, '000000', '000000', 100, txtOK)
                                if typeName == "queijos":
                                    player.shopCheeses += count
                                elif typeName == "fraises":
                                    player.shopFraises += count
				elif typeName == "bootcamps":
				    player.bootcampCount += count
				elif typeName == "firsts":
				    player.cheeseCount += count
				    player.firstCount += count
				elif typeName == "moedas":
				    player.XDCoins += count
				elif typeName == "fichas":
				    player.XDFichas += count
				elif typeName == "saves":
				    player.shamanSaves += count
                    except: this.client.sendMessage("<BL>ERROR! Use: <ROSE>/give nick tipo quantidade<BL>.")
                else: this.client.sendMessage("<ROSE>• <N>Você não tem privilégio suficiente para utilizar este comando.")

            elif _command == "ungive" or _command == "tirar":
                if this.client.privLevel >= 10:
                    this.requireArgs(3)
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    type = args[1].lower()
                    count = int(args[2]) if args[2].isdigit() else 0
                    type = "queijos" if type.startswith("queijos") else "morangos" if type.startswith("morangos") else "bootcamps" if type.startswith("bc") or type.startswith("bootcamp") else "firsts" if type.startswith("first") else "profile" if type.startswith("perfilqesos") else "saves" if type.startswith("saves") else "hardSaves" if type.startswith("saveshard") else "divineSaves" if type.startswith("savesdivime") else "moedas" if type.startswith("moedas") or type.startswith("monedas") else "fichas" if type.startswith("fichas") else ""
                    yeah = False
                    if count > 0 and not type == "":
                        player = this.server.players.get(playerName)
                        if player != None:
                            this.server.sendStaffMessage(7, "<V>%s</V> tirou <V>%s %s</V> de <V>%s</V>." %(this.client.playerName, count, type, playerName))
                            if type == "queijos":
                                if not count > player.shopCheeses:
                                    player.shopCheeses -= count
                                    yeah = True
                            if type == "morangos":
                                if not count > player.shopFraises:
                                    player.shopFraises -= count
                                    yeah = True
                            if type == "bootcamps":
                                if not count > player.bootcampCount:
                                    player.bootcampCount -= count
                                    yeah = True
                            if type == "firsts":
                                if not count > player.firstCount:
                                    player.cheeseCount -= count
                                    player.firstCount -= count
                                    yeah = True
                            if type == "profile":
                                if not count > player.cheeseCount:
                                    player.cheeseCount -= count
                                    yeah = True
                            if type == "saves":
                                if not count > player.shamanSaves:
                                    player.shamanSaves -= count
                                    yeah = True
                            if type == "hardSaves":
                                if not count > player.hardModeSaves:
                                    player.hardModeSaves -= count
                                    yeah = True
                            if type == "divineSaves":
                                if not count > player.divineModeSaves:
                                    player.divineModeSaves -= count
                                    yeah = True
                            if type == "moedas":
                                if not count > player.XDFichas:
                                    player.XDCoins += count
                                    yeah = True
                            if type == "fichas":
                                if not count > player.XDFichas:
                                    player.XDFichas -= count
                                    yeah = True
                            if yeah:
                                this.client.sendMessage("Foram removidos de você <V>%s %s</V>." %(count, type))
                            else:
                                this.client.sendMessage("Você não pode colocar o valor abaixo do qual o jogador já tem.")
			
	    elif _command == "ch":
                if this.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    client = this.server.players.get(playerName)
                    if client != None and client.roomName == this.client.roomName:
                        this.client.sendMessageLangue("", "$ProchaineChamane", client.playerName)
                        this.client.room.forceNextShaman = client.playerCode
                        this.client.sendClientMessage("O usuário <V>"+playerName+"<BL> será o próximo Shaman.")
                    else: this.client.sendClientMessage("O usuário <V>"+playerName+"<BL> não está online ou não está na mesma sala que você.")
                else: this.client.sendMessage("<ROSE>• <N>Você não tem privilégio suficiente para utilizar este comando.")

            elif _command == "warn":
                if this.client.privLevel >= 7:
                    try:
                        playerName = Utils.parsePlayerName(args[0])
                        message = argsNotSplited.split(" ", 1)[1]

                        if not this.server.checkExistingUser(playerName):
                            this.client.sendClientMessage("Não foi possível encontrar o usuário: <V>"+playerName+"<BL>.")
                        else:
                            rank = "Helper" if this.client.privLevel == 5 else "MapCrew" if this.client.privLevel == 6 else "Moderador" if this.client.privLevel == 7 else "Super Moderador" if this.client.privLevel == 8 else "Coordenador" if this.client.privLevel == 9 else "Administrador" if this.client.privLevel >= 10 else ""
                            client = this.server.players.get(playerName)
                            if client != None:
                                client.sendClientMessage("<ROSE>[<b>ALERTA</b>] O "+str(rank)+" "+this.client.playerName+" lhe enviou um alerta. Motivo: "+str(message))
                                this.client.sendClientMessage("<BL>Seu alerta foi enviado com sucesso para <V>"+playerName+"<BL>.")
                                this.server.sendModMessage(7, "<V>"+this.client.playerName+"<BL> enviou um alerta para"+"<V> "+playerName+"<BL>. Motivo: <V>"+str(message))
                            else: this.client.sendMessage("<ROSE>• <N>Você não tem privilégio suficiente para utilizar este comando.")
                    except: this.client.sendMessage("<BL>ERROR! Use: <ROSE>/warn nick motivo<BL>.")

            elif _command in ["moveplayer", "mjoin"]:
                if this.client.privLevel >= 8:
                    this.requireArgs(2)
                    playerName = Utils.parsePlayerName(args[0])
                    roomName = argsNotSplited.split(" ", 1)[1]
                    rank = "Helper" if this.client.privLevel == 5 else "MapCrew" if this.client.privLevel == 6 else "Moderador" if this.client.privLevel == 7 else "Super Moderador" if this.client.privLevel == 8 else "Coordenador" if this.client.privLevel == 9 else "Administrador" if this.client.privLevel >= 10 else ""
                    client = this.server.players.get(playerName)
                    if client != None:
                        client.enterRoom(roomName)
                        client.sendClientMessage("<ROSE>[<b>ALERTA</b>] O "+str(rank)+" "+this.client.playerName+" moveu você para a sala: "+str(roomName))
                        this.client.sendClientMessage("<BL>Você moveu o jogador <V>"+playerName+"<BL> para a sua sala com sucesso.")
                        this.server.sendModMessage(7, "<V>"+this.client.playerName+"<BL> moveu o jogador"+"<V> "+playerName+"<BL> para a sala: <V>"+str(roomName))
                    else: this.client.sendMessage("<ROSE>• <N>Você não tem privilégio suficiente para utilizar este comando.")

        except Exception as ERROR:
            import time, traceback
            c = open("./errorsCommands.log", "a")
            c.write("\n" + "=" * 60 + "\n- Time: %s\n- Jogador: %s\n- Error comando: \n" %(time.strftime("%d/%m/%Y - %H:%M:%S"), this.client.playerName))
            traceback.print_exc(file=c)
            c.close()
            this.server.sendModMessage(7, "<BL>[<R>ERROR<BL>] O usuário <R>%s achou um erro nos comandos." %(this.client.playerName))

    def sendListServerHelp(this):
        message = "<p align = \"center\"><font size = \"12\"><ROSE>Lista de comandos do TransforVida</font><br></p>"
        message += "\n<J><p align = \"left\">Informações:\n<V>First começa a contar com <J>4<V> ratos na sala.\nBootcamp começa a contar com <J>4 <V>ratos na sala.\nDeathmatch começa a contar com <J>4 <V>ratos na sala.\nConta first em <J>primeiro<V>, <J>segundo <V>e <J>terceiro <V>lugar.\n\n"
            
        if this.client.privLevel >= 1:
            message += "<J>/comandos</J> - <V> Visualizar o Menu com novidades do jogo.\n"
            message += "<J>/play</J> - <V> Ativar a rádio online do jogo.\n"
            message += "<J>/stop</J> - <V> Desativar a rádio online do jogo.\n"
            message += "<J>/senha</J> - <V> Alterar a sua senha atual.\n"
            message += "<J>/email</J> - <V> Definir e-mail para poder mudar sua senha.\n"
            message += "<J>/pontos</J> - <V> Veja quantos pontos de Deathmatch você possui.\n"
            message += "<J>/moedas</J> - <V> Veja quantas moedas você possui atualmente.\n"
            message += "<J>/ping</J> - <V> Conexão do seu PC com o nosso servidor. Quanto menor melhor.\n"
            message += "<J>/title</J> - <V> Seus títulos.\n"
            message += "<J>/standalone</J> - <V> Download do Standalone.\n"
            message += "<J>/perfil [nick]</J> - <V> Visualize o perfil de um jogador.\n"
            message += "<J>/mods</J> - <V> Moderação online.\n"
            message += "<J>/meusmapas</J> - <V> Visualize os seus mapas.\n"
            message += "<J>/title [número]</J> - <V> Mudar o seu título atual.\n"
            message += "<J>/meuip</J> - <V> Visualize o seu IP atual.\n"
            message += "<J>/editeur</J> - <V> Entrar no modo de editor de mapas.\n"
            message += "<J>/totem</J> - <V> Entrar no modo de Totem.\n"
            message += "<J>/sauvertotem</J> - <V> Atualizar o Totem.\n"
            message += "<J>/resettotem</J> - <V> Resetar o Totem.\n"
            message += "<J>/skip</J> - <V> Mudar música.\n"
            message += "<J>/mort</J> - <V> Comando de suicidar-se.\n"
            
        if this.client.privLevel >= 2:
            message += "<J>/ajudavip</J> - <V> Visualize os seus comandos VIP.\n\n"

        if this.client.privLevel >= 3:
            message += "<J>/re</J> - <V> Comando de reviver no mapa.\n"
            message += "<J>/premiums</J> - <V> Visualiza a lista de jogadores Premiums.\n"
            message += "<J>/premium [message]</J> - <V> Mensagem de Global para todos do servidor.\n\n"

        if this.client.privLevel >= 4:
            message += "<J>/ls</J> - <V> Estatísticas das Salas/Jogadores\n"
            message += "<J>/d</J> - <V> FunCorp Chat.\n"
        
        if this.client.privLevel >= 5:
            message += "<J>/hide</J> - <V> Ficar invisível na sala.\n"
            message += "<J>/unhide</J> - <V> Ficar visível na sala.\n"
            message += "<J>/sy? [nome]</J> - <V> Sincronizar um jogador na sala.\n"
            message += "<J>/clearchat</J> - <V> Limpar chat dos jogadores na sala atual.\n"
            message += "<J>/ban [nome]</J> - <V> Banir um jogador.\n"
            message += "<J>/find [nome]</J> - <V> Procurar jogador.\n\n"
            
        if this.client.privLevel >= 6:
            message += "<J>/np</J> - <V> Pular mapa.\n"
            message += "<J>/mapinfo</J> - <V> Informações do Mapa.\n"
            message += "<J>/np [code]</J> - <V> Mudar mapa por código.\n"
            message += "<J>/kick [nome]</J> - <V> Expulsar jogador.\n"
            message += "<J>/lsmaps</J> - <V> Mapas disponíveis.\n\n"

        if this.client.privLevel >= 7:
            message += "<J>/ch [nome]</J> - <V> Escolhe o próximo Shaman.\n"
            message += "<J>/warn [nome]</J> - <V> Envia um alerta a um jogador.\n"
            message += "<J>/log</J> - <V> Log de bans/kicks do servidor.\n"
            message += "<J>/lsc</J> - <V> LSC Room Client.\n"
            message += "<J>/unbanip [nome]</J> - <V> Desbanir IP de algum jogador.\n"
            message += "<J>/unban [nome]</J> - <V> Desbanir um jogador do jogo.\n"
            message += "<J>/mute [nome] [horas]</J> - <V> Bloquear o chat de um jogador.\n"
            message += "<J>/unmute [nome]</J> - <V> Liberar o chat de um jogador.\n"
            message += "<J>/sy [nome]</J> - <V> Sincronizar jogador.\n"
            message += "<J>/clearban [nome]</J> - <V> Deleta histórico de ban um jogador.\n"
            message += "<J>/ip [nome]</J> - <V> Visualiza IP de um jogador.\n"
            message += "<J>/mm</J> - <V> Global Moderátion.\n"
            message += "<J>/log [name]</J> - <V> Log de um jogador.\n"
            message += "<J>/maxplayers [quantidade]</J> - <V>Define quantidade de jogadores em uma sala.\n\n"
            
        if this.client.privLevel >= 8:
            message += "<J>/call</J> - <V> Enviar uma mensagem no cochicho de todos os jogadores.\n"
            message += "<J>/move</J> - <V> Mover todos jogadores de uma sala para outra.\n"
            message += "<J>/moveplayer [nome]</J> - <V> Mover jogador para uma sala diferente.\n"
            
        if this.client.privLevel >= 10:
            message += "<J>/limparlogs</J> - <V> Limpa todo o log de banimento do servidor.\n"
            message += "<J>/unranked [nome]</J> - <V> Remove um jogador do ranking.\n"
            message += "<J>/ranked [nome]</J> - <V> Re-coloca um jogador no ranking.\n"
            message += "<J>/reset [nick]</J> - <V> Zera o perfil de um jogador.\n"
            message += "<J>/changepassword [nick] [senha]</J> - <V> Altera a senha de um jogador.\n"
            message += "<J>/settime [tempo]</J> - <V> Altera o tempo do mapa.\n"
            message += "<J>/clearcache</J> - <V> Limpa cache do servidor.\n"
            message += "<J>/clearipbans</J> - <V> Limpa todos os IPs banidos.\n"
            message += "<J>/clearreports</J> - <V> Limpa todo o histórico de denúncias.\n"
            message += "<J>/updatesql</J> - <V> Salva todos os dados do mice no banco de dados do servidor.\n"
            message += "<J>/reboot</J> - <V> Reinicia o servidor em caso de atualização.\n"
            message += "<J>/shutdown [Nome]</J> - <V> Desliga o servidor em caso de emergência.\n"
            message += "<J>/reviver [Nome]</J> - <V> Revive um jogador.\n"
            message += "<J>/rank [Nome] [cargo]</J> - <V> Dá um cargo a um jogador.\n"
            message += "<J>/setvip [Nome] [dias]</J> - <V> Dá VIP a um jogador por dias.\n"
            message += "<J>/removevip [Nome]</J> - <V> Remove o VIP de um jogador.\n"
            message += "<J>/emailde [Nome]</J> - <V> Visualiza o e-mail de um jogador.\n"
            message += "<J>/teleport</J> - <V> Ativa o Modo de se Teletransportar.\n"
            message += "<J>/speed</J> - <V> Ativa o Modo Speed.\n"
            message += "<J>/fly</J> - <V> Ativa o Modo de Voar.\n"
            message += "<J>/size [nome] [tamanho]</J> - <V> Altera o tamanho do rato.\n"
            message += "<J>/neve</J> - <V> Ativa neve na sala atual para todos jogadores.\n"
            message += "<J>/configs</J> - <V> Configurações de jogo do mice.\n"
            message += "<J>/addtext [blacklist/whitelist] [link]</J> - <V>Adiciona um link/palavra na lista negra do chat.\n"
            message += "<J>/removetext [blacklist/whitelist] [link]</J> - <V>Remove um link/palavra da lista negra do chat.\n"
        return message
