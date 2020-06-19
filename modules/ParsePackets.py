#coding: utf-8
import re, json, random, urllib, traceback, time as _time, base64, hashlib, struct

# Modules
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers

# Library
from collections import deque
from twisted.internet import reactor

class ParsePackets:
    def __init__(this, player, server):
        this.client = player
        this.server = player.server
        this.Cursor = player.Cursor

    def parsePacket(this, packetID, C, CC, packet):
        if not C in [26, 28, 4, 29]:
            if not CC in [2]:  
                this.client.packetSent += 1
                    
        if this.client.packetSent >= this.client.limitPacket:
            #print "[%s] - [%s] Limite de Pacotes - C: %s - CC: %s" %(this.client.roomName, this.client.playerName, C, CC)
            this.client.resultLimitPacket()
        
        elif C == Identifiers.recv.Old_Protocol.C:
            if CC == Identifiers.recv.Old_Protocol.Old_Protocol:
                data = packet.readUTF()
                this.client.parsePackets.parsePacketUTF(data)
                return

        elif C == Identifiers.recv.Sync.C:
            if CC == Identifiers.recv.Sync.Object_Sync:
                if this.client.playerName in ["", " "]:
                    this.client.transport.loseConnection()
                else:
                    roundCode = packet.readInt()
                    if roundCode == this.client.room.lastRoundCode:
                        packet2 = ByteArray()
                        while packet.bytesAvailable():
                            objectID = packet.readShort()
                            objectCode = packet.readShort()
                            if objectCode == -1:
                                packet2.writeShort(objectID)
                                packet2.writeShort(-1)
                            else:
                                try:
                                    posX = packet.readShort()
                                    posY = packet.readShort()
                                    velX = packet.readShort()
                                    velY = packet.readShort()
                                    rotation = packet.readShort()
                                    rotationSpeed = packet.readShort()
                                    ghost = packet.readBoolean()
                                    stationary = packet.readBoolean()
                                    packet2.writeShort(objectID).writeShort(objectCode).writeShort(posX).writeShort(posY).writeShort(velX).writeShort(velY).writeShort(rotation).writeShort(rotationSpeed).writeBoolean(ghost).writeBoolean(stationary).writeBoolean(this.client.room.getAliveCount() > 1)
                                except: return
                        this.client.room.sendAllOthers(this.client, Identifiers.send.Sync, packet2.toByteArray())
                    return

            elif CC == Identifiers.recv.Sync.Mouse_Movement:
                roundCode, droiteEnCours, gaucheEnCours, px, py, vx, vy, jump, jump_img, portal, isAngle = packet.readInt(), packet.readBoolean(), packet.readBoolean(), packet.readUnsignedShort(), packet.readUnsignedShort(), packet.readUnsignedShort(), packet.readUnsignedShort(), packet.readBoolean(), packet.readByte(), packet.readByte(), packet.bytesAvailable(),
                angle = packet.readUnsignedShort() if isAngle else -1
                vel_angle = packet.readUnsignedShort() if isAngle else -1
                loc_1 = packet.readBoolean() if isAngle else False

                if roundCode == this.client.room.lastRoundCode:
                    if droiteEnCours or gaucheEnCours:
                        this.client.isMovingRight = droiteEnCours
                        this.client.isMovingLeft = gaucheEnCours

                        if this.client.isAfk:
                            this.client.isAfk = False

                    this.client.posX = px * 800 / 2700
                    this.client.posY = py * 800 / 2700
                    this.client.velX = vx
                    this.client.velY = vy
                    this.client.isJumping = jump

                    if this.client.room.isDeathmatch:
                        if this.client.room.checkIfOneFewRemaining():
                            if this.client.ClientGotHole == 1 and this.client.room.getPlayerCountUnique() >= this.client.server.needToFirst:
                                this.client.isDead = True
                                this.client.room.canCannon = False
                                this.client.firstCount += 7
                                this.client.cheeseCount += 7
                                this.client.XDCoins += 7
                                this.client.deathCount += 1
                                this.client.deathRoundWinner(this.client.playerName)
                    if droiteEnCours == 1:
                        this.client.mDirection = "1"
                    elif gaucheEnCours == 1:
                        this.client.mDirection = "0"

                    packet2 = ByteArray().writeInt(this.client.playerCode).writeInt(roundCode).writeBoolean(droiteEnCours).writeBoolean(gaucheEnCours).writeUnsignedShort(px).writeUnsignedShort(py).writeUnsignedShort(vx).writeUnsignedShort(vy).writeBoolean(jump).writeByte(jump_img).writeByte(portal)
                    if isAngle:
                        packet2.writeUnsignedShort(angle).writeUnsignedShort(vel_angle).writeBoolean(loc_1)
                    this.client.room.sendAllOthers(this.client, Identifiers.send.Player_Movement, packet2.toByteArray())
                return

            elif CC == Identifiers.recv.Sync.Mort:
                roundCode, loc_1 = packet.readInt(), packet.readByte()
                if roundCode == this.client.room.lastRoundCode:
                    this.client.isDead = True
                    if not this.client.room.noAutoScore: this.client.playerScore += 1
                    this.client.sendPlayerDied()

                    if this.client.room.getPlayerCountUnique() >= this.server.needToFirst:
                        if this.client.room.isSurvivor:
                            for playerCode, client in this.client.room.clients.items():
                                if client.isShaman:
                                    client.survivorDeath += 1
                                    if client.survivorDeath == 4:
                                        id = 2260
                                        if not id in client.playerConsumables:
                                            client.playerConsumables[id] = 1
                                        else:
                                            count = client.playerConsumables[id] + 1
                                            client.playerConsumables[id] = count
                                        client.sendAnimZeldaInventory(4, id, 1)
                                        client.survivorDeath = 0

                    if not this.client.room.currentShamanName == "":
                        player = this.client.room.clients.get(this.client.room.currentShamanName)

                        if player != None and not this.client.room.noShamanSkills:
                            if player.bubblesCount > 0:
                                if this.client.room.getAliveCount() != 1:
                                    player.bubblesCount -= 1
                                    this.client.sendPlaceObject(this.client.room.objectID + 2, 59, this.client.posX, 450, 0, 0, 0, True, True)

                            if player.desintegration:
                                this.client.parseSkill.sendSkillObject(6, this.client.posX, 395, 0)
                    this.client.room.checkChangeMap()
                return

            elif CC == Identifiers.recv.Sync.Player_Position:
                direction = packet.readBoolean()
                this.client.room.sendAll(Identifiers.send.Player_Position, ByteArray().writeInt(this.client.playerCode).writeBoolean(direction).toByteArray())
                return

            elif CC == Identifiers.recv.Sync.Shaman_Position:
                direction = packet.readBoolean()
                this.client.room.sendAll(Identifiers.send.Shaman_Position, ByteArray().writeInt(this.client.playerCode).writeBoolean(direction).toByteArray())
                return

            elif CC == Identifiers.recv.Sync.Crouch:
                crouch = packet.readByte()
                this.client.room.sendAll(Identifiers.send.Crouch, ByteArray().writeInt(this.client.playerCode).writeByte(crouch).writeByte(0).toByteArray())
                return

        elif C == Identifiers.recv.Room.C:
            if CC == Identifiers.recv.Room.Map_26:
                if this.client.room.currentMap == 26:
                    posX, posY, width, height = packet.readShort(), packet.readShort(), packet.readShort(), packet.readShort()
                    bodyDef = {}
                    bodyDef["type"] = 12
                    bodyDef["width"] = width
                    bodyDef["height"] = height
                    this.client.room.addPhysicObject(0, posX, posY, bodyDef)
                return

            elif CC == Identifiers.recv.Room.Shaman_Message:
                type, x, y = packet.readByte(), packet.readShort(), packet.readShort()
                this.client.room.sendAll(Identifiers.send.Shaman_Message, ByteArray().writeByte(type).writeShort(x).writeShort(y).toByteArray())
                return

            elif CC == Identifiers.recv.Room.Convert_Skill:
                objectID = packet.readInt()
                this.client.parseSkill.sendConvertSkill(objectID)
                return

            elif CC == Identifiers.recv.Room.Demolition_Skill:
                objectID = packet.readInt()
                this.client.parseSkill.sendDemolitionSkill(objectID)
                return

            elif CC == Identifiers.recv.Room.Projection_Skill:
                posX, posY, dir = packet.readShort(), packet.readShort(), packet.readShort()
                this.client.parseSkill.sendProjectionSkill(posX, posY, dir)
                return

            elif CC == Identifiers.recv.Room.Enter_Hole:
                holeType, roundCode, monde, distance, holeX, holeY = packet.readByte(), packet.readInt(), packet.readInt(), packet.readShort(), packet.readShort(), packet.readShort()
                if roundCode == this.client.room.lastRoundCode and (this.client.room.currentMap == -1 or monde == this.client.room.currentMap or this.client.room.EMapCode != 0):
                    this.client.playerWin(holeType, distance)
                return

            elif CC == Identifiers.recv.Room.Get_Cheese:
                roundCode, cheeseX, cheeseY, distance = packet.readInt(), packet.readShort(), packet.readShort(), packet.readShort()
                if roundCode == this.client.room.lastRoundCode:
                    this.client.sendGiveCheese(distance)
                return

            elif CC == Identifiers.recv.Room.Place_Object:
                if not this.client.isShaman:
                    return
                if this.client.isShaman:
                    if not this.client.room.isSurvivor:
                        if not this.client.canUseSpawnAll:
                            return
                        this.client.canUseSpawnAll = False
                        this.client.spawnTimer = reactor.callLater(1, setattr, this.client, "canUseSpawnAll", True)

                    roundCode, objectID, code, px, py, angle, vx, vy, dur, origin = packet.readByte(), packet.readInt(), packet.readShort(), packet.readShort(), packet.readShort(), packet.readShort(), packet.readByte(), packet.readByte(), packet.readBoolean(), packet.readBoolean()
                    if this.client.room.isTotemEditor:
                        if this.client.tempTotem[0] < 20:
                            this.client.tempTotem[0] = int(this.client.tempTotem[0]) + 1
                            this.client.sendTotemItemCount(this.client.tempTotem[0])
                            this.client.tempTotem[1] += "#2#" + chr(1).join(map(str, [code, px, py, angle, vx, vy, dur]))
                    else:
                        if code == 44:
                            if not this.client.useTotem:
                                this.client.sendTotem(this.client.totem[1], px, py, this.client.playerCode)
                                this.client.useTotem = True

                        this.client.sendPlaceObject(objectID, code, px, py, angle, vx, vy, dur, False)
                        this.client.parseSkill.placeSkill(objectID, code, px, py, angle)
                return

            elif CC == Identifiers.recv.Room.Ice_Cube:
                playerCode, px, py = packet.readInt(), packet.readShort(), packet.readShort()
                if this.client.isShaman and not this.client.isDead and not this.client.room.isSurvivor and this.client.room.numCompleted > 1:
                    if this.client.iceCount != 0 and playerCode != this.client.playerCode:
                        for client in this.client.room.clients.values():
                            if client.playerCode == playerCode and not client.isShaman:
                                client.isDead = True
                                if not this.client.room.noAutoScore: this.client.playerScore += 1
                                client.sendPlayerDied()
                                this.client.sendPlaceObject(this.client.room.objectID + 2, 54, px, py, 0, 0, 0, True, True)
                                this.client.iceCount -= 1
                                this.client.room.checkChangeMap()
                return

            elif CC == Identifiers.recv.Room.Bridge_Break:
                if this.client.room.currentMap in [6, 10, 110, 116]:
                    bridgeCode = packet.readShort()
                    this.client.room.sendAllOthers(this.client, Identifiers.send.Bridge_Break, ByteArray().writeShort(bridgeCode).toByteArray())
                return

            elif CC == Identifiers.recv.Room.Defilante_Points:
                this.client.defilantePoints += 1
                return

            elif CC == Identifiers.recv.Room.Restorative_Skill:
                objectID, id = packet.readInt(), packet.readInt()
                this.client.parseSkill.sendRestorativeSkill(objectID, id)
                return

            elif CC == Identifiers.recv.Room.Recycling_Skill:
                id = packet.readShort()
                this.client.parseSkill.sendRecyclingSkill(id)
                return

            elif CC == Identifiers.recv.Room.Gravitational_Skill:
                velX, velY = packet.readShort(), packet.readShort()
                this.client.parseSkill.sendGravitationalSkill(0, velX, velY)
                return

            elif CC == Identifiers.recv.Room.Antigravity_Skill:
                objectID = packet.readInt()
                this.client.parseSkill.sendAntigravitySkill(objectID)
                return

            elif CC == Identifiers.recv.Room.Handymouse_Skill:
                handyMouseByte, objectID = packet.readByte(), packet.readInt()
                if this.client.room.lastHandymouse[0] == -1:
                    this.client.room.lastHandymouse = [objectID, handyMouseByte]
                else:
                    this.client.parseSkill.sendHandymouseSkill(handyMouseByte, objectID)
                    this.client.room.sendAll(Identifiers.send.Skill, chr(77) + chr(1))
                    this.client.room.lastHandymouse = [-1, -1]
                return

            elif CC == Identifiers.recv.Room.Enter_Room:
                community, roomName, isSalonAuto = packet.readByte(), packet.readUTF(), packet.readBoolean()
                if this.client.playerName in ["", " "]:
                    this.client.transport.loseConnection()
                else:
                    if isSalonAuto or roomName == "":
                        this.client.startBulle(this.server.recommendRoom(this.client.langue))
                    elif not roomName == this.client.roomName or not this.client.room.isEditor or not len(roomName) > 64 or not this.client.roomName == "%s-%s" %(this.client.langue, roomName):
                        if this.client.privLevel < 8: roomName = this.server.checkRoom(roomName, this.client.langue)
                        roomEnter = this.server.rooms.get(roomName if roomName.startswith("*") else ("%s-%s" %(this.client.langue, roomName)))
                        if roomEnter == None or this.client.privLevel >= 7:
                            this.client.startBulle(roomName)
                        else:
                            if not roomEnter.roomPassword == "":
                                this.client.sendPacket(Identifiers.send.Room_Password, ByteArray().writeUTF(roomName).toByteArray())
                            else: this.client.startBulle(roomName)
                    return

            elif CC == Identifiers.recv.Room.Room_Password:
                roomPass, roomName = packet.readUTF(), packet.readUTF()
                roomEnter = this.server.rooms.get(roomName if roomName.startswith("*") else ("%s-%s" %(this.client.langue, roomName)))
                if roomEnter == None or this.client.privLevel >= 7:
                    this.client.startBulle(roomName)
                else:
                    if not roomEnter.roomPassword == roomPass:
                        this.client.sendPacket(Identifiers.send.Room_Password, ByteArray().writeUTF(roomName).toByteArray())
                    else: this.client.startBulle(roomName)
                return
            
        elif C == Identifiers.recv.Chat.C:
            if CC == Identifiers.recv.Chat.Chat_Message:
                    #packet = this.descriptPacket(packetID, packet)
                    message = packet.readUTF().replace("&amp;#", "&#").replace("<", "&lt;")
                    message = message.replace("|", "").replace("  ", "").replace("&nbsp;", "").replace("\n", "").replace("<br>", "").replace("<br/>", "").replace("</br>", "")
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
                    if this.client.isGuest:
                        this.client.sendLangueMessage("", "$Créer_Compte_Parler")
                    elif not message == "" and len(message) < 256:
                        sucess = False
                        isSuspect = this.client.privLevel < 6 and this.server.checkMessage(this.client, message)
                        this.client.lastMessage = message
                        if this.client.privLevel >= 10 and not this.client.isMute:
                            for room in this.client.server.rooms.values():
                               if room.name == this.client.room.name:
                                    for playerCode, client in room.clients.items():
                                        client.sendMessage('<ROSE>[%s] <N>%s' % (this.client.playerName, message))
                        if this.client.privLevel == 9 and not this.client.modMute:
                            for room in this.client.server.rooms.values():
                               if room.name == this.client.room.name:
                                    for playerCode, client in room.clients.items():
                                        client.sendMessage('<VI>[%s] <N>%s' % (this.client.playerName, message))
                        if this.client.privLevel == 8 and not this.client.isMute:
                               for room in this.client.server.rooms.values():
                                   if room.name == this.client.room.name:
                                       for playerCode, client in room.clients.items():
                                           client.sendMessage('<J>[%s] <N>%s' % (this.client.playerName, message))
                        if this.client.privLevel == 7 and not this.client.isMute:
                               for room in this.client.server.rooms.values():
                                   if room.name == this.client.room.name:
                                       for playerCode, client in room.clients.items():
                                           client.sendMessage('<N>[%s] <N>%s' % (this.client.playerName, message))
                        if this.client.privLevel == 6 and not this.client.isMute:
                               for room in this.client.server.rooms.values():
                                   if room.name == this.client.room.name:
                                       for playerCode, client in room.clients.items():
                                           client.sendMessage('<font color="#FFCC99">[%s]</font> <N>%s' % (this.client.playerName, message))
                        if this.client.privLevel == 5 and not this.client.isMute:
                               for room in this.client.server.rooms.values():
                                   if room.name == this.client.room.name:
                                       for playerCode, client in room.clients.items():
                                           client.sendMessage('<font color="#3366FF">[%s]</font> <N>%s' % (this.client.playerName, message))
                        if this.client.privLevel == 4 and not this.client.isMute:
                               for room in this.client.server.rooms.values():
                                   if room.name == this.client.room.name:
                                       for playerCode, client in room.clients.items():
                                           client.sendMessage('<font color="#00FA9A">[%s]</font> <N>%s' % (this.client.playerName, message))
                        if this.client.privLevel == 3 and not this.client.isMute:
                               for room in this.client.server.rooms.values():
                                   if room.name == this.client.room.name:
                                       for playerCode, client in room.clients.items():
                                           client.sendMessage('<font color="#F9F9F9">[%s]</font> <N>%s' % (this.client.playerName, message))
                        if this.client.privLevel == 2:
                            if _time.time() - this.client.CMDTime > 1:
                                this.client.CMDTime = _time.time()
                                if this.client.isMute:
                                    muteInfo = this.server.getModMuteInfo(this.client.playerName)
                                    timeCalc = Utils.getHoursDiff(muteInfo[1])
                                    if timeCalc <= 0:
                                        this.client.isMute = False
                                        this.server.removeModMute(this.client.playerName)
                                        this.client.room.sendAllChat(this.client.playerCode, this.client.playerName, message, this.client.langueID, this.server.checkMessage(this.client, message))
                                    else:
                                        this.client.sendModMute(this.client.playerName, timeCalc, muteInfo[0], True)
                                        return
                                else:
                                    for room in this.client.server.rooms.values():
                                       if room.name == this.client.room.name:
                                           for playerCode, client in room.clients.items():
                                               client.sendMessage('<VP>[VIP]<V>[%s] <N>%s' % (this.client.playerName, message)) 
                        if this.client.privLevel == 1:
                            if _time.time() - this.client.CMDTime > 1.2:
                                this.client.CMDTime = _time.time()
                                if this.client.isMute:
                                    muteInfo = this.server.getModMuteInfo(this.client.playerName)
                                    timeCalc = Utils.getHoursDiff(muteInfo[1])
                                    if timeCalc <= 0:
                                        this.client.isMute = False
                                        this.server.removeModMute(this.client.playerName)
                                        this.client.room.sendAllChat(this.client.playerCode, this.client.playerName if this.client.mouseName == "" else this.client.mouseName, message, this.client.langueID, isSuspect)
                                    else:
                                        this.client.sendModMute(this.client.playerName, timeCalc, muteInfo[0], True)
                                        return
                                else: this.client.room.sendAllChat(this.client.playerCode, this.client.playerName, message, this.client.langueID, this.server.checkMessage(this.client, message))
                        if not this.server.chatMessages.has_key(this.client.playerName):
                             messages = deque([], 60)
                             messages.append([_time.strftime("%Y/%m/%d %H:%M:%S"), message])
                             this.server.chatMessages[this.client.playerName] = messages
                        else: this.server.chatMessages[this.client.playerName].append([_time.strftime("%Y/%m/%d %H:%M:%S"), message])
                    return

            elif CC == Identifiers.recv.Chat.Staff_Chat:
                type, message = packet.readByte(), packet.readUTF()
                if ((type == 0 and this.client.privLevel >= 7) or (type == 1 and this.client.privLevel >= 9) or ((type == 2 or type == 5) and this.client.privLevel >= 5) or ((type == 3 or type == 4) and this.client.privLevel >= 7) or ((type == 6 or type == 7) and this.client.privLevel >= 6) or (type == 8 and this.client.privLevel >= 3) or (type == 9 and this.client.privLevel >= 4)):
                    this.server.sendStaffChat(type, this.client.langue, this.client.playerName, message, this.client)
                return

            elif CC == Identifiers.recv.Chat.Commands:
                #packet = this.descriptPacket(packetID, packet)
                command = packet.readUTF()
                try:
                    if _time.time() - this.client.CMDTime > 2:
                        this.client.parseCommands.parseCommand(command)
                        this.client.CMDTime = _time.time()
                    else: this.client.sendMessage("Por favor, tente novamente mais tarde.")
                except Exception as e:
                    with open("./MErros.log", "a") as f:
                        traceback.print_exc(file = f)
                        f.write("\n")
                return

        elif C == Identifiers.recv.Player.C:
            if CC == Identifiers.recv.Player.Emote:
                emoteID, playerCode = packet.readByte(), packet.readInt()
                flag = packet.readUTF() if emoteID == 10 else ""
                this.client.sendPlayerEmote(emoteID, flag, True, False)
                if playerCode != -1:
                    if emoteID == 14:
                        this.client.sendPlayerEmote(14, flag, False, False)
                        this.client.sendPlayerEmote(15, flag, False, False)
                        client = filter(lambda p: p.playerCode == playerCode, this.server.players.values())[0]
                        if client != None:
                            client.sendPlayerEmote(14, flag, False, False)
                            client.sendPlayerEmote(15, flag, False, False)

                    elif emoteID == 18:
                        this.client.sendPlayerEmote(18, flag, False, False)
                        this.client.sendPlayerEmote(19, flag, False, False)
                        client = filter(lambda p: p.playerCode == playerCode, this.server.players.values())[0]
                        if client != None:
                            client.sendPlayerEmote(17, flag, False, False)
                            client.sendPlayerEmote(19, flag, False, False)

                    elif emoteID == 22:
                        this.client.sendPlayerEmote(22, flag, False, False)
                        this.client.sendPlayerEmote(23, flag, False, False)
                        client = filter(lambda p: p.playerCode == playerCode, this.server.players.values())[0]
                        if client != None:
                            client.sendPlayerEmote(22, flag, False, False)
                            client.sendPlayerEmote(23, flag, False, False)

                    elif emoteID == 26:
                        this.client.sendPlayerEmote(26, flag, False, False)
                        this.client.sendPlayerEmote(27, flag, False, False)
                        client = filter(lambda p: p.playerCode == playerCode, this.server.players.values())[0]
                        if client != None:
                            client.sendPlayerEmote(26, flag, False, False)
                            client.sendPlayerEmote(27, flag, False, False)
                            this.client.room.sendAll(Identifiers.send.Joquempo, ByteArray().writeInt(this.client.playerCode).writeByte(random.randint(0, 2)).writeInt(client.playerCode).writeByte(random.randint(0, 2)).toByteArray())

                if this.client.isShaman:
                    this.client.parseSkill.parseEmoteSkill(emoteID)
                return
                    
            elif CC == Identifiers.recv.Player.Langue:
                this.client.langueID = packet.readByte()
                langue = Utils.getTFMLangues(this.client.langueID)
                this.client.langue = langue
                return

            elif CC == Identifiers.recv.Player.Emotions:
                emotion = packet.readByte()
                this.client.sendEmotion(emotion)
                return

            elif CC == Identifiers.recv.Player.Shaman_Fly:
                fly = packet.readBoolean()
                this.client.parseSkill.sendShamanFly(fly)
                return

            elif CC == Identifiers.recv.Player.Shop_List:
                this.client.parseShop.sendShopList()
                return

            elif CC == Identifiers.recv.Player.Buy_Skill:
                skill = packet.readByte()
                this.client.parseSkill.buySkill(skill)
                return

            elif CC == Identifiers.recv.Player.Redistribute:
                this.client.parseSkill.redistributeSkills()
                return
				
	    elif CC == Identifiers.recv.Player.Report:
                playerName, type, comments = packet.readUTF(), packet.readByte(), packet.readUTF()
                this.client.modoPwet.makeReport(playerName, type, comments)
                return

            elif CC == Identifiers.recv.Player.Ping:
                if (_time.time() - this.client.PInfo[1]) >= 5:
                    this.client.PInfo[1] = _time.time()
                    this.client.sendPacket(Identifiers.send.Ping, this.client.PInfo[0])
                    this.client.PInfo[0] += 1
                    if this.client.PInfo[0] == 31:
                        this.client.PInfo[0] = 0
                return
            
            elif CC == Identifiers.recv.Player.Meep:
                posX, posY = packet.readShort(), packet.readShort()
                this.client.room.sendAll(Identifiers.send.Meep_IMG, ByteArray().writeInt(this.client.playerCode).toByteArray())
                this.client.room.sendAll(Identifiers.send.Meep, ByteArray().writeInt(this.client.playerCode).writeShort(posX).writeShort(posY).writeInt(10 if this.client.isShaman else 5).toByteArray())
                return
            
            elif CC == Identifiers.recv.Player.Bolos:
                sla, sla2, id, type = packet.readByte(), packet.readByte(), packet.readByte(), packet.readByte()
                imageID = (38 if id == 1 else 39 if id == 2 else 40 if id == 3 else 41 if id == 4 else 42 if id == 5 else 43)
                p = ByteArray()
                p.writeByte(24)
                p.writeByte(1)
                p.writeByte(2)
                p.writeUTF(str(this.client.playerCode))
                p.writeUTF(str(id))
                this.client.room.sendAll([16, 10], p.toByteArray())
                this.client.room.sendAll([100, 101], ByteArray().writeByte(2).writeInt(this.client.playerCode).writeUTF("x_transformice/x_aventure/x_recoltables/x_%s.png" % (38 if id == 1 else 39 if id == 2 else 40 if id == 3 else 41 if id == 4 else 42 if id == 5 else 43)).writeInt(-1900574).writeByte(0).writeShort(100).writeShort(0).toByteArray())
                this.client.sendPacket([100, 101], "\x01\x00")
                this.client.hasArtefact = True
                this.client.activeArtefact = 1
                this.client.artefactID = imageID

            elif CC == Identifiers.recv.Player.Calendario:
                 pass
##                playerName = packet.readUTF()
##                p = ByteArray()
##                player = this.server.players.get(playerName)
##                p.writeUTF(playerName)
##                p.writeUTF(player.playerLook)
##                count = 0
##                for c in player.aventurePoints.values():
##                    count += c
##                p.writeInt(count)
##                p.writeShort(len(player.titleList))
##                p.writeShort(len(player.shopBadges))
##                p.writeShort(len(this.server.calendarioSystem.keys()))
##                for aventure in this.server.calendarioSystem.keys()[::-1]:
##                    p.writeShort(9)
##                    p.writeByte(1)
##                    p.writeShort(aventure)
##                    p.writeInt(this.server.calendarioSystem[aventure][0])
##                    p.writeShort(this.client.aventurePoints[aventure] if aventure in this.client.aventurePoints.keys() else 0)
##                    p.writeByte(1 if aventure < this.server.adventureID else 0)
##                    p.writeByte(len(this.server.calendarioSystem[aventure][1:]))
##                    for item in this.server.calendarioSystem[aventure][1:]:
##                        itens = item.split(":")
##                        p.writeByte(itens[0])
##                        p.writeByte(itens[1])
##                        if int(itens[1]) == 0:
##                            p.writeShort(itens[2])
##                        else:
##                            p.writeUTF(itens[2])
##                        p.writeShort(itens[3])
##                        splitedItem = itens[2].split("|")[0]
##                        p.writeByte(this.server.getPointsColor(playerName, aventure, splitedItem, itens[0], itens[4]))
##                        if int(itens[0]) != 0:
##                            p.writeByte(1)
##                        if int(itens[0]) == 0:
##                            p.writeByte(2)
##                            p.writeByte(itens[4])
##                        else:
##                            p.writeShort(this.server.getAventureCounts(playerName, aventure, splitedItem, itens[0]))#itens q vc tem
##                            p.writeShort(itens[4])
##                    p.writeByte(len(this.server.calendarioCount[aventure]))
##                    for item in this.server.calendarioCount[aventure]:
##                        itens = item.split(":")
##                        p.writeShort(itens[0])
##                        p.writeShort(itens[1])
##                        p.writeShort(this.server.getAventureItems(playerName, aventure, int(itens[0]), int(itens[1])))
##                this.client.sendPacket([8, 70], p.toByteArray())
##                return

            elif CC == Identifiers.recv.Player.Vampire:
                this.client.sendVampireMode(True)
                return

        elif C == Identifiers.recv.Buy_Fraises.C:
            if CC == Identifiers.recv.Buy_Fraises.Buy_Fraises:
                return

        elif C == Identifiers.recv.Tribe.C:
            if CC == Identifiers.recv.Tribe.Tribe_House:
                if not this.client.tribeName == "":
                    this.client.startBulle("*\x03%s" %(this.client.tribeName))
                return

            elif CC == Identifiers.recv.Tribe.Election_Vote:
                name = packet.readUTF()
                if this.client.cheeseCount >= 10:
                    election = this.server.election
                    #self.Database.execute('SELECT votesusers FROM election WHERE name = ?', [name])
                    if this.client.votemayor == 0 and election == 0:
                            this.client.votemayor = 1
                            this.Cursor.execute('SELECT votes FROM election WHERE name = ? and rank = ?', [name, 0])
                            votes = this.Cursor.fetchone()[0]+1
                            this.Cursor.execute('UPDATE election SET votes = ? WHERE name = ? and rank = ?', [votes, name, 0])
                            this.client.sendMayor()
                    else:
                            this.client.votepresidente = 1
                            this.Cursor.execute('SELECT votes FROM election WHERE name = ? and rank = ?', [name, 1])
                            votes = this.Cursor.fetchone()[0]+1
                            this.Cursor.execute('UPDATE election SET votes = ? WHERE name = ? and rank = ?', [votes, name, 1])
                            this.client.sendPresidente()
                else:
                        this.client.sendMessage("<ROSE>Voce precisa ter <CH>10 queijos <ROSE>para votar em alguem. Atualmente voce tem: <CH>" +str(this.client.cheeseCount), True)
                return
            elif CC == Identifiers.recv.Tribe.Election_Candidatar:
                    text = packet.readUTF()
                    if this.client.candidatar == 0:
                            this.client.candidatar = 1
                            fur = this.client.playerLook.split(";")[0]
                            this.Cursor.execute('INSERT INTO election (name, fur, text1, text2, votes, rank, mayor, presidente) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [this.client.playerName, fur, text, "", 0, 0, 0, 0])
                            this.client.sendMayor()
                    return
            elif CC == Identifiers.recv.Tribe.Election_Change_Text:
                    typee, text = packet.readByte(), packet.readUTF() 
                    if typee == 0 or typee == 2:
                            this.Cursor.execute('UPDATE election SET text1 = ? WHERE name = ?', [text, this.client.playerName])
                            this.client.sendMayor()
                    else:
                            this.Cursor.execute('UPDATE election SET text2 = ? WHERE name = ?', [text, this.client.playerName])
                            this.client.sendMayor()
                    return
            elif CC == Identifiers.recv.Tribe.Election_Delete:
                    name = packet.readUTF()
                    this.Cursor.execute('DELETE from election WHERE name = ?', [name])
                    this.client.sendMayor()
                    return
            elif CC == Identifiers.recv.Tribe.Election_Back:
                    this.client.sendMayor()
                    return
            elif CC == Identifiers.recv.Tribe.Election_Viewfurs:
                    fur = packet.readInt()
                    p = ByteArray()
                    furs = []
                    for x in this.server.shopList:
                        z = x.split(",")
                        if z[0] == '22':
                            furs.append(int(z[1]))
                    furs.append(1)
                    p.writeShort(len(furs))
                    for x in furs:
                        if x == 1:
                            p.writeInt(-9209983)
                        else:
                            p.writeInt(x)
                    if not fur in furs:
                        fur = 1
                    count = 0
                    for furzinha in furs:
                        if furzinha == fur:
                            break
                        else:
                            count+=1
                    p.writeByte(count)
                    this.Cursor.execute('SELECT * FROM election WHERE fur = ? AND rank = ?', [fur, 0])
                    rrfs = this.Cursor.fetchall()
                    p.writeShort(len(rrfs))
                    if len(rrfs) == 0:
                        pass
                    else:
                        for rrf in rrfs:
                            name = rrf[0]
                            text1 = rrf[2]
                            text2 = rrf[3]
                            votes = rrf[4]
                            look = this.client.getLookUser(name)
                            furlook = look.split(";")[0]
                            p.writeByte(1)
                            p.writeUTF(name)
                            p.writeByte(1)
                            p.writeInt(furlook)
                            p.writeInt(votes)
                            p.writeByte(0)
                            p.writeUTF(look)
                            p.writeUTF(text1)
                            p.writeUTF(text2)
                                
                    this.client.sendPacket([100, 81], p.toByteArray())
                    return

            elif CC == Identifiers.recv.Tribe.Bot_Bolo:
                pass
                return

        elif C == Identifiers.recv.Shop.C:
            if CC == Identifiers.recv.Shop.Equip_Clothe:
                this.client.parseShop.equipClothe(packet)
                return

            elif CC == Identifiers.recv.Shop.Save_Clothe:
                this.client.parseShop.saveClothe(packet)
                return
            
            elif CC == Identifiers.recv.Shop.Info:
                this.client.parseShop.sendShopInfo()
                return

            elif CC == Identifiers.recv.Shop.Equip_Item:
                this.client.parseShop.equipItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Item:
                this.client.parseShop.buyItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Custom:
                this.client.parseShop.customItemBuy(packet)
                return

            elif CC == Identifiers.recv.Shop.Custom_Item:
                this.client.parseShop.customItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Clothe:
                this.client.parseShop.buyClothe(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Visu_Done:
                p = ByteArray(packet.toByteArray())
                visuID = p.readShort()
                lookBuy = p.readUTF()
                look = this.server.newVisuList[visuID].split(";")
                look[0] = int(look[0])
                count = 0
                if this.client.shopFraises >= this.client.priceDoneVisu:
                    for visual in look[1].split(","):
                        if not visual == "0":
                            item, customID = visual.split("_", 1) if "_" in visual else [visual, ""]
                            item = int(item)
                            itemID = this.client.getFullItemID(count, item)
                            itemInfo = this.client.getItemInfo(count, item)
                            if len(this.client.shopItems) == 1:
                                if not this.client.parseShop.checkInShop(itemID):
                                    this.client.shopItems += str(itemID)+"_" if this.client.shopItems == "" else "," + str(itemID)+"_"
                                    if not itemID in this.client.custom:
                                        this.client.custom.append(itemID)
                                    else:
                                        if not str(itemID) in this.client.custom:
                                            this.client.custom.append(str(itemID))
                            else:
                                if not this.client.parseShop.checkInShop(str(itemID)):
                                    this.client.shopItems += str(itemID)+"_" if this.client.shopItems == "" else "," + str(itemID)+"_"
                                    if not itemID in this.client.custom:
                                        this.client.custom.append(itemID)
                                    else:
                                        if not str(itemID) in this.client.custom:
                                            this.client.custom.append(str(itemID))
                        count += 1
                        
                    this.client.clothes.append("%02d/%s/%s/%s" %(len(this.client.clothes), lookBuy, "78583a", "fade55" if this.client.shamanSaves >= 1000 else "95d9d6"))
                    furID = this.client.getFullItemID(22, look[0])
                    this.client.shopItems += str(furID) if this.client.shopItems == "" else "," + str(furID)
                    this.client.shopFraises -= this.client.priceDoneVisu
                    this.client.visuDone.append(lookBuy)
                else:
                    this.sendMessage("<Você não tem morangos suficientes.")
                this.client.parseShop.sendShopList(False)

            elif CC == Identifiers.recv.Shop.Buy_Shaman_Item:
                this.client.parseShop.buyShamanItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Equip_Shaman_Item:
                this.client.parseShop.equipShamanItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Shaman_Custom:
                this.client.parseShop.customShamanItemBuy(packet)
                return

            elif CC == Identifiers.recv.Shop.Custom_Shaman_Item:
                this.client.parseShop.customShamanItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Send_Gift:
                this.client.parseShop.sendGift(packet)
                return

            elif CC == Identifiers.recv.Shop.Gift_Result:
                this.client.parseShop.giftResult(packet)
                return
				
	elif C == Identifiers.recv.Modopwet.C:
            if CC == Identifiers.recv.Modopwet.Modopwet:
                if this.client.privLevel >= 7:
                    isOpen = packet.readBoolean()
                    this.client.isModoPwet = isOpen
                    if isOpen:
                        this.client.modoPwet.openModoPwet()
                return

            elif CC == Identifiers.recv.Modopwet.Delete_Report:
                if this.client.privLevel >= 7:
                    playerName, closeType = packet.readUTF(), packet.readByte()
                    this.server.reports[playerName]["status"] = "deleted"
                    this.server.reports[playerName]["deletedby"] = this.client.playerName
                    this.client.modoPwet.openModoPwet()
                return

            elif CC == Identifiers.recv.Modopwet.Watch:
                if this.client.privLevel >= 7:
                    playerName = packet.readUTF()
                    if not this.client.playerName == playerName:
                        roomName = this.server.players[playerName].roomName if this.server.players.has_key(playerName) else ""
                        if not roomName == "" and not roomName == this.client.roomName and not "[Editeur]" in roomName and not "[Totem]" in roomName:
                            this.client.startBulle(roomName)
                return

            elif CC == Identifiers.recv.Modopwet.Ban_Hack:
                if this.client.privLevel >= 7:
                    playerName, iban = packet.readUTF(), packet.readBoolean()
                    if this.server.banPlayer(playerName, 360, "Hack (last warning before account deletion)", this.client.playerName, iban):
                        this.server.sendStaffMessage(5, "<V>%s<BL> baniu <V>%s<BL> por <V>360 <BL>horas. Motivo: <V>Hack (last warning before account deletion)<BL>." %(this.client.playerName, playerName))
                    this.client.modoPwet.openModoPwet()
                return

            elif CC == Identifiers.recv.Modopwet.Change_Langue:
                if this.client.privLevel >= 7:
                    langue = packet.readUTF()
                    this.client.modoPwetLangue = langue.upper()
                    this.client.modoPwet.openModoPwet()
                return
                
            elif CC == Identifiers.recv.Modopwet.Chat_Log:
                if this.client.privLevel >= 7:
                    playerName = packet.readUTF()
                    this.client.modoPwet.openChatLog(playerName)
                return

        elif C == Identifiers.recv.Login.C:
            if CC == Identifiers.recv.Login.Create_Account:
#                packet = this.descriptPacket(packetID, packet)
                playerName, password, captcha, url = Utils.parsePlayerName(packet.readUTF()), packet.readUTF(), packet.readUTF(), packet.readUTF()
                
                if this.client.checkTimeAccount():
                    createTime = _time.time() - this.client.createTime
                    if createTime < 5.2:
                        this.server.sendModMessage(7, "[<V>ANTI-BOT</V>][<J>"+this.client.ipAddress+"</J>] Jogador suspeito de criação de conta muito rápido.")
                        this.client.transport.loseConnection()
                        return
                    canLogin = False
                    for urlCheck in this.server.serverURL:
                        if url.startswith(urlCheck):
                            canLogin = True
                            break
                    if not canLogin:
                        this.server.sendModMessage(7, "[<V>URL</V>][<J>%s</J>][<V>%s</V>][<R>%s</R>] Invalid login url." %(this.client.ipAddress, playerName, url))
                        this.client.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Acesse pelo site: %s" %(this.server.serverURL[0])])
                        this.client.transport.loseConnection()
                        return
                    if this.server.checkExistingUser(playerName):
                        this.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(3).writeUTF(playerName + str(random.randint(0, 50))).toByteArray())
                        this.client.wrongLoginAttempts += 1
                    elif not re.match("^(?=^(?:(?!.*_$).)*$)(?=^(?:(?!_{2,}).)*$)[A-Za-z][A-Za-z0-9_]{2,11}$", playerName):
                        this.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(4).writeUTF(playerName).toByteArray())
                    elif not this.client.currentCaptcha == captcha:
                        this.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(4).writeUTF(playerName).toByteArray())
                        this.client.wrongLoginAttempts += 1
                    elif this.client.wrongLoginAttempts >= 15:
                        this.server.sendModMessage(7, "[<V>ANTI-BOT</V>][<J>%s</J>][<V>%s</V>] Kick - Tentativa de Força Bruta." %(this.client.ipAddress, playerName))
                        this.client.sendPlayerBan(0, "Tentativa de Força Bruta.", True)
                        this.client.sendPacket([26, 3], [""])
                    elif playerName == "" or password == "" or playerName == " ":
                        this.client.transport.loseConnection()
                    elif captcha in ["", " "]:
                        this.client.transport.loseConnection()
                        this.server.sendModMessage(7, "[<V>ANTI-BOT</V>][<J>"+this.client.ipAddress+"</J>] Tentativa de cadastrar-se sem o captcha.")
                    else:
                        this.client.sendAccountTime()
                        this.server.lastPlayerID += 1
                        this.Cursor.execute("insert into users values (?, ?, 1, 0, 0, 0, 0, 0, '', '', '1;0,0,0,0,0,0,0,0,0,0', ?, '', '', '', '', 0, '', '', '78583a', 0, '', ?, ?, 0, '', 0, '', 0, '', 0, ?, 0, '', '', 3, 0, 0, 0, '', 0, '0,0,0,0', '0,0,0,0', '23:10', 0, '', 0, '', '95d9d6', '0,0,0,0,0,0,0,0,0,0', 1, 0, 0, 0, 150, 0, 0, '0', '', '', '', 0, 1484114948, 0, '', '24:0', 0, '2,8,0,0,0,189,133,0,0', 0, 0, '', '0#0#0#0#0#0', 0)", [playerName, this.server.lastPlayerID, this.server.initialCheeses, this.server.initialFraises, Utils.getTime(), password])
                        this.client.loginPlayer(playerName, password, "1")
                        this.client.sendNewConsumable(23, 10)
                        this.server.sendModMessage(7, "[<J>%s</J>] <ROSE>O usuário <J>%s</J> <ROSE>registrou-se no Tsuna." %(this.client.ipAddress, playerName))
                    return
                else: this.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(5).writeUTF(playerName).toByteArray())

            elif CC == Identifiers.recv.Login.Login:
#                packet = this.descriptPacket(packetID, packet)
                playerName, password, url, startRoom = Utils.parsePlayerName(packet.readUTF()), packet.readUTF(), packet.readUTF(), packet.readUTF()
                loginTime = _time.time() - this.client.loginTime             
                if loginTime < 2 and loginTime > 1:
                    this.client.sendPlayerBan(0, "Você está entrando muito rápido! Logue-se novamente.", True)
                    this.server.sendModMessage(7, "[<V>ANTI-BOT</V>][<J>%s</J>][<V>%s</V>] Jogador suspeito de criação de conta muito rápido." %(this.client.ipAddress, this.client.playerName))
                    this.client.transport.loseConnection()
                    return
                elif not len(this.client.playerName) == 0:
                    this.server.sendModMessage(7, "[<V>ANTI-BOT</V>][<J>%s</J>][<V>%s</V>] Criação de múltiplas contas." %(this.client.ipAddress, this.client.playerName))
                    this.client.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Criação de múltiplas contas."])
                    this.client.transport.loseConnection()
                    return
                elif not re.match("^(|(\\+|)(?=^(?:(?!.*_$).)*$)(?=^(?:(?!_{2,}).)*$)[A-Za-z][A-Za-z0-9_]{0,25})$", playerName) or (len(playerName) >= 1 and "+" in playerName[1:]):
                    this.server.sendModMessage(7, "[<V>ANTI-BOT</V>][<J>%s</J>][<V>%s</V>] Nome inválido detectado." %(this.client.ipAddress, playerName))
                    this.client.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Nome inválido detectado."])
                    this.client.transport.loseConnection()
                    return
                elif playerName in [" "]:
                    this.client.transport.loseConnection()
                    return
                elif this.client.wrongLoginAttempts >= 15:
                    this.server.sendModMessage(7, "[<V>ANTI-BOT</V>][<J>%s</J>][<V>%s</V>] Kick - Tentativa de Força Bruta." %(this.client.ipAddress, playerName))
                    this.client.sendPlayerBan(0, "Tentativa de Força Bruta.", True)
                    this.client.sendPacket([26, 3], [""])
                elif playerName == "" or password == "" or playerName == " ":
                    reactor.callLater(1, lambda: this.client.sendPacket(Identifiers.send.Login_Result, 2))
                    this.client.wrongLoginAttempts += 1
                for urlCheck in this.server.serverURL:
                    if url.startswith(urlCheck):
                        canLogin = True
                        break
                if not canLogin:
                    this.server.sendModMessage(7, "[<V>URL</V>][<J>%s</J>][<V>%s</V>][<R>%s</R>] Invalid login url." %(this.client.ipAddress, playerName, url))
                    this.client.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Acesse pelo site: %s" %(this.server.serverURL[0])])
                    this.client.transport.loseConnection()
                else: this.client.loginPlayer(playerName, password, startRoom)

            elif CC == Identifiers.recv.Login.Player_FPS:
                return

            elif CC == Identifiers.recv.Login.Captcha:
                if _time.time() - this.client.CAPTime > 2:
                    this.client.currentCaptcha, px, ly, lines = this.server.buildCaptchaCode()
                    packet = ByteArray().writeShort(px).writeShort(ly).writeShort((px * ly))
                    for line in lines:
                        packet.writeBytes("\x00" * 4)
                        for value in line.split(","):
                            packet.writeUnsignedByte(value).writeBytes("\x00" * 3)
                        packet.writeBytes("\x00" * 4)
                    packet.writeBytes("\x00" * (((px * ly) - (packet.getLength() - 6) / 4) * 4))
                    this.client.sendPacket(Identifiers.send.Captcha, packet.toByteArray())
                    this.client.CAPTime = _time.time()
                return

            elif CC == Identifiers.recv.Login.Dummy:
                if this.client.awakeTimer.getTime() - _time.time() < 110.0:
                    this.client.awakeTimer.reset(120)
                return

            elif CC == Identifiers.recv.Login.Player_Info:
                return

            elif CC == Identifiers.recv.Login.Player_Info2:
                return

            elif CC == Identifiers.recv.Login.Temps_Client:
                return

            elif CC == Identifiers.recv.Login.Rooms_List:
                mode = packet.readByte()
                this.client.lastGameMode = mode
                this.client.sendGameMode(mode)
                return

            elif CC == Identifiers.recv.Login.Undefined:
                return

        elif C == Identifiers.recv.Transformation.C:
            if CC == Identifiers.recv.Transformation.Transformation_Object:
                objectID = packet.readShort()
                if not this.client.isDead and this.client.room.currentMap in range(200, 211):
                    this.client.room.sendAll(Identifiers.send.Transformation, ByteArray().writeInt(this.client.playerCode).writeShort(objectID).toByteArray())
                return

        elif C == Identifiers.recv.Informations.C:
            if CC == Identifiers.recv.Informations.Game_Log:
                errorC, errorCC, oldC, oldCC, error = packet.readByte(), packet.readByte(), packet.readUnsignedByte(), packet.readUnsignedByte(), packet.readUTF()
                if this.server.isDebug:
                    if errorC == 1 and errorCC == 1:
                        print "[%s] [%s][OLD] GameLog Error - C: %s CC: %s error: %s" %(_time.strftime("%H:%M:%S"), this.client.playerName, oldC, oldCC, error)
                    elif errorC == 60 and errorCC == 1:
                        if oldC == Identifiers.tribulle.send.ET_SignaleDepartMembre or oldC == Identifiers.tribulle.send.ET_SignaleExclusion: return
                        print "[%s] [%s][TRIBULLE] GameLog Error - Code: %s error: %s" %(_time.strftime("%H:%M:%S"), this.client.playerName, oldC, error)
                    else:
                        print "[%s] [%s] GameLog Error - C: %s CC: %s error: %s" %(_time.strftime("%H:%M:%S"), this.client.playerName, errorC, errorCC, error)
                return

            elif CC == Identifiers.recv.Informations.Player_Ping:
                try:
                    VC = (ord(packet.toByteArray()) + 1)
                    if this.client.PInfo[0] == VC:
                        this.client.PInfo[2] = int((_time.time() - this.client.PInfo[1]) * 1000)
                except: pass
                return


            elif CC == Identifiers.recv.Informations.Change_Shaman_Type:
                type = packet.readByte()
                this.client.shamanType = type
                this.client.sendShamanType(type, (this.client.shamanSaves >= 2500 and this.client.hardModeSaves >= 1000))
                return

            elif CC == Identifiers.recv.Informations.Letter:
                return

            elif CC == Identifiers.recv.Informations.Send_Gift:
                this.client.sendPacket(Identifiers.send.Send_Gift, 1)
                return

            elif CC == Identifiers.recv.Informations.Computer_Info:
                return

            elif CC == Identifiers.recv.Informations.Change_Shaman_Color:
                color = packet.readInt()
                this.client.shamanColor = "%06X" %(0xFFFFFF & color)
                return

            elif CC == Identifiers.recv.Informations.Request_Info:
                this.client.sendPacket(Identifiers.send.Request_Info, ByteArray().writeUTF("http://195.154.124.74/outils/info.php").toByteArray())
                return

        elif C == Identifiers.recv.Lua.C:
            if CC == Identifiers.recv.Lua.Key_Board:
                key, down, posX, posY = packet.readShort(), packet.readBoolean(), packet.readShort(), packet.readShort()
                if this.client.isFly and key == 32:
                    this.client.room.movePlayer(this.client.playerName, 0, 0, True, 0, -50, True)
                if this.client.isSpeed and key == 32:
                    this.client.room.movePlayer(this.client.playerName, 0, 0, True, 0, 50 if this.client.isMovingRight else -50, True)
                if this.client.room.isFlyGame and key == 32:
                    if this.client.flypoints >= 1:
                        this.client.room.movePlayer(this.client.playerName, 0, 0, True, 0, -50, True)
                        this.client.flypoints -= 1
                        this.client.sendMessage("<ROSE>[FLY] - <N>Você possui: "+str(this.client.flypoints)+" fly.")
                    else: this.client.sendMessage("<ROSE>[FLY] - <N>Você não possui fly, aguarde...")
                if this.client.room.isBallonRace:
                    this.client.Minigames.ballonEventKeyboard(this.client.playerName, key, down, posX, posY)
                if this.client.room.isInvocationGame:
                    this.client.Minigames.InvocationEventKeyboard(this.client.playerName, key, down, posX, posY)
                if this.client.room.isExplosionGame:
                    this.client.Minigames.explosionEventKeyboard(this.client.playerName, key, down, posX, posY)
                if this.client.room.isDeathmatch:
                    this.client.Minigames.deathEventKeyboard(this.client.playerName, key, down, posX, posY)
                if this.client.room.isDeathmatch and key == ord("L"):
                    this.client.PlayerDeathVivo = False
                    this.client.ranking.open()
                if this.client.room.isDeathmatch and key == 79:
                    this.client.sendDeathInventory()
                if this.client.room.isDeathmatch and key == 80:
                    this.client.sendDeathProfile()
                if key == ord("J"):
                    this.client.openStaffChat = True
                    this.client.viewMessage = 0
                    this.client.sendStaffChats()
                    this.client.sendMessage("Você abriu o STAFF CHAT. Para fechar aperte a tecla K.")
                if key == ord("K"):
                    this.client.openStaffChat = False
                    this.client.viewMessage = 0
                    this.client.sendStaffChats()
                    this.client.sendMessage("Você fechou o STAFF CHAT. Para abrir, aperte a tecla J.")
                return
            
            elif CC == Identifiers.recv.Lua.Mouse_Click:
                posX, posY = packet.readShort(), packet.readShort()
                return

            elif CC == Identifiers.recv.Lua.Popup_Answer:
                popupID, answer = packet.readInt(), packet.readUTF()
                if not this.client.server.activeStaffChat == 1:
                    if popupID == 3:
                        answer = answer.replace("&amp;#", "&#").replace("<", "&lt;")
                        if this.client.privLevel >= 3:
                            if this.client.privLevel >= 9:
                                message = "<V>[Admin]<ROSE>[" + this.client.playerName.capitalize() + "]</ROSE> <N>" + answer                   
                            if this.client.privLevel == 8:
                                message = "<V>[Coord]<VI>[" + this.client.playerName.capitalize() + "]</VI> <N>" + answer
                            if this.client.privLevel == 7:
                                message = "<V>[SMod]<J>[" + this.client.playerName.capitalize() + "]</J> <N>" + answer
                            if this.client.privLevel == 6:
                                message = "<V>[Mod]<N>[" + this.client.playerName.capitalize() + "]</N> <N>" + answer
                            if this.client.privLevel == 5:
                                message = "<V>[Mapcrew]<font color='#FFCC99'>[" + this.client.playerName.capitalize() + "]</font> <N>" + answer
                            if this.client.privLevel == 4:
                                message = "<V>[Helper]<font color='#3366FF'>[" + this.client.playerName.capitalize() + "]</font> <N>" + answer
                        if answer != "" and answer != " " and answer != " "*len(answer):
                            if not len(answer) >= 50:
                                if not len(answer) <= 0:
                                    this.server.staffChat.append(message)
                                    for client in this.server.players.values():
                                        if client.privLevel >= 3:
                                            if not client.openStaffChat:
                                                client.viewMessage += 1
                                    this.client.sendStaffChats()
                                else: this.client.sendStaffChats()
                            else:
                                this.client.sendMessage("<ROSE>Oops! Sua mensagem está muito grande.")
                                this.client.sendStaffChats()
                if int(popupID == 1):
                    if this.client.privLevel >= 1:
                        #Alterar Senha
                        if this.client.gamePassword >= 1:
                            this.client.gamePassword = 0
                            if not this.client.emailAddress == "":
                                password = answer
                                if len(password) < 5 or len(password) > 20:
                                    this.client.sendMessage("<ROSE>Você não pode alterar sua senha com menos de 5 caractéres ou mais de 20 caractéres.")
                                    return
                                else:
                                    this.Cursor.execute("update Users set Password = ? where username = ?", [base64.b64encode(hashlib.sha256(hashlib.sha256(password).hexdigest() + "\xf7\x1a\xa6\xde\x8f\x17v\xa8\x03\x9d2\xb8\xa1V\xb2\xa9>\xddC\x9d\xc5\xdd\xceV\xd3\xb7\xa4\x05J\r\x08\xb0").digest()), this.client.playerName])
                                    this.client.sendMessage("<N>[-5] <ROSE>Senha alterada com sucesso! Sua nova senha é: <N>"+password+"")
                                    this.client.XDCoins -= 5
                            else: this.client.sendMessage("<ROSE>Por favor, adicione um e-mail para a sua conta usando o comando: /email")

                        #Definir E-mail
                        if this.client.gameEmail >= 1:
                            this.client.gameEmail = 0
                            if this.client.changepw == 0:
                                if not this.server.checkDuplicateEmail(answer) and "@" in answer and "." in answer:
                                    this.client.tempEmailAddress = answer
                                    if this.client.emailAddress == "":
                                        this.client.emailAddress = this.client.tempEmailAddress
                                        this.client.tempEmailAddress = ""
                                        this.client.changepw += 1
                                        if not this.client.parseShop.checkInShop(209):
                                            this.client.shopItems += "209" if this.client.shopItems == "" else ",209"
                                        this.client.parseShop.checkUnlockShopTitle()
                                        this.client.sendAnimZelda(2, 9)
                                        this.Cursor.execute("update Users set Email = ? where username = ?", [answer, this.client.playerName])
                                        this.client.sendMessage("Você alterou o seu e-mail com sucesso! O seu e-mail é: "+answer)

                                else: this.client.sendMessage("E-mail <R>inválido</R>. Use um e-mail válido!\nExemplo: "+str(this.client.playerName)+"@gmail.com")

                #Alterar Avatar
                if int(popupID == 1):
                    if this.client.gameAvatar >= 1:
                        this.client.gameAvatar = 0
                        avatar = answer
                        if len(avatar) < 1 or len(avatar) > 15:
                            this.client.sendMessage('[Avatar]<N> Seu avatar deve possuir de <b>1 a 15</b> caractéres (números)!')
                        elif not avatar.isdigit():
                            this.client.sendMessage('[Avatar]<N> Seu avatar não pode conter letras, apenas números. Deve ser assim, exemplo: <b>/avatar 85621722</b>.')
                        else:
                            avatar = int(avatar) 
                            if this.client.playerAvatar != avatar:
                                if avatar >= 99999999:
                                    this.client.sendMessage('<ROSE>[Avatar]<N> Parâmetros inválidos. Tente novamente!')
                                else:
                                    this.Cursor.execute('UPDATE users SET avatar = ? WHERE username = ?', [avatar, this.client.playerName])
                                    this.client.sendMessage("<ROSE>[Avatar]<N> Novo avatar alterado, número: [%r]" % (avatar))
		#Alterar Nome							
		if int(popupID == 1):
                    if this.client.privLevel >= 1:
                        if this.client.gameUsername >= 1:
                            this.client.gameUsername = 0
                            if this.client.changeuser == 0:
                                playerName = answer
                                if not this.client.emailAddress == "":
                                    if not re.match("^[A-Z][0-9_a-z]{2,11}$", playerName) or len(playerName) < 3 or len(playerName) > 12:
                                        if this.client.langue.lower() in ["en", "fr", "cn", "tr", "vk", "pl", "hu", "nl", "ro", "id", "de", "e2", "ar", "ph", "lt", "jp", "ch", "fi", "cz", "sk", "hr", "bu", "lv", "he", "it", "et", "az"]:
                                            this.client.sendMessage("<ROSE>You may not have to have less than 3 letters and can not have more than 12 letters (Example: Newname)")
                                        if this.client.langue.lower() in ["es"]:
                                            this.client.sendMessage("<ROSE>Puede tener menos de 3 letras y no más de 12 letras (ejemplo: Nuevonombre)")
                                        if this.client.langue.lower() in ["br"]:
                                            this.client.sendMessage("<ROSE>Você pode ter menos de 3 letras e não mais de 12 letras (exemplo: Novonome)")
                                    elif this.client.server.checkExistingUser(playerName):
                                        if this.client.langue.lower() in ["en", "fr", "cn", "tr", "vk", "pl", "hu", "nl", "ro", "id", "de", "e2", "ar", "ph", "lt", "jp", "ch", "fi", "cz", "sk", "hr", "bu", "lv", "he", "it", "et", "az"]:
                                            this.client.sendMessage("<ROSE>That user already exists!")
                                        if this.client.langue.lower() in ["es"]:
                                            this.client.sendMessage("<ROSE>Ese usuario ya existe!")
                                        if this.client.langue.lower() in ["br"]:
                                            this.client.sendMessage("<ROSE>Esse usuário já existe!")
                                    else:
                                        this.client.changeuser += 1
                                        this.Cursor.execute("update Users set Username = ? where Username = ?", [playerName, this.client.playerName])
                                        if this.client.langue.lower() in ["en", "fr", "cn", "tr", "vk", "pl", "hu", "nl", "ro", "id", "de", "e2", "ar", "ph", "lt", "jp", "ch", "fi", "cz", "sk", "hr", "bu", "lv", "he", "it", "et", "az"]:
                                            this.client.sendMessage("<ROSE>Your username has been changed to: "+ playerName +"")
                                        if this.client.langue.lower() in ["es"]:
                                            this.client.sendMessage("<ROSE>Tu nuevo usuario es: "+ playerName +"")
                                        if this.client.langue.lower() in ["br"]:
                                            this.client.sendMessage("<ROSE>Seu novo usuario é: "+ playerName +"")
                                        this.client.shopCheeses += 100
                                        this.client.shopFraises += 100
                                        this.client.updateDatabase()                                      
                                else:
                                    if this.client.langue.lower() in ["en", "fr", "cn", "tr", "vk", "pl", "hu", "nl", "ro", "id", "de", "e2", "ar", "ph", "lt", "jp", "ch", "fi", "cz", "sk", "hr", "bu", "lv", "he", "it", "et", "az"]:
                                        this.client.sendMessage("<ROSE>Please add an email to your account using the command: /email")
                                    if this.client.langue.lower() in ["es"]:
                                        this.client.sendMessage("<ROSE>Porfavor, agrega un email en tu cuenta usando el comando: /email")
                                    if this.client.langue.lower() in ["br"]:
                                        this.client.sendMessage("<ROSE>Por favor, adicione um e-mail para a sua conta usando o comando: /email")
                            else:
                                this.client.sendMessage("<ROSE>Ya has cambiado tu usuario una vez!.")

            elif CC == Identifiers.recv.Lua.Text_Area_Callback:
                textAreaID, event = packet.readInt(), packet.readUTF()
                ## Danshweger Menu System ##
                if event.startswith("fullMenu"):
                    if event == "fullMenu:open": 
                        this.client.fullMenu.open()
                    elif event.startswith("fullMenu:changeTab"):
                        args = event.split("-", 3)
                        this.client.shop.changeTab(int(args[1]), int(args[2]))
                    elif event == "fullMenu:close":
                        this.client.close()

                if event.startswith("openStaffChat"):
                    this.client.openStaffChat = True
                    this.client.viewMessage = 0
                    this.client.sendStaffChats()

                if event.startswith("closeStaffChat"):
                    this.client.openStaffChat = False
                    this.client.viewMessage = 0
                    this.client.sendStaffChats()

                if event.startswith("clearStaffChat"):
                    if len(this.client.server.staffChat) >= 1:
                        if this.client.server.activeStaffChat == 0:
                            del this.client.server.staffChat[:]
                            this.client.sendStaffChats()
                            this.server.sendStaffMessage(4, "As conversas do STAFF CHAT foram removidas pelo Administrador <V>"+str(this.client.playerName)+".")
                        else: this.client.sendMessage("Reative o chat antes de tentar limpa-lo.")
                    else: this.client.sendMessage("Não há conversas no chat para serem removidas.")

                if event.startswith("desativarStaffChat"):
                    if not this.client.server.activeStaffChat == 1:
                        this.client.server.activeStaffChat = 1
                        this.server.sendStaffMessage(4, "O STAFF CHAT foi desativado pelo Administrador <V>"+str(this.client.playerName)+".")
                        this.client.sendStaffChats()
                    else:
                        this.client.server.activeStaffChat = 0
                        this.client.sendStaffChats()
                        this.server.sendStaffMessage(4, "O STAFF CHAT foi reativado pelo Administrador <V>"+str(this.client.playerName)+".")        
                        
                elif event.startswith("ranking"):
                    if event == "ranking:open":
                        this.client.ranking.open()
                    elif event == "ranking:firsts":
                        this.client.ranking.sendRanking(1)
                    elif event == "ranking:coletados":
                        this.client.ranking.sendRanking(2)
                    elif event == "ranking:saves":
                        this.client.ranking.sendRanking(3)
                    elif event == "ranking:bootcamps":
                        this.client.ranking.sendRanking(4)
                    elif event == "ranking:moedas":
                        this.client.ranking.sendRanking(5)
                    elif event == "ranking:death":
                        this.client.ranking.sendRanking(6)
                    elif event == "ranking:tribo":
                        this.client.ranking.sendRanking(7)

                elif event.startswith("equipe"):
                    if event == "equipe:open": 
                        this.client.equipe.open()
                    elif event == "equipe:founders":
                        this.client.equipe.sendStaff(0)
                    elif event == "equipe:coords":
                        this.client.equipe.sendStaff(1)
                    elif event == "equipe:smods":
                        this.client.equipe.sendStaff(2)
                    elif event == "equipe:mods":
                        this.client.equipe.sendStaff(3)
                    elif event == "equipe:mapcrews":
                        this.client.equipe.sendStaff(4)
                    elif event == "equipe:helpers":
                        this.client.equipe.sendStaff(5)
                        
                elif event.startswith("shop"):
                    if event == "shop:open":
                        this.client.shop.open()
                    elif event.startswith("shop:changeTab"):
                        args = event.split("-", 3)
                        this.client.shop.changeTab(int(args[1]), int(args[2]))
                    elif event.startswith("shop:buyItem"):
                        args = event.split("-", 3)
                        this.client.shop.buyItem(int(args[1]), int(args[2]))
                    elif event.startswith("shop:confirmBuyItem"):
                        args = event.split("-", 3)
                        this.client.shop.confirmBuyItem(int(args[1]), int(args[2]))

                elif event.startswith("roleta"):
                    if event == "roleta:open":
                        this.client.roleta.open()
                    elif event.startswith("roleta:changeTab"):
                        args = event.split("-", 2)
                        this.client.roleta.changeTab(int(args[1]))

                elif event.startswith("consumablesShop"):
                    if event == "consumablesShop:open":
                        this.client.consumablesShop.open()
                    elif event.startswith("consumablesShop:changePage"):
                        args = event.split("-", 2)
                        this.client.consumablesShop.changePage(int(args[1]))
                    elif event.startswith("consumablesShop:addItem"):
                        args = event.split("-", 3)
                        this.client.consumablesShop.addItem(int(args[1]), int(args[2]))
                    elif event.startswith("consumablesShop:removeItem"):
                        args = event.split("-", 3)
                        this.client.consumablesShop.removeItem(int(args[1]), int(args[2]))
                    elif event == "consumablesShop:endBuy":
                        this.client.consumablesShop.endBuy()
                    elif event == "consumablesShop:cancelBuy":
                        this.client.consumablesShop.changePage(-1)
                    elif event.startswith("consumablesShop:confirmBuy"):
                        args = event.split("-", 2)
                        this.client.consumablesShop.confirmBuy(int(args[1]) == 1)
                    elif event == "consumablesShop:backToHome":
                        this.client.consumablesShop.changePage(-1)

                elif event == "staffList":
                    this.client.parseCommands.parseCommand("equipe")
                    
                elif event.startswith("changeColor"):
                    this.client.parseCommands.parseCommand("color")

                elif event == "fechar":
                        this.client.sendPacket([29, 22], struct.pack("!l", 10050))
                        this.client.sendPacket([29, 22], struct.pack("!l", 10051))
                        this.client.sendPacket([29, 22], struct.pack("!l", 10052))
                        this.client.sendPacket([29, 22], struct.pack("!l", 10053))

                elif event == "girar":
                    if this.client.XDFichas >=1:
                        bg = '<img src="http://www.transforxd.top/images/icones/bgroleta.png">'
                        txt = 'Sorteando, aguarde...'
                        this.client.sendAddPopupText(10056, 300, 130, 299, 100, '000000', '000000', 100, bg)
                        this.client.sendAddPopupText(10057, 360, 170, 225, 60, '000000', '000000', 100, txt)
                        this.client.roleta.sendGetTimeRoleta()
                    else:
                        bg = '<img src="http://www.transforxd.top/images/icones/bgroleta.png">'
                        txt = 'Você não tem fichas suficientes para \ngirar a roleta.'
                        txtOK = '<font size="12"><V><a href="event:fecharPop">OK</a></font>'
                        this.client.sendAddPopupText(10056, 300, 130, 299, 100, '000000', '000000', 100, bg)
                        this.client.sendAddPopupText(10057, 325, 150, 225, 60, '000000', '000000', 100, txt)
                        this.client.sendAddPopupText(10058, 420, 180, 30, 60, '000000', '000000', 100, txtOK)

                elif event == "fecharPop":
                    this.client.sendPacket([29, 22], struct.pack("!l", 10056))
                    this.client.sendPacket([29, 22], struct.pack("!l", 10057))
                    this.client.sendPacket([29, 22], struct.pack("!l", 10058))

                elif event == "help":
                     this.client.parseCommands.parseCommand("ajuda")
                ## End Danshweger Menu System ##

                if event.startswith("fechadin"):
                    for x in range(0, 100):									
                        this.client.sendPacket([29, 22], ByteArray().writeInt(x).toByteArray())
                        
                if textAreaID in [8983, 8984, 8985]:
                    if event.startswith("inventory"):
                        event = event.split("#")
                        if event[1] == "use":
                            this.client.deathStats[4] = int(event[2])
                        else:
                            this.client.deathStats[4] = 0
                        this.client.sendDeathInventory(this.client.page)

                if textAreaID == 123480 or textAreaID == 123479:
                    if event == "next":
                        if not this.client.page >= 3:
                            this.client.page += 1
                            this.client.sendDeathInventory(this.client.page)
                    else:
                        if not this.client.page <= 1:
                            this.client.page -= 1
                            this.client.sendDeathInventory(this.client.page)

                if textAreaID == 9012:
                    if event == "close":
                        ids = 131458, 123479, 130449, 131459, 123480, 6992, 8002, 23, 9012, 9013, 9893, 8983, 9014, 9894, 8984, 9015, 9895, 8985, 504, 505, 506, 507
                        for id in ids:
                            if id <= 507 and not id == 23:
                                this.client.sendPacket([29, 18], ByteArray().writeInt(id).toByteArray())
                            else:
                                this.client.sendPacket([29, 22], ByteArray().writeInt(id).toByteArray())

                if textAreaID == 9009:
                    if event == "close":
                        ids = 39, 40, 41, 7999, 20, 9009, 7239, 8249, 270
                        for id in ids:
                            if id <= 41 and not id == 20:
                                this.client.sendPacket([29, 18], ByteArray().writeInt(id).toByteArray())
                            else:
                                this.client.sendPacket([29, 22], ByteArray().writeInt(id).toByteArray())

                if textAreaID == 20:
                    if event.startswith("offset"):
                        event = event.split("#")
                        if event[1] == "offsetX":
                            if event[2] == "1":
                                if not this.client.deathStats[0] >= 25:
                                    this.client.deathStats[5] += 1
                                    this.client.deathStats[0] += 1
                            else:
                                if not this.client.deathStats[0] <= -25:
                                    this.client.deathStats[5] -= 1
                                    this.client.deathStats[0] -= 1
                        else:
                            if event[2] == "1":
                                if not this.client.deathStats[1] >= 25:
                                    this.client.deathStats[6] += 1
                                    this.client.deathStats[1] += 1
                            else:
                                if not this.client.deathStats[1] <= -25:
                                    this.client.deathStats[6] -= 1
                                    this.client.deathStats[1] -= 1
                    elif event == "show":
                        if this.client.deathStats[3] == 1:
                            this.client.deathStats[3] = 0
                        else:
                            this.client.deathStats[3] = 1
                    this.client.sendDeathProfile()
                return

        elif CC == Identifiers.recv.Lua.Color_Picked:
                colorPickerId, color = packet.readInt(), packet.readInt()
                try:
                    if colorPickerId == 10000:
                        if color != -1:
                            this.client.nameColor = "%06X" %(0xFFFFFF & color)
                            this.client.room.setNameColor(this.client.playerName, color)
                            this.client.sendMessage("<ROSE>Você alterou a cor do nome do seu rato com sucesso.")
                    elif colorPickerId == 10001:
                        if color != -1:
                            this.client.mouseColor = "%06X" %(0xFFFFFF & color)
                            this.client.playerLook = "1;%s" %(this.client.playerLook.split(";")[1])
                            this.client.sendMessage("<ROSE>Você alterou a cor do seu rato com sucesso.\nAguarde a próxima rodada para utilizar a nova cor.")
                except: this.client.sendMessage("<ROSE>Cor incorreta, tente novamente usando outra cor.")
                return

        elif C == Identifiers.recv.Cafe.C:
            if CC == Identifiers.recv.Cafe.Reload_Cafe:
                if not this.client.isReloadCafe:
                    this.client.cafe.loadCafeMode()
                    this.client.isReloadCafe = True
                    reactor.callLater(3, setattr, this.client, "isReloadCafe", False)
                return

            elif CC == Identifiers.recv.Cafe.Open_Cafe_Topic:
                topicID = packet.readInt()
                this.client.cafe.openCafeTopic(topicID)
                return

            elif CC == Identifiers.recv.Cafe.Create_New_Cafe_Topic:
                if this.client.privLevel >= 1:
                    message, title = packet.readUTF(), packet.readUTF()
                    this.client.cafe.createNewCafeTopic(message, title)
                return

            elif CC == Identifiers.recv.Cafe.Create_New_Cafe_Post:
                if this.client.privLevel >= 1:
                    topicID, message = packet.readInt(), packet.readUTF()
                    this.client.cafe.createNewCafePost(topicID, message)
                return

            elif CC == Identifiers.recv.Cafe.Open_Cafe:
                this.client.isCafe = packet.readBoolean()
                return

            elif CC == Identifiers.recv.Cafe.Vote_Cafe_Post:
                if this.client.privLevel >= 1:
                    topicID, postID, mode = packet.readInt(), packet.readInt(), packet.readBoolean()
                    this.client.cafe.voteCafePost(topicID, postID, mode)
                return

            elif CC == Identifiers.recv.Cafe.Delete_Cafe_Message:
                if this.client.privLevel >= 7:
                    topicID, postID = packet.readInt(), packet.readInt()
                    this.client.cafe.deleteCafePost(topicID, postID)
                else: this.client.sendMessage("Você não está autorizado a usar esta função.")
                return

            elif CC == Identifiers.recv.Cafe.Delete_All_Cafe_Message:
                if this.client.privLevel >= 7:
                    topicID, playerName = packet.readInt(), packet.readUTF()
                    this.client.cafe.deleteAllCafePost(topicID, playerName)
                else: this.client.sendMessage("Você não está autorizado a usar esta função.")
                return

        elif C == Identifiers.recv.Inventory.C:
            if CC == Identifiers.recv.Inventory.Open_Inventory:
                this.client.sendInventoryConsumables()
                return

            elif CC == Identifiers.recv.Inventory.Use_Consumable:
                id = packet.readShort()
                if this.client.playerConsumables.has_key(id) and not this.client.isDead and not this.client.room.isRacing and not this.client.room.isBootcamp and not this.client.room.isSurvivor and not this.client.room.isDefilante:
                    if not this.client.canUseConsumable:
                        this.client.sendMessage("Por favor, aguarde 5 segundos para usar um consumível novamente.")
                        return
                    this.client.canUseConsumable = False
                    this.client.consumablesTimer = reactor.callLater(5, setattr, this.client, "canUseConsumable", True)
                    
                    if not id in [31, 34, 2240, 2247, 2262, 2332, 2340] or this.client.pet == 0:
                        count = this.client.playerConsumables[id]
                        if count > 0:
                            count -= 1
                            this.client.playerConsumables[id] -= 1
                            if count == 0:
                                del this.client.playerConsumables[id]
                                if this.client.equipedConsumables:
                                    for id in this.client.equipedConsumables:
                                        if not id:
                                            this.client.equipedConsumables.remove(id)
                                    None
                                    if id in this.client.equipedConsumables:
                                        this.client.equipedConsumables.remove(id)

                            if id in [1, 5, 6, 8, 11, 20, 24, 25, 26]:
                                if id == 11:
                                    this.client.room.objectID += 2
                                this.client.sendPlaceObject(this.client.room.objectID if id == 11 else 0, 65 if id == 1 else 4 if id == 5 else 34 if id == 6 else 89 if id == 8 else 90 if id == 11 else 33 if id == 20 else 63 if id == 24 else 80 if id == 25 else 95 if id == 26 else 0, this.client.posX + 28 if this.client.isMovingRight else this.client.posY - 28, this.client.posY, 0, 0 if id == 11 or id == 24 else 10 if this.client.isMovingRight else -10, -3, True, True)

                            if id == 10:
                                x = 0
                                for client in this.client.room.clients.values():
                                    if x < 5 and client != this.client:
                                        if client.posX >= this.client.posX - 400 and client.posX <= this.client.posX + 400:
                                            if client.posY >= this.client.posY - 300 and client.posY <= this.client.posY + 300:
                                                client.sendPlayerEmote(3, "", False, False)
                                                x += 1

                            if id == 11:
                                this.client.room.newConsumableTimer(this.client.room.objectID)
                                this.client.isDead = True
                                if not this.client.room.noAutoScore: this.client.playerScore += 1
                                this.client.sendPlayerDied()
                                this.client.room.checkChangeMap()
                        
                            if id == 28:
                                this.client.parseSkill.sendBonfireSkill(this.client.posX, this.client.posY, 15)

                            if id in [31, 34, 2240, 2247, 2262, 2332, 2340]:
                                this.client.pet = {31:2, 34:3, 2240:4, 2247:5, 2262:6, 2332:7, 2340:8}[id]
                                this.client.petEnd = Utils.getTime() + (1200 if this.client.pet == 8 else 3600)
                                this.client.room.sendAll(Identifiers.send.Pet, ByteArray().writeInt(this.client.playerCode).writeUnsignedByte(this.client.pet).toByteArray())

                            if id == 33:
                                this.client.sendPlayerEmote(16, "", False, False)

                            if id == 35:
                                if len(this.client.shamanBadges) > 0:
                                    this.client.room.sendAll(Identifiers.send.Balloon_Badge, ByteArray().writeInt(this.client.playerCode).writeUnsignedByte(random.randint(0, len(this.client.shopBadges))).toByteArray())

                            if id == 800:
                                this.client.shopCheeses += 5
                                this.client.sendAnimZelda(2, 0)
                                this.client.sendGiveCurrency(0, 5)

                            if id == 801:
                                this.client.shopFraises += 5
                                this.client.sendAnimZelda(2, 2)

                            if id == 2234:
                                x = 0
                                this.client.sendPlayerEmote(20, "", False, False)
                                for client in this.client.room.clients.values():
                                    if x < 5 and client != this.client:
                                        if client.posX >= this.client.posX - 400 and client.posX <= this.client.posX + 400:
                                            if client.posY >= this.client.posY - 300 and client.posY <= this.client.posY + 300:
                                                client.sendPlayerEmote(6, "", False, False)
                                                x += 1

                            if id == 2239:
                                this.client.room.sendAll(Identifiers.send.Crazzy_Packet, ByteArray().writeByte(4).writeInt(this.client.playerCode).writeInt(this.client.shopCheeses).toByteArray())

                            if id == 2246:
                                this.client.sendPlayerEmote(24, "", False, False)

                            if id == 2255:
                                this.client.sendAnimZelda(7, case="$De6", id=random.randint(0, 6))

                            this.client.updateInventoryConsumable(id, count)
                            this.client.useInventoryConsumable(id)
                return

            elif CC == Identifiers.recv.Inventory.Equip_Consumable:
                id, equip = packet.readShort(), packet.readBoolean()
                return
                
            elif CC == Identifiers.recv.Inventory.Trade_Invite:
                playerName = packet.readUTF()
                this.client.tradeInvite(playerName)
                return
                
            elif CC == Identifiers.recv.Inventory.Cancel_Trade:
                playerName = packet.readUTF()
                this.client.cancelTrade(playerName)
                return
                
            elif CC == Identifiers.recv.Inventory.Trade_Add_Consusmable:
                id, isAdd = packet.readShort(), packet.readBoolean()
                try:
                    this.client.tradeAddConsumable(id, isAdd)
                except: pass
                return
                
            elif CC == Identifiers.recv.Inventory.Trade_Result:
                isAccept = packet.readBoolean()
                this.client.tradeResult(isAccept)
                return

        elif C == Identifiers.recv.Tribulle.C:
            if CC == Identifiers.recv.Tribulle.Tribulle:
                if not this.client.isGuest:
                    #packet = this.descriptPacket(packetID, packet)
                    code = packet.readShort()                    
                    this.client.tribulle.parseTribulleCode(code, packet)
                return

        elif C == Identifiers.recv.Transformice.C:
            if CC == Identifiers.recv.Transformice.Invocation:
                objectCode, posX, posY, rotation, position, invocation = packet.readShort(), packet.readShort(), packet.readShort(), packet.readShort(), packet.readUTF(), packet.readBoolean()
                if this.client.isShaman:
                    showInvocation = True
                    if this.client.room.isSurvivor:
                        showInvocation = invocation
                    pass
                    if showInvocation:
                        try:
                            this.client.room.sendAllOthers(this.client, Identifiers.send.Invocation, ByteArray().writeInt(this.client.playerCode).writeShort(objectCode).writeShort(posX).writeShort(posY).writeShort(rotation).writeUTF(position).writeBoolean(invocation).toByteArray())
                        except: pass
                return

            elif CC == Identifiers.recv.Transformice.Remove_Invocation:
                if this.client.isShaman:
                    this.client.room.sendAllOthers(this.client, Identifiers.send.Remove_Invocation, ByteArray().writeInt(this.client.playerCode).toByteArray())
                return

            elif CC == Identifiers.recv.Transformice.Change_Shaman_Badge:
                badge = packet.readByte()
                if str(badge) or badge == 0 in this.client.shamanBadges:
                    this.client.equipedShamanBadge = str(badge)
                    this.client.sendProfile(this.client.playerName)
                return

            elif CC == Identifiers.recv.Transformice.Bots_Village:
                packet = packet.toByteArray()
                p = ByteArray(packet)
                if packet[3:] == "Papaille" or packet[3:] == "Elise" or packet[3:] == "Von Drekkemouse" or packet[3:] == "Cassidy" or packet[3:] == "Oracle" or packet[3:] == "Prof" or packet[3:] == "Buffy" or packet[3:] == "Indiana Mouse" or packet[3:] == "Tod":          
                    id, bot = p.readByte(), p.readUTF()
                    this.client.botVillage = bot
                    this.client.BotsVillage(bot)
                else:
                    id, linha = p.readByte(), p.readByte()
                    coisa = this.client.itensBots[this.client.botVillage][linha]
                    this.client.premioVillage(coisa)
                        
                this.client.room.sendAll([100, 40], ByteArray().writeByte(2).writeInt(this.client.playerCode).toByteArray() + "\x00\xc9>" + packet)


            elif CC == Identifiers.recv.Transformice.Done_Visual:
                p = ByteArray(packet.toByteArray())
                visuID = p.readShort()

                shopItems = [] if this.client.shopItems == "" else this.client.shopItems.split(",")
                look = this.server.newVisuList[visuID].split(";")
                look[0] = int(look[0])
                lengthCloth = len(this.client.clothes)
                buyCloth = 5 if (lengthCloth == 0) else (50 if lengthCloth == 1 else 100)

                this.client.visuItems = {-1: {"ID": -1, "Buy": buyCloth, "Bonus": True, "Customizable": False, "HasCustom": False, "CustomBuy": 0, "Custom": "", "CustomBonus": False}, 22: {"ID": this.client.getFullItemID(22, look[0]), "Buy": this.client.getItemInfo(22, look[0])[6], "Bonus": False, "Customizable": False, "HasCustom": False, "CustomBuy": 0, "Custom": "", "CustomBonus": False}}

                count = 0
                for visual in look[1].split(","):
                    if not visual == "0":
                        item, customID = visual.split("_", 1) if "_" in visual else [visual, ""]
                        item = int(item)
                        itemID = this.client.getFullItemID(count, item)
                        itemInfo = this.client.getItemInfo(count, item)
                        this.client.visuItems[count] = {"ID": itemID, "Buy": itemInfo[6], "Bonus": False, "Customizable": bool(itemInfo[2]), "HasCustom": customID != "", "CustomBuy": itemInfo[7], "Custom": customID, "CustomBonus": False}
                        if this.client.parseShop.checkInShop(this.client.visuItems[count]["ID"]):
                            this.client.visuItems[count]["Buy"] -= itemInfo[6]
                        if len(this.client.custom) == 1:
                            if itemID in this.client.custom:
                                this.client.visuItems[count]["HasCustom"] = True
                            else:
                                this.client.visuItems[count]["HasCustom"] = False
                        else:
                            if str(itemID) in this.client.custom:
                                this.client.visuItems[count]["HasCustom"] = True
                            else:
                                this.client.visuItems[count]["HasCustom"] = False
                    count += 1
                hasVisu = map(lambda y: 0 if y in shopItems else 1, map(lambda x: x["ID"], this.client.visuItems.values()))
                visuLength = reduce(lambda x, y: x + y, hasVisu)
                allPriceBefore = 0
                allPriceAfter = 0
                promotion = 70.0 / 100

                p.writeUnsignedShort(visuID)
                p.writeUnsignedByte(20)
                p.writeUTF(this.server.newVisuList[visuID])
                p.writeUnsignedByte(visuLength)

                for category in this.client.visuItems.keys():
                    if len(this.client.visuItems.keys()) == category:
                        category = 22
                    itemID = this.client.getSimpleItemID(category, this.client.visuItems[category]["ID"])

                    buy = [this.client.visuItems[category]["Buy"], int(this.client.visuItems[category]["Buy"] * promotion)]
                    customBuy = [this.client.visuItems[category]["CustomBuy"], int(this.client.visuItems[category]["CustomBuy"] * promotion)]

                    p.writeShort(this.client.visuItems[category]["ID"])
                    p.writeUnsignedByte(2 if this.client.visuItems[category]["Bonus"] else (1 if not this.client.parseShop.checkInShop(this.client.visuItems[category]["ID"]) else 0))
                    p.writeUnsignedShort(buy[0])
                    p.writeUnsignedShort(buy[1])
                    p.writeUnsignedByte(3 if not this.client.visuItems[category]["Customizable"] else (2 if this.client.visuItems[category]["CustomBonus"] else (1 if this.client.visuItems[category]["HasCustom"] == False else 0)))
                    p.writeUnsignedShort(customBuy[0])
                    p.writeUnsignedShort(customBuy[1])
                    
                    allPriceBefore += buy[0] + customBuy[0]
                    allPriceAfter += (0 if (this.client.visuItems[category]["Bonus"]) else (0 if this.client.parseShop.checkInShop(itemID) else buy[1])) + (0 if (not this.client.visuItems[category]["Customizable"]) else (0 if this.client.visuItems[category]["CustomBonus"] else (0 if this.client.visuItems[category]["HasCustom"] else (customBuy[1]))))
                    
                p.writeShort(allPriceBefore)
                p.writeShort(allPriceAfter)
                this.client.priceDoneVisu = allPriceAfter

                this.client.sendPacket([100, 31], p.toByteArray())

            elif CC == Identifiers.recv.Transformice.Map_Info:
                this.client.room.cheesesList = []
                cheesesCount = packet.readByte()
                i = 0
                while i < cheesesCount / 2:
                    cheeseX, cheeseY = packet.readShort(), packet.readShort()
                    this.client.room.cheesesList.append([cheeseX, cheeseY])
                    i += 1
                
                this.client.room.holesList = []
                holesCount = packet.readByte()
                i = 0
                while i < holesCount / 3:
                    holeType, holeX, holeY = packet.readShort(), packet.readShort(), packet.readShort()
                    this.client.room.holesList.append([holeType, holeX, holeY])
                    i += 1
                return

        if this.server.isDebug:
            print "[%s] Packet not implemented - C: %s - CC: %s - packet: %s" %(this.client.playerName, C, CC, repr(packet.toByteArray()))

    def parsePacketUTF(this, packet):
        values = packet.split(chr(1))
        C = ord(values[0][0])
        CC = ord(values[0][1])
        values = values[1:]

        if C == Identifiers.old.recv.Player.C:
            if CC == Identifiers.old.recv.Player.Conjure_Start:
                this.client.room.sendAll(Identifiers.old.send.Conjure_Start, values)
                return

            elif CC == Identifiers.old.recv.Player.Conjure_End:
                this.client.room.sendAll(Identifiers.old.send.Conjure_End, values)
                return

            elif CC == Identifiers.old.recv.Player.Conjuration:
                reactor.callLater(10, this.client.sendConjurationDestroy, int(values[0]), int(values[1]))
                this.client.room.sendAll(Identifiers.old.send.Add_Conjuration, values)
                return

            elif CC == Identifiers.old.recv.Player.Snow_Ball:
                this.client.sendPlaceObject(0, 34, int(values[0]), int(values[1]), 0, 0, 0, False, True)
                return

            elif CC == Identifiers.old.recv.Player.Bomb_Explode:
                this.client.room.sendAll(Identifiers.old.send.Bomb_Explode, values)
                return

        elif C == Identifiers.old.recv.Room.C:
            if CC == Identifiers.old.recv.Room.Anchors:
                this.client.room.sendAll(Identifiers.old.send.Anchors, values)
                this.client.room.anchors.extend(values)
                return

            elif CC == Identifiers.old.recv.Room.Begin_Spawn:
                if not this.client.isDead:
                    this.client.room.sendAll(Identifiers.old.send.Begin_Spawn, [this.client.playerCode] + values)
                return

            elif CC == Identifiers.old.recv.Room.Spawn_Cancel:
                this.client.room.sendAll(Identifiers.old.send.Spawn_Cancel, [this.client.playerCode])
                return

            elif CC == Identifiers.old.recv.Room.Totem_Anchors:
                if this.client.room.isTotemEditor:
                    if this.client.tempTotem[0] < 20:
                        this.client.tempTotem[0] = int(this.client.tempTotem[0]) + 1
                        this.client.sendTotemItemCount(this.client.tempTotem[0])
                        this.client.tempTotem[1] += "#3#" + chr(1).join(map(str, [values[0], values[1], values[2]]))
                return

            elif CC == Identifiers.old.recv.Room.Move_Cheese:
                this.client.room.sendAll(Identifiers.old.send.Move_Cheese, values)
                return

            elif CC == Identifiers.old.recv.Room.Bombs:
                this.client.room.sendAll(Identifiers.old.send.Bombs, values)
                return

        elif C == Identifiers.old.recv.Balloons.C:
            if CC == Identifiers.old.recv.Balloons.Place_Balloon:
                this.client.room.sendAll(Identifiers.old.send.Balloon, values)
                return

            elif CC == Identifiers.old.recv.Balloons.Remove_Balloon:
                this.client.room.sendAllOthers(this.client, Identifiers.old.send.Balloon, [this.client.playerCode, "0"])
                return

        elif C == Identifiers.old.recv.Map.C:
            if CC == Identifiers.old.recv.Map.Vote_Map:
                if len(values) == 0:
                    this.client.room.receivedNo += 1
                else:
                    this.client.room.receivedYes += 1
                return

            elif CC == Identifiers.old.recv.Map.Load_Map:
                try:
                    values[0] = values[0].replace("@", "")
                    if values[0].isdigit():
                        code = int(values[0])
                        this.client.room.CursorMaps.execute("select * from Maps where Code = ?", [code])
                        rs = this.client.room.CursorMaps.fetchone()
                        if rs:
                            if this.client.playerName == rs["Name"] or this.client.privLevel >= 6:
                                this.client.sendPacket(Identifiers.old.send.Load_Map, [rs["XML"], rs["YesVotes"], rs["NoVotes"], rs["Perma"]])
                                this.client.room.EMapXML = rs["XML"]
                                this.client.room.EMapLoaded = code
                                this.client.room.EMapValidated = False
                            else:
                                this.client.sendPacket(Identifiers.old.send.Load_Map_Result, [])
                        else:
                            this.client.sendPacket(Identifiers.old.send.Load_Map_Result, [])
                    else:
                        this.client.sendPacket(Identifiers.old.send.Load_Map_Result, [])
                except: pass
                return

            elif CC == Identifiers.old.recv.Map.Validate_Map:
                mapXML = values[0]
                if this.client.room.isEditor:
                    this.client.sendPacket(Identifiers.old.send.Map_Editor, [""])
                    this.client.room.EMapValidated = False
                    this.client.room.EMapCode = 1
                    this.client.room.EMapXML = mapXML
                    this.client.room.mapChange()
                return

            elif CC == Identifiers.old.recv.Map.Map_Xml:
                this.client.room.EMapXML = values[0]
                return

            elif CC == Identifiers.old.recv.Map.Return_To_Editor:
                this.client.room.EMapCode = 0
                this.client.sendPacket(Identifiers.old.send.Map_Editor, ["", ""])
                return

            elif CC == Identifiers.old.recv.Map.Export_Map:
                isTribeHouse = len(values) != 0
                if this.client.cheeseCount < 1500 and this.client.privLevel < 6 and not isTribeHouse:
                    this.client.sendPacket(Identifiers.old.send.Editor_Message, [""])
                    this.client.sendMessage("<ROSE>Atenção! Você precisa de <b>1500</b> queijos coletados para Exportar um Mapa.")
                elif this.client.shopCheeses < (5 if isTribeHouse else 40) and this.client.privLevel < 6:
                    this.client.sendPacket(Identifiers.old.send.Editor_Message, ["", ""])
                elif this.client.room.EMapValidated or isTribeHouse:
                    if this.client.privLevel < 6:
                        this.client.shopCheeses -= 5 if isTribeHouse else 40
                    code = 0
                    if this.client.room.EMapLoaded != 0:
                        code = this.client.room.EMapLoaded
                        this.client.room.CursorMaps.execute("update Maps set XML = ?, Updated = ? where Code = ?", [this.client.room.EMapXML, Utils.getTime(), code])
                    else:
                        this.server.lastMapEditeurCode += 1
                        this.server.configs("game.lastMapCodeId", str(this.server.lastMapEditeurCode))
                        code = this.server.lastMapEditeurCode
                        this.client.room.CursorMaps.execute("insert into Maps (Code, Name, XML, YesVotes, NoVotes, Perma, Del) values (?, ?, ?, ?, ?, ?, ?)", [code, this.client.playerName, this.client.room.EMapXML, 0, 0, 22 if isTribeHouse else 0, 0])
                        this.client.updateConfig()
                    this.client.sendPacket(Identifiers.old.send.Map_Editor, ["0"])
                    this.client.enterRoom(this.server.recommendRoom(this.client.langue))
                    this.client.sendPacket(Identifiers.old.send.Map_Exported, [code])
                return

            elif CC == Identifiers.old.recv.Map.Reset_Map:
                this.client.room.EMapLoaded = 0
                return

            elif CC == Identifiers.old.recv.Map.Exit_Editor:
                this.client.sendPacket(Identifiers.old.send.Map_Editor, ["0"])
                this.client.enterRoom(this.server.recommendRoom(this.client.langue))
                return

        elif C == Identifiers.old.recv.Draw.C:
            if CC == Identifiers.old.recv.Draw.Drawing:
                if this.client.privLevel == 10:
                    this.client.room.sendAllOthers(this.client, Identifiers.old.send.Drawing_Start, values)
                return

            elif CC == Identifiers.old.recv.Draw.Point:
                if this.client.privLevel == 10:
                    this.client.room.sendAllOthers(this.client, Identifiers.old.send.Drawing_Point, values)
                return

            elif CC == Identifiers.old.recv.Draw.Clear:
                if this.client.privLevel == 10:
                    this.client.room.sendAll(Identifiers.old.send.Drawing_Clear, values)
                return

        if this.server.isDebug:
            print "[%s][OLD] Packet not implemented - C: %s - CC: %s - values: %s" %(this.client.playerName, C, CC, repr(values))

    def descriptPacket(this, packetID, packet):
        data = ByteArray()
        while packet.bytesAvailable():
            packetID += 1
            packetID %= len(this.server.packetKeys)
            data.writeUnsignedByte(packet.readUnsignedByte() ^ this.server.packetKeys[packetID])
        return data
