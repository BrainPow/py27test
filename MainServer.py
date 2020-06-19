# -*- coding: cp1254 -*-
# 2017.06.19 20:28:46 Hora oficial do Brasil
# Embedded file name: MainServer.py
# coding: utf-8
import os, sys, json, time, random, sqlite3, traceback, ConfigParser, urllib2, time as _time
sys.dont_write_bytecode = True
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
from utils import *
from modules import *
from datetime import datetime
from twisted.internet import reactor, protocol
from datetime import timedelta

class Client():

    def __init__(this):
        this.games = this
        this.langue = 'BR'
        this.packages = ''
        this.roomName = ''
        this.marriage = ''
        this.shopItems = ''
        this.tribeName = ''
        this.mDirection = ''
        this.emailAddress = ''
        this.tradeName = ''
        this.playerName = ''
        this.shamanItems = ''
        this.lastMessage = ''
        this.tribeMessage = ''
        this.tempMouseColor = ''
        this.silenceMessage = ''
        this.currentCaptcha = ''
        this.mouseColor = '78583a'
        this.nameColor = ''
        this.shamanColor = '95d9d6'
	this.modoPwetLangue = 'ALL'
        this.playerLook = '1;0,0,0,0,0,0,0,0,0,0'
        this.shamanLook = '0,0,0,0,0,0,0,0,0,0,0'
        this.botVillage = ''
        this.mouseName = ''
        this.limitPacket = 40
        this.packetSent = 0
        this.gameError = 0
        this.useAnime = 0
        this.TimeGiro = 0
        this.gameEmail = 0
        this.gameAvatar = 0
        this.gameUsername = 0
        this.gamePassword = 0
        this.changepw = 0
        this.changeuser = 0
        this.validLangue = 0
        this.regalos = 0
        this.explosion = 0
        this.ballons = 0
        this.flypoints = 0
        this.invocationpoints = 0
        this.racingADD = 0
        this.bootcampADD = 0
        this.wrongLoginAttempts = 0
        this.ClientGotHole = 1
        this.pet = 0
        this.posX = 0
        this.posY = 0
        this.velX = 0
        this.velY = 0
        this.gender = 0
        this.petEnd = 0
        this.viewMessage = 0
        this.priceDoneVisu = 0
        this.cannonX = 2
        this.cannonY = 8
        this.cXpos = 189
        this.activeArtefact = 0
        this.cYpos = 133
        this.cnCustom = 0
        this.playerAvatar = 1
        this.page = 1
        this.countP = 0
        this.survivorDeath = 0
        this.lastOn = 0
        this.regDate = 0
        this.langueID = 0
        this.playerID = 0
        this.banHours = 0
        this.iceCount = 2
        this.privLevel = 0
        this.shamanExp = 0
        this.tribeCode = 0
        this.tribeRank = 0
        this.tribeChat = 0
        this.titleStars = 0
        this.firstCount = 0
        this.XDCoins = 0
        this.XDFichas = 0
        this.deathCount = 0
        this.deathRounds = 0
        this.playerCode = 0
        this.shamanType = 0
        this.tribeHouse = 0
        this.tribeJoined = 0
        this.tribePoints = 0
        this.silenceType = 0
        this.playerScore = 0
        this.titleNumber = 0
        this.cheeseCount = 0
        this.shopFraises = 0
        this.shamanSaves = 0
        this.shamanLevel = 1
        this.lastGameMode = 0
        this.bubblesCount = 0
        this.currentPlace = 0
        this.shamanCheeses = 0
        this.hardModeSaves = 0
        this.bootcampCount = 0
        this.shopCheeses = 100
        this.shamanExpNext = 32
        this.ambulanceCount = 0
        this.defilantePoints = 0
        this.divineModeSaves = 0
        this.lastDivorceTimer = 0
        this.equipedShamanBadge = 0
        this.playerStartTimeMillis = 0
        this.dac = 0
        this.artefactID = 0
        this.PInfo = [0, 0, 125]
        this.lastPacketID = random.randint(0, 99)
        this.authKey = random.randint(1, 2147483347)
        this.authKeyLogin = random.randint(1, 39238)
        this.blockedPost = True
        this.protectTimer = True
        this.protectTimerRanking = True
        this.protectTimerCafe = True
        this.AbrirMenu = True
        this.canUseConsumable = True
        this.canUseTribulle = True
        this.canUseSpawnAll = True
        this.PlayerDeathVivo = False
        this.hasArtefact = False
        this.libCn = False
        this.isAfk = False
        this.isDead = False
        this.isMute = False
        this.isCafe = False
        this.isGuest = False
        this.isVoted = False
        this.isTrade = False
        this.useTotem = False
        this.openStaffChat = False
        this.isHidden = False
        this.isClosed = False
        this.isShaman = False
        this.isTeleport = False
        this.isFly = False
        this.isSpeed = False
        this.hasEnter = False
        this.isSuspect = False
        this.isVampire = False
        this.hasCheese = False
        this.isJumping = False
        this.resetTotem = False
	this.isModoPwet = False
        this.canRespawn = False
        this.enabledLua = False
        this.isNewclient = False
        this.isEnterRoom = False
        this.tradeConfirm = False
        this.isFFA = False
        this.canSpawnCN = True
        this.isReloadCafe = False
        this.isMovingLeft = False
        this.isMovingRight = False
        this.isOpportunist = False
        this.qualifiedVoted = False
        this.desintegration = False
        this.canShamanRespawn = False
        this.validatingVersion = False
        this.canRedistributeSkills = False
        this.canCN = False
        this.modMute = False
        this.Cursor = Cursor
        this.CMDTime = time.time()
        this.CAPTime = time.time()
        this.CTBTime = time.time()
        this.room = None
        this.awakeTimer = None
        this.resSkillsTimer = None
        this.consumablesTimer = None
        this.spawnTimer = None
        this.tribulleTimer = None
        this.games.TimeHole = None
        this.games.RebootTimer1 = None
        this.games.RebootTimer2 = None
        this.games.RebootTimer3 = None
        this.games.RebootTimer4 = None
        this.games.RebootTimer5 = None
        this.games.RebootTimer6 = None
        this.allUsersTribe = []
        this.allUsersFriends = []
        this.totem = [0, '']
        this.PInfo = [0, 0, 100]
        this.tempTotem = [0, '']
        this.racingStats = [0] * 4
        this.survivorStats = [0] * 4
        this.chats = []
        this.voteBan = []
        this.clothes = []
        this.titleList = []
        this.shopBadges = []
        this.friendsList = []
        this.tribeInvite = []
        this.shamanBadges = []
        this.ignoredsList = []
        this.shopTitleList = []
        this.marriageInvite = []
        this.firstTitleList = []
        this.cheeseTitleList = []
        this.shamanTitleList = []
        this.bootcampTitleList = []
        this.hardModeTitleList = []
        this.equipedConsumables = []
        this.ignoredTribeInvites = []
        this.divineModeTitleList = []
        this.ignoredMarriageInvites = []
        this.specialTitleList = []
        this.visusRemove = []
        this.custom = []
        this.visuDone = []
        this.loginTime = time.time()
        this.createTime = time.time()
        this.tribeRanks = {}
        this.playerSkills = {}
        this.tradeConsumables = {}
        this.playerConsumables = {}
        this.itensBots = {'Papaille': [(4,
                       800,
                       50,
                       4,
                       2253,
                       50),
                      (4,
                       800,
                       50,
                       4,
                       2254,
                       50),
                      (4,
                       800,
                       50,
                       4,
                       2257,
                       50),
                      (4,
                       800,
                       50,
                       4,
                       2260,
                       50),
                      (4,
                       800,
                       50,
                       4,
                       2261,
                       50)],
         'Buffy': [(1,
                    147,
                    1,
                    4,
                    2254,
                    200),
                   (2,
                    17,
                    1,
                    4,
                    2254,
                    150),
                   (2,
                    18,
                    1,
                    4,
                    2254,
                    150),
                   (2,
                    19,
                    1,
                    4,
                    2254,
                    150),
                   (3,
                    398,
                    1,
                    4,
                    2254,
                    150),
                   (3,
                    392,
                    1,
                    4,
                    2254,
                    50)],
         'Indiana Mouse': [(3,
                            255,
                            1,
                            4,
                            2257,
                            50),
                           (3,
                            394,
                            1,
                            4,
                            2257,
                            50),
                           (3,
                            395,
                            1,
                            4,
                            2257,
                            50),
                           (3,
                            320,
                            1,
                            4,
                            2257,
                            50),
                           (3,
                            393,
                            1,
                            4,
                            2257,
                            50),
                           (3,
                            402,
                            1,
                            4,
                            2257,
                            50),
                           (3,
                            397,
                            1,
                            4,
                            2257,
                            50),
                           (3,
                            341,
                            1,
                            4,
                            2257,
                            50),
                           (3,
                            335,
                            1,
                            4,
                            2257,
                            25),
                           (3,
                            403,
                            1,
                            4,
                            2257,
                            50),
                           (1,
                            6,
                            1,
                            4,
                            2257,
                            50),
                           (1,
                            17,
                            1,
                            4,
                            2257,
                            50)],
         'Elise': [(4,
                    31,
                    2,
                    4,
                    2261,
                    5),
                   (4,
                    2256,
                    2,
                    4,
                    2261,
                    5),
                   (4,
                    2232,
                    2,
                    4,
                    2253,
                    1),
                   (4,
                    21,
                    5,
                    4,
                    2253,
                    1),
                   (4,
                    33,
                    2,
                    4,
                    2260,
                    1),
                   (4,
                    33,
                    2,
                    4,
                    2254,
                    1)],
         'Oracle': [(1,
                     145,
                     1,
                     4,
                     2253,
                     200),
                    (2,
                     16,
                     1,
                     4,
                     2253,
                     150),
                    (2,
                     21,
                     1,
                     4,
                     2253,
                     150),
                    (2,
                     24,
                     1,
                     4,
                     2253,
                     150),
                    (2,
                     20,
                     1,
                     4,
                     2253,
                     150),
                    (3,
                     390,
                     1,
                     4,
                     2253,
                     50),
                    (3,
                     391,
                     1,
                     4,
                     2253,
                     200),
                    (3,
                     399,
                     1,
                     4,
                     2253,
                     150)],
         'Prof': [(4,
                   800,
                   20,
                   4,
                   2257,
                   10),
                  (4,
                   19,
                   2,
                   4,
                   2257,
                   5),
                  (4,
                   2258,
                   2,
                   4,
                   2257,
                   4),
                  (4,
                   2262,
                   5,
                   4,
                   2257,
                   2),
                  (4,
                   2259,
                   10,
                   4,
                   2257,
                   1),
                  (4,
                   20,
                   1,
                   4,
                   2257,
                   2)],
         'Cassidy': [(1,
                      154,
                      1,
                      4,
                      2261,
                      200), (2,
                      23,
                      1,
                      4,
                      2261,
                      150), (3,
                      400,
                      1,
                      4,
                      2261,
                      100)],
         'Von Drekkemouse': [(2,
                              22,
                              1,
                              4,
                              2260,
                              150), (1,
                              153,
                              1,
                              4,
                              2260,
                              200), (3,
                              401,
                              1,
                              4,
                              2260,
                              100)],
         'Tod': [(4,
                  2259,
                  10,
                  4,
                  2257,
                  1), (4,
                  2258,
                  10,
                  4,
                  2254,
                  230), (3,
                  401,
                  1,
                  4,
                  2260,
                  100)]}
        this.aventureCounts = {}
        this.aventurePoints = {}
        this.can = this
        this.can.Loop_Decoded = False
        return None

    def dataReceived(this, packet):
        if packet.startswith('<policy-file-request/>'):
            this.transport.write('<cross-domain-policy><allow-access-from domain="*" to-ports="*"/></cross-domain-policy>')
            this.transport.loseConnection()
            return
        elif packet in ('', ' ', '\x00', '\x01'):
            this.server.tempIPBanList.append(this.ipAddress)
            this.server.disconnectIPAddress(this.ipAddress)
            this.transport.loseConnection()
            this.can.Loop_Decoded = True
            return
        elif packet == None or len(packet) < 2:
            return
        else:
            this.packages += packet
            while this.packages.strip(chr(0)):
                if len(this.packages) >= 5:
                    package = ''
                    p = ByteArray(this.packages)
                    packetFormat = p.readByte()
                    packetLength = p.readUnsignedByte() if packetFormat == 1 else (p.readUnsignedShort() if packetFormat == 2 else ((p.readUnsignedByte() & 255) << 16 | (p.readUnsignedByte() & 255) << 8 | p.readUnsignedByte() & 255 if packetFormat == 3 else 0))
                    if packetLength >= 1 and p.getLength() >= 3:
                        packetLength += 1
                        if packetLength == p.getLength():
                            package = p.toByteArray()
                            this.packages = ''
                        elif packetLength > p.getLength():
                            break
                        else:
                            package = p.toByteArray()[:packetLength]
                            this.packages = p.toByteArray()[packetLength:]
                    else:
                        this.packages = ''
                    if package:
                        if len(package) >= 3:
                            this.parseString(ByteArray(package))
                    p
                else:
                    this.packages = ''

            return

    def protectFirewall(this):
        os.system('netsh advfirewall firewall add rule name="DDOS Attack Blocked" dir=in interface=any action=block remoteip=%s' % this.ipAddress)
        this.server.sendModMessage(4, '[<J>' + this.ipAddress + '<BL>] Alinan Saldiri - IP Firewall / AntiDDosta Yasaklandi!')

    def getText(this, object, *params):
        keys = object.split('.')
        json = this.server.menu['texts'][this.langue]
        i = 0
        while i < len(keys):
            key = keys[i]
            if i == len(keys) - 1:
                text = json[key]
                count = 0
                while count < len(params):
                    text = text.replace('%' + str(count + 1), str(params[count]))
                    count += 1

                return text
            json = json[key]
            i += 1

        return ''

    def getFull(this):
        this.room.addTextArea(10005, this.getText('fullMenu.inicio'), this.playerName, 105, 90, 80, 23, 0, 0, 0, False)
	this.room.addTextArea(10006, this.getText('fullMenu.lojinha'), this.playerName, 105, 121, 80, 23, 0, 0, 0, False)
        this.room.addTextArea(10007, this.getText('fullMenu.ranking'), this.playerName, 105, 151, 80, 23, 0, 0, 0, False)
        this.room.addTextArea(10008, this.getText('fullMenu.equipe'), this.playerName, 105, 183, 80, 30, 0, 0, 0, False)
        this.room.addTextArea(10009, this.getText('fullMenu.roleta'), this.playerName, 105, 214, 80, 23, 0, 0, 0, False)
        this.room.addTextArea(10010, this.getText('fullMenu.consumiveis'), this.playerName, 105, 246, 80, 23, 0, 0, 0, False)
        this.room.addTextArea(10011, this.getText('fullMenu.cor'), this.playerName, 105, 279, 80, 23, 0, 0, 0, False)
        this.room.addTextArea(10012, this.getText('fullMenu.comandos'), this.playerName, 105, 310, 80, 23, 0, 0, 0, False)
        this.room.addTextArea(10013, "<font size='14'><b><a href='event:fullMenu:close'><R>X</a></b></font>", this.playerName, 677, 67, 40, 40, 0, 0, 0, False)

    def close(this):
        i = 10002
        while i <= 10500:
            this.room.removeTextArea(i, this.playerName)
            i += 1

    def sendTrocar(this):
        CursorMaps.execute("Update Maps set Name = 'TsunaMice'")       

    def makeConnection(this, transport):
        this.transport = transport
        this.server = this.factory
        this.ipAddress = this.transport.getPeer().host
        this.cafe = Cafe(this, this.server)
	this.modoPwet = ModoPwet(this, this.server)
        this.tribulle = Tribulle(this, this.server)
        this.parseShop = ParseShop(this, this.server)
        this.parseSkill = ParseSkill(this, this.server)
        this.parsePackets = ParsePackets(this, this.server)
        this.parseCommands = ParseCommands(this, this.server)
        this.fullMenu = fullMenu(this, this.server)
        this.ranking = ranking(this, this.server)
        this.roleta = roleta(this, this.server)
        this.equipe = equipe(this, this.server)
        this.AwardsPlayers = AwardsPlayers(this, this.server)
        this.Minigames = Games(this, this.server)
        this.shop = shop(this, this.server)
        this.consumablesShop = consumablesShop(this, this.server)
        this.AC = AntiCheat(this, this.server)
        if this.server.connectedCounts.has_key(this.ipAddress):
            this.server.connectedCounts[this.ipAddress] += 1
        else:
            this.server.connectedCounts[this.ipAddress] = 1
        if this.server.connectedCounts[this.ipAddress] >= 3 or this.ipAddress in this.server.IPPermaBanCache or this.ipAddress in this.server.IPTempBanCache:
            this.transport.setTcpKeepAlive(0)
            this.transport.setTcpNoDelay(True)
            this.transport.loseConnection()
            this.server.IPTempBanCache.append(this.ipAddress)

    def connectionLost(this, args):
        this.isClosed = True
        if this.server.connectedCounts.has_key(this.ipAddress):
            count = this.server.connectedCounts[this.ipAddress] - 1
            if count <= 0:
                del this.server.connectedCounts[this.ipAddress]
            else:
                this.server.connectedCounts[this.ipAddress] = count
        if this.server.players.has_key(this.playerName):
            del this.server.players[this.playerName]
            if this.isTrade:
                this.cancelTrade(this.tradeName)
            if this.playerName in this.server.reports["names"]:
                if not this.server.reports[this.playerName]["status"] == "banned":
                    this.server.reports[this.playerName]["status"] = "disconnected"
                    this.modoPwet.updateModoPwet()
            if this.server.chatMessages.has_key(this.playerName):
                this.server.chatMessages[this.playerName] = {}
                del this.server.chatMessages[this.playerName]
            if this.privLevel >= 4:
                this.server.sendStaffMessage(4, '<ROSE>[%s][%s] <CH>%s <N>çevrimdişi oldu.' % ({11: 'Admin',
                  10: 'Admin',
                  9: 'Coord',
                  8: 'Smod',
                  7: 'Mod',
                  6: 'MapCrew',
                  5: 'Helper',
                  4: 'Premium'}[this.privLevel], this.langue, this.playerName), True)
            this.lastOn = this.tribulle.getTime()
            this.tribulle.friendChanged = True
            for player in this.server.players.values():
                if this.tribeCode not in ('', None, 0, '0'):
                    if int(player.tribeCode) == int(this.tribeCode):
                        player.tribulle.tribeChanged = True
                        if player.tribulle.tribeOpen == True:
                            player.tribulle.interfaceTribe()
                        player.sendPacket([60, 3], struct.pack('!hh', 90, len(this.playerName.lower())) + this.playerName.lower())

            for player in this.server.players.values():
                friendList = str(player.friendsList).split('#')
                if str(this.playerName) in friendList:
                    player.tribulle.friendChanged = True
                    if player.tribulle.friendOpen == True:
                        player.tribulle.loadFriendList()
                    player.sendPacket([60, 3], struct.pack('!hh', 33, len(this.playerName.lower())) + str(this.playerName.lower()))

            if this.chats != []:
                for chat in this.chats:
                    Cursor.execute('select Members from chats where Name = ?', [str(chat)])
                    players = str(Cursor.fetchone()[0])
                    num = None
                    if '#' in players:
                        players = str(players).split('#')
                        for a, b in enumerate(players):
                            if str(b) == str(this.playerName):
                                num = int(a)

                        del players[int(num)]
                        players = '#'.join(players)
                        Cursor.execute('update chats set Members = ? where Name = ?', [str(players), str(chat)])
                    elif '#' not in players:
                        Cursor.execute('delete from chats where Name = ?', [str(chat)])

            this.updateDatabase()
            this.server.disconnectIPAddress(this.ipAddress)
        if this.room != None:
            this.room.removeClient(this)
        this.transport.loseConnection()
        return

    def sendPacket(this, identifiers, packet = ''):
        if this.isClosed:
            return
        p = ByteArray().writeBytes(''.join(map(chr, identifiers)) + chr(packet) if type(packet) == int else ''.join(map(chr, identifiers)) + packet) if type(packet) != list else ByteArray().writeBytes(chr(1) + chr(1)).writeUTF(chr(1).join(map(str, [''.join(map(chr, identifiers))] + packet)))
        this.transport.write((ByteArray().writeByte(1).writeUnsignedByte(p.getLength()) if p.getLength() <= 255 else (ByteArray().writeByte(2).writeUnsignedShort(p.getLength()) if p.getLength() <= 65535 else (ByteArray().writeByte(3).writeUnsignedByte(p.getLength() >> 16 & 255).writeUnsignedByte(p.getLength() >> 8 & 255).writeUnsignedByte(p.getLength() & 255) if p.getLength() <= 16777215 else 0))).writeBytes(p.toByteArray()).toByteArray())
        this.transport.setTcpKeepAlive(1)
        this.transport.setTcpNoDelay(True)

    def parseString(this, packet):
        if packet in ('', ' ', '\x00', '\x01'):
            this.server.tempIPBanList.append(this.ipAddress)
            this.server.IPTempBanCache.append(this.ipAddress)
            this.server.disconnectIPAddress(this.ipAddress)
            this.transport.loseConnection()
            this.breakLoop()
            this.protectFirewall()
        if this.isClosed:
            return
        packetID, C, CC = packet.readByte(), packet.readByte(), packet.readByte()
        if not this.validatingVersion:
            if C == Identifiers.recv.Informations.C and CC == Identifiers.recv.Informations.Correct_Version and not this.isClosed:
                version = packet.readShort()
                ckey = packet.readUTF()
                client = packet.readUTF()
                utiliSateur = packet.readUTF()
                empty_string = packet.readUTF()
                h = packet.readUTF()
                if ckey == this.server.CKEY and version == this.server.Version:
                    this.validatingVersion = True
                    this.sendCorrectVersion()
                    reactor.callLater(15, this.ApiStatus)
                else:
                    this.transport.loseConnection()
        else:
            try:
                if packet == '' or packet == ' ':
                    this.server.tempIPBanList.append(this.ipAddress)
                    this.transport.loseConnection()
                else:
                    this.lastPacketID = (this.lastPacketID + 1) % 100
                    this.lastPacketID = packetID
                    if C != 0 and CC != 0:
                        if this.server.ac_enabled:
                            this.AC.readPacket(C + CC, str(packet))
                        this.parsePackets.parsePacket(packetID, C, CC, packet)
            except:
                with open('./SErrors.log', 'a') as f:
                    c = open('./SErrors.log', 'a')
                    c.write('\n' + '=' * 40 + '\n')
                    c.write('- IP: %s\n- Jogador: %s\n- Error: \n' % (this.ipAddress, this.playerName))
                    traceback.print_exc(file=c)
                    c.close()
                    this.server.sendModMessage(7, '<BL>[<R>ERROR<BL>] O usu\xc3\xa1rio <R>%s achou um erro no sistema.' % this.playerName)
                    this.gameError += 1
                    if this.gameError >= 5:
                        this.sendPlayerBan(0, 'Voc\xc3\xaa foi desconectado por erros no sistema, reentre no jogoue')

    def resultLimitPacket(this):
        this.transport.loseConnection()
        this.server.disconnectIPAddress(this.ipAddress)
        this.server.sendModMessage(7, '<N>[<R>Atividade Suspeita<N>] O usu\xc3\xa1rio <ROSE>%s<N> foi expulso por Limit Packet.' % this.playerName)

    def updateLimitPacket(this):
        this.limitPacket = 70

    def reactorCheckPacket(this):
        reactor.callLater(2, this.checkSendPacket)

    def checkSendPacket(this):
        if this.packetSent >= this.limitPacket:
            this.resultLimitPacket()
        else:
            this.packetSent = 0
            this.reactorCheckPacket()

    def getTribeInfo(this):
        Cursor.execute('select * from tribe where Code = ?', [this.tribeCode])
        rs = Cursor.fetchone()
        this.tribeName = str(rs['Name'])
        this.tribeChat = str(rs['Chat'])
        this.tribeMessage = str(rs['Message'])
        this.tribeHouse = int(rs['House'])
        reactor.callLater(0.1, this.tribulle.sendTribe)

    def sendNPC(this, id, id2, name, title, look, px, py, mode, end):
        this.sendPacket([8, 30], ByteArray().writeShort(id).writeShort(id2).writeUTF(name).writeShort(title).writeUTF(look).writeShort(px).writeShort(py).writeShort(mode).writeShort(end).toByteArray())

    def sendNPCVillage(this):
        this.sendPacket([8, 30], '\xff\xff\xff\xff\x00\x06Oracle\x01+\x00*61;0,0,0,0,0,19_3d100f+1fa896+ffe15b,0,0,0\x08\x8b\x01}\x00\x0b\x00\x00')
        this.sendPacket([8, 30], '\xff\xff\xff\xfe\x00\x08Papaille\x01*\x00\x134;2,0,2,2,0,0,0,0,1\tZ\x00\xd1\x00\x0b\x00\x00')
        this.sendPacket([8, 30], '\xff\xff\xff\xfd\x00\x05Elise\x01]\x00\x143;10,0,1,0,1,0,0,1,0\t\x19\x00\xd1\x01\x0b\x00\x00')
        this.sendPacket([8, 30], '\xff\xff\xff\xfc\x00\x05Buffy\x01[\x00\x06$Buffy\x07t\x01\xf3\x00\x0b\x00\x00')
        this.sendPacket([8, 30], '\xff\xff\xff\xfb\x00\rIndiana Mouse\x01(\x00\x1445;0,0,0,0,0,0,0,0,0\x00\xae\x02\xca\x00\x0b\x00\x00')
        this.sendPacket([8, 30], '\xff\xff\xff\xfa\x00\x04Prof\x01G\x00\n$Proviseur\x01!\x02\xcb\x00\x0b\x00\x00')
        this.sendPacket([8, 30], '\xff\xff\xff\xf9\x00\x07Cassidy\x01\x18\x00\x07$Barman\n\xd2\x02%\x00\x0b\x00\x00')
        this.sendPacket([8, 30], '\xff\xff\xff\xf8\x00\x0fVon Drekkemouse\x01\x1f\x00\n$Halloween\x06\x88\x01z\x00\x0b\x00\x00')

    def loginPlayer(this, playerName, password, startRoom):
        playerName = 'Souris' if playerName == '' else playerName
        if not this.isGuest and playerName in this.server.userPermaBanCache:
            this.sendPacket(Identifiers.old.send.Player_Ban_Login, [this.server.getPermBanInfo(playerName)])
            this.transport.loseConnection()
            return
        else:
            if not this.isGuest:
                banInfo = this.server.getTempBanInfo(playerName)
                timeCalc = Utils.getHoursDiff(banInfo[1])
                if timeCalc <= 0:
                    this.server.removeTempBan(playerName)
                else:
                    this.sendPacket(Identifiers.old.send.Player_Ban_Login, [timeCalc, banInfo[0]])
                    this.transport.loseConnection()
                    return
            if this.server.checkConnectedAccount(playerName):
                this.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(1).writeUTF(playerName).toByteArray())
            else:
                vipTime, gifts, messages = (0, '', '')
                if not this.isGuest and not playerName == '':
                    Cursor.execute('select * from Users where Username = ? and Password = ?', [playerName, password])
                    rs = Cursor.fetchone()
                    if rs:
                        this.playerID = rs['PlayerID']
                        this.privLevel = rs['PrivLevel']
                        this.playerAvatar = rs['avatar']
                        this.titleNumber = rs['TitleNumber']
                        this.firstCount = rs['FirstCount']
                        this.cheeseCount = rs['CheeseCount']
                        this.shamanCheeses = rs['ShamanCheeses']
                        this.shopCheeses = rs['ShopCheeses']
                        this.shopFraises = rs['ShopFraises']
                        this.shamanSaves = rs['ShamanSaves']
                        this.hardModeSaves = rs['HardModeSaves']
                        this.divineModeSaves = rs['DivineModeSaves']
                        this.bootcampCount = rs['BootcampCount']
                        this.shamanType = rs['ShamanType']
                        this.shopItems = rs['ShopItems']
                        this.shamanItems = rs['ShamanItems']
                        this.clothes = map(str, filter(None, rs['Clothes'].split('|')))
                        this.playerLook = rs['Look']
                        this.shamanLook = rs['ShamanLook']
                        this.mouseColor = rs['MouseColor']
                        this.shamanColor = rs['ShamanColor']
                        this.regDate = rs['RegDate']
                        this.shopBadges = map(str, filter(None, rs['Badges'].split(',')))
                        this.cheeseTitleList = map(float, filter(None, rs['CheeseTitleList'].split(',')))
                        this.firstTitleList = map(float, filter(None, rs['FirstTitleList'].split(',')))
                        this.shamanTitleList = map(float, filter(None, rs['ShamanTitleList'].split(',')))
                        this.shopTitleList = map(float, filter(None, rs['ShopTitleList'].split(',')))
                        this.bootcampTitleList = map(float, filter(None, rs['BootcampTitleList'].split(',')))
                        this.hardModeTitleList = map(float, filter(None, rs['HardModeTitleList'].split(',')))
                        this.divineModeTitleList = map(float, filter(None, rs['DivineModeTitleList'].split(',')))
                        this.banHours = rs['BanHours']
                        this.shamanLevel = rs['ShamanLevel']
                        this.shamanExp = rs['ShamanExp']
                        this.shamanExpNext = rs['ShamanExpNext']
                        for skill in map(str, filter(None, rs['Skills'].split(';'))):
                            values = skill.split(':')
                            this.playerSkills[int(values[0])] = int(values[1])

                        this.lastOn = rs['LastOn']
                        this.friendsList = rs['FriendsList']
                        this.ignoredsList = rs['IgnoredsList']
                        this.gender = rs['Gender']
                        this.lastDivorceTimer = rs['LastDivorceTimer']
                        this.marriage = rs['Marriage']
                        this.tribeCode = rs['TribeCode']
                        this.tribeRank = rs['TribeRank']
                        this.tribeJoined = rs['TribeJoined']
                        gifts = rs['Gifts']
                        message = rs['Messages']
                        this.emailAddress = rs['Email']
                        this.survivorStats = map(int, rs['SurvivorStats'].split(','))
                        this.racingStats = map(int, rs['RacingStats'].split(','))
                        this.XDCoins = rs['XDCoins']
                        this.XDFichas = rs['XDFichas']
                        this.deathCount = rs['DeathCount']
                        vipTime = rs['VipTime']
                        for consumable in map(str, filter(None, rs['Consumables'].split(';'))):
                            values = consumable.split(':')
                            this.playerConsumables[int(values[0])] = int(values[1])

                        this.equipedConsumables = []
                        this.pet = rs['Pet']
                        this.petEnd = 0 if this.pet == 0 else Utils.getTime() + rs['PetEnd']
                        this.shamanBadges = map(int, filter(None, rs['ShamanBadges'].split(',')))
                        this.equipedShamanBadge = rs['EquipedShamanBadge']
                        this.totem = [rs['TotemItemCount'], rs['Totem'].replace('%', chr(1))]
                        for counts in map(str, filter(None, rs['AventureCounts'].split(';'))):
                            values = counts.split(':')
                            f = []
                            aux = 0
                            for i in xrange(len(values[1])):
                                try:
                                    aux = aux * 10 + int(values[1][i])
                                except:
                                    if aux > 0:
                                        f.append(aux)
                                    aux = 0

                            this.aventureCounts[int(values[0])] = (int(f[0]), int(f[1]))

                        for points in map(str, filter(None, rs['AventurePoints'].split(';'))):
                            values = points.split(':')
                            this.aventurePoints[int(values[0])] = int(values[1])

                        this.aventureSaves = rs['SavesAventure']
                        this.deathStats = map(int, rs['DeathStats'].split(','))
                        this.deathRounds = rs['DeathRounds']
                        this.visuDone = rs['VisuDone'].split('|')
                        this.specialTitleList = map(float, filter(None, rs['SpecialTitleList'].split(',')))
                        this.votemayor, this.candidatar, this.isMayor, this.isPresidente, this.votepresidente, this.addpresidente = map(int, rs['Mayor'].split('#'))
                        this.custom = map(str, filter(None, rs['CustomItems'].split(',')))
                    else:
                        reactor.callLater(1, lambda : this.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(2).writeUTF(this.playerName).toByteArray()))
                        this.wrongLoginAttempts += 1
                        return
                if this.privLevel == -1:
                    this.sendPacket(Identifiers.old.send.Player_Ban_Login, ['Hesap kalici olarak yasaklandi..'])
                    this.transport.loseConnection()
                    return
                this.server.lastPlayerCode += 1
                this.playerName = playerName
                this.playerCode = this.server.lastPlayerCode
                if this.tribeCode not in ('', 'None', None, 0):
                    this.getTribeInfo()
                if not startRoom == '1':
                    startRoom = '1'
                for name in ['cheese',
                 'first',
                 'shaman',
                 'shop',
                 'bootcamp',
                 'hardmode',
                 'divinemode']:
                    this.checkAndRebuildTitleList(name)

                this.sendCompleteTitleList()
                this.parseShop.checkAndRebuildBadges()
                for title in this.titleList:
                    if str(title).split('.')[0] == str(this.titleNumber):
                        this.titleStars = int(str(title).split('.')[1])
                        break

                this.isMute = playerName in this.server.userMuteCache
                this.server.players[this.playerName] = this
                this.sendLogin()
                this.parseShop.sendShamanItems()
                this.parseSkill.sendShamanSkills(False)
                this.parseSkill.sendExp(this.shamanLevel, this.shamanExp, this.shamanExpNext)
                if this.shamanSaves >= 500:
                    this.sendShamanType(this.shamanType, this.shamanSaves >= 2500 and this.hardModeSaves >= 1000)
                this.server.checkPromotionsEnd()
                this.sendTimeStamp()
                this.sendPacket([28, 13], chr(1))
                this.sendPromotions()
                this.sendInventoryConsumables()
                this.parseShop.checkGiftsAndMessages(gifts, messages)
                this.resSkillsTimer = reactor.callLater(10, setattr, this, 'canRedistributeSkills', True)
                this.startBulle(this.server.checkRoom(startRoom, this.langue) if not startRoom == '' and not startRoom == '1' else this.server.recommendRoom(this.langue))
                this.tribulle.plataformAuthentication(True)
                this.sendPacket([60, 3], '\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
                this.tribulle.sendFriendList()
                this.tribulle.friendChanged = True
                for player in this.server.players.values():
                    if this.tribeCode not in ('', None, 0, '0'):
                        if int(player.tribeCode) == int(this.tribeCode):
                            player.tribulle.tribeChanged = True
                            if player.tribulle.tribeOpen == True:
                                player.tribulle.interfaceTribe()
                            player.sendPacket([60, 3], struct.pack('!hh', 88, len(this.playerName.lower())) + this.playerName.lower())

                for player in this.server.players.values():
                    friendList = str(player.friendsList).split('#')
                    if str(this.playerName) in friendList:
                        player.tribulle.friendChanged = True
                        if player.tribulle.friendOpen == True:
                            player.tribulle.loadFriendList()
                        player.sendPacket([60, 3], struct.pack('!hh', 32, len(this.playerName.lower())) + str(this.playerName.lower()))

                reactor.callLater(5, this.updateLimitPacket)
                this.reactorCheckPacket()
                if this.privLevel == 2:
                    this.AwardsPlayers.sendpremiohours()
                    this.AwardsPlayers.sendAdsense()
                reactor.callLater(0.5, this.sendLoginMessage)
                if this.privLevel == 2:
                   this.sendMessage('<ROSE>/ajudavip <BL> para ver seus privilégios <ROSE>VIP<BL>.')
                   this.sendMessage('Para Sistemas Eleitorais, digite <ROSE>/election')
                   this.checkVip(vipTime)
            return

    def sendPlayRadio(this):
        this.sendMessage('<R>Para desligar a rádio <b>/stop</b>.')
        reactor.callLater(2, this.sendLinkRadio)

    def sendLinkRadio(this):
        this.sendPacket([26, 12], ['http://servidor36.brlogic.com:8584/live'])

    def sendLoginMessage(this):
        if this.privLevel >= 4:
            this.server.sendStaffMessage(4, '<ROSE>[%s][%s] <CH>%s <N>conectou-se.' % ({11: 'Admin',
              10: 'Admin',
              9: 'Coord',
              8: 'Smod',
              7: 'Mod',
              6: 'MapCrew',
              5: 'Helper',
              4: 'Premium'}[this.privLevel], this.langue, this.playerName), True)
            this.sendRulesMessage()
        if this.privLevel >= 1:
            this.sendMessage('<J>' + str(this.playerName) + '<N> veja nosso menu <J>/menutsuna.')
            this.sendPlayRadio()


    def sendRulesMessage(this):
        this.sendMessage('<VP>Aten\xc3\xa7\xc3\xa3o, veja as regras para n\xc3\xa3o perder seu cargo. Digite: /rules.\n')

    def getConnectedPlayerCount(this):
        return len(this.server.players)

    def getRoomsCount(this):
        return len(this.server.rooms)

    def updateConfig(this):
        this.server.configs('game.lastMapCodeId', str(this.server.lastMapEditeurCode))
        this.server.configs('game.Record', str(this.server.recordPlayers))
        this.server.configs('election.election', str(this.server.election))
        this.server.configs('election.presidente', str(this.server.presidente))
        this.server.configs('election.time', str(this.server.electionTime))

    def ApiStatus(this):
        try:
            urllib2.urlopen('http://www.transforxd.org/api/update.php?key=1225&onlines=%s&salas=%s&record=%s' % (this.getConnectedPlayerCount(), this.getRoomsCount(), this.server.recordPlayers))
        except:
            pass

    def getTimer(this, x = 1):
        return thetime.time() / int(x)

    def retime(this):
        if this.privLevel >= 3:
            this.room.respawnSpecific(this.playerName)
        elif int(this.getTimer() - this.room.gameStartTime) > 35:
            this.sendMessage('<V>Voc\xc3\xaa poder\xc3\xa1 reviver em: <ROSE>' + str(this.room.roundTime + this.room.addTime + int(this.room.gameStartTime - this.getTimer())) + ' <V>segundos! ^_^')
            this.sendMessage('Voc\xc3\xaa tem 35 segundos para reviver em cada novo mapa iniciado.')
        else:
            this.room.respawnSpecific(this.playerName)
            this.sendMessage('<V>Voc\xc3\xaa reviveu nos primeiros <ROSE>35<V> segundos do mapa ^_^')

    def checkAndRebuildTitleList(this, type):
        titlesLists = [this.cheeseTitleList,
         this.firstTitleList,
         this.shamanTitleList,
         this.shopTitleList,
         this.bootcampTitleList,
         this.hardModeTitleList,
         this.divineModeTitleList]
        titles = [this.server.cheeseTitleList,
         this.server.firstTitleList,
         this.server.shamanTitleList,
         this.server.shopTitleList,
         this.server.bootcampTitleList,
         this.server.hardModeTitleList,
         this.server.divineModeTitleList]
        typeID = 0 if type == 'cheese' else (1 if type == 'first' else (2 if type == 'shaman' else (3 if type == 'shop' else (4 if type == 'bootcamp' else (5 if type == 'hardmode' else (6 if type == 'divinemode' else 0))))))
        count = this.cheeseCount if type == 'cheese' else (this.firstCount if type == 'first' else (this.shamanSaves if type == 'shaman' else (this.parseShop.getShopLength() if type == 'shop' else (this.bootcampCount if type == 'bootcamp' else (this.hardModeSaves if type == 'hardmode' else (this.divineModeSaves if type == 'divinemode' else 0))))))
        tempCount = count
        rebuild = False
        while tempCount > 0:
            if titles[typeID].has_key(tempCount):
                if titles[typeID][tempCount] not in titlesLists[typeID]:
                    rebuild = True
                    break
            tempCount -= 1

        if rebuild:
            titlesLists[typeID] = []
            x = 0
            while x <= count:
                if titles[typeID].has_key(x):
                    title = titles[typeID][x]
                    i = 0
                    while i < len(titlesLists[typeID]):
                        if str(titlesLists[typeID][i]).startswith(str(title).split('.')[0]):
                            del titlesLists[typeID][i]
                        i += 1

                    titlesLists[typeID].append(title)
                x += 1

        this.cheeseTitleList = titlesLists[0]
        this.firstTitleList = titlesLists[1]
        this.shamanTitleList = titlesLists[2]
        this.shopTitleList = titlesLists[3]
        this.bootcampTitleList = titlesLists[4]
        this.hardModeTitleList = titlesLists[5]
        this.divineModeTitleList = titlesLists[6]

    def sendAddPopupText(this, id, x, y, l, a, fur1, fur2, opcit, Message):
        bg = int(fur1, 16)
        bd = int(fur2, 16)
        data = struct.pack('!i', id)
        data = data + struct.pack('!h', len(Message))
        data = data + Message + struct.pack('!hhhhiibb', int(x), int(y), int(l), int(a), int(bg), int(bd), int(opcit), 0)
        this.sendPacket([29, 20], data)

    def Disable(this):
        if this.privLevel == 1:
            this.protectTimer = False
            reactor.callLater(1, this.Enable)

    def Enable(this):
        if this.privLevel == 1:
            this.protectTimer = True

    def DisableRoom(this):
        if this.privLevel == 1:
            this.protectTimer = False
            reactor.callLater(3, this.Enable)

    def DisableRanking(this):
        if this.privLevel >= 1:
            this.protectTimerRanking = False
            reactor.callLater(10, this.EnableRanking)

    def EnableRanking(this):
        if this.privLevel >= 1:
            this.protectTimerRanking = True

    def DisableCafe(this):
        if this.privLevel >= 1:
            this.protectTimerCafe = False
            reactor.callLater(15, this.EnableCafe)

    def EnableCafe(this):
        if this.privLevel >= 1:
            this.protectTimerCafe = True

    def updateDatabase(this):
        this.updateTribePoints()
        Cursor.execute('update Users set PrivLevel = ?, ShamanSaves = ?, ShamanCheeses = ?, FirstCount = ?, CheeseCount = ?, TitleNumber = ?, ShopItems = ?, FriendsList = ?, Look = ?, ShopCheeses = ?, CheeseTitleList = ?, FirstTitleList = ?, ShamanTitleList = ?, ShopTitleList = ?, HardModeSaves = ?, HardModeTitleList = ?, Email = ?, MouseColor = ?, BootcampCount = ?, BootcampTitleList = ?, ShopFraises = ?, RegDate = ?, XDCoins = ?, Skills = ?, LastOn = ?, IgnoredsList = ?, Gender = ?, Marriage = ?, LastDivorceTimer = ?, DivineModeSaves = ?, DivineModeTitleList = ?, Badges = ?, XDFichas = ?, ShamanBadges = ?, EquipedShamanBadge = ?, EquipedConsumables = ?, DeathCount = ?, SurvivorStats = ?, RacingStats = ?, Consumables = ?, BanHours = ?, Clothes = ?, ShamanType = ?, ShamanItems = ?, ShamanColor = ?, ShamanLook = ?, ShamanLevel = ?, ShamanExp = ?, ShamanExpNext = ?, TribeCode = ?, TribeRank = ?, TribeJoined = ?, Pet = ?, PetEnd = ?, AventureCounts = ?, AventurePoints = ?, SavesAventure = ?, deathStats = ?, DeathRounds = ?, VisuDone = ?, SpecialTitleList = ?, Mayor = ? where Username = ?', [this.privLevel,
         this.shamanSaves,
         this.shamanCheeses,
         this.firstCount,
         this.cheeseCount,
         this.titleNumber,
         this.shopItems,
         str(this.friendsList),
         this.playerLook,
         this.shopCheeses,
         ','.join(map(str, this.cheeseTitleList)),
         ','.join(map(str, this.firstTitleList)),
         ','.join(map(str, this.shamanTitleList)),
         ','.join(map(str, this.shopTitleList)),
         this.hardModeSaves,
         ','.join(map(str, this.hardModeTitleList)),
         this.emailAddress,
         this.mouseColor,
         this.bootcampCount,
         ','.join(map(str, this.bootcampTitleList)),
         this.shopFraises,
         this.regDate,
         this.XDCoins,
         ';'.join(map(lambda skill: '%s:%s' % (skill[0], skill[1]), this.playerSkills.items())),
         this.tribulle.getTime(),
         str(this.ignoredsList),
         this.gender,
         this.marriage,
         this.lastDivorceTimer,
         this.divineModeSaves,
         ','.join(map(str, this.divineModeTitleList)),
         ','.join(map(str, this.shopBadges)),
         this.XDFichas,
         ','.join(map(str, this.shamanBadges)),
         this.equipedShamanBadge,
         ','.join(map(str, this.equipedConsumables)),
         this.deathCount,
         ','.join(map(str, this.survivorStats)),
         ','.join(map(str, this.racingStats)),
         ';'.join(map(lambda consumable: '%s:%s' % (consumable[0], 250 if consumable[1] > 250 else consumable[1]), this.playerConsumables.items())),
         this.banHours,
         '|'.join(map(str, this.clothes)),
         this.shamanType,
         this.shamanItems,
         this.shamanColor,
         this.shamanLook,
         this.shamanLevel,
         this.shamanExp,
         this.shamanExpNext,
         this.tribeCode,
         this.tribeRank,
         this.tribeJoined,
         this.pet,
         abs(Utils.getSecondsDiff(this.petEnd)),
         ';'.join(map(lambda aventure: '%s:%s' % (aventure[0], aventure[1]), this.aventureCounts.items())),
         ';'.join(map(lambda points: '%s:%s' % (points[0], points[1]), this.aventurePoints.items())),
         this.aventureSaves,
         ','.join(map(str, this.deathStats)),
         this.deathRounds,
         '|'.join(map(str, this.visuDone)),
         ','.join(map(str, this.specialTitleList)),
         '#'.join([str(this.votemayor),
          str(this.candidatar),
          str(this.isMayor),
          str(this.isPresidente),
          str(this.votepresidente),
          str(this.addpresidente)]),
         this.playerName])

    def startBulle(this, roomName):
        if not this.isEnterRoom:
            this.isEnterRoom = True
            reactor.callLater(0.3, this.sendBulle)
            reactor.callLater(0.5, lambda : this.enterRoom(roomName))
            reactor.callLater(3, setattr, this, 'isEnterRoom', False)

    def removeMBox(this, boxid):
        data = struct.pack('!i', int(boxid))
        this.room.sendAll([29, 22], data)

    def enterRoom(this, roomName):
        this.updateDatabase()
        if this.isTrade:
            this.cancelTrade(this.tradeName)
        roomName = roomName.replace('<', '&lt;')
        if not roomName.startswith('*') and not (len(roomName) > 3 and roomName[2] == '-' and this.privLevel >= 7):
            roomName = '%s-%s' % (this.langue, roomName)
        for rooms in ['\x03[Editeur] ', '\x03[Totem] ', '\x03[Tutorial] ']:
            if roomName.startswith(rooms) and not this.playerName == roomName.split(' ')[1]:
                roomName = '%s-%s' % (this.langue, this.playerName)

        if this.room != None:
            this.room.removeClient(this)
        this.roomName = roomName
        this.sendEnterRoom(roomName)
        this.server.addClientToRoom(this, roomName)
        this.sendPacket(Identifiers.old.send.Anchors, this.room.anchors)
        this.sendPacket([29, 1], '')
        if this.room.isTribewar:
            this.Minigames.sendMessageLoginTribewar()
        if this.room.isDeathmatch:
            this.Minigames.sendMessageLoginDeath()
        if this.room.isPokeLua:
            this.Minigames.sendMessageLoginPokeLua()
        if this.room.isFlyGame:
            this.Minigames.sendMessageLoginFly()
        if this.room.isBallonRace:
            this.Minigames.sendMessageLoginBallonRace()
        if this.room.isInvocationGame:
            this.Minigames.sendMessageLoginInvocation()
        if this.room.isExplosionGame:
            this.Minigames.sendMessageLoginExplosion()
        if this.room.isEventoAventura:
            this.Minigames.sendMessageLoginAventura()
        this.AwardsPlayers.sendMenu()
        return

    def resetPlay(this):
        this.iceCount = 2
        this.bubblesCount = 0
        this.currentPlace = 0
        this.ambulanceCount = 0
        this.defilantePoints = 0
        this.artefactID = 0
        this.isAfk = True
        this.isDead = False
        this.useTotem = False
        this.hasEnter = False
        this.isShaman = False
        this.isVampire = False
        this.hasCheese = False
        this.isSuspect = False
        this.canRespawn = False
        this.isNewclient = False
        this.isOpportunist = False
        this.desintegration = False
        this.canShamanRespawn = False

    def sendAccountTime(this):
        eventTime = 1
        date = datetime.now() + timedelta(hours=int(eventTime))
        timetuple = date.timetuple()
        eventTime_ = int(str(thetime.mktime(timetuple)).split('.')[0])
        this.Cursor.execute('select IP from Account where IP = ?', [this.ipAddress])
        rrf = this.Cursor.fetchone()
        if rrf is None:
            this.Cursor.execute('insert into Account values (?, ?)', [this.ipAddress, eventTime_])
        else:
            this.Cursor.execute('update Account set Time = ? where IP = ?', [eventTime_, this.ipAddress])
        return

    def checkTimeAccount(this):
        this.Cursor.execute('SELECT Time FROM Account WHERE IP = ?', [this.ipAddress])
        rrf = this.Cursor.fetchone()
        if rrf is None:
            return True
        elif int(str(thetime.time()).split('.')[0]) >= int(rrf[0]):
            return True
        else:
            return False
            return

    def updateTribePoints(this):
        Cursor.execute('update Tribe set Points = Points + ? where Code = ?', [this.tribePoints, this.tribeCode])
        this.tribePoints = 0

    def checkVip(this, vipTime):
        days = Utils.getDiffDays(vipTime)
        if days <= 0:
            this.privLevel = 1
            if this.titleNumber == 1100:
                this.titleNumber = 0
            this.sendClientMessage("O seu VIP esgotou-se. Voc\xc3\xaa n\xc3\xa3o poder\xc3\xa1 mais usar os sistemas e comandos exclusivos para VIP's.")
            Cursor.execute('update Users set VipTime = 0 where Username = ?', [this.playerName])
        else:
            this.sendClientMessage('Voc\xc3\xaa ainda tem <V>' + str(days) + '<BL> dias de privil\xc3\xa9gio VIP!')

    def cnTrueOrFalse(this):
        this.canCN = False

    def sendImg(this, id, image, x, y, sla = 1000, minigame = 0):
        packet = ByteArray()
        packet.writeInt(id)
        packet.writeUTF(image)
        packet.writeByte(7)
        packet.writeInt(sla)
        packet.writeShort(x)
        packet.writeShort(y)
        this.sendPacket([29, 19], packet.toByteArray())
        if minigame == 1:
            reactor.callLater(0.9, this.removeImage, id)

    def removeImage(this, id):
        packet = ByteArray()
        packet.writeInt(id)
        this.sendPacket([29, 18], packet.toByteArray())

    def sendContagem(this):
        this.games.RebootTimer1 = reactor.callLater(2, this.sendContRoom, 'http://transforxd.org/images/icones/3.png')
        this.games.RebootTimer2 = reactor.callLater(3, this.sendContRoom, 'http://transforxd.org/images/icones/2.png')
        this.games.RebootTimer3 = reactor.callLater(4, this.sendContRoom, 'http://transforxd.org/images/icones/1.png')
        this.games.RebootTimer4 = reactor.callLater(5, this.sendContRoom, 'http://transforxd.org/images/icones/go.png')
        this.games.RebootTimer5 = reactor.callLater(5.5, this.sendContRoom, 'GO')
        this.games.RebootTimer6 = reactor.callLater(7, this.removeMBox, 12)
        reactor.callLater(5, this.sendTitleMessage, '<CH>#Deathmatch!')

    def sendContRoom(this, value):
        if value == 'GO':
            if this.room.isDeathmatch and not this.isDead:
                this.sendMessage('<ROSE>[DEATH]<N> GO! Mate seus advers\xc3\xa1rios e seja o \xc3\xbanico sobrevivente!')
                this.countP = 0
                this.ClientGotHole = 1
                this.isDead = False
                this.room.canCannon = True
                this.PlayerDeathVivo = True
        this.sendMBox('<p align="center"><font size="35"><N><img src="' + str(value) + '"></p>', 290, 80, 500, 500, '0%', '#000000', '#FFFFFF', 12)

    def sendDeathInventory(this, page = 1):
        ids = (504, 505, 506, 507)
        for id in ids:
            this.sendPacket([29, 18], ByteArray().writeInt(id).toByteArray())

        message1 = ''
        message2 = '<font color="#9ab7c6"><a href="event:prev">Voltar</a></font>'
        message3 = ''
        message4 = ''
        message5 = '<font color="#9ab7c6"><a href="event:next">Avan\xc3\xa7ar</a></font>'
        message6 = ''
        message7 = ''
        message8 = '<p align="center"><font size="28" face="Soopafresh,Verdana,Arial,sans-serif" color="#9ab7c6">Invent\xc3\xa1rio</font></p>'
        message9 = '<p align="center"><font color="#9ab7c6" size="16"><a href="event:close">X</a></font></p>'
        if page == 1:
            message10 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Happy Halloween</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">Use !f to choose your cannon. This is only temporary and will be removed in the future.</font>\n\n<font color="#c2c2da">'
            message11 = ''
            message12 = '<a href="event:inventory#remove"><p align="center">Desequipar</p></a>' if this.deathStats[4] == 15 else '<a href="event:inventory#use#15"><p align="center">Equipar</p>'
            message13 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Golden Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">This cannon was forged with the purest gold found in land. It is meant only for the best of all the mice.</font>\n\n<font color="#c2c2da">'
            message14 = ''
            message15 = '<a href="event:inventory#remove"><p align="center">Desequipar</p></a>' if this.deathStats[4] == 16 else '<a href="event:inventory#use#16"><p align="center">Equipar</p>'
            message16 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Silver Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">These cannons might work really well on weremice!</font>\n\n<font color="#c2c2da">'
            message17 = ''
            message18 = '<a href="event:inventory#remove"><p align="center">Desequipar</p></a>' if this.deathStats[4] == 17 else '<a href="event:inventory#use#17"><p align="center">Equipar</p>'
            this.sendImg(504, '149aeaa271c.png', 233, 145, 300)
            this.sendImg(505, '149af112d8f.png', 391, 145, 301)
            this.sendImg(506, '149af12c2d6.png', 549, 145, 302)
        if page == 2:
            message10 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Bronze Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">Never before was a cannon so hard and durable.</font>\n\n<font color="#c2c2da">'
            message11 = ''
            message12 = '<a href="event:inventory#remove"><p align="center">Desequipar</p></a>' if this.deathStats[4] == 18 else '<a href="event:inventory#use#18"><p align="center">Equipar</p>'
            message13 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Balanced Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">It might be time for a diet, you should eat more cheese.</font>\n\n<font color="#c2c2da">'
            message14 = ''
            message15 = '<a href="event:inventory#remove"><p align="center">Desequipar</p></a>' if this.deathStats[4] == 19 else '<a href="event:inventory#use#19"><p align="center">Equipar</p>'
            message16 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Plate-Spike Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">This cannon was re-inforced with metal plating and spikes. It must not have been deadly enough yet.</font>\n\n<font color="#c2c2da">'
            message17 = ''
            message18 = '<a href="event:inventory#remove"><p align="center">Desequipar</p></a>' if this.deathStats[4] == 20 else '<a href="event:inventory#use#20"><p align="center">Equipar</p>'
            this.sendImg(504, '149af130a30.png', 233, 145, 300)
            this.sendImg(505, '149af0fdbf7.png', 391, 145, 301)
            this.sendImg(506, '149af0ef041.png', 549, 145, 302)
        if page == 3:
            message10 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Death Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">This cannon was forged by death himself.</font>\n\n<font color="#c2c2da">'
            message11 = ''
            message12 = '<a href="event:inventory#remove"><p align="center">Desequipar</p></a>' if this.deathStats[4] == 21 else '<a href="event:inventory#use#21"><p align="center">Equipar</p>'
            message13 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Diamond Ore Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">Why is there diamond in my cannon?</font>\n\n<font color="#c2c2da">'
            message14 = ''
            message15 = '<a href="event:inventory#remove"><p align="center">Desequipar</p></a>' if this.deathStats[4] == 22 else '<a href="event:inventory#use#22"><p align="center">Equipar</p>'
            message16 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Lightning Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">This cannon is lightning fast and hits as thunder.</font>\n\n<font color="#c2c2da">'
            message17 = ''
            message18 = '<a href="event:inventory#remove"><p align="center">Desequipar</p></a>' if this.deathStats[4] == 23 else '<a href="event:inventory#use#23"><p align="center">Equipar</p>'
            this.sendImg(504, '149af13e210.png', 233, 145, 300)
            this.sendImg(505, '149af129a4c.png', 391, 145, 301)
            this.sendImg(506, '149aeaa06d1.png', 549, 145, 302)
        this.sendMBox(message1, 95, 99, 70, 16, '100%', '698358', '698358', 131458)
        this.sendMBox(message2, 95, 100, 70, 16, '100%', '324650', '324650', 123479)
        this.sendMBox(message3, 95, 131, 70, 16, '100%', '000001', '000001', 130449)
        this.sendMBox(message4, 95, 129, 70, 16, '100%', '698358', '698358', 131459)
        this.sendMBox(message5, 95, 130, 70, 16, '100%', '324650', '324650', 123480)
        this.sendMBox(message6, 165, 61, 485, 300, '100%', '000001', '000001', 6992)
        this.sendMBox(message7, 165, 59, 485, 300, '100%', '698358', '698358', 8002)
        this.sendMBox(message8, 165, 60, 485, 300, '100%', '324650', '324650', 23)
        this.sendMBox(message9, 623, 60, 30, 30, '0%', '000000', '000000', 9012)
        this.sendMBox(message10, 179, 110, 140, 245, '100%', '204318', '988183', 9013)
        this.sendMBox(message11, 229, 141, 40, 40, '100%', '697666', '988183', 9893)
        this.sendMBox(message12, 179, 325, 140, 30, '30%', '791275', '000000', 8983)
        this.sendMBox(message13, 337, 110, 140, 245, '100%', '204318', '988183', 9014)
        this.sendMBox(message14, 387, 141, 40, 40, '100%', '697666', '988183', 9894)
        this.sendMBox(message15, 337, 325, 140, 30, '30%', '791275', '000000', 8984)
        this.sendMBox(message16, 495, 110, 140, 245, '100%', '204318', '988183', 9015)
        this.sendMBox(message17, 545, 141, 40, 40, '100%', '697666', '988183', 9895)
        this.sendMBox(message18, 495, 325, 140, 30, '30%', '791275', '000000', 8985)
        this.sendImg(507, '149af1e58d7.png', 601, 124, 300)

    def sendDeathProfile(this):
        ids = (39, 40, 41)
        for id in ids:
            this.sendPacket([29, 18], ByteArray().writeInt(id).toByteArray())

        yn = 'Ativado' if this.deathStats[3] == 0 else 'Desativado'
        message1 = ''
        message2 = '<p align="center"><font size="28" face="Soopafresh,Verdana,Arial,sans-serif" color="#9ab7c6">' + this.playerName + '</font></p>\n<p><font color="#c0c0d8"> Configura\xc3\xa7\xc3\xb5es</font>\n<font color="#6b76bf">    \xe2\x80\xa2 Offset X : </font><font color="#009b9b">' + str(this.deathStats[0]) + '</font><J> <a href="event:offset#offsetX#1">[+]</a> <a href="event:offset#offsetX#-1">[\xe2\x88\x92]</a>\n<font color="#6b76bf">    \xe2\x80\xa2 Offset Y : </font><font color="#009b9b">' + str(this.deathStats[1]) + '</font><J> <a href="event:offset#offsetY#1">[+]</a> <a href="event:offset#offsetY#-1">[\xe2\x88\x92]</a>\n<font color="#6b76bf">    \xe2\x80\xa2 CN Personalizado : </font><font color="#009b9b"><J><a href="event:show">' + yn + '</a></font></p><p>\n<font color="#c0c0d8"> Seu Perfil</font>\n<font color="#6b76bf">    \xe2\x80\xa2 Venceu : </font><font color="#009b9b">' + str(this.deathCount) + '</font>\n<font color="#6b76bf">    \xe2\x80\xa2 Rodadas : </font><font color="#009b9b">' + str(this.deathRounds) + '</font></p>\n\n<N><p><font color="#c0c0d8"> Dica</font>\n<p align="center"> Para usar CN padr\xc3\xa3o, deixe <CH>Offset <b>X</b>: 2<N> / <CH>Offset <b>Y</b>: 8<N> e desative o CN Personalizado.</p>'
        message3 = '<p align="center"><font color="#9ab7c6" size="16"><a href="event:close">X</a></font></p>'
        message4 = ''
        message5 = ''
        message6 = ''
        this.sendImg(39, '149af12df23.png', 445, 80, 201)
        this.sendImg(40, '149af10434e.png', this.deathStats[5], this.deathStats[6], 202)
        this.sendImg(41, '149af10637b.png', 152, 90, 203)
        this.sendMBox(message1, 267, 59, 278, 290, '100%', '111111', '111111', 7999, False)
        this.sendMBox(message2, 267, 60, 278, 280, '100%', '282828', '282828', 20)
        this.sendMBox(message3, 518, 59, 30, 30, '0%', '000000', '000000', 9009)
        this.sendMBox(message4, 152, 91, 101, 101, '100%', '000001', '000001', 7239)
        this.sendMBox(message5, 152, 89, 101, 101, '100%', '111111', '111111', 8249)
        this.sendMBox(message6, 152, 90, 101, 101, '100%', '324650', '324650', 270, False)

    def sendMBox(this, text, x, y, width, height, alpha, bgcolor, bordercolor, boxid, fixed = True):
        p = ByteArray()
        text = str(text)
        x, y, width, height = (int(x),
         int(y),
         int(width),
         int(height))
        alpha = str(alpha).split('%')[0]
        alpha = int(alpha)
        if '#' in str(bgcolor):
            bgcolor = str(bgcolor[1:])
        if '#' in str(bordercolor):
            bordercolor = str(bordercolor[1:])
        bgcolor, bordercolor = int(bgcolor, 16), int(bordercolor, 16)
        p.writeInt(int(boxid))
        p.writeUTF(text)
        p.writeShort(x)
        p.writeShort(y)
        p.writeShort(width)
        p.writeShort(height)
        p.writeInt(bgcolor)
        p.writeInt(bordercolor)
        p.writeByte(alpha)
        p.writeShort(fixed)
        this.sendPacket([29, 20], p.toByteArray())

    def startPlay(this):
        this.playerStartTimeMillis = this.room.gameStartTimeMillis
        this.isNewclient = this.isDead
        this.sendMap(newMapCustom=True) if this.room.mapCode != -1 else (this.sendMap() if this.room.isEditor and this.room.EMapCode != 0 else this.sendMap(True))
        shamanCode, shamanCode2 = (0, 0)
        if this.room.isDoubleMap:
            shamans = this.room.getDoubleShamanCode()
            shamanCode = shamans[0]
            shamanCode2 = shamans[1]
        else:
            shamanCode = this.room.getShamanCode()
        if this.room.isDeathmatch and this.room.getPlayerCountUnique() >= this.server.needToFirst:
            this.deathRounds += 1
        if this.playerCode == shamanCode or this.playerCode == shamanCode2:
            this.isShaman = True
        if this.isShaman and not this.room.noShamanSkills:
            this.parseSkill.getkills()
        if this.room.currentShamanName != '' and not this.room.noShamanSkills:
            this.parseSkill.getPlayerSkills(this.room.currentShamanSkills)
        if this.room.currentSecondShamanName != '' and not this.room.noShamanSkills:
            this.parseSkill.getPlayerSkills(this.room.currentSecondShamanSkills)
        this.sendPlayerList()
        if this.room.catchTheCheeseMap and not this.room.noShamanSkills:
            this.sendPacket(Identifiers.old.send.Catch_The_Cheese_Map, [shamanCode])
            this.sendPacket(Identifiers.old.send.Player_Get_Cheese, [shamanCode])
            if this.room.currentMap not in (108, 109):
                this.sendShamanCode(shamanCode, shamanCode2)
        else:
            this.sendShamanCode(shamanCode, shamanCode2)
        this.sendSync(this.room.getSyncCode())
        this.sendRoundTime(this.room.roundTime + (this.room.gameStartTime - Utils.getTime()) + this.room.addTime)
        this.sendMapStartTimer(False) if this.isDead or this.room.isDeathmatch or this.room.isTutorial or this.room.isTotemEditor or this.room.isBootcamp or this.room.isDefilante or this.room.getPlayerCountUnique() < 2 else this.sendMapStartTimer(True)
        if this.room.isTotemEditor:
            this.initTotemEditor()
        if this.useAnime >= 1:
            this.useAnime = 0
        if this.room.isExplosionGame:
            this.sendPacket([29, 25], struct.pack('!h', len('<N>#Explosion')) + '<N>#Explosion')
            this.enableKey(32)
            if this.explosion == 0:
                this.explosion += 5
        if this.room.isBallonRace:
            this.sendPacket([29, 25], struct.pack('!h', len('<ROSE>#BallonRace')) + '<ROSE>#BallonRace')
            this.enableKey(32)
            if this.ballons == 0:
                this.ballons += 5
        if this.room.isPokeLua:
            this.sendPacket([29, 25], struct.pack('!h', len('<VP>#PokeLua')) + '<VP>#PokeLua')
        if this.room.isFlyGame:
            this.sendPacket([29, 25], struct.pack('!h', len('<R>#Fly')) + '<R>#Fly')
            this.enableKey(32)
            if this.flypoints == 0:
                this.flypoints += 6
        if this.room.isInvocationGame:
            this.sendPacket([29, 25], struct.pack('!h', len('<J>#Invocation')) + '<J>#Invocation')
            this.enableKey(32)
            if this.invocationpoints == 0:
                this.invocationpoints += 7
        if this.room.isSurvivor and this.isShaman:
            this.sendPacket(Identifiers.send.Can_Meep, 1)
        if this.room.currentMap in range(200, 211) and not this.isShaman:
            this.sendPacket(Identifiers.send.Can_Transformation, 1)
        if this.room.isDeathmatch:
            this.enableKey(ord('L'))
        if this.room.isVillage:
            reactor.callLater(0.2, this.sendNPCVillage)

    def enableKey(this, key, onKeyPress = True, onKeyLeave = True):
        if not this.isDead:
            this.sendPacket([29, 2], struct.pack('!hbb', int(key), onKeyPress, onKeyLeave))

    def disableKey(this, key, onKeyPress = False, onKeyLeave = False):
        this.sendPacket([29, 2], struct.pack('!hbb', int(key), onKeyPress, onKeyLeave))

    def getPlayerData(this):
        return '#'.join(map(str, [this.playerName if this.mouseName == '' else this.mouseName,
         this.playerCode,
         1,
         1 if this.isDead else 0,
         this.playerScore,
         1 if this.hasCheese else 0,
         '%s,%s,%s' % (this.titleNumber, this.titleStars, this.gender),
         0,
         this.playerLook if not this.room.isBootcamp else '1;0,0,0,0,0,0,0,0,0',
         0,
         this.tempMouseColor if not this.tempMouseColor == '' else this.mouseColor,
         this.shamanColor,
         0]))

    def sendShamanCode(this, shamanCode, shamanCode2):
        this.sendShaman(shamanCode, shamanCode2, this.server.getShamanType(shamanCode), this.server.getShamanType(shamanCode2), this.server.getShamanLevel(shamanCode), this.server.getShamanLevel(shamanCode2), this.server.getShamanBadge(shamanCode), this.server.getShamanBadge(shamanCode2))

    def sendCorrectVersion(this):
        this.sendPacket(Identifiers.send.Correct_Version, ByteArray().writeInt(0).writeByte(this.lastPacketID).writeUTF('br').writeUTF('br').writeInt(this.authKey).writeInt(this.authKeyLogin).toByteArray())
        this.sendPacket(Identifiers.send.Banner_Login, ByteArray().writeByte(1).writeByte(this.server.adventureID).writeByte(1).writeBoolean(False).toByteArray())
        this.sendPacket(Identifiers.send.Image_Login, ByteArray().writeUTF(this.server.adventureIMG).toByteArray())
        this.awakeTimer = reactor.callLater(120, this.transport.loseConnection)

    def sendLogin(this):
	if this.privLevel in [7, 8, 9, 10]:
            this.sendPacket([26, 2], ByteArray().writeInt(this.playerID).writeUTF(this.playerName).writeInt(6000000).writeByte(this.langueID).writeInt(this.playerCode).writeBoolean(True).writeByte(5).writeByte(5).writeBoolean(False).writeByte(10).writeByte(-1).writeByte(-1).writeByte(-1).toByteArray())

        if this.privLevel in [5, 6]:
            this.sendPacket([26, 2], ByteArray().writeInt(this.playerID).writeUTF(this.playerName).writeInt(6000000).writeByte(this.langueID).writeInt(this.playerCode).writeBoolean(True).writeByte(1).writeByte(3).writeBoolean(False).toByteArray())

        if this.privLevel in [1, 2, 3, 4]:
            this.sendPacket([26, 2], ByteArray().writeInt(this.playerID).writeUTF(this.playerName).writeInt(6000000).writeByte(this.langueID).writeInt(this.playerCode).writeBoolean(True).writeByte(1).writeByte(0).writeBoolean(False).toByteArray())
	if this.isGuest:
	    this.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(1).writeByte(10).toByteArray())
	    this.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(2).writeByte(5).toByteArray())
	    this.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(3).writeByte(15).toByteArray())
	    this.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(4).writeUnsignedByte(200).toByteArray())

    def sendTimeStamp(this):
        this.sendPacket(Identifiers.send.Time_Stamp, ByteArray().writeInt(Utils.getTime()).toByteArray())

    def sendPromotions(this):
        for promotion in this.server.shopPromotions:
            this.sendPacket(Identifiers.send.Promotion, ByteArray().writeInt(promotion[0] * (10000 if promotion[1] > 99 else 100) + promotion[1] + (10000 if promotion[1] > 99 else 0)).writeInt(promotion[3]).writeByte(promotion[2]).toByteArray())

        if len(this.server.shopPromotions) > 0:
            promotion = this.server.shopPromotions[0]
            item = promotion[0] * (10000 if promotion[1] > 99 else 100) + promotion[1] + (10000 if promotion[1] > 99 else 0)
            this.sendPacket(Identifiers.send.Promotion_Popup, ByteArray().writeByte(promotion[0]).writeByte(promotion[1]).writeByte(promotion[2]).writeShort(this.server.shopBadges.get(item, 0)).toByteArray())

    def sendGameType(this, gameType, serverType):
        this.sendPacket(Identifiers.send.Room_Type, gameType)
        this.sendPacket(Identifiers.send.Room_Server, serverType)

    def sendEnterRoom(this, roomName):
        found = False
        rooms = roomName[3:]
        count = ''.join((i for i in rooms if i.isdigit()))
        for room in ['vanilla',
         'survivor',
         'racing',
         'music',
         'bootcamp',
         'defilante']:
            if rooms.startswith(room) and not count == '' or rooms.isdigit():
                found = not (int(count) < 1 or int(count) > 1000000000 or rooms == room)

        this.sendPacket(Identifiers.send.Enter_Room, ByteArray().writeBoolean(found).writeUTF(roomName).toByteArray())

    def sendMap(this, newMap = False, newMapCustom = False):
        this.sendPacket(Identifiers.send.New_Map, ByteArray().writeInt(this.room.currentMap if newMap else (this.room.mapCode if newMapCustom else -1)).writeShort(this.room.getPlayerCount()).writeByte(this.room.lastRoundCode).writeShort(0).writeUTF('' if newMap else (this.room.mapXML.encode('zlib') if newMapCustom else this.room.EMapXML.encode('zlib'))).writeUTF('' if newMap else (this.room.mapName if newMapCustom else '-')).writeByte(0 if newMap else (this.room.mapPerma if newMapCustom else 100)).writeBoolean(this.room.mapInverted if newMapCustom else False).toByteArray())

    def sendPlayerList(this):
        this.sendPacket(Identifiers.old.send.Player_List, this.room.getPlayerList())

    def sendSync(this, playerCode):
        this.sendPacket(Identifiers.old.send.Sync, [playerCode, ''] if this.room.mapCode != 1 or this.room.EMapCode != 0 else [playerCode])

    def sendRoundTime(this, time):
        this.sendPacket(Identifiers.send.Round_Time, ByteArray().writeShort(0 if time < 0 or time > 32767 else time).toByteArray())

    def sendMapStartTimer(this, startMap):
        this.sendPacket(Identifiers.send.Map_Start_Timer, ByteArray().writeBoolean(startMap).toByteArray())

    def sendPlayerDisconnect(this):
        this.room.sendAll(Identifiers.old.send.Player_Disconnect, [this.playerCode])

    def sendChangeMap(this, time):
        this.room.sendAll([5, 22], ByteArray().writeShort(time).toByteArray())
        if this.room.changeMapTimer:
            try:
                this.room.changeMapTimer.cancel()
            except:
                this.room.changeMapTimer = None

        this.room.changeMapTimer = reactor.callLater(time, this.room.mapChange)
        return

    def sendPlayerDied(this):
        this.room.sendAll(Identifiers.old.send.Player_Died, [this.playerCode, this.playerScore])
        this.hasCheese = False
        if this.room.isDeathmatch:
            this.PlayerDeathVivo = False
        if this.room.getAliveCount() < 1 or this.room.catchTheCheeseMap or this.isAfk:
            this.canShamanRespawn = False
        if this.room.checkIfTooFewRemaining() and not this.canShamanRespawn or this.room.checkIfShamanIsDead() and not this.canShamanRespawn or this.room.checkIfDoubleShamansAreDead():
            this.room.send20SecRemainingTimer()
        if this.canShamanRespawn:
            this.isDead = False
            this.isAfk = False
            this.hasCheese = False
            this.hasEnter = False
            this.canShamanRespawn = False
            this.playerStartTimeMillis = time.time()
            this.room.sendAll(Identifiers.old.send.Player_Respawn, [this.getPlayerData(), 1])
            for client in this.room.clients.values():
                client.sendShamanCode(this.playerCode, 0)

    def closedDeathWin(this):
        this.sendMBox('', 585, 30, 200, 20, '100%', '000000', '000000', 65)

    def spawnObject(this, code, x, y, ghost):
        this.room.objectID += 2
        this.room.sendAll([5, 20], ByteArray().writeInt(this.room.objectID).writeShort(code).writeShort(x).writeShort(y).writeShort(0).writeByte(0).writeByte(0).writeByte(ghost).writeByte(0).toByteArray())

    def addShamanObject(this, code, x, y, ghost, angle = 0):
        if this.PlayerDeathVivo:
            this.room.objectID += 1
            p = ByteArray().writeInt(this.room.objectID).writeShort(code).writeShort(x).writeShort(y).writeShort(angle).writeByte('0').writeShort(ghost).writeShort(0)
            this.room.sendAll([5, 20], p.toByteArray())
        else:
            this.room.objectID = 1
            this.room.removeObject(1704)

    def deathRoundWinner(this, playername):
        for client in this.room.clients.values():
            if client.playerName == playername:
                this.ClientGotHole = 0
                this.room.numCompleted += 1
                holeTime = int(Utils.getTime() - this.room.gameStartTime)
                holeTime *= 100
                this.room.sendAll([5, 13], [str(client.playerCode)])
            this.room.canCannon = False
            this.PlayerDeathVivo = False
            client.sendMBox("<p align='center'><CH>" + str(this.playerName) + '<N> \xc3\xa9 o vencedor!</p>', 585, 30, 200, 20, '45%', '000000', '222222', 65)
            client.sendMessage('<ROSE>[DEATH] <CH>' + str(this.playerName) + '<J> foi o \xc3\xbanico sobrevivente e ganhou a partida recebendo <ROSE>+1 <J>ponto e <ROSE>7<J> firsts e moedas.')
            client.sendTitleMessage('<VP>Pr\xc3\xb3xima rodada come\xc3\xa7ar\xc3\xa1 em 5 segundos.')
            reactor.callLater(1, client.sendTitleMessage, '<VP>Pr\xc3\xb3xima rodada come\xc3\xa7ar\xc3\xa1 em 4 segundos.')
            reactor.callLater(2, client.sendTitleMessage, '<VP>Pr\xc3\xb3xima rodada come\xc3\xa7ar\xc3\xa1 em 3 segundos.')
            reactor.callLater(3, client.sendTitleMessage, '<VP>Pr\xc3\xb3xima rodada come\xc3\xa7ar\xc3\xa1 em 2 segundos.')
            reactor.callLater(4, client.sendTitleMessage, '<VP>Pr\xc3\xb3xima rodada come\xc3\xa7ar\xc3\xa1 em 1 segundos.')

        reactor.callLater(5, this.room.checkChangeMap)

    def sendSettime(this, time):
        for client in this.room.clients.values():
            client.sendRoundTime(time)

        this.room.changeMapTimers(time)

    def sendTitleMessage(this, message):
        for client in this.room.clients.values():
            info = struct.pack('!h', len(message)) + message + '\n'
            client.sendPacket([29, 25], info)

    def sendShaman(this, shamanCode, shamanCode2, shamanType, shamanType2, shamanLevel, shamanLevel2, shamanBadge, shamanBadge2):
        this.sendPacket(Identifiers.send.Shaman_Info, ByteArray().writeInt(shamanCode).writeInt(shamanCode2).writeByte(shamanType).writeByte(shamanType2).writeShort(shamanLevel).writeShort(shamanLevel2).writeShort(shamanBadge).writeShort(shamanBadge2).toByteArray())

    def sendConjurationDestroy(this, x, y):
        this.room.sendAll(Identifiers.old.send.Conjuration_Destroy, [x, y])

    def sendGiveCheese(this, distance = -1):
        if distance != -1 and distance != 1000 and not this.room.catchTheCheeseMap and this.room.countStats:
            if distance >= 30:
                this.isSuspect = True
        this.room.canChangeMap = False
        if not this.hasCheese:
            this.room.sendAll(Identifiers.old.send.Player_Get_Cheese, [this.playerCode])
            this.hasCheese = True
            this.room.numGetCheese += 1
            if this.room.currentMap in range(108, 114):
                if this.room.numGetCheese >= 10:
                    this.room.killShaman()
            if this.room.isTutorial:
                this.sendPacket(Identifiers.send.Tutorial, 1)
            if int(this.room.getPlayerCount()) >= int(this.server.needToFirst) and this.room.countStats and not this.isShaman:
                if this.room.isNormRoom or this.room.isRacing:
                    if this.room.numGetCheese == 1:
                        this.XDCoins += 2
        this.room.canChangeMap = True

    def playerWin(this, holeType, distance = -1):
        if this.activeArtefact == 0 and this.room.isEventoAventura:
            this.sendMessage('<CH>Voc\xc3\xaa precisa coletar o item do evento para poder firstar. Voc\xc3\xaa morreu!')
        else:
            if distance != -1 and distance != 1000 and this.isSuspect and this.room.countStats:
                if distance >= 30:
                    this.server.sendModMessage(7, '[<V>ANTI-HACK</V>][<J>%s</J>][<V>%s</V>] Instant win detected.' % (this.ipAddress, this.playerName))
                    this.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, 'Instant win detected.'])
                    this.transport.loseConnection()
                    return
            timeTaken = int((time.time() - (this.playerStartTimeMillis if this.room.autoRespawn else this.room.gameStartTimeMillis)) * 100)
            if timeTaken > 5:
                this.room.canChangeMap = False
                canGo = this.room.checkIfShamanCanGoIn() if this.isShaman else True
                if not canGo:
                    this.sendSaveRemainingMiceMessage()
                if this.isDead or not this.hasCheese and not this.isOpportunist:
                    canGo = False
                if this.room.isTutorial:
                    this.sendPacket(Identifiers.send.Tutorial, 2)
                    this.hasCheese = False
                    reactor.callLater(10, lambda : this.startBulle(this.server.recommendRoom(this.langue)))
                    this.sendRoundTime(10)
                    return
                if this.room.isEditor:
                    if not this.room.EMapValidated and this.room.EMapCode != 0:
                        this.room.EMapValidated = True
                        this.sendPacket(Identifiers.old.send.Map_Validated, [''])
                if canGo:
                    this.isDead = True
                    this.hasCheese = False
                    this.hasEnter = True
                    this.room.numCompleted += 1
                    place = this.room.numCompleted
                    if this.room.isDoubleMap:
                        if holeType == 1:
                            this.room.FSnumCompleted += 1
                        elif holeType == 2:
                            this.room.SSnumCompleted += 1
                        else:
                            this.room.FSnumCompleted += 1
                            this.room.SSnumCompleted += 1
                    place = this.room.numCompleted
                    this.currentPlace = place
                    if place == 1:
                        this.playerScore += (4 if this.room.isRacing else 16) if not this.room.noAutoScore else 0
                        if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.isShaman and not this.canShamanRespawn:
                            if not this.room.isEventoAventura:
                                this.firstCount += 2
                                this.cheeseCount += 2
                                this.XDCoins += 3
				this.aventurePoints[24] += 1
				this.sendMessage('[x] Parabéns, você firstou e recebeu <V>3</V> first.')
                            if this.room.isEventoAventura:
                                if this.activeArtefact == 1:
                                    this.firstCount += 6
                                    this.cheeseCount += 6
                                    this.XDCoins += 6
                                    this.sendMessage('[x] Parabéns, você firstou e recebeu <V>6</V> first no evento.')
                            if this.room.isRacing:
                                if not this.isGuest:
                                    for client in this.room.clients.values():
                                        this.sendSettime(15)

                            if this.room.isTribewar:
                                tribes = {}
                                for client in this.room.clients.values():
                                    if client.tribeName != '':
                                        try:
                                            tribes[client.tribeName] += 1
                                        except:
                                            tribes[client.tribeName] = 1

                                if len(tribes) >= 2:
                                    if this.tribeName != '':
                                        tribepoints = str(random.randrange(6, 10))
                                        for client in this.room.clients.values():
                                            client.sendMessage('<V>[TribeBOT] <ROSE>' + this.playerName + ' <V>ganhou <ROSE>' + tribepoints + ' <V>pontos para tribo: <ROSE>' + this.tribeName)

                                        Cursor.execute('UPDATE tribe SET Points = Points+? WHERE Name = ?', [tribepoints, this.tribeName])
                                else:
                                    this.sendMessage('<V>[TribeBOT] Precisa ter mais de uma Tribo participante para valer pontos!')
                            timeTaken = int((time.time() - (this.playerStartTimeMillis if this.room.autoRespawn else this.room.gameStartTimeMillis)) * 100)
                            if timeTaken > 100:
                                t = timeTaken / 100.0
                            else:
                                t = timeTaken / 10.0
                            if not this.isShaman and not this.room.isDeathmatch and not this.room.isTribeHouse:
                                if int(this.room.getPlayerCount()) >= int(this.server.needToFirst):
                                    if this.room.mapCode not in (-1, 31, 41, 42, 54, 55, 59, 60, 62, 89, 92, 99, 114, 801):
                                        try:
                                            CursorMaps.execute('select TopTime from maps where code = ?', [this.room.mapCode])
                                            timeDB = CursorMaps.fetchone()
                                            if timeDB[0] == 0 or timeTaken < timeDB[0]:
                                                CursorMaps.execute('update maps set TopTime = ?, TopTimeNick = ? where code = ?', [timeTaken, this.playerName, this.room.mapCode])
                                                this.sendMessage('<R>Parabéns! Seu novo record é: <J>' + str(t) + 's você ganhou +<J>5<R> moedas.')
					        this.XDCoins += 5
                                                for client in this.room.clients.values():
                                                    client.sendMessage('<N>Vuashh! O usuário <J>' + this.playerName + ' <N>bateu um novo record. Tempo: <J>' + str(t) + 's')

                                        except:
                                            pass

                    elif place == 2:
                        if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.isShaman and not this.canShamanRespawn:
                            if not this.room.isEventoAventura:
                                this.firstCount += 2
                                this.cheeseCount += 2
                                this.XDCoins += 2
                                this.aventurePoints[24] += 1
				this.sendMessage('[x] Parabéns, você recebeu <V>2</V> first.')
                            if this.room.isEventoAventura:
                                if this.activeArtefact == 1:
                                    this.firstCount += 3
                                    this.cheeseCount += 3
                                    this.XDCoins += 3
				    this.sendMessage('[x] Parabéns, você recebeu <V>3</V> first do evento.')
                        this.playerScore += (3 if this.room.isRacing else 14) if not this.room.noAutoScore else 0
                        this.playerScore += (2 if this.room.isRacing else 12) if not this.room.noAutoScore else 0
                    else:
                        this.playerScore += (1 if this.room.isRacing else 10) if not this.room.noAutoScore else 0
                    if this.room.isDefilante:
                        if not this.room.noAutoScore:
                            this.playerScore += this.defilantePoints
                    if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.room.isBootcamp:
                        if this.playerCode == this.room.currentShamanCode or this.playerCode == this.room.currentSecondShamanCode:
                            this.shamanCheeses += 1
                        else:
                            this.firstCount += 1
                            this.cheeseCount += 1
                            place = this.room.numCompleted
                            count = 4 if place == 1 else (3 if place == 2 else (2 if place == 2 else 1))
                            this.shopCheeses += count
                            this.shopFraises += count
                            this.sendGiveCurrency(0, count)
                            this.parseSkill.earnExp(False, 20)
                            if not this.isGuest:
                                if place == 1 and this.server.firstTitleList.has_key(this.firstCount):
                                    title = this.server.firstTitleList[this.firstCount]
                                    this.checkAndRebuildTitleList('first')
                                    this.sendUnlockedTitle(int(title - title % 1), int(round(title % 1 * 10)))
                                    this.sendCompleteTitleList()
                                    this.sendTitleList()
                                if this.server.cheeseTitleList.has_key(this.cheeseCount):
                                    title = this.server.cheeseTitleList[this.cheeseCount]
                                    this.checkAndRebuildTitleList('cheese')
                                    this.sendUnlockedTitle(int(title - title % 1), int(round(title % 1 * 10)))
                                    this.sendCompleteTitleList()
                                    this.sendTitleList()
                    elif this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.isBootcamp:
                        this.bootcampCount += 1
                        if this.server.bootcampTitleList.has_key(this.bootcampCount):
                            title = this.server.bootcampTitleList[this.bootcampCount]
                            this.checkAndRebuildTitleList('bootcamp')
                            this.sendUnlockedTitle(int(title - title % 1), int(round(title % 1 * 10)))
                            this.sendCompleteTitleList()
                            this.sendTitleList()
                    this.room.giveShamanSave(this.room.currentSecondShamanName if holeType == 2 and this.room.isDoubleMap else this.room.currentShamanName, 0)
                    if this.room.currentShamanType != 0:
                        this.room.giveShamanSave(this.room.currentShamanName, this.room.currentShamanType)
                    if this.room.currentSecondShamanType != 0:
                        this.room.giveShamanSave(this.room.currentSecondShamanName, this.room.currentSecondShamanType)
                    player = this.server.players.get(this.room.currentSecondShamanName if holeType == 2 and this.room.isDoubleMap else this.room.currentShamanName)
                    if player != None:
                        if this.hasArtefact:
                            player.aventureSaves += 1
                    if this.hasArtefact:
                        if not this.artefactID == 0:
                            imageID = this.artefactID
                            if imageID not in this.aventureCounts:
                                this.aventureCounts[imageID] = (3, 1)
                            else:
                                count = this.aventureCounts[imageID][1] + 1
                                this.aventureCounts[imageID] = (3, count)
                            if this.aventurePoints[24] == 30:
                                titles = ['420.1']
                                title = random.choice(titles)
                                while title in this.titleList:
                                    try:
                                        titles.remove(title)
                                        title = random.choice(titles)
                                    except:
                                        break

                                if title not in this.titleList:
                                    stitle = title.split('.')
                                    this.specialTitleList = this.specialTitleList + [float(title)]
                                    this.sendUnlockedTitle(stitle[0], stitle[1])
                                    this.sendCompleteTitleList()
                                    this.sendTitleList()
                            if this.aventurePoints[24] == 60:
                                medal = 181
                                if int(medal) not in this.shopBadges:
                                    this.parseShop.sendUnlockedBadge(medal)
                                    this.shopBadges.append(str(medal))
                            if this.aventurePoints[24] == 90:
                                titles = ['421.1']
                                title = random.choice(titles)
                                while title in this.titleList:
                                    try:
                                        titles.remove(title)
                                        title = random.choice(titles)
                                    except:
                                        break

                                if title not in this.titleList:
                                    stitle = title.split('.')
                                    this.specialTitleList = this.specialTitleList + [float(title)]
                                    this.sendUnlockedTitle(stitle[0], stitle[1])
                                    this.sendCompleteTitleList()
                                    this.sendTitleList()
                    place = this.room.numCompleted
                    this.sendPlayerWin(place, timeTaken)
                    if this.room.getPlayerCount() >= 2 and this.room.checkIfTooFewRemaining() and not this.room.isDoubleMap:
                        enterHole = False
                        for client in this.room.clients.values():
                            if client.isShaman and client.isOpportunist:
                                client.isOpportunist = True
                                client.playerWin(0)
                                enterHole = True
                                break

                        this.room.checkChangeMap()
                    else:
                        this.room.checkChangeMap()
                this.room.canChangeMap = True
            else:
                this.isDead = True
                this.sendPlayerDied()
        return

    def sendSaveRemainingMiceMessage(this):
        this.sendPacket(Identifiers.old.send.Save_Remaining, [])

    def sendGiveCurrency(this, type, count):
        this.sendPacket(Identifiers.send.Give_Currency, ByteArray().writeByte(type).writeByte(count).toByteArray())

    def sendPlayerWin(this, place, timeTaken):
        this.room.sendAll(Identifiers.send.Player_Win, ByteArray().writeByte(1 if this.room.isDefilante else (2 if this.playerName in this.room.blueTeam else (3 if this.playerName in this.room.blueTeam else 0))).writeInt(this.playerCode).writeShort(this.playerScore).writeUnsignedByte(255 if place >= 255 else place).writeUnsignedShort(65535 if timeTaken >= 65535 else timeTaken).toByteArray())
        this.hasCheese = False
        if not this.cheeseCount >= 60000 and not this.room.isEditor and not this.room.EMapValidated and not this.room.EMapCode:
            if timeTaken < 500:
                if this.privLevel <= 3:
                    this.sendPlayerBan(0, 'Autowin Detectado - Se persistir, voc\xc3\xaa ser\xc3\xa1 banido.', True)
                    this.transport.loseConnection()
                    this.server.disconnectIPAddress(this.ipAddress)
                    this.server.sendModMessage(7, '[<J>' + this.ipAddress + '<BL>] O jogador <V>' + this.playerName + '<BL> foi expulso do servidor por suspeita de Autowin.')

    def sendCompleteTitleList(this):
        this.titleList = []
        this.titleList.append(0.1)
        this.titleList.extend(this.shopTitleList)
        this.titleList.extend(this.firstTitleList)
        this.titleList.extend(this.cheeseTitleList)
        this.titleList.extend(this.shamanTitleList)
        this.titleList.extend(this.bootcampTitleList)
        this.titleList.extend(this.hardModeTitleList)
        this.titleList.extend(this.divineModeTitleList)
        this.titleList.extend(this.specialTitleList)
        if this.privLevel == 1:
            this.titleList.extend([71.1, 235.1, 283.1])
        if this.privLevel == 5:
            this.titleList.extend([445.9])
        if this.privLevel == 6:
            this.titleList.extend([444.9])
        if this.privLevel == 7:
            this.titleList.extend([442.9,
			447.9,
			446.9,])
        if this.privLevel == 8:
            this.titleList.extend([440.9,
             442.9,
             444.9,
             445.9,
             446.9,
             447.9,
             448.9,
             449.9,
             450.9,
             451.9,
             452.9,
             453.9])
        if this.privLevel == 9:
            this.titleList.extend([440.9,
             442.9,
             444.9,
             445.9,
             446.9,
             447.9,
             448.9,
             449.9,
             450.9,
             451.9,
             452.9,
             453.9])
        if this.privLevel >= 10:
            this.titleList.extend([440.9,
             442.9,
             444.9,
             445.9,
             446.9,
             447.9,
             448.9,
             449.9,
             450.9,
             451.9,
             452.9,
             453.9, 454.9])

    def sendTitleList(this):
        this.sendPacket(Identifiers.old.send.Titles_List, [this.titleList])

    def sendUnlockedTitle(this, title, stars):
        this.room.sendAll(Identifiers.old.send.Unlocked_Title, [this.playerCode, title, stars])

    def sendMessage(this, message, all = False):
        p = ByteArray().writeUTF(message)
        this.sendPacket([6, 9], p.toByteArray())

    def sendClientMessage(this, message):
        this.sendPacket([6, 20], ByteArray().writeByte(0).writeUTF(message).writeByte(0).toByteArray())

    def sendProfile(this, playerName):
        player = this.server.players.get(playerName)
        if player != None and not player.isGuest:
            packet = ByteArray().writeUTF(player.playerName).writeInt(this.server.getplayerAvatar(playerName)).writeInt(str(player.regDate)[:10]).writeByte({1: 1,
             2: 1,
             3: 13,
             4: 13,
             5: 11,
             6: 11,
             7: 5,
             8: 5,
             9: 10,
             10: 10}[player.privLevel]).writeByte(player.gender).writeUTF(player.tribeName).writeUTF(player.marriage)
            for stat in [player.shamanSaves,
             player.shamanCheeses,
             player.firstCount,
             player.cheeseCount,
             player.hardModeSaves,
             player.bootcampCount,
             player.divineModeSaves]:
                packet.writeInt(stat)

            packet.writeShort(player.titleNumber).writeShort(len(player.titleList))
            for title in player.titleList:
                packet.writeShort(int(title - title % 1))
                packet.writeByte(int(round(title % 1 * 10)))

            packet.writeUTF(player.playerLook + ';' + player.mouseColor)
            packet.writeShort(player.shamanLevel)
            packet.writeShort(len(player.shopBadges) * 2)
            badges = map(int, player.shopBadges)
            for badge in [120,
             121,
             122,
             123,
             124,
             125,
             126,
             127,
             145,
             42,
             54,
             55,
             0,
             1,
             6,
             7,
             9,
             16,
             17,
             18,
             28,
             29,
             30,
             33,
             34,
             35,
             46,
             47,
             50,
             51,
             57,
             58,
             59,
             64,
             65,
             69,
             71,
             73,
             129,
             130,
             131,
             132,
             133,
             134,
             139,
             142,
             144,
             147,
             153,
             154,
             158,
             161,
             162,
             169,
             170]:
                if badge in badges:
                    packet.writeUnsignedByte(badge).writeByte(player.racingStats[0] / 1500 if badge == 124 else (player.racingStats[1] / 10000 if badge == 125 else (player.racingStats[2] / 10000 if badge == 127 else (player.racingStats[3] / 10000 if badge == 126 else (player.survivorStats[0] / 1000 if badge == 120 else (player.survivorStats[1] / 800 if badge == 121 else (player.survivorStats[2] / 20000 if badge == 122 else (player.survivorStats[3] / 10000 if badge == 123 else 0))))))))
                    badges.remove(int(badge))

            for badge in badges:
                packet.writeUnsignedByte(badge).writeByte(player.racingStats[0] / 1500 if badge == 124 else (player.racingStats[1] / 10000 if badge == 125 else (player.racingStats[2] / 10000 if badge == 127 else (player.racingStats[3] / 10000 if badge == 126 else (player.survivorStats[0] / 1000 if badge == 120 else (player.survivorStats[1] / 800 if badge == 121 else (player.survivorStats[2] / 20000 if badge == 122 else (player.survivorStats[3] / 10000 if badge == 123 else 0))))))))

            stats = [[30,
              player.racingStats[0],
              1500,
              124],
             [31,
              player.racingStats[1],
              10000,
              125],
             [33,
              player.racingStats[2],
              10000,
              127],
             [32,
              player.racingStats[3],
              10000,
              126],
             [26,
              player.survivorStats[0],
              1000,
              120],
             [27,
              player.survivorStats[1],
              800,
              121],
             [28,
              player.survivorStats[2],
              20000,
              122],
             [29,
              player.survivorStats[3],
              10000,
              123]]
            packet.writeByte(len(stats))
            for stat in stats:
                packet.writeByte(stat[0]).writeInt(stat[1]).writeInt(stat[2]).writeByte(stat[3])

            shamanBadges = range(1, 31)
            packet.writeUnsignedByte(player.equipedShamanBadge).writeUnsignedByte(len(shamanBadges))
            for shamanBadge in shamanBadges:
                packet.writeUnsignedByte(shamanBadge)

            count = 0
            for c in player.aventurePoints.values():
                count += c

            packet.writeByte(1).writeInt(count)
            this.sendPacket(Identifiers.send.Profile, packet.toByteArray())
        return None

    def sendPlayerBan(this, hours, reason, silent):
        this.sendPacket(Identifiers.old.send.Player_Ban, [hours * 3600000, reason])
        if not silent and this.room != None:
            for client in this.room.clients.values():
                client.sendLangueMessage('', '<ROSE>\xe2\x80\xa2 [Modera\xc3\xa7\xc3\xa3o] $Message_Ban', this.playerName, str(hours), reason)

        this.server.disconnectIPAddress(this.ipAddress)
        return

    def sendPlayerEmote(this, emoteID, flag, others, lua):
        packet = ByteArray().writeInt(this.playerCode).writeByte(emoteID)
        if not flag == '':
            packet.writeUTF(flag)
        this.room.sendAllOthers(this, Identifiers.send.Player_Emote, packet.writeBoolean(lua).toByteArray()) if others else this.room.sendAll(Identifiers.send.Player_Emote, packet.writeBoolean(lua).toByteArray())

    def sendEmotion(this, emotion):
        this.room.sendAllOthers(this, Identifiers.send.Emotion, ByteArray().writeInt(this.playerCode).writeByte(emotion).toByteArray())

    def sendPlaceObject(this, objectID, code, px, py, angle, vx, vy, dur, sendAll):
        packet = ByteArray().writeInt(objectID).writeShort(code).writeShort(px).writeShort(py).writeShort(angle).writeByte(vx).writeByte(vy).writeBoolean(dur)
        if this.isGuest or sendAll:
            packet.writeByte(0)
        else:
            packet.writeBytes(this.parseShop.getShamanItemCustom(code))
        if not sendAll:
            this.room.sendAllOthers(this, Identifiers.send.Spawn_Object, packet.toByteArray())
            this.room.objectID = objectID
        else:
            this.room.sendAll(Identifiers.send.Spawn_Object, packet.toByteArray())

    def sendPlaceObjectDeath(this, objectID, code, px, py, angle, vx, vy, dur, sendAll):
        if this.PlayerDeathVivo:
            packet = ByteArray().writeInt(objectID).writeShort(code).writeShort(px).writeShort(py).writeShort(angle).writeByte(vx).writeByte(vy).writeBoolean(dur)
            if this.isGuest or sendAll:
                packet.writeByte(0)
            else:
                packet.writeBytes(this.parseShop.getShamanItemCustom(code))
            if not sendAll:
                this.room.sendAllOthers(this, Identifiers.send.Spawn_Object, packet.toByteArray())
                this.room.objectID = objectID
            else:
                this.room.sendAll(Identifiers.send.Spawn_Object, packet.toByteArray())
        else:
            this.room.objectID = 1
            this.room.removeObject(objectID)

    def sendTotem(this, totem, x, y, playerCode):
        this.sendPacket(Identifiers.old.send.Totem, ['%s#%s#%s%s' % (playerCode,
          x,
          y,
          totem)])

    def sendTotemItemCount(this, number):
        if this.room.isTotemEditor:
            this.sendPacket(Identifiers.send.Totem_Item_Count, ByteArray().writeShort(number * 2).toByteArray())

    def initTotemEditor(this):
        if this.resetTotem:
            this.sendTotemItemCount(0)
            this.resetTotem = False
        elif not this.totem[1] == '':
            this.tempTotem[0] = this.totem[0]
            this.tempTotem[1] = this.totem[1]
            this.sendTotemItemCount(this.tempTotem[0])
            this.sendTotem(this.tempTotem[1], 400, 204, this.playerCode)
        else:
            this.sendTotemItemCount(0)

    def sendShamanType(this, mode, canDivine):
        this.sendPacket(Identifiers.send.Shaman_Type, ByteArray().writeByte(mode).writeBoolean(canDivine).writeInt(int(this.shamanColor, 16)).toByteArray())

    def sendBanConsideration(this):
        this.sendPacket(Identifiers.old.send.Ban_Consideration, ['0'])

    def sendShamanPosition(this, direction):
        this.room.sendAll(Identifiers.send.Shaman_Position, ByteArray().writeInt(this.playerCode).writeBoolean(direction).toByteArray())

    def sendLangueMessage(this, community, message, *args):
        packet = ByteArray().writeUTF(community).writeUTF(message).writeByte(len(args))
        for arg in args:
            packet.writeUTF(arg)

        this.sendPacket(Identifiers.send.Message_Langue, packet.toByteArray())

    def sendMessageLangueError(this):
        this.sendPacket([28, 28], ByteArray().writeShort(1).toByteArray())

    def sendMessageLangue(this, message1, message2, *args):
        p = ByteArray().writeUTF(message1).writeUTF(message2).writeByte(len(args))
        for arg in args:
            p.writeUTF(arg)

        this.sendPacket([28, 5], p.toByteArray())

    def sendModMute(this, playerName, hours, reason, only):
        if not only:
            this.room.sendMessage('', '<ROSE>\xe2\x80\xa2 [Modera\xc3\xa7\xc3\xa3o] $MuteInfo2', playerName, playerName, hours, reason)
        else:
            client = this.server.players.get(playerName)
            if client:
                client.sendLangueMessage('', '<ROSE>\xe2\x80\xa2 [Modera\xc3\xa7\xc3\xa3o] $MuteInfo1', hours, reason)

    def sendVampireMode(this, others):
        this.isVampire = True
        if others:
            this.room.sendAllOthers(this, Identifiers.send.Vampire_Mode, ByteArray().writeInt(this.playerCode).toByteArray())
        else:
            this.room.sendAll(Identifiers.send.Vampire_Mode, ByteArray().writeInt(this.playerCode).toByteArray())

    def sendRemoveCheese(this):
        this.room.sendAll(Identifiers.send.Remove_Cheese, ByteArray().writeInt(this.playerCode).toByteArray())

    def sendLuaMessage(this, message):
        this.sendPacket(Identifiers.send.Lua_Message, ByteArray().writeUTF(message).toByteArray())

    def sendGameMode(this, mode):
        try:
            mode = 1 if mode == 0 else mode
            types = [1,
             3,
             8,
             9,
             11,
             2,
             10,
             18,
             16]
            p = ByteArray().writeByte(len(types))
            for roomType in types:
                p.writeByte(roomType)

            p.writeByte(mode)
            modeInfo = this.server.getPlayersCountMode(mode, this.langue)
            if not modeInfo[0] == '':
                roomsCount = 0
                p.writeUnsignedByte(1).writeUnsignedByte(this.langueID).writeUTF(str(modeInfo[0])).writeUTF(str(modeInfo[1])).writeUTF('mjj').writeUTF('1')
                for checkRoom in this.server.rooms.values():
                    if (checkRoom.isNormRoom + checkRoom.isTribeHouse + checkRoom.isVillage + checkRoom.isPokeLua + checkRoom.isTribewar + checkRoom.isExplosionGame + checkRoom.isBallonRace + checkRoom.isFlyGame + checkRoom.isDeathmatch + checkRoom.isTotemEditor + checkRoom.isDoubleMap + checkRoom.isVanilla + checkRoom.isSurvivor + checkRoom.isRacing + checkRoom.isMusic + checkRoom.isBootcamp + checkRoom.isDefilante if mode == 1 else (checkRoom.isVanilla if mode == 3 else (checkRoom.isSurvivor if mode == 8 else (checkRoom.isRacing if mode == 9 else (checkRoom.isMusic if mode == 11 else (checkRoom.isBootcamp if mode == 2 else (checkRoom.isVillage if mode == 16 else checkRoom.isDefilante))))))) and checkRoom.community == this.langue.lower():
                        roomsCount += 1
                        p.writeUnsignedByte(0).writeUnsignedByte(this.langueID).writeUTF(checkRoom.roomName).writeUnsignedShort(checkRoom.getPlayerCount()).writeUnsignedByte(checkRoom.maxPlayers).writeBoolean(False)

                if roomsCount == 0:
                    p.writeUnsignedByte(0).writeUnsignedByte(this.langueID).writeUTF(('' if mode == 1 else str(modeInfo[0].split(' ')[1])) + '1').writeUnsignedShort(0).writeUnsignedByte(200).writeBoolean(False)
            else:
                minigamesList = {}
                minigames = ['#eventoaventura',
                 '#fly',
                 '#ballonrace',
                 '#invocation',
                 '#explosion',
                 '#pokelua',
                 '#deathmatch',
                 '#tribewar']
                roomsList = {}
                for minigame in minigames:
                    minigamesList[minigame] = 0
                    for checkRoom in this.server.rooms.values():
                        if checkRoom.roomName == minigame:
                            minigamesList[minigame] = minigamesList[minigame] + checkRoom.getPlayerCount()
                        elif checkRoom.roomName.startswith(minigame) and checkRoom.community == this.langue.lower():
                            roomsList[checkRoom.roomName] = [checkRoom.getPlayerCount(), checkRoom.maxPlayers]

                for minigame, count in minigamesList.items():
                    p.writeUnsignedByte(1).writeUnsignedByte(this.langueID).writeUTF(str(minigame)).writeUTF(str(count)).writeUTF('mjj').writeUTF(minigame)

                for minigame, count in roomsList.items():
                    p.writeUnsignedByte(0).writeUnsignedByte(this.langueID).writeUTF(minigame).writeShort(count[0]).writeUnsignedByte(count[1]).writeBoolean(False)

            this.sendPacket(Identifiers.send.Game_Mode, p.toByteArray())
        except:
            this.transport.loseConnection()

    def sendStaffMessage(this, message, othersLangues, tab = False):
        for client in this.server.players.values():
            if othersLangues or client.langue == this.langue:
                client.sendMessage(message, tab)

    def sendBulle(this):
        this.sendPacket(Identifiers.send.Bulle, ByteArray().writeInt(0).writeUTF('x').toByteArray())

    def sendLogMessage(this, message):
        this.sendPacket(Identifiers.send.Log_Message, ByteArray().writeByte(0).writeUTF('').writeUnsignedByte(len(message) >> 16 & 255).writeUnsignedByte(len(message) >> 8 & 255).writeUnsignedByte(len(message) & 255).writeBytes(message).toByteArray())

    def sendAnimZelda(this, type, item = 0, case = '', id = 0):
        packet = ByteArray().writeInt(this.playerCode).writeByte(type)
        if type == 7:
            packet.writeUTF(case).writeUnsignedByte(id)
        elif type == 5:
            packet.writeUTF(case)
        else:
            packet.writeInt(item)
        this.room.sendAll(Identifiers.send.Anim_Zelda, packet.toByteArray())

    def sendAnimZeldaInventory(this, id1, id2, count):
        if id1 == 4:
            this.sendPacket([100, 67], ByteArray().writeByte(0).writeShort(id2).writeShort(count).toByteArray())
        this.room.sendAll([8, 44], ByteArray().writeInt(this.playerCode).writeByte(id1).writeInt(id2).toByteArray())

    def checkElection(this, fur):
        this.Cursor.execute('SELECT fur from election WHERE name = ?', [this.playerName])
        rrf = this.Cursor.fetchone()
        if rrf is None:
            pass
        elif this.server.election == 0:
            this.Cursor.execute('UPDATE election SET fur = ? WHERE name = ?', [fur, this.playerName])
        return

    def sendSelectPresidente(this):
        this.Cursor.execute('SELECT name FROM election WHERE rank = ? ORDER BY votes DESC LIMIT 1', [1])
        rrf = this.Cursor.fetchone()
        if rrf is None:
            pass
        else:
            name = rrf[0]
            this.Cursor.execute('SELECT Mayor FROM users WHERE Username = ?', [name])
            rrf2 = this.Cursor.fetchone()[0]
            votemayor, candidatar, mayor, presidente, votepresidente, addpresidente = rrf2.split('#')
            presidente = '1'
            a = '#'.join([votemayor,
             candidatar,
             mayor,
             presidente,
             votepresidente,
             addpresidente])
            this.Cursor.execute('UPDATE users SET Mayor = ? WHERE Username = ?', [a, name])
            this.Cursor.execute('UPDATE election SET presidente = ? WHERE name = ?', [1, name])
            this.server.presidente = 1
        this.sendMessage('<J>Presidente escolhido', True)
        return

    def sendSelectMayors(this):
        shop = this.server.shopList
        furs = [1]
        for item in shop:
            classes = item.split(',')
            if int(classes[0]) == 22:
                furs.append(int(classes[1]))

        for fur in furs:
            this.Cursor.execute('SELECT name FROM election WHERE fur = ? AND rank = ? ORDER BY votes DESC LIMIT 1', [fur, 0])
            rrf = this.Cursor.fetchone()
            if rrf is None:
                pass
            else:
                name = rrf[0]
                this.Cursor.execute('SELECT mayor FROM users WHERE Username = ?', [name])
                rrf2 = this.Cursor.fetchone()[0]
                votemayor, candidatar, mayor, presidente, votepresidente, addpresidente = rrf2.split('#')
                mayor = '1'
                a = '#'.join([votemayor,
                 candidatar,
                 mayor,
                 presidente,
                 votepresidente,
                 addpresidente])
                this.Cursor.execute('UPDATE users SET Mayor = ? WHERE Username = ?', [a, name])
                this.Cursor.execute('UPDATE election SET mayor = ? WHERE name = ?', [1, name])
                fur = this.getLookUser(name).split(';')[0]
                this.Cursor.execute('INSERT INTO election (name, fur, text1, text2, votes, rank, mayor, presidente) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [name,
                 fur,
                 '',
                 '',
                 0,
                 1,
                 0,
                 0])

        this.server.election = 2
        this.sendMessage('<J>Prefeitos escolhidos', True)
        return

    def sendResetarElection(this):
        this.Cursor.execute('DELETE FROM election WHERE rank = ?', [0])
        this.Cursor.execute('SELECT name FROM election where presidente = ?', [1])
        presidente = this.Cursor.fetchone()[0]
        this.Cursor.execute('DELETE from election WHERE name != ?', [presidente])
        this.Cursor.execute('UPDATE users SET Mayor = ? where Username != ?', ['0#0#0#0#0#0', presidente])
        this.Cursor.execute('UPDATE users SET Mayor = ? WHERE Username = ?', ['0#0#0#1#0#0', presidente])
        this.server.election = 0
        this.server.presidente = 0
        this.sendMessage('<J>Elei\xc3\xa7\xc3\xa3o resetada', True)

    def sendResetarPresidente(this):
        this.Cursor.execute('SELECT name FROM election where presidente = ?', [1])
        presidente = this.Cursor.fetchone()[0]
        this.Cursor.execute('DELETE FROM election where rank = ?', [1])
        this.Cursor.execute('UPDATE users SET Mayor = ? where Username = ?', ['0#0#0#0#0#0', presidente])
        this.sendMessage('<J>Presidente resetado', True)

    def sendMayor(this):
        p = ByteArray().writeByte(this.server.election)
        fur = this.playerLook.split(';')[0]
        if this.server.election == 0:
            if this.votemayor == 0:
                p.writeByte(1)
            else:
                p.writeByte(0)
            if this.candidatar == 0:
                p.writeByte(1)
            else:
                p.writeByte(0)
            time = '1-1'
            p.writeUTF(time)
            this.Cursor.execute('SELECT * FROM election WHERE rank = ? AND presidente = ?', [1, 1])
            rrf = this.Cursor.fetchone()
            if rrf is None:
                p.writeByte(0)
            else:
                name = rrf[0]
                text1 = rrf[2]
                text2 = rrf[3]
                votes = rrf[4]
                look = this.getLookUser(name)
                furlook = look.split(';')[0]
                p.writeByte(1)
                p.writeUTF(name)
                p.writeByte(2)
                p.writeInt(furlook)
                p.writeInt(votes)
                p.writeByte(0)
                p.writeUTF(look)
                p.writeUTF(text1)
                p.writeUTF(text2)
            this.Cursor.execute('SELECT * FROM election WHERE fur = ? AND rank = ?', [fur, 0])
            rrfs = this.Cursor.fetchall()
            if len(rrfs) == 0:
                pass
            else:
                for rrf in rrfs:
                    name = rrf[0]
                    text1 = rrf[2]
                    text2 = rrf[3]
                    votes = rrf[4]
                    look = this.getLookUser(name)
                    furlook = look.split(';')[0]
                    p.writeByte(1)
                    p.writeUTF(name)
                    p.writeByte(1)
                    p.writeInt(furlook)
                    p.writeInt(votes)
                    p.writeByte(0)
                    p.writeUTF(look)
                    p.writeUTF(text1)
                    p.writeUTF(text2)

            this.sendPacket([100, 80], p.toByteArray())
        elif this.server.election == 2:
            if this.isMayor == 1 and this.server.presidente == 0:
                this.sendPresidente()
            else:
                p.writeShort(0)
                time = 'you like-my dick for'
                p.writeUTF(time)
                this.Cursor.execute('SELECT * FROM election WHERE fur = ? AND rank = ? AND mayor = ?', [fur, 0, 1])
                rrf = this.Cursor.fetchone()
                nonemayor = False
                if rrf is None:
                    p.writeByte(0)
                    nonemayor = True
                else:
                    name = rrf[0]
                    text1 = rrf[2]
                    text2 = rrf[3]
                    votes = rrf[4]
                    look = this.getLookUser(name)
                    furlook = look.split(';')[0]
                    p.writeByte(1)
                    p.writeUTF(name)
                    p.writeByte(1)
                    p.writeInt(furlook)
                    p.writeInt(votes)
                    p.writeByte(0)
                    p.writeUTF(look)
                    p.writeUTF(text1)
                    p.writeUTF(text2)
                this.Cursor.execute('SELECT * FROM election WHERE rank = ? AND presidente = ?', [1, 1])
                rrf = this.Cursor.fetchone()
                if rrf is None:
                    p.writeByte(0)
                else:
                    name = rrf[0]
                    text1 = rrf[2]
                    text2 = rrf[3]
                    votes = rrf[4]
                    look = this.getLookUser(name)
                    furlook = look.split(';')[0]
                    p.writeByte(1)
                    p.writeUTF(name)
                    p.writeByte(1)
                    p.writeInt(furlook)
                    p.writeInt(votes)
                    p.writeByte(0)
                    p.writeUTF(look)
                    p.writeUTF(text1)
                    p.writeUTF(text2)
                this.sendPacket([100, 80], p.toByteArray())
        return

    def sendPresidente(this):
        p = ByteArray().writeByte(1)
        fur = this.playerLook.split(';')[0]
        if this.votepresidente == 0:
            p.writeByte(1)
        else:
            p.writeByte(0)
        p.writeByte(0)
        time = 'you like-my dick for'
        p.writeUTF(time)
        this.Cursor.execute('SELECT * FROM election WHERE fur = ? AND rank = ? AND mayor = ?', [fur, 0, 1])
        rrf = this.Cursor.fetchone()
        nonemayor = False
        if rrf is None:
            p.writeByte(0)
            nonemayor = True
        else:
            name = rrf[0]
            text1 = rrf[2]
            text2 = rrf[3]
            votes = rrf[4]
            look = this.getLookUser(name)
            furlook = look.split(';')[0]
            p.writeByte(1)
            p.writeUTF(name)
            p.writeByte(1)
            p.writeInt(furlook)
            p.writeInt(votes)
            p.writeByte(0)
            p.writeUTF(look)
            p.writeUTF(text1)
            p.writeUTF(text2)
        this.Cursor.execute('SELECT * FROM election WHERE rank = ?', [1])
        rrfs = this.Cursor.fetchall()
        if len(rrfs) == 0:
            pass
        else:
            for rrf in rrfs:
                name = rrf[0]
                text1 = rrf[2]
                text2 = rrf[3]
                votes = rrf[4]
                look = this.getLookUser(name)
                furlook = look.split(';')[0]
                p.writeByte(1)
                p.writeUTF(name)
                p.writeByte(1)
                p.writeInt(furlook)
                p.writeInt(votes)
                p.writeByte(0)
                p.writeUTF(look)
                p.writeUTF(text1)
                p.writeUTF(text2)

        this.sendPacket([100, 80], p.toByteArray())
        return

    def getLookUser(this, name):
        for room in this.server.rooms.values():
            for client in room.clients.values():
                if client.playerName == name:
                    return client.playerLook

        this.Cursor.execute('SELECT Look FROM users WHERE Username = ?', [name])
        return this.Cursor.fetchone()[0]

    def sendInventoryConsumables(this):
        packet = ByteArray().writeShort(len(this.playerConsumables))
        for id in this.playerConsumables.items():
            packet.writeShort(id[0]).writeUnsignedByte(250 if id[1] > 250 else id[1]).writeByte(0).writeBoolean(True).writeBoolean(True).writeBoolean(True).writeBoolean(True).writeBoolean(True).writeBoolean(False).writeBoolean(False).writeByte(this.equipedConsumables.index(id[0]) + 1 if id[0] in this.equipedConsumables else 0)

        this.sendPacket(Identifiers.send.Inventory, packet.toByteArray())

    def updateInventoryConsumable(this, id, count):
        this.sendPacket(Identifiers.send.Update_Inventory_Consumable, ByteArray().writeShort(id).writeUnsignedByte(250 if count > 250 else count).toByteArray())

    def useInventoryConsumable(this, id):
        if id in (29, 30, 2241, 2330):
            this.sendPacket(Identifiers.send.Use_Inventory_Consumable, ByteArray().writeInt(this.playerCode).writeShort(id).toByteArray())
        else:
            this.room.sendAll(Identifiers.send.Use_Inventory_Consumable, ByteArray().writeInt(this.playerCode).writeShort(id).toByteArray())

    def sendTradeResult(this, playerName, result):
        this.sendPacket(Identifiers.send.Trade_Result, ByteArray().writeUTF(playerName).writeByte(result).toByteArray())

    def sendTradeInvite(this, playerCode):
        this.sendPacket(Identifiers.send.Trade_Invite, ByteArray().writeInt(playerCode).toByteArray())

    def sendTradeStart(this, playerCode):
        this.sendPacket(Identifiers.send.Trade_Start, ByteArray().writeInt(playerCode).toByteArray())

    def premioVillage(this, coisa):
        if coisa[0] == 1:
            medal = coisa[1]
            if this.playerConsumables[coisa[4]] >= coisa[5]:
                if int(medal) not in this.shopBadges:
                    this.parseShop.sendUnlockedBadge(medal)
                    this.shopBadges.append(str(medal))
                    this.playerConsumables[coisa[4]] -= coisa[5]
        elif coisa[0] == 2:
            symbol = str(coisa[1])
            if symbol not in this.shamanBadges:
                if this.shamanBadges == '':
                    this.shamanBadges = [symbol]
                else:
                    test = [symbol]
                    this.shamanBadges = this.shamanBadges + test
                this.playerConsumables[coisa[4]] -= coisa[5]
                this.sendAnimZeldaInventory(6, coisa[1], 1)
        elif coisa[0] == 3:
            titles = [str(coisa[1]) + '.1']
            title = random.choice(titles)
            if this.playerConsumables[coisa[4]] >= coisa[5]:
                while title in this.titleList:
                    try:
                        titles.remove(title)
                        title = random.choice(titles)
                    except:
                        break

                if title not in this.titleList:
                    stitle = title.split('.')
                    this.specialTitleList = this.specialTitleList + [float(title)]
                    this.sendUnlockedTitle(stitle[0], stitle[1])
                    this.sendCompleteTitleList()
                    this.sendTitleList()
                    this.playerConsumables[coisa[4]] -= coisa[5]
        elif coisa[0] == 4:
            if this.playerConsumables[coisa[4]] >= coisa[5]:
                id = coisa[1]
                if id not in this.playerConsumables:
                    this.playerConsumables[id] = coisa[2]
                else:
                    count = this.playerConsumables[id] + coisa[2]
                    this.playerConsumables[id] = count
                this.playerConsumables[coisa[4]] -= coisa[5]
                this.sendAnimZeldaInventory(4, id, coisa[2])
        this.BotsVillage(this.botVillage)

    def BotsVillage(this, bot):
        itens = list()
        for item in this.itensBots[bot]:
            if item[0] == 1 and str(item[1]) in this.shopBadges:
                itens.append(item)
            elif item[0] == 2 and str(item[1]) in this.shamanBadges:
                itens.append(item)
            elif item[0] == 3 and float(str(item[1]) + '.1') in this.titleList:
                itens.append(item)

        for item in itens:
            this.itensBots[bot].remove(item)

        p = ByteArray()
        for items in this.itensBots[bot]:
            count = items[5]
            if items[4] in this.playerConsumables:
                one = 0 if this.playerConsumables[items[4]] >= count else 1
            else:
                one = 1
            p.writeByte(one).writeByte(items[0]).writeShort(items[1]).writeShort(items[2]).writeByte(items[3]).writeShort(items[4]).writeShort(items[5])

        this.sendPacket([26, 38], ByteArray().writeUTF(bot).writeByte(len(this.itensBots[bot])).toByteArray() + p.toByteArray())

    def tradeInvite(this, playerName):
        client = this.room.clients.get(playerName)
        if client != None and (not this.ipAddress == client.ipAddress or this.privLevel == 10 or client.privLevel == 11) and this.privLevel != 0 and client.privLevel != 0:
            if not client.isTrade:
                if not client.room.name == this.room.name:
                    this.sendTradeResult(playerName, 3)
                elif client.isTrade:
                    this.sendTradeResult(playerName, 0)
                else:
                    this.sendLangueMessage('', '$Demande_Envoy\xc3\xa9e')
                    client.sendTradeInvite(this.playerCode)
                this.tradeName = playerName
                this.isTrade = True
            else:
                this.tradeName = playerName
                this.isTrade = True
                this.sendTradeStart(client.playerCode)
                client.sendTradeStart(this.playerCode)
        return

    def cancelTrade(this, playerName):
        client = this.room.clients.get(playerName)
        if client != None:
            this.tradeName = ''
            this.isTrade = False
            this.tradeConsumables = {}
            this.tradeConfirm = False
            client.tradeName = ''
            client.isTrade = False
            client.tradeConsumables = {}
            client.tradeConfirm = False
            client.sendTradeResult(this.playerName, 2)
        return

    def tradeAddConsumable(this, id, isAdd):
        client = this.room.clients.get(this.tradeName)
        if client != None and client.isTrade and client.tradeName == this.playerName:
            if isAdd:
                if this.tradeConsumables.has_key(id):
                    this.tradeConsumables[id] += 1
                else:
                    this.tradeConsumables[id] = 1
            else:
                count = this.tradeConsumables[id] - 1
                if count > 0:
                    this.tradeConsumables[id] = count
                else:
                    del this.tradeConsumables[id]
            client.sendPacket(Identifiers.send.Trade_Add_Consumable, ByteArray().writeBoolean(False).writeShort(id).writeBoolean(isAdd).writeByte(1).writeBoolean(False).toByteArray())
            this.sendPacket(Identifiers.send.Trade_Add_Consumable, ByteArray().writeBoolean(True).writeShort(id).writeBoolean(isAdd).writeByte(1).writeBoolean(False).toByteArray())
        return

    def tradeResult(this, isAccept):
        client = this.room.clients.get(this.tradeName)
        if client != None and client.isTrade and client.tradeName == this.playerName:
            this.tradeConfirm = isAccept
            client.sendPacket(Identifiers.send.Trade_Confirm, ByteArray().writeBoolean(False).writeBoolean(isAccept).toByteArray())
            this.sendPacket(Identifiers.send.Trade_Confirm, ByteArray().writeBoolean(True).writeBoolean(isAccept).toByteArray())
            if this.tradeConfirm and client.tradeConfirm:
                for consumable in client.tradeConsumables.items():
                    if this.playerConsumables.has_key(consumable[0]):
                        this.playerConsumables[consumable[0]] += consumable[1]
                    else:
                        this.playerConsumables[consumable[0]] = consumable[1]
                    count = client.playerConsumables[consumable[0]] - consumable[1]
                    if count <= 0:
                        del client.playerConsumables[consumable[0]]
                        if consumable[0] in client.equipedConsumables:
                            client.equipedConsumables.remove(consumable[0])
                    else:
                        client.playerConsumables[consumable[0]] = count

                for consumable in this.tradeConsumables.items():
                    if client.playerConsumables.has_key(consumable[0]):
                        client.playerConsumables[consumable[0]] += consumable[1]
                    else:
                        client.playerConsumables[consumable[0]] = consumable[1]
                    count = this.playerConsumables[consumable[0]] - consumable[1]
                    if count <= 0:
                        del this.playerConsumables[consumable[0]]
                        if consumable[0] in this.equipedConsumables:
                            this.equipedConsumables.remove(consumable[0])
                    else:
                        this.playerConsumables[consumable[0]] = count

                client.tradeName = ''
                client.isTrade = False
                client.tradeConsumables = {}
                client.tradeConfirm = False
                client.sendPacket(Identifiers.send.Trade_Close)
                client.sendInventoryConsumables()
                this.tradeName = ''
                this.isTrade = False
                this.tradeConsumables = {}
                this.tradeConfirm = False
                this.sendPacket(Identifiers.send.Trade_Close)
                this.sendInventoryConsumables()
        return

    def sendGiveConsumables(this, id, amount = 80, limit = 80):
        this.sendAnimZelda(4, id)
        this.sendNewConsumable(id, amount)
        sum = (this.playerConsumables[id] if this.playerConsumables.has_key(id) else 0) + amount
        if limit != -1 and sum > limit:
            sum = limit
        if this.playerConsumables.has_key(id):
            this.playerConsumables[id] = sum
            this.updateInventoryConsumable(id, sum)
        else:
            this.playerConsumables[id] = sum
            this.updateInventoryConsumable(id, sum)

    def sendNewConsumable(this, consumable, count):
        this.sendPacket(Identifiers.send.New_Consumable, ByteArray().writeByte(0).writeShort(consumable).writeShort(count).toByteArray())

    def getFullItemID(this, category, itemID):
        if itemID >= 100:
            return itemID + 10000 + 1000 * category
        return itemID + 100 * category

    def getSimpleItemID(this, category, itemID):
        if itemID >= 10000:
            return itemID - 10000 - 1000 * category
        return itemID - 100 * category

    def getItemInfo(this, category, itemID):
        shop = map(lambda x: map(int, x.split(',')), this.server.shopList)
        return filter(lambda x: x[0] == category and x[1] == itemID, shop)[0] + ([20] if category != 22 else [0])


class Server(protocol.ServerFactory):
    protocol = Client

    def __init__(this):
        this.ac_config = open('./cheat/anticheat_config.txt', 'r').read()
        this.ac_enabled = True
        this.ac_c = json.loads(this.ac_config)
        this.learning = this.ac_c['learning']
        this.bantimes = this.ac_c['ban_times']
        this.s_list = open('./cheat/anticheat_allow', 'r').read()
        if this.s_list != '':
            this.s_list = this.s_list.split(',')
            this.s_list.remove('')
        else:
            this.s_list = []
        this.miceName = str(this.config('game.miceName'))
        this.isDebug = bool(int(this.config('game.debug')))
        this.adventureIMG = this.config('game.adventureIMG')
        this.lastChatID = int(this.config('ids.lastChatID'))
        this.serverURL = this.config('server.url').split(', ')
        this.adventureID = int(this.config('game.adventureID'))
        this.needToFirst = int(this.config('game.needToFirst'))
        this.lastPlayerID = int(this.config('ids.lastPlayerID'))
        this.initialCheeses = int(this.config('game.initialCheeses'))
        this.initialFraises = int(this.config('game.initialFraises'))
        this.EmailAddress = this.config('game.email')
        this.recordPlayers = int(this.config('game.Record'))
        this.lastMapEditeurCode = int(this.config('game.lastMapCodeId'))
        this.timeEvent = int(this.config('game.timeevent'))
        this.calendarioSystem = eval(this.config('game.calendario'))
        this.calendarioCount = eval(this.config('game.calendarioCount'))
        this.newVisuList = eval(this.configShop('shop.visuDone'))
        this.election = int(this.config('election.election'))
        this.presidente = int(this.config('election.presidente'))
        this.electionTime = int(this.config('election.time'))
        this.shopList = this.configShop('shop.shopList').split(';')
        this.shamanShopList = this.configShop('shop.shamanShopList').split(';')
        this.STARTTIME = datetime.today()
        this.lastGiftID = 0
        this.lastPlayerCode = 0
        this.startServer = datetime.today()
        this.activeStaffChat = 0
        this.rebootTimer = None
        this.rankingTimer = None
        this.packetKeys = [0,
         26,
         37,
         36,
         24,
         59,
         22,
         35,
         56,
         34,
         121,
         120,
         68,
         103,
         114,
         71,
         92,
         70,
         113,
         112]
        this.loginKeys = [5204292,
         13207023,
         1024,
         2097152,
         1024,
         2543425,
         10182091,
         16280609,
         16384,
         67108864,
         13037573,
         8858369,
         2597112]
        this.tempIPBanList = []
        this.userMuteCache = []
        this.shopPromotions = []
        this.IPTempBanCache = []
        this.IPPermaBanCache = []
        this.userTempBanCache = []
        this.userPermaBanCache = []
        this.staffChat = []
        this.ranking = [{},
         {},
         {},
         {}]
        this.rankingsList = [{},
         {},
         {},
         {}]
        this.rooms = {}
        this.players = {}
        this.shopGifts = {}
        this.vanillaMaps = {}
        this.chatMessages = {}
        this.shopListCheck = {}
        this.connectedCounts = {}
        this.reports = {'names': []}
        this.shamanShopListCheck = {}
        this.statsclient = {'racingCount': [1500,
                         10000,
                         10000,
                         10000],
         'survivorCount': [1000,
                           800,
                           20000,
                           10000],
         'racingBadges': [124,
                          125,
                          126,
                          127],
         'survivorBadges': [120,
                            121,
                            122,
                            123]}
        this.hardModeTitleList = {500: 213.1,
         2000: 214.1,
         4000: 215.1,
         7000: 216.1,
         10000: 217.1,
         14000: 218.1,
         18000: 219.1,
         22000: 220.1,
         26000: 221.1,
         30000: 222.1,
         40000: 223.1}
        this.divineModeTitleList = {500: 324.1,
         2000: 325.1,
         4000: 326.1,
         7000: 327.1,
         10000: 328.1,
         14000: 329.1,
         18000: 330.1,
         22000: 331.1,
         26000: 332.1,
         30000: 333.1,
         40000: 334.1}
        this.shamanTitleList = {10: 1.1,
         100: 2.1,
         1000: 3.1,
         2000: 4.1,
         3000: 13.1,
         4000: 14.1,
         5000: 15.1,
         6000: 16.1,
         7000: 17.1,
         8000: 18.1,
         9000: 19.1,
         10000: 20.1,
         11000: 21.1,
         12000: 22.1,
         13000: 23.1,
         14000: 24.1,
         15000: 25.1,
         16000: 94.1,
         18000: 95.1,
         20000: 96.1,
         22000: 97.1,
         24000: 98.1,
         26000: 99.1,
         28000: 100.1,
         30000: 101.1,
         35000: 102.1,
         40000: 103.1,
         45000: 104.1,
         50000: 105.1,
         55000: 106.1,
         60000: 107.1,
         65000: 108.1,
         70000: 109.1,
         75000: 110.1,
         80000: 111.1,
         85000: 112.1,
         90000: 113.1,
         100000: 114.1,
         140000: 115.1}
        this.firstTitleList = {1: 9.1,
         10: 10.1,
         100: 11.1,
         200: 12.1,
         300: 42.1,
         400: 43.1,
         500: 44.1,
         600: 45.1,
         700: 46.1,
         800: 47.1,
         900: 48.1,
         1000: 49.1,
         1100: 50.1,
         1200: 51.1,
         1400: 52.1,
         1600: 53.1,
         1800: 54.1,
         2000: 55.1,
         2200: 56.1,
         2400: 57.1,
         2600: 58.1,
         2800: 59.1,
         3000: 60.1,
         3200: 61.1,
         3400: 62.1,
         3600: 63.1,
         3800: 64.1,
         4000: 65.1,
         4500: 66.1,
         5000: 67.1,
         5500: 68.1,
         6000: 69.1,
         7000: 231.1,
         8000: 232.1,
         9000: 233.1,
         10000: 70.1,
         12000: 224.1,
         14000: 225.1,
         16000: 226.1,
         18000: 227.1,
         20000: 202.1,
         25000: 228.1,
         30000: 229.1,
         35000: 230.1,
         40000: 71.1}
        this.cheeseTitleList = {5: 5.1,
         20: 6.1,
         100: 7.1,
         200: 8.1,
         300: 35.1,
         400: 36.1,
         500: 37.1,
         600: 26.1,
         700: 27.1,
         800: 28.1,
         900: 29.1,
         1000: 30.1,
         1100: 31.1,
         1200: 32.1,
         1300: 33.1,
         1400: 34.1,
         1500: 38.1,
         1600: 39.1,
         1700: 40.1,
         1800: 41.1,
         2000: 72.1,
         2300: 73.1,
         2700: 74.1,
         3200: 75.1,
         3800: 76.1,
         4600: 77.1,
         6000: 78.1,
         7000: 79.1,
         8000: 80.1,
         9001: 81.1,
         10000: 82.1,
         14000: 83.1,
         18000: 84.1,
         22000: 85.1,
         26000: 86.1,
         30000: 87.1,
         34000: 88.1,
         38000: 89.1,
         42000: 90.1,
         46000: 91.1,
         50000: 92.1,
         55000: 234.1,
         60000: 235.1,
         65000: 236.1,
         70000: 237.1,
         75000: 238.1,
         80000: 93.1}
        this.shopBadges = {2227: 2,
         2208: 3,
         2202: 4,
         2209: 5,
         2228: 8,
         2218: 10,
         2206: 11,
         2219: 12,
         2229: 13,
         2230: 14,
         2231: 15,
         2211: 19,
         2232: 20,
         2224: 21,
         2217: 22,
         2214: 23,
         2212: 24,
         2220: 25,
         2223: 26,
         2234: 27,
         2203: 31,
         2220: 32,
         2236: 36,
         2204: 40,
         2239: 43,
         2241: 44,
         2243: 45,
         2244: 48,
         2207: 49,
         2246: 52,
         2247: 53,
         210: 54,
         2225: 56,
         2213: 60,
         2248: 61,
         2226: 62,
         2249: 63,
         2250: 66,
         2252: 67,
         2253: 68,
         2254: 70,
         2255: 72,
         2256: 128,
         2257: 135,
         2258: 136,
         2259: 137,
         2260: 138,
         2261: 140,
         2262: 141,
         2263: 143,
         2264: 146,
         2265: 148,
         2267: 149,
         2268: 150,
         2269: 151,
         2270: 152,
         2271: 155,
         2272: 156,
         2273: 157,
         2274: 160,
         2276: 165,
         2277: 167,
         2278: 171,
         2279: 173,
         2280: 175,
         2281: 176,
         2282: 177,
         2283: 178,
         2284: 179,
         2285: 180,
         2286: 183,
         2287: 185,
         2288: 186}
        this.shopTitleList = {1: 115.1,
         2: 116.1,
         4: 117.1,
         6: 118.1,
         8: 119.1,
         10: 120.1,
         12: 121.1,
         14: 122.1,
         16: 123.1,
         18: 124.1,
         20: 125.1,
         22: 126.1,
         23: 115.2,
         24: 116.2,
         26: 117.2,
         28: 118.2,
         30: 119.2,
         32: 120.2,
         34: 121.2,
         36: 122.2,
         38: 123.2,
         40: 124.2,
         42: 125.2,
         44: 126.2,
         45: 115.3,
         46: 116.3,
         48: 117.3,
         50: 118.3,
         52: 119.3,
         54: 120.3,
         56: 121.3,
         58: 122.3,
         60: 123.3,
         62: 124.3,
         64: 125.3,
         66: 126.3,
         67: 115.4,
         68: 116.4,
         70: 117.4,
         72: 118.4,
         74: 119.4,
         76: 120.4,
         78: 121.4,
         80: 122.4,
         82: 123.4,
         84: 124.4,
         86: 125.4,
         88: 126.4,
         89: 115.5,
         90: 116.5,
         92: 117.5,
         94: 118.5,
         96: 119.5,
         98: 120.5,
         100: 121.5,
         102: 122.5,
         104: 123.5,
         106: 124.5,
         108: 125.5,
         110: 126.5,
         111: 115.6,
         112: 116.6,
         114: 117.6,
         116: 118.6,
         118: 119.6,
         120: 120.6,
         122: 121.6,
         124: 122.6,
         126: 123.6,
         128: 124.6,
         130: 125.6,
         132: 126.6,
         133: 115.7,
         134: 116.7,
         136: 117.7,
         138: 118.7,
         140: 119.7,
         142: 120.7,
         144: 121.7,
         146: 122.7,
         148: 123.7,
         150: 124.7,
         152: 125.7,
         154: 126.7,
         155: 115.8,
         156: 116.8,
         158: 117.8,
         160: 118.8,
         162: 119.8,
         164: 120.8,
         166: 121.8,
         168: 122.8,
         170: 123.8,
         172: 124.8,
         174: 125.8,
         176: 126.8,
         177: 115.9,
         178: 116.9,
         180: 117.9,
         182: 118.9,
         184: 119.9,
         186: 120.9,
         188: 121.9,
         190: 122.9,
         192: 123.9,
         194: 124.9,
         196: 125.9,
         198: 126.9}
        this.bootcampTitleList = {1: 256.1,
         3: 257.1,
         5: 258.1,
         7: 259.1,
         10: 260.1,
         15: 261.1,
         20: 262.1,
         25: 263.1,
         30: 264.1,
         40: 265.1,
         50: 266.1,
         60: 267.1,
         70: 268.1,
         80: 269.1,
         90: 270.1,
         100: 271.1,
         120: 272.1,
         140: 273.1,
         160: 274.1,
         180: 275.1,
         200: 276.1,
         250: 277.1,
         300: 278.1,
         350: 279.1,
         400: 280.1,
         500: 281.1,
         600: 282.1,
         700: 283.1,
         800: 284.1,
         900: 285.1,
         1000: 286.1,
         1001: 256.2,
         1003: 257.2,
         1005: 258.2,
         1007: 259.2,
         1010: 260.2,
         1015: 261.2,
         1020: 262.2,
         1025: 263.2,
         1030: 264.2,
         1040: 265.2,
         1050: 266.2,
         1060: 267.2,
         1070: 268.2,
         1080: 269.2,
         1090: 270.2,
         1100: 271.2,
         1120: 272.2,
         1140: 273.2,
         1160: 274.2,
         1180: 275.2,
         1200: 276.2,
         1250: 277.2,
         1300: 278.2,
         1350: 279.2,
         1400: 280.2,
         1500: 281.2,
         1600: 282.2,
         1700: 283.2,
         1800: 284.2,
         1900: 285.2,
         2000: 286.2,
         2001: 256.3,
         2003: 257.3,
         2005: 258.3,
         2007: 259.3,
         2010: 260.3,
         2015: 261.3,
         2020: 262.3,
         2025: 263.3,
         2030: 264.3,
         2040: 265.3,
         2050: 266.3,
         2060: 267.3,
         2070: 268.3,
         2080: 269.3,
         2090: 270.3,
         2100: 271.3,
         2120: 272.3,
         2140: 273.3,
         2160: 274.3,
         2180: 275.3,
         2200: 276.3,
         2250: 277.3,
         2300: 278.3,
         2350: 279.3,
         2400: 280.3,
         2500: 281.3,
         2600: 282.3,
         2700: 283.3,
         2800: 284.3,
         2900: 285.3,
         3000: 286.3,
         3001: 256.4,
         3003: 257.4,
         3005: 258.4,
         3007: 259.4,
         3010: 260.4,
         3015: 261.4,
         3020: 262.4,
         3025: 263.4,
         3030: 264.4,
         3040: 265.4,
         3050: 266.4,
         3060: 267.4,
         3070: 268.4,
         3080: 269.4,
         3090: 270.4,
         3100: 271.4,
         3120: 272.4,
         3140: 273.4,
         3160: 274.4,
         3180: 275.4,
         3200: 276.4,
         3250: 277.4,
         3300: 278.4,
         3350: 279.4,
         3400: 280.4,
         3500: 281.4,
         3600: 282.4,
         3700: 283.4,
         3800: 284.4,
         3900: 285.4,
         4000: 286.4,
         4001: 256.5,
         4003: 257.5,
         4005: 258.5,
         4007: 259.5,
         4010: 260.5,
         4015: 261.5,
         4020: 262.5,
         4025: 263.5,
         4030: 264.5,
         4040: 265.5,
         4050: 266.5,
         4060: 267.5,
         4070: 268.5,
         4080: 269.5,
         4090: 270.5,
         4100: 271.5,
         4120: 272.5,
         4140: 273.5,
         4160: 274.5,
         4180: 275.5,
         4200: 276.5,
         4250: 277.5,
         4300: 278.5,
         4350: 279.5,
         4400: 280.5,
         4500: 281.5,
         4600: 282.5,
         4700: 283.5,
         4800: 284.5,
         4900: 285.5,
         5000: 286.5,
         5001: 256.6,
         5003: 257.6,
         5005: 258.6,
         5007: 259.6,
         5010: 260.6,
         5015: 261.6,
         5020: 262.6,
         5025: 263.6,
         5030: 264.6,
         5040: 265.6,
         5050: 266.6,
         5060: 267.6,
         5070: 268.6,
         5080: 269.6,
         5090: 270.6,
         5100: 271.6,
         5120: 272.6,
         5140: 273.6,
         5160: 274.6,
         5180: 275.6,
         5200: 276.6,
         5250: 277.6,
         5300: 278.6,
         5350: 279.6,
         5400: 280.6,
         5500: 281.6,
         5600: 282.6,
         5700: 283.6,
         5800: 284.6,
         5900: 285.6,
         6000: 286.6,
         6001: 256.7,
         6003: 257.7,
         6005: 258.7,
         6007: 259.7,
         6010: 260.7,
         6015: 261.7,
         6020: 262.7,
         6025: 263.7,
         6030: 264.7,
         6040: 265.7,
         6050: 266.7,
         6060: 267.7,
         6070: 268.7,
         6080: 269.7,
         6090: 270.7,
         6100: 271.7,
         6120: 272.7,
         6140: 273.7,
         6160: 274.7,
         6180: 275.7,
         6200: 276.7,
         6250: 277.7,
         6300: 278.7,
         6350: 279.7,
         6400: 280.7,
         6500: 281.7,
         6600: 282.7,
         6700: 283.7,
         6800: 284.7,
         6900: 285.7,
         7000: 286.7,
         7001: 256.8,
         7003: 257.8,
         7005: 258.8,
         7007: 259.8,
         7010: 260.8,
         7015: 261.8,
         7020: 262.8,
         7025: 263.8,
         7030: 264.8,
         7040: 265.8,
         7050: 266.8,
         7060: 267.8,
         7070: 268.8,
         7080: 269.8,
         7090: 270.8,
         7100: 271.8,
         7120: 272.8,
         7140: 273.8,
         7160: 274.8,
         7180: 275.8,
         7200: 276.8,
         7250: 277.8,
         7300: 278.8,
         7350: 279.8,
         7400: 280.8,
         7500: 281.8,
         7600: 282.8,
         7700: 283.8,
         7800: 284.8,
         7900: 285.8,
         8000: 286.8,
         8001: 256.9,
         8003: 257.9,
         8005: 258.9,
         8007: 259.9,
         8010: 260.9,
         8015: 261.9,
         8020: 262.9,
         8025: 263.9,
         8030: 264.9,
         8040: 265.9,
         8050: 266.9,
         8060: 267.9,
         8070: 268.9,
         8080: 269.9,
         8090: 270.9,
         8100: 271.9,
         8120: 272.9,
         8140: 273.9,
         8160: 274.9,
         8180: 275.9,
         8200: 276.9,
         8250: 277.9,
         8300: 278.9,
         8350: 279.9,
         8400: 280.9,
         8500: 281.9,
         8600: 282.9,
         8700: 283.9,
         8800: 284.9,
         8900: 285.9,
         9000: 286.9}
        this.parseSWF = this.parseFile('./include/files/infoSWF.json')
        this.captchaList = this.parseFile('./include/files/captchas.json')
        this.promotions = this.parseFile('./include/files/promotions.json')
        this.serverList = this.parseFile('./include/files/serverList.json')
        this.CursorCafe = CursorCafe
        this.parseFunctions()
        this.getVanillaMaps()
        this.parsePromotions()
        this.rankingTimer = reactor.callLater(1, this.getRanking)
        this.menu = this.parseMenu()
        this.resetDDoS = Cursor.execute('delete from ddos where ip')
        return None

    def checkMessage(this, client, message):
        blackList = this.serverList['blacklist']
        suspectWords = this.serverList['suspectwords']
        whiteList = this.serverList['whitelist']
        isSuspect = False
        i = 0
        while i < len(blackList):
            if re.search('[^a-zA-Z]*'.join(blackList[i]), message.lower()):
                this.sendStaffMessage(7, '[<V>ANTI-DV</V>][<J>%s</J>][<V>%s</V>][<R>%s</R>] Est\xc3\xa1 enviando um link da blacklist, portanto esta mensagem n\xc3\xa3o aparece para outros jogadores.' % (client.ipAddress, client.playerName, message))
                isSuspect = True
                return True
            i += 1

        if not isSuspect:
            if filter(lambda word: word in message.lower(), suspectWords) and not filter(lambda white: white in message.lower(), whiteList):
                this.sendStaffMessage(7, '[<V>ANTI-DV</V>][<J>%s</J>][<V>%s</V>][<J>%s</J>] Enviou uma mensagem suspeita com link, digite <V>/addtext blacklist link</V> para adicionar na <b>/blacklist</b> caso o link seja de outro servidor.' % (client.ipAddress, client.playerName, message))
        return False

    def getPointsColor(this, playerName, aventure, itemID, itemType, itemNeeded):
        for client in this.players.values():
            if client.playerName == playerName:
                if int(itemID) in client.aventureCounts.keys():
                    if client.aventureCounts[int(itemID)][1] >= int(itemNeeded):
                        return 1

        return 0

    def getAventureCounts(this, playerName, aventure, itemID, itemType):
        for client in this.players.values():
            if client.playerName == playerName:
                if int(itemID) in client.aventureCounts.keys():
                    return client.aventureCounts[int(itemID)][1]

        return 0

    def getAventureItems(this, playerName, aventure, itemType, itemID):
        c = 0
        for client in this.players.values():
            if client.playerName == playerName:
                if aventure == 24:
                    if itemType == 0 and itemID == 1:
                        return client.aventureSaves
                    if itemType == 0 and itemID == 2:
                        for item in client.aventureCounts.keys():
                            if item in range(38, 44):
                                c += client.aventureCounts[item][1]

                        return c

        return 0

    def parseFunctions(this):
        data = this.parseSWF
        this.CKEY = data['key']
        this.Version = data['version']
        for item in this.shopList:
            values = item.split(',')
            this.shopListCheck[values[0] + '|' + values[1]] = [int(values[5]), int(values[6])]

        for item in this.shamanShopList:
            values = item.split(',')
            this.shamanShopListCheck[values[0]] = [int(values[3]), int(values[4])]

        Cursor.execute('select ip from IPPermaBan')
        rs = Cursor.fetchone()
        if rs:
            this.IPPermaBanCache.append(rs['ip'])
        Cursor.execute('select Username from UserPermaBan')
        rs = Cursor.fetchone()
        if rs:
            this.userPermaBanCache.append(rs['Username'])
        Cursor.execute('select Username from UserTempBan')
        rs = Cursor.fetchone()
        if rs:
            this.userTempBanCache.append(rs['Username'])
        Cursor.execute('select Username from UserTempMute')
        rs = Cursor.fetchone()
        if rs:
            this.userMuteCache.append(rs['Username'])

    def config(this, setting):
        return config.get('configGame', setting, 0)

    def configShop(this, setting):
        return config.get('configShop', setting, 0)

    def configs(this, setting, value):
        config.set('configGame', setting, value)
        with open('./include/configs.properties', 'w') as f:
            config.write(f)

    def updateServerList(this):
        with open('./include/files/serverList.json', 'w') as f:
            f.write(str(this.serverList))

    def parseMenu(this):
        with open('./include/files/menu.json', 'r') as f:
            T = eval(f.read())
        return T

    def parseFile(this, directory):
        with open(directory, 'r') as f:
            return eval(f.read())

    def updateBlackList(this):
        with open('./include/files/serverList.json', 'w') as f:
            json.dump(this.serverList, f)

    def getVanillaMaps(this):
        for fileName in os.listdir('./include/maps/vanilla'):
            with open('./include/maps/vanilla/' + fileName) as f:
                this.vanillaMaps[int(fileName[:-4])] = f.read()

    def sendServerRestart(this, no, sec):
        if sec > 0 or no != 5:
            this.sendServerRestartSEC(120 if no == 0 else (60 if no == 1 else (30 if no == 2 else (20 if no == 3 else (10 if no == 4 else sec)))))
            if this.rebootTimer != None:
                this.rebootTimer.cancel()
            this.rebootTimer = reactor.callLater(60 if no == 0 else (30 if no == 1 else (10 if no == 2 or no == 3 else 1)), lambda : this.sendServerRestart(no if no == 5 else no + 1, 9 if no == 4 else (sec - 1 if no == 5 else 0)))
        return

    def sendServerRestartSEC(this, seconds):
        this.sendPanelRestartMessage(seconds)
        this.sendWholeServer(Identifiers.send.Server_Restart, ByteArray().writeInt(seconds * 1000).toByteArray())

    def sendPanelRestartMessage(this, seconds):
        if seconds == 120:
            print '[%s] [SERVER] The server will restart in 2 minutes.' % time.strftime('%H:%M:%S')
        elif seconds < 120 and seconds > 1:
            print '[%s] [SERVER] The server will restart in %s seconds.' % (time.strftime('%H:%M:%S'), seconds)
        else:
            print '[%s] [SERVER] The server will restart in 1 second.' % time.strftime('%H:%M:%S')
            for client in this.players.values():
                client.updateDatabase()

            os._exit(0)

    def buildCaptchaCode(this):
        CC = ''.join([ random.choice(this.captchaList.keys()) for x in range(4) ])
        words, px, py, lines = (list(CC),
         0,
         1,
         [])
        for count in range(1, 17):
            wc, values = 1, []
            for word in words:
                ws = this.captchaList[word]
                if count > len(ws):
                    count = len(ws)
                ws = ws[str(count)]
                values += ws.split(',')[1 if wc > 1 else 0:]
                wc += 1

            lines += [','.join(map(str, values))]
            if px < len(values):
                px = len(values)
            py += 1

        return [CC,
         px + 2,
         17,
         lines]

    def checkAlreadyExistingGuest(this, playerName):
        if not playerName:
            playerName = 'Souris'
        if this.checkConnectedAccount(playerName):
            playerName += '_%s' % ''.join([ random.choice(string.ascii_lowercase) for x in range(4) ])
        return playerName

    def checkConnectedAccount(this, playerName):
        return this.players.has_key(playerName)

    def disconnectIPAddress(this, ip):
        for client in this.players.values():
            if client.ipAddress == ip:
                client.transport.loseConnection()

    def checkExistingUser(this, playerName):
        Cursor.execute('select 1 from Users where Username = ?', [playerName])
        return Cursor.fetchone() != None

    def recommendRoom(this, langue, prefix = ''):
        count = 0
        result = ''
        while result == '':
            count += 1
            if this.rooms.has_key('%s-%s' % (langue, count) if prefix == '' else '%s-%s%s' % (langue, prefix, count)):
                if this.rooms['%s-%s' % (langue, count) if prefix == '' else '%s-%s%s' % (langue, prefix, count)].getPlayerCount() < 25:
                    result = str(count)
            else:
                result = str(count)

        return result

    def checkRoom(this, roomName, langue):
        found = False
        x = 0
        result = roomName
        if this.rooms.has_key(not roomName.startswith('*') and ('%s-%s' % (langue, roomName) if roomName[0] != chr(3) else roomName)):
            room = this.rooms.get('%s-%s' % (langue, roomName) if not roomName.startswith('*') and roomName[0] != chr(3) else roomName)
            if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                found = True
        else:
            found = True
        while not found:
            x += 1
            if this.rooms.has_key(not roomName.startswith('*') and ('%s-%s' % (langue, roomName) if roomName[0] != chr(3) else roomName) + str(x)):
                room = this.rooms.get(('%s-%s' % (langue, roomName) if not roomName.startswith('*') and roomName[0] != chr(3) else roomName) + str(x))
                if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                    found = True
                    result += str(x)
            else:
                found = True
                result += str(x)

        return result

    def addClientToRoom(this, client, roomName):
        if this.rooms.has_key(roomName):
            this.rooms[roomName].addClient(client)
        else:
            room = Room(this, roomName)
            this.rooms[roomName] = room
            room.addClient(client, True)
            room.mapChange()

    def banPlayer(this, playerName, bantime, reason, modName, silent):
        found = False
        client = this.players.get(playerName)
        if client != None:
            found = True
            if not modName == 'Server':
                client.banHours += bantime
                Cursor.execute("insert into BanLog values (?, ?, ?, ?, ?, 'Online', ?)", [playerName,
                 modName,
                 bantime,
                 reason,
                 int(time.time() / 10),
                 client.ipAddress])
            else:
                this.sendStaffMessage(5, '<V>Servidor <BL>baniu o jogador <V>%s<BL> por <V>1 <BL> hora. Motivo: <V>Vote Populaire<BL>.' % playerName)
            Cursor.execute('update Users set BanHours = ?, UnRanked = 1 where Username = ?', [bantime, playerName])
            if bantime >= 361 or client.banHours >= 361:
                this.userPermaBanCache.append(playerName)
                Cursor.execute('insert into UserPermaBan values (?, ?, ?)', [playerName, reason, modName])
            if client.banHours >= 361:
                this.IPPermaBanCache.append(client.ipAddress)
                Cursor.execute('insert into IPPermaBan values (?, ?, ?)', [client.ipAddress, modName, reason])
            if bantime >= 1 and bantime <= 360:
                this.tempBanUser(playerName, bantime, reason)
                this.tempBanIP(client.ipAddress, bantime)
            if playerName in this.reports['names']:
                this.reports[playerName]['status'] = 'banned'
                this.reports[playerName]['status'] = 'modname'
                this.reports[playerName]['status'] = str(bantime)
                this.reports[playerName]['banreason'] = 'hack'
            client.sendPlayerBan(bantime, reason, silent)
        if not found and this.checkExistingUser(playerName) and not modName == 'Server' and bantime >= 1:
            found = True
            totalBanTime = this.getTotalBanHours(playerName) + bantime
            if totalBanTime >= 361 and bantime <= 360 or bantime >= 361:
                this.userPermaBanCache.append(playerName)
                Cursor.execute('insert into UserPermaBan values (?, ?, ?)', [playerName, reason, modName])
            if bantime >= 1 and bantime <= 360:
                this.tempBanUser(playerName, bantime, reason)
            Cursor.execute('update Users set BanHours = ?, UnRanked = 1 where Username = ?', [bantime, playerName])
            Cursor.execute("insert into BanLog values (?, ?, ?, ?, ?, 'Offline', 'Offline')", [playerName,
             modName,
             str(bantime),
             reason,
             int(time.time() / 10)])
        return found

    def checkTempBan(this, playerName):
        Cursor.execute('select 1 from UserTempBan where Username = ?', [playerName])
        return Cursor.fetchone() != None

    def removeTempBan(this, playerName):
        if playerName in this.userTempBanCache:
            this.userTempBanCache.remove(playerName)
        Cursor.execute('delete from UserTempBan where Username = ?', [playerName])

    def tempBanUser(this, playerName, bantime, reason):
        if this.checkTempBan(playerName):
            this.removeTempBan(playerName)
        this.userTempBanCache.append(playerName)
        Cursor.execute('insert into UserTempBan values (?, ?, ?)', [playerName, reason, str(Utils.getTime() + bantime * 60 * 60)])

    def getTempBanInfo(this, playerName):
        Cursor.execute('select Reason, Time from UserTempBan where Username = ?', [playerName])
        for rs in Cursor.fetchall():
            return [rs['Reason'], rs['Time']]
        else:
            return ['Without a reason', 0]

    def getPermBanInfo(this, playerName):
        Cursor.execute('select Reason from UserPermaBan where Username = ?', [playerName])
        for rs in Cursor.fetchall():
            return rs['Reason']
        else:
            return 'Without a reason'

    def checkPermaBan(this, playerName):
        Cursor.execute('select 1 from UserPermaBan where Username = ?', [playerName])
        return Cursor.fetchone() != None

    def removePermaBan(this, playerName):
        if playerName in this.userPermaBanCache:
            this.userPermaBanCache.remove(playerName)
        Cursor.execute('delete from UserPermaBan where Username = ?', [playerName])
        Cursor.execute('update Users set UnRanked = 0 where Username = ?', [playerName])

    def tempBanIP(this, ip, time):
        if ip not in this.IPTempBanCache:
            this.IPTempBanCache.append(ip)
            if ip in this.IPTempBanCache:
                reactor.callLater(time, lambda : this.IPTempBanCache.remove(ip))

    def getTotalBanHours(this, playerName):
        Cursor.execute('select BanHours from Users where Username = ?', [playerName])
        rs = Cursor.fetchone()
        if rs:
            return rs['BanHours']
        else:
            return 0

    def voteBanPopulaire(this, playerName, playerVoted, ip):
        client = this.players.get(playerName)
        if client != None and client.privLevel == 1 and ip not in client.voteBan:
            client.voteBan.append(ip)
            if len(client.voteBan) == 10:
                this.banPlayer(playerName, 1, 'Vote Populaire', 'Server', False)
            this.sendStaffMessage(7, 'O jogador <V>%s</V> est\xc3\xa1 votando contra <V>%s</V> [<R>%s</R>/10]' % (playerVoted, playerName, len(client.voteBan)))
        return

    def muteUser(this, playerName, mutetime, reason):
        this.userMuteCache.append(playerName)
        Cursor.execute('insert into UserTempMute values (?, ?, ?)', [playerName, str(Utils.getTime() + mutetime * 60 * 60), reason])

    def removeModMute(this, playerName):
        if playerName in this.userMuteCache:
            this.userMuteCache.remove(playerName)
        Cursor.execute('delete from UserTempMute where Username = ?', [playerName])

    def getModMuteInfo(this, playerName):
        Cursor.execute('select Reason, Time from UserTempMute where Username = ?', [playerName])
        rs = Cursor.fetchone()
        if rs:
            return [rs['Reason'], rs['Time']]
        else:
            return ['Without a reason', 0]

    def mutePlayer(this, playerName, hours, reason, modName):
        client = this.players.get(playerName)
        if client != None:
            this.sendStaffMessage(5, '<V>%s</V> deixou <V>%s</V> sem falar por <V>%s</V> %s pelo seguinte motivo: <V>%s</V>' % (modName,
             playerName,
             hours,
             'hora' if hours == 1 else 'horas',
             reason))
            if playerName in this.userMuteCache:
                this.removeModMute(playerName)
            client.isMute = True
            client.sendModMute(playerName, hours, reason, False)
            client.sendModMute(playerName, hours, reason, True)
            this.muteUser(playerName, hours, reason)
        return

    def desmutePlayer(this, playerName, modName):
        client = this.players.get(playerName)
        if client != None:
            this.sendStaffMessage(5, '<V>%s</V> desmutou <V>%s</V>.' % (modName, playerName))
            this.removeModMute(playerName)
            client.isMute = False
        return

    def sendStaffChat(this, type, langue, playerName, message, sender):
        playerName = sender.playerName if type == -1 else ('' if type == 0 else ('Message Serveur' if type == 1 else sender.langue.upper() + '][' + {11: 'Admin][',
         10: 'Admin][',
         9: 'Coord][',
         8: 'Smod][',
         7: 'Mod][',
         6: 'MapCrew][',
         5: 'Helper][',
         4: 'DV][',
         3: 'LUA]['}[sender.privLevel]))
        if '][' in playerName:
            playerName += sender.playerName
        for client in (sender.room.clients if type == 0 else this.players).values():
            if (type == -1 or type == 0 or type == 1 or (type == 2 or type == 5) and client.privLevel >= 5 or (type == 3 or type == 4) and client.privLevel >= 7 or (type == 6 or type == 7) and client.privLevel >= 6 or type == 8 and client.privLevel >= 3 or type == 9 and client.privLevel >= 4) and (client.langue == langue or type == -1 or type == 1 or type == 4 or type == 5 or type == 6):
                client.sendPacket(Identifiers.send.Staff_Chat, ByteArray().writeByte(1 if type == -1 else type).writeUTF(playerName).writeUTF(message).writeShort(0).writeByte(0).toByteArray())

    def getplayerAvatar(this, playerName):
        if playerName.startswith('*'):
            return 0
        else:
            Cursor.execute('select avatar from Users where Username = ?', [playerName])
            rrf = Cursor.fetchone()
            if rrf is None:
                return 0
            if rrf[0] == 'None':
                return 0
            return int(rrf[0])
            return

    def getShamanType(this, playerCode):
        for client in this.players.values():
            if client.playerCode == playerCode:
                return client.shamanType

        return 0

    def getShamanLevel(this, playerCode):
        for client in this.players.values():
            if client.playerCode == playerCode:
                return client.shamanLevel

        return 0

    def getShamanBadge(this, playerCode):
        for client in this.players.values():
            if client.playerCode == playerCode:
                return client.parseSkill.getShamanBadge()

        return 0

    def getTribeHouse(this, tribeName):
        Cursor.execute('select House from Tribe where Name = ?', [tribeName])
        rs = Cursor.fetchone()
        if rs:
            return rs['House']
        else:
            return -1

    def getPlayerID(this, playerName):
        if playerName.startswith('*'):
            return 0
        elif this.players.has_key(playerName):
            return this.players[playerName].playerID
        Cursor.execute('select PlayerID from Users where Username = ?', [playerName])
        rs = Cursor.fetchone()
        if rs:
            return rs['PlayerID']
        else:
            return 0

    def getPlayerPrivlevel(this, playerName):
        if playerName.startswith('*'):
            return 0
        elif this.players.has_key(playerName):
            return this.players[playerName].privLevel
        Cursor.execute('select PrivLevel from Users where Username = ?', [playerName])
        rs = Cursor.fetchone()
        if rs:
            return rs['PrivLevel']
        else:
            return 0

    def getPlayerName(this, playerID):
        Cursor.execute('select Username from Users where PlayerID = ?', [playerID])
        rs = Cursor.fetchone()
        if rs:
            return rs['Username']
        else:
            return ''

    def getPlayerRoomName(this, playerName):
        if this.players.has_key(playerName):
            return this.players[playerName].roomName
        else:
            return ''

    def checkDuplicateEmail(this, email):
        Cursor.execute('select Username from Users where Email = ?', [email])
        if Cursor.fetchone():
            return True
        return False

    def checkEmailAddress(this, playerName, email):
        Cursor.execute('select Email from Users where Username = ?', [playerName])
        rs = Cursor.fetchone()
        if rs:
            return rs['Email'] == email
        return False

    def getPlayersCountMode(this, mode, langue):
        modeName = 'TsunaMice' if mode == 1 else ('TsunaMice vanilla' if mode == 3 else ('TsunaMice survivor' if mode == 8 else ('TsunaMice racing' if mode == 9 else ('TsunaMice music' if mode == 11 else ('TsunaMice bootcamp' if mode == 2 else ('TsunaMice defilante' if mode == 10 else ('TsunaMice village' if mode == 16 else ('' if mode == 18 else 'TsunaMice Module'))))))))
        playerCount = 0
        for room in this.rooms.values():
            if (room.isNormRoom or room.isTribeHouse or room.isTribewar or room.isBallonRace or room.isFlyGame or room.isDeathmatch or room.isPokeLua or room.isExplosionGame or room.isVillage or room.isTotemEditor or room.isTutorial or room.isDoubleMap or room.isVillage or room.isVanilla or room.isSurvivor or room.isRacing or room.isMusic or room.isBootcamp or room.isDefilante if mode == 1 else (room.isVanilla if mode == 3 else (room.isSurvivor if mode == 8 else (room.isRacing if mode == 9 else (room.isMusic if mode == 11 else (room.isBootcamp if mode == 2 else (room.isDefilante if mode == 10 else (room.isVillage if mode == 16 else True)))))))) and room.community == langue.lower():
                playerCount += room.getPlayerCount()

        return [modeName, playerCount]

    def parsePromotions(this):
        needUpdate = False
        i = 0
        while i < len(this.promotions):
            item = this.promotions[i]
            if item[3] < 1000:
                item[3] = Utils.getTime() + item[3] * 86400 + 30
                needUpdate = True
            this.shopPromotions.append([item[0],
             item[1],
             item[2],
             item[3]])
            i += 1

        if needUpdate:
            with open('./include/files/promotions.json', 'w') as f:
                json.dump(this.promotions, f)
        this.checkPromotionsEnd()

    def checkPromotionsEnd(this):
        needUpdate = False
        for promotion in this.shopPromotions:
            if Utils.getHoursDiff(promotion[3]) <= 0:
                this.shopPromotions.remove(promotion)
                needUpdate = True
                i = 0
                while i < len(this.promotions):
                    if this.promotions[i][0] == promotion[0] and this.promotions[i][1] == promotion[1]:
                        del this.promotions[i]
                    i += 1

        if needUpdate:
            with open('./include/files/promotions.json', 'w') as f:
                json.dump(this.promotions, f)

    def sendWholeServer(this, identifiers, result):
        for client in this.players.values():
            client.sendPacket(identifiers, result)

    def setVip(this, playerName, days):
        client = this.players.get(playerName)
        if client != None:
            if client.privLevel == 1:
                Cursor.execute('update Users SET VipTime = ? WHERE Username = ?', [Utils.getTime() + 24 * days * 3600, playerName])
                client.privLevel = 2
                this.sendModMessage(7, '<V>' + playerName + '<BL> se tornou <ROSE>VIP <BL>do <ROSE>TsunaMice<BL> por <V>' + str(days) + '<BL> dias.')
        else:
            Cursor.execute('update Users SET VipTime = ?, PrivLevel = 2 WHERE Username = ?', [Utils.getTime() + 24 * days * 3600, playerName])
            Cursor.fetchall()
            this.sendModMessage(7, '<V>' + playerName + '<BL> se tornou VIP do <ROSE>TsunaMice<BL> por <V>' + str(days) + '<BL> dias.')
        return

    def getPlayerCode(this, playerName):
        client = this.players.get(Utils.parsePlayerName(playerName))
        if client != None:
            return client.playerCode
        else:
            return 0

    def sendStaffMessage(this, minLevel, message, tab = False):
        for client in this.players.values():
            if client.privLevel >= minLevel:
                client.sendMessage(message, tab)

    def sendModMessage(this, minLevel, message):
        for client in this.players.values():
            if client.privLevel >= minLevel:
                client.sendPacket([6, 20], ByteArray().writeByte(0).writeUTF(message).writeShort(0).toByteArray())

    def getRanking(this):
        this.rankingTimer = reactor.callLater(300, this.getRanking)
        this.rankingsList = [{},
         {},
         {},
         {},
         {},
         {},
         {}]
        Cursor.execute('select Username, FirstCount from Users where PrivLevel < 3 order by FirstCount desc limit 0, 13')
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs['Username']
            this.rankingsList[0][count] = [playerName, this.players[playerName].firstCount if this.checkConnectedAccount(playerName) else rs['FirstCount']]
            count += 1

        Cursor.execute('select Username, CheeseCount from Users where PrivLevel < 3 order by CheeseCount desc limit 0, 13')
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs['Username']
            this.rankingsList[1][count] = [playerName, this.players[playerName].cheeseCount if this.checkConnectedAccount(playerName) else rs['CheeseCount']]
            count += 1

        Cursor.execute('select Username, ShamanSaves from Users where PrivLevel < 3 order by ShamanSaves desc limit 0, 13')
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs['Username']
            this.rankingsList[2][count] = [playerName, this.players[playerName].shamanSaves if this.checkConnectedAccount(playerName) else rs['ShamanSaves']]
            count += 1

        Cursor.execute('select Username, BootcampCount from Users where PrivLevel < 3 order by BootcampCount desc limit 0, 13')
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs['Username']
            this.rankingsList[3][count] = [playerName, this.players[playerName].bootcampCount if this.checkConnectedAccount(playerName) else rs['BootcampCount']]
            count += 1

        Cursor.execute('select Username, XDCoins from Users where PrivLevel < 3 order by XDCoins desc limit 0, 13')
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs['Username']
            this.rankingsList[4][count] = [playerName, this.players[playerName].XDCoins if this.checkConnectedAccount(playerName) else rs['XDCoins']]
            count += 1

        Cursor.execute('select Username, DeathCount from Users where PrivLevel < 3 order by DeathCount desc limit 0, 13')
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs['Username']
            this.rankingsList[5][count] = [playerName, this.players[playerName].deathCount if this.checkConnectedAccount(playerName) else rs['DeathCount']]
            count += 1

        Cursor.execute('select Name, Points from tribe ORDER By Points DESC LIMIT 0, 13')
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs['Name']
            this.rankingsList[6][count] = [playerName, this.players[playerName].tribePoints if this.checkConnectedAccount(playerName) else rs['Points']]
            count += 1


class Room():

    def __init__(this, server, name):
        this.mapXML = ''
        this.mapName = ''
        this.EMapXML = ''
        this.roomPassword = ''
        this.forceNextMap = '-1'
        this.currentSyncName = ''
        this.currentShamanName = ''
        this.currentSecondShamanName = ''
        this.addTime = 0
        this.mapCode = -1
        this.cloudID = -1
        this.EMapCode = 0
        this.objectID = 0
        this.redCount = 0
        this.mapPerma = -1
        this.blueCount = 0
        this.mapStatus = -1
        this.mapNoVotes = 0
        this.currentMap = 0
        this.receivedNo = 0
        this.EMapLoaded = 0
        this.roundTime = 120
        this.mapYesVotes = 0
        this.receivedYes = 0
        this.roundsCount = -1
        this.maxPlayers = 20
        this.numCompleted = 0
        this.numGetCheese = 0
        this.companionBox = -1
        this.gameStartTime = 0
        this.lastRoundCode = 0
        this.FSnumCompleted = 0
        this.SSnumCompleted = 0
        this.forceNextShaman = -1
        this.currentSyncCode = -1
        this.changeMapAttemps = 0
        this.currentShamanCode = -1
        this.currentShamanType = -1
        this.gameStartTimeMillis = 0
        this.currentSecondShamanCode = -1
        this.currentSecondShamanType = -1
        this.isMusic = False
        this.isClosed = False
        this.noShaman = False
        this.isEditor = False
        this.isRacing = False
        this.isSnowing = False
        this.isVillage = False
        this.isVanilla = False
        this.is801Room = False
        this.countStats = True
        this.isFixedMap = False
        this.isNormRoom = False
        this.isEventoAventura = False
        this.isTribewar = False
        this.isMinigame = False
        this.canCannon = False
        this.isDeathmatch = False
        this.isPokeLua = False
        this.isExplosionGame = False
        this.isInvocationGame = False
        this.isBallonRace = False
        this.isFlyGame = False
        this.isTutorial = False
        this.isBootcamp = False
        this.isSurvivor = False
        this.isVotingBox = False
        this.autoRespawn = False
        this.noAutoScore = False
        this.isDoubleMap = False
        this.specificMap = False
        this.mapInverted = False
        this.isDefilante = False
        this.canChangeMap = True
        this.isVotingMode = False
        this.isTribeHouse = False
        this.isNoShamanMap = False
        this.EMapValidated = False
        this.isTotemEditor = False
        this.initVotingMode = True
        this.disableAfkKill = False
        this.noShamanSkills = False
        this.isSurvivorVamp = False
        this.never20secTimer = False
        this.isTribeHouseMap = False
        this.changed20secTimer = False
        this.catchTheCheeseMap = False
        this.killAfkTimer = None
        this.endSnowTimer = None
        this.changeMapTimer = None
        this.contagemDeath = None
        this.voteCloseTimer = None
        this.startTimerLeft = None
        this.autoRespawnTimer = None
        this.anchors = []
        this.redTeam = []
        this.blueTeam = []
        this.roomTimers = []
        this.lastHandymouse = [-1, -1]
        this.noShamanMaps = [7,
         8,
         14,
         22,
         23,
         28,
         29,
         54,
         55,
         57,
         58,
         59,
         60,
         61,
         70,
         77,
         78,
         87,
         88,
         92,
         122,
         123,
         124,
         125,
         126,
         1007,
         888,
         200,
         201,
         202,
         203,
         204,
         205,
         206,
         207,
         208,
         209,
         210]
        this.mapList = [0,
         1,
         2,
         3,
         4,
         5,
         6,
         7,
         8,
         9,
         10,
         11,
         12,
         13,
         14,
         15,
         16,
         17,
         18,
         19,
         20,
         21,
         22,
         23,
         24,
         25,
         26,
         27,
         28,
         29,
         30,
         31,
         32,
         33,
         34,
         35,
         36,
         37,
         38,
         39,
         40,
         41,
         42,
         43,
         44,
         45,
         46,
         47,
         48,
         49,
         50,
         51,
         52,
         53,
         54,
         55,
         56,
         57,
         58,
         59,
         60,
         61,
         62,
         63,
         64,
         65,
         66,
         67,
         68,
         69,
         70,
         71,
         72,
         73,
         74,
         75,
         76,
         77,
         78,
         79,
         80,
         81,
         82,
         83,
         84,
         85,
         86,
         87,
         88,
         89,
         90,
         91,
         92,
         93,
         94,
         95,
         96,
         97,
         98,
         99,
         100,
         101,
         102,
         103,
         104,
         105,
         106,
         107,
         108,
         109,
         110,
         111,
         112,
         113,
         114,
         115,
         116,
         117,
         118,
         119,
         120,
         121,
         122,
         123,
         124,
         125,
         126,
         127,
         128,
         129,
         130,
         131,
         132,
         133,
         134,
         136,
         137,
         138,
         139,
         140,
         141,
         142,
         143,
         200,
         201,
         202,
         203,
         204,
         205,
         206,
         207,
         208,
         209,
         210]
        this.clients = {}
        this.currentTimers = {}
        this.currentShamanSkills = {}
        this.currentSecondShamanSkills = {}
        this.name = name
        this.server = server
        this.CursorMaps = CursorMaps
        this.recordTimer = reactor.callLater(5, this.recordAPI)
        if this.name.startswith('*'):
            this.community = 'xx'
            this.roomName = this.name
        else:
            this.community = this.name.split('-')[0].lower()
            this.roomName = this.name.split('-')[1]
        roomNameCheck = this.roomName[1:] if this.roomName.startswith('*') else this.roomName
        if this.roomName.startswith('\x03[Editeur] '):
            this.countStats = False
            this.isEditor = True
            this.never20secTimer = True
        elif this.roomName.startswith('\x03[Tutorial] '):
            this.countStats = False
            this.currentMap = 900
            this.specificMap = True
            this.noShaman = True
            this.never20secTimer = True
            this.isTutorial = True
        elif this.roomName.startswith('\x03[Totem] '):
            this.countStats = False
            this.specificMap = True
            this.currentMap = 444
            this.isTotemEditor = True
            this.never20secTimer = True
        elif this.roomName.startswith('*\x03'):
            this.countStats = False
            this.isTribeHouse = True
            this.autoRespawn = True
            this.never20secTimer = True
            this.noShaman = True
            this.disableAfkKill = True
            this.isFixedMap = True
            this.roundTime = 0
        elif re.search('racing', name.lower()):
            this.isRacing = True
            this.noShaman = True
            this.noAutoScore = True
            this.roundTime = 63
        elif re.search('bootcamp', name.lower()):
            this.isBootcamp = True
            this.countStats = False
            this.roundTime = 360
            this.never20secTimer = True
            this.autoRespawn = True
            this.noShaman = True
        elif re.search('vanilla', name.lower()):
            this.isVanilla = True
        elif re.search('eventoaventura', name.lower()):
            this.isNormRoom = True
            this.isEventoAventura = True
        elif re.search('vamp', name.lower()):
            this.isVillage = True
            this.noShaman = True
            this.isFixedMap = True
            this.roundTime = 0
        elif re.search('survivor', name.lower()):
            this.isSurvivor = True
            this.roundTime = 90
        elif re.search('defilante', name.lower()):
            this.isDefilante = True
            this.noShaman = True
            this.countStats = False
            this.noAutoScore = True
        elif re.search('#ballonrace', name.lower()):
            this.isBallonRace = True
            this.isVanilla = True
            this.isMinigame = True
            this.maxPlayers = 25
            this.roundTime = 120
            this.noShaman = True
        elif re.search('#deathmatch', name.lower()):
            this.countStats = True
            this.isDeathmatch = True
            this.isMinigame = True
            this.maxPlayers = 25
            this.roundTime = 120
            this.noShaman = True
            this.never20secTimer = True
        elif re.search('#fly', name.lower()):
            this.isFlyGame = True
            this.isVanilla = True
            this.isMinigame = True
            this.maxPlayers = 25
            this.roundTime = 120
            this.noShaman = True
        elif re.search('#pokelua', name.lower()):
            this.isPokeLua = True
            this.isVanilla = True
            this.isMinigame = True
            this.maxPlayers = 30
            this.roundTime = 120
        elif re.search('#tribewar', name.lower()):
            this.isTribewar = True
            this.isRacing = True
            this.noShaman = True
            this.roundTime = 63
            this.never20secTimer = True
        elif re.search('#explosion', name.lower()):
            this.isExplosionGame = True
            this.isVanilla = True
            this.isMinigame = True
            this.maxPlayers = 25
            this.roundTime = 120
            this.noShaman = True
        elif roomNameCheck.startswith('801') or roomNameCheck.startswith('village'):
            if roomNameCheck.startswith('village'):
                this.isVillage = True
            else:
                this.is801Room = True
            this.roundTime = 0
            this.never20secTimer = True
            this.autoRespawn = True
            this.countStats = False
            this.noShaman = True
            this.isFixedMap = True
            this.disableAfkKill = True
        else:
            this.isNormRoom = True
        this.mapChange()
        return None

    def addTextPopUpStaff(this, id, type, text, targetPlayer, x, y, width):
        p = ByteArray().writeInt(id).writeByte(type).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeByte(4)
        if targetPlayer == '':
            this.sendAll([29, 23], p.toByteArray())
        else:
            player = this.clients.get(targetPlayer)
            if player != None:
                player.sendPacket([29, 23], p.toByteArray())
        return

    def startTimer(this):
        for client in this.clients.values():
            client.sendMapStartTimer(False)

    def recordAPI(this):
        for client in this.clients.values():
            players = client.getConnectedPlayerCount()
            if players > this.server.recordPlayers:
                this.server.recordPlayers = players
                client.sendMessage('<R>Batemos nosso novo recorde de ' + str(players) + ' jogadores conectados.\nTodos jogadores online ganharam: 2 firsts e 10 moedas.')
                client.firstCount += 2
                client.cheeseCount += 2
                client.XDCoins += 10
                client.updateConfig()

        this.recordTimer = reactor.callLater(15, this.recordAPI)

    def checkIfOneFewRemaining(this):
        counts = [0, 0]
        for clientCode, client in this.clients.items():
            if client.isDead:
                counts[0] = counts[0] + 1
            else:
                counts[1] = counts[1] + 1

        if this.getPlayerCount >= 1:
            if counts[1] <= 1:
                return True
        return False

    def mapChange(this):
        if this.changeMapTimer != None:
            this.changeMapTimer.cancel()
        for client in this.clients.values():
            client.activeArtefact = 0

        for room in this.server.rooms.values():
            for playerCode, client in room.clients.items():
                if this.isDeathmatch:
                    if this.contagemDeath is not None:
                        this.contagemDeath.cancel()

        if not this.canChangeMap:
            this.changeMapAttemps += 1
            if this.changeMapAttemps < 5:
                this.changeMapTimer = reactor.callLater(1, this.mapChange)
                return
        for timer in this.roomTimers:
            timer.cancel()

        this.roomTimers = []
        for timer in [this.voteCloseTimer,
         this.killAfkTimer,
         this.autoRespawnTimer,
         this.startTimerLeft]:
            if timer != None:
                timer.cancel()

        if this.initVotingMode:
            if not this.isVotingBox and this.mapPerma == 0 and this.mapCode != -1 and this.getPlayerCount() >= 2:
                this.isVotingMode = True
                this.isVotingBox = True
                this.voteCloseTimer = reactor.callLater(8, this.closeVoting)
                for client in this.clients.values():
                    client.sendPacket(Identifiers.old.send.Vote_Box, [this.mapName, this.mapYesVotes, this.mapNoVotes])

            else:
                this.votingMode = False
                this.closeVoting()
        elif this.isTribeHouse and this.isTribeHouseMap:
            pass
        else:
            if this.isVotingMode:
                TotalYes = this.mapYesVotes + this.receivedYes
                TotalNo = this.mapNoVotes + this.receivedNo
                isDel = False
                if TotalYes + TotalNo >= 100:
                    TotalVotes = TotalYes + TotalNo
                    Rating = 1.0 * TotalYes / TotalNo * 100
                    rate = str(Rating).split('.')
                    if int(rate[0]) < 50:
                        isDel = True
                CursorMaps.execute('update Maps set YesVotes = ?, NoVotes = ?, Perma = 44 where Code = ?' if isDel else 'update Maps set YesVotes = ?, NoVotes = ? where Code = ?', [TotalYes, TotalNo, this.mapCode])
                this.isVotingMode = False
                this.receivedNo = 0
                this.receivedYes = 0
                for client in this.clients.values():
                    client.qualifiedVoted = False
                    client.isVoted = False

            this.initVotingMode = True
            this.lastRoundCode = (this.lastRoundCode + 1) % 127
            if this.isSurvivor:
                for client in this.clients.values():
                    if not client.isDead and (not client.isVampire if this.mapStatus == 0 else not client.isShaman):
                        if not this.noAutoScore:
                            client.playerScore += 10

            if this.catchTheCheeseMap:
                this.catchTheCheeseMap = False
            else:
                numCom = this.FSnumCompleted - 1 if this.isDoubleMap else this.numCompleted - 1
                numCom2 = this.SSnumCompleted - 1 if this.isDoubleMap else 0
                if numCom < 0:
                    numCom = 0
                if numCom2 < 0:
                    numCom2 = 0
                client = this.clients.get(this.currentShamanName)
                if client != None:
                    this.sendAll(Identifiers.old.send.Shaman_Perfomance, [this.currentShamanName, numCom])
                    if not this.noAutoScore:
                        client.playerScore = numCom
                    if numCom > 0:
                        client.parseSkill.earnExp(True, numCom)
                player2 = this.clients.get(this.currentSecondShamanName)
                if player2 != None:
                    this.sendAll(Identifiers.old.send.Shaman_Perfomance, [this.currentSecondShamanName, numCom2])
                    if not this.noAutoScore:
                        player2.playerScore = numCom2
                    if numCom2 > 0:
                        player2.parseSkill.earnExp(True, numCom2)
            if this.getPlayerCount() >= this.server.needToFirst:
                this.giveSurvivorStats() if this.isSurvivor else (this.giveRacingStats() if this.isRacing else None)
            this.currentSyncCode = -1
            this.currentShamanCode = -1
            this.currentShamanType = -1
            this.currentSecondShamanCode = -1
            this.currentSecondShamanType = -1
            this.currentSyncName = ''
            this.currentShamanName = ''
            this.currentSecondShamanName = ''
            this.currentShamanSkills = {}
            this.currentSecondShamanSkills = {}
            this.changed20secTimer = False
            this.isDoubleMap = False
            this.isNoShamanMap = False
            this.FSnumCompleted = 0
            this.SSnumCompleted = 0
            this.objectID = 0
            this.numGetCheese = 0
            this.addTime = 0
            this.cloudID = -1
            this.companionBox = -1
            this.lastHandymouse = [-1, -1]
            this.isTribeHouseMap = False
            this.canChangeMap = True
            this.changeMapAttemps = 0
            this.getSyncCode()
            this.anchors = []
            this.mapStatus = (this.mapStatus + 1) % 10
            this.numCompleted = 0
            this.currentMap = this.selectMap()
            this.checkMapXML()
            if this.currentMap in [range(44, 54), range(138, 144)] or this.mapPerma == 8 and this.getPlayerCount() >= 3:
                this.isDoubleMap = True
            if this.mapPerma in (7, 17, 42) or this.isSurvivor and this.mapStatus == 0:
                this.isNoShamanMap = True
            if this.currentMap in range(108, 114):
                this.catchTheCheeseMap = True
            this.gameStartTime = Utils.getTime()
            this.gameStartTimeMillis = time.time()
            for client in this.clients.values():
                client.resetPlay()

            for client in this.clients.values():
                client.startPlay()
                if client.isHidden:
                    client.sendPlayerDisconnect()

            for client in this.clients.values():
                if client.pet != 0:
                    if Utils.getSecondsDiff(client.petEnd) >= 0:
                        client.pet = 0
                        client.petEnd = 0
                    else:
                        this.sendAll(Identifiers.send.Pet, ByteArray().writeInt(client.playerCode).writeUnsignedByte(client.pet).toByteArray())

            if this.mapCode not in (-1, 31, 41, 42, 54, 55, 59, 60, 62, 89, 92, 99, 114, 801):
                CursorMaps.execute('select TopTime,TopTimeNick from maps where code = ?', [this.mapCode])
                rs = CursorMaps.fetchone()
                try:
                    if rs[0] > 0:
                        if rs[0] > 100:
                            t = rs[0] / 100.0
                        else:
                            t = rs[0] / 10.0
                        for client in this.clients.values():
                            client.sendMessage('<BL>Este mapa' '<J> @' + str(this.mapCode) + '<BL> tem record de <J>' + str(t) + 's<BL> por <J>' + str(rs[1]) + '<BL>.')
                    else: client.sendMessage('<BL>Este mapa' '<J> @' + str(this.mapCode) + '<BL> não possui record, faça o tempo mais rápido''<BL>.')
                except: pass

            if this.getPlayerCount() >= this.server.needToFirst:
                if this.isEventoAventura:
                    anyone = random.choice([0, 1])
                    itemID = random.choice([7462, 7463, 7464, 7465, 7466, 7467])
                    positionY = random.randint(0, 30)
                    if itemID == 7462:
                        idI = 1
                    elif itemID == 7463:
                        idI = 2
                    elif itemID == 7464:
                        idI = 3
                    elif itemID == 7465:
                        idI = 4
                    elif itemID == 7466:
                        idI = 5
                    elif itemID == 7467:
                        idI = 6
                    for player in this.clients.values():
                        if anyone == 1:
                            p = ByteArray()
                            p.writeByte(24)
                            p.writeByte(idI)
                            p.writeShort(itemID)
                            p.writeShort(positionY)
                            p.writeShort(-100)
                            player.sendPacket([5, 51], p.toByteArray())
                        player.sendPacket([100, 101], "\x01\x01")

            if this.isDeathmatch:
                this.PlayerDeathVivo = False
                this.canCannon = False
                for client in this.clients.values():
                    client.closedDeathWin()
                    client.sendContagem()

            if this.isRacing or this.isDefilante:
                this.roundsCount = (this.roundsCount + 1) % 10
                client = this.clients.get(this.getHighestScore())
                this.sendAll(Identifiers.send.Rounds_Count, ByteArray().writeByte(this.roundsCount).writeInt(client.playerCode if client != None else 0).toByteArray())
            this.startTimerLeft = reactor.callLater(3, this.startTimer)
            if not this.isFixedMap and not this.isTribeHouse and not this.isTribeHouseMap:
                this.changeMapTimer = reactor.callLater(this.roundTime + this.addTime, this.mapChange)
            this.killAfkTimer = reactor.callLater(30, this.killAfk)
            if this.autoRespawn or this.isTribeHouseMap:
                this.autoRespawnTimer = reactor.callLater(2, this.respawnMice)
        return

    def getPlayerCount(this):
        return len(filter(lambda client: not client.isHidden, this.clients.values()))

    def getPlayerCountUnique(this):
        ipList = []
        for client in this.clients.values():
            if client.ipAddress not in ipList:
                ipList.append(client.ipAddress)

        return len(ipList)

    def getPlayerList(this):
        result = []
        for client in this.clients.values():
            if not client.isHidden:
                result.append(client.getPlayerData())

        return result

    def addClient(this, client, newRoom = False):
        this.clients[client.playerName] = client
        client.room = this
        if not newRoom:
            client.isDead = True
            this.sendAllOthers(client, Identifiers.old.send.Player_Respawn, [client.getPlayerData()])
            client.startPlay()

    def removeClient(this, client):
        if client.playerName in this.clients:
            del this.clients[client.playerName]
            client.resetPlay()
            client.isDead = True
            client.playerScore = 0
            client.sendPlayerDisconnect()
            if len(this.clients) == 0:
                for timer in [this.autoRespawnTimer,
                 this.changeMapTimer,
                 this.endSnowTimer,
                 this.killAfkTimer,
                 this.voteCloseTimer]:
                    if timer != None:
                        timer.cancel()

                del this.server.rooms[this.name]
            else:
                if client.playerCode == this.currentSyncCode:
                    this.currentSyncCode = -1
                    this.currentSyncName = ''
                    this.getSyncCode()
                this.checkChangeMap()
        return

    def checkChangeMap(this):
        if not (this.isBootcamp or this.autoRespawn or this.isTribeHouse and this.isTribeHouseMap or this.isFixedMap):
            alivePeople = filter(lambda client: not client.isDead, this.clients.values())
            if not alivePeople:
                this.mapChange()

    def sendMessage(this, message1, message2, AP, *args):
        for client in this.clients.values():
            if client.playerName != AP:
                client.sendLangueMessage(message1, message2, *args)

    def sendAll(this, identifiers, packet = ''):
        for client in this.clients.values():
            client.sendPacket(identifiers, packet)

    def sendAllOthers(this, senderClient, identifiers, packet = ''):
        for client in this.clients.values():
            if not client == senderClient:
                client.sendPacket(identifiers, packet)

    def sendAllChat(this, playerCode, playerName, message, langueID, isOnly):
        packet = ByteArray().writeInt(playerCode).writeUTF(playerName).writeByte(langueID).writeUTF(message)
        if not isOnly:
            for client in this.clients.values():
                if playerName not in client.ignoredsList:
                    client.sendPacket(Identifiers.send.Chat_Message, packet.toByteArray())

        else:
            client = this.clients.get(playerName)
            if client != None:
                client.sendPacket(Identifiers.send.Chat_Message, packet.toByteArray())
        return

    def getSyncCode(this):
        if this.getPlayerCount() > 0:
            if this.currentSyncCode == -1:
                client = random.choice(this.clients.values())
                this.currentSyncCode = client.playerCode
                this.currentSyncName = client.playerName
        elif this.currentSyncCode == -1:
            this.currentSyncCode = 0
            this.currentSyncName = ''
        return this.currentSyncCode

    def selectMap(this):
        if not this.forceNextMap == '-1':
            force = this.forceNextMap
            this.forceNextMap = '-1'
            this.mapCode = -1
            if force.isdigit():
                return this.selectMapSpecificic(force, 'Vanilla')
            elif force.startswith('@'):
                return this.selectMapSpecificic(force[1:], 'Custom')
            elif force.startswith('#'):
                return this.selectMapSpecificic(force[1:], 'Perm')
            elif force.startswith('<'):
                return this.selectMapSpecificic(force, 'Xml')
            else:
                return 0
        else:
            if this.specificMap:
                this.mapCode = -1
                return this.currentMap
            if this.isEditor:
                return this.EMapCode
            if this.isTribeHouse:
                tribeName = this.roomName[2:]
                runMap = this.server.getTribeHouse(tribeName)
                if runMap == 0:
                    this.mapCode = 0
                    this.mapName = 'Danshweger'
                    this.mapXML = '<C><P /><Z><S><S Y="360" T="0" P="0,0,0.3,0.2,0,0,0,0" L="800" H="80" X="400" /></S><D><P Y="0" T="34" P="0,0" X="0" C="719b9f" /><T Y="320" X="49" /><P Y="320" T="16" X="224" P="0,0" /><P Y="319" T="17" X="311" P="0,0" /><P Y="284" T="18" P="1,0" X="337" C="57703e,e7c3d6" /><P Y="284" T="21" X="294" P="0,0" /><P Y="134" T="23" X="135" P="0,0" /><P Y="320" T="24" P="0,1" X="677" C="46788e" /><P Y="320" T="26" X="588" P="1,0" /><P Y="193" T="14" P="0,0" X="562" C="95311e,bde8f3,faf1b3" /></D><O /></Z></C>'
                    this.mapYesVotes = 0
                    this.mapNoVotes = 0
                    this.mapPerma = 22
                    this.mapInverted = False
                else:
                    run = this.selectMapSpecificic(runMap, 'Custom')
                    if run != -1:
                        this.mapCode = 0
                        this.mapName = 'Danshweger'
                        this.mapXML = '<C><P /><Z><S><S Y="360" T="0" P="0,0,0.3,0.2,0,0,0,0" L="800" H="80" X="400" /></S><D><P Y="0" T="34" P="0,0" X="0" C="719b9f" /><T Y="320" X="49" /><P Y="320" T="16" X="224" P="0,0" /><P Y="319" T="17" X="311" P="0,0" /><P Y="284" T="18" P="1,0" X="337" C="57703e,e7c3d6" /><P Y="284" T="21" X="294" P="0,0" /><P Y="134" T="23" X="135" P="0,0" /><P Y="320" T="24" P="0,1" X="677" C="46788e" /><P Y="320" T="26" X="588" P="1,0" /><P Y="193" T="14" P="0,0" X="562" C="95311e,bde8f3,faf1b3" /></D><O /></Z></C>'
                        this.mapYesVotes = 0
                        this.mapNoVotes = 0
                        this.mapPerma = 22
                        this.mapInverted = False
            else:
                if this.is801Room or this.isVillage:
                    return 801
                if this.isVanilla:
                    this.mapCode = -1
                    this.mapName = 'Invalid'
                    this.mapXML = '<C><P /><Z><S /><D /><O /></Z></C>'
                    this.mapYesVotes = 0
                    this.mapNoVotes = 0
                    this.mapPerma = -1
                    this.mapInverted = False
                    map = random.choice(this.mapList)
                    while map == this.currentMap:
                        map = random.choice(this.mapList)

                    return map
                this.mapCode = -1
                this.mapName = 'Invalid'
                this.mapXML = '<C><P /><Z><S /><D /><O /></Z></C>'
                this.mapYesVotes = 0
                this.mapNoVotes = 0
                this.mapPerma = -1
                this.mapInverted = False
                return this.selectMapStatus()
        return -1

    def selectMapStatus(this):
        maps = [0,
         -1,
         4,
         9,
         5,
         0,
         -1,
         8,
         6,
         7]
        selectPerma = (17 if this.mapStatus % 2 == 0 else 17) if this.isRacing else ((13 if this.mapStatus % 2 == 0 else 3) if this.isBootcamp else (18 if this.isDefilante else ((11 if this.mapStatus == 0 else 10) if this.isSurvivor else (31 if this.isDeathmatch else (19 if this.isMusic and this.mapStatus % 2 == 0 else 0)))))
        isMultiple = False
        if this.isNormRoom:
            if this.mapStatus < len(maps) and maps[this.mapStatus] != -1:
                isMultiple = maps[this.mapStatus] == 0
                selectPerma = maps[this.mapStatus]
            else:
                map = random.choice(this.mapList)
                while map == this.currentMap:
                    map = random.choice(this.mapList)

                return map
        elif this.isDeathmatch:
            CursorMaps.execute('select Code from maps where Perma = 31 ORDER BY RANDOM() LIMIT 1')
            r = CursorMaps.fetchall()
            for rs in r:
                this.mapList.append(rs[0])

        elif this.isVanilla or this.isMusic and this.mapStatus % 2 != 0:
            map = random.choice(this.mapList)
            while map == this.currentMap:
                map = random.choice(this.mapList)

            return map
        CursorMaps.execute('select * from Maps where Code != ' + str(this.currentMap) + ' and Perma = 0 or Perma = 1 ORDER BY RANDOM() LIMIT 1' if isMultiple else 'select * from Maps where Code != ' + str(this.currentMap) + ' and Perma = ' + str(selectPerma) + ' order by random() limit 1')
        rs = CursorMaps.fetchone()
        if rs:
            this.mapCode = rs['Code']
            this.mapName = rs['Name']
            this.mapXML = rs['XML']
            this.mapYesVotes = rs['YesVotes']
            this.mapNoVotes = rs['NoVotes']
            this.mapPerma = rs['Perma']
            this.mapInverted = random.randint(0, 100) > 85
        else:
            map = random.choice(this.mapList)
            while map == this.currentMap:
                map = random.choice(this.mapList)

            return map
        return -1

    def selectMapSpecificic(this, code, type):
        if type == 'Vanilla':
            return int(code)
        else:
            if type == 'Custom':
                mapInfo = this.getMapInfo(int(code))
                if mapInfo[0] == None:
                    return 0
                else:
                    this.mapCode = int(code)
                    this.mapName = str(mapInfo[0])
                    this.mapXML = str(mapInfo[1])
                    this.mapYesVotes = int(mapInfo[2])
                    this.mapNoVotes = int(mapInfo[3])
                    this.mapPerma = int(mapInfo[4])
                    this.mapInverted = False
                    return -1
            elif type == 'Perm':
                mapList = []
                CursorMaps.execute('select Code from Maps where Perma = ?', [int(str(code))])
                for rs in CursorMaps.fetchall():
                    mapList.append(rs['Code'])

                if len(mapList) >= 1:
                    runMap = random.choice(mapList)
                else:
                    runMap = 0
                if len(mapList) >= 2:
                    while runMap == this.currentMap:
                        runMap = random.choice(mapList)

                if runMap == 0:
                    map = random.choice(this.MapList)
                    while map == this.currentMap:
                        map = random.choice(this.MapList)

                    return map
                else:
                    mapInfo = this.getMapInfo(runMap)
                    this.mapCode = runMap
                    this.mapName = str(mapInfo[0])
                    this.mapXML = str(mapInfo[1])
                    this.mapYesVotes = int(mapInfo[2])
                    this.mapNoVotes = int(mapInfo[3])
                    this.mapPerma = int(mapInfo[4])
                    this.mapInverted = False
                    return -1
            elif type == 'Xml':
                this.mapCode = 0
                this.mapName = '#Module'
                this.mapXML = str(code)
                this.mapYesVotes = 0
                this.mapNoVotes = 0
                this.mapPerma = 22
                this.mapInverted = False
                return -1
            return

    def getMapInfo(this, mapCode):
        mapInfo = ['',
         '',
         0,
         0,
         0]
        CursorMaps.execute('select Name, XML, YesVotes, NoVotes, Perma from Maps where Code = ?', [mapCode])
        rs = CursorMaps.fetchone()
        if rs:
            mapInfo = (rs['Name'],
             rs['XML'],
             rs['YesVotes'],
             rs['NoVotes'],
             rs['Perma'])
        return mapInfo

    def checkIfDeathMouse(this):
        return len(filter(lambda client: not client.isDead, this.clients.values())) <= 1

    def checkIfTooFewRemaining(this):
        return len(filter(lambda client: not client.isDead, this.clients.values())) <= 2

    def getAliveCount(this):
        return len(filter(lambda client: not client.isDead, this.clients.values()))

    def getDeathCountNoShaman(this):
        return len(filter(lambda client: not client.isShaman and not client.isDead, this.clients.values()))

    def getHighestScore(this):
        playerScores = []
        playerID = 0
        for client in this.clients.values():
            playerScores.append(client.playerScore)

        for client in this.clients.values():
            if client.playerScore == max(playerScores):
                playerID = client.playerCode

        return playerID

    def getSecondHighestScore(this):
        playerScores = []
        playerID = 0
        for client in this.clients.values():
            playerScores.append(client.playerScore)

        playerScores.remove(max(playerScores))
        if len(playerScores) >= 1:
            for client in this.clients.values():
                if client.playerScore == max(playerScores):
                    playerID = client.playerCode

        return playerID

    def getShamanCode(this):
        if this.currentShamanCode == -1:
            if this.currentMap in this.noShamanMaps or this.isNoShamanMap or this.noShaman:
                pass
            elif this.forceNextShaman > 0:
                this.currentShamanCode = this.forceNextShaman
                this.forceNextShaman = 0
            else:
                this.currentShamanCode = this.getHighestScore()
            if this.currentShamanCode == -1:
                this.currentShamanName = ''
            else:
                for client in this.clients.values():
                    if client.playerCode == this.currentShamanCode:
                        this.currentShamanName = client.playerName
                        this.currentShamanType = client.shamanType
                        this.currentShamanSkills = client.playerSkills
                        break

        return this.currentShamanCode

    def getDoubleShamanCode(this):
        if this.currentShamanCode == -1 and this.currentSecondShamanCode == -1:
            if this.forceNextShaman > 0:
                this.currentShamanCode = this.forceNextShaman
                this.forceNextShaman = 0
            else:
                this.currentShamanCode = this.getHighestScore()
            if this.currentSecondShamanCode == -1:
                this.currentSecondShamanCode = this.getSecondHighestScore()
            if this.currentSecondShamanCode == this.currentShamanCode:
                tempClient = random.choice(this.clients.values())
                this.currentSecondShamanCode = tempClient.playerCode
            for client in this.clients.values():
                if client.playerCode == this.currentShamanCode:
                    this.currentShamanName = client.playerName
                    this.currentShamanType = client.shamanType
                    this.currentShamanSkills = client.playerSkills
                    break
                if client.playerCode == this.currentSecondShamanCode:
                    this.currentSecondShamanName = client.playerName
                    this.currentSecondShamanType = client.shamanType
                    this.currentSecondShamanSkills = client.playerSkills
                    break

        return [this.currentShamanCode, this.currentSecondShamanCode]

    def closeVoting(this):
        this.initVotingMode = False
        this.isVotingBox = False
        if this.voteCloseTimer != None:
            this.voteCloseTimer.cancel()
        this.mapChange()
        return

    def killShaman(this):
        for client in this.clients.values():
            if client.playerCode == this.currentShamanCode:
                client.isDead = True
                client.sendPlayerDied()

        this.checkChangeMap()

    def killAfk(this):
        if this.isEditor or this.isTotemEditor or this.isBootcamp or this.isTribeHouseMap or this.disableAfkKill:
            return
        if Utils.getTime() - this.gameStartTime < 32 and Utils.getTime() - this.gameStartTime > 28:
            for client in this.clients.values():
                if not client.isDead and client.isAfk:
                    client.isDead = True
                    if not this.noAutoScore:
                        client.playerScore += 1
                    client.sendPlayerDied()

            this.checkChangeMap()

    def checkIfDoubleShamansAreDead(this):
        player1 = this.clients.get(this.currentShamanName)
        player2 = this.clients.get(this.currentSecondShamanName)
        return (False if player1 == None else player1.isDead) and (False if player2 == None else player2.isDead)

    def checkIfShamanIsDead(this):
        client = this.clients.get(this.currentShamanName)
        if client == None:
            return False
        else:
            return client.isDead

    def checkIfShamanCanGoIn(this):
        for client in this.clients.values():
            if client.playerCode != this.currentShamanCode and client.playerCode != this.currentSecondShamanCode and not client.isDead:
                return False

        return True

    def giveShamanSave(this, shamanName, type):
        if not this.countStats:
            return
        else:
            client = this.clients.get(shamanName)
            if client != None:
                if type == 0:
                    client.shamanSaves += 1
                elif type == 1:
                    client.hardModeSaves += 1
                elif type == 2:
                    client.divineModeSaves += 1
                if client.privLevel != 0:
                    counts = [client.shamanSaves, client.hardModeSaves, client.divineModeSaves]
                    titles = [this.server.shamanTitleList, this.server.hardModeTitleList, this.server.divineModeTitleList]
                    rebuilds = ['shaman', 'hardmode', 'divinemode']
                    if titles[type].has_key(counts[type]):
                        title = titles[type][counts[type]]
                        client.checkAndRebuildTitleList(rebuilds[type])
                        client.sendUnlockedTitle(int(title - title % 1), int(round(title % 1 * 10)))
                        client.sendCompleteTitleList()
                        client.sendTitleList()
            return

    def respawnMice(this):
        for client in this.clients.values():
            if client.isDead:
                client.isDead = False
                client.playerStartTimeMillis = time.time()
                this.sendAll(Identifiers.old.send.Player_Respawn, [client.getPlayerData(), 0 if this.isBootcamp else 1])

        if this.autoRespawn or this.isTribeHouseMap:
            this.autoRespawnTimer = reactor.callLater(2, this.respawnMice)

    def respawnSpecific(this, playerName):
        client = this.clients.get(playerName)
        if client != None and client.isDead:
            client.resetPlay()
            client.isAfk = False
            client.playerStartTimeMillis = time.time()
            this.sendAll(Identifiers.old.send.Player_Respawn, [client.getPlayerData(), 0 if this.isBootcamp else 1])
        return

    def checkMapXML(this):
        if int(this.currentMap) in this.server.vanillaMaps:
            this.mapCode = int(this.currentMap)
            this.mapName = '_Atelier 801' if this.mapCode == 801 else 'Transformice'
            this.mapXML = str(this.server.vanillaMaps[int(this.currentMap)])
            this.mapYesVotes = 0
            this.mapNoVotes = 0
            this.mapPerma = 41
            this.currentMap = -1
            this.mapInverted = False

    def sendVampireMode(this):
        client = this.clients.get(this.currentSyncName)
        if client != None:
            client.sendVampireMode(False)
        return

    def addPhysicObject(this, id, x, y, bodyDef):
        this.sendAll(Identifiers.send.Add_Physic_Object, ByteArray().writeShort(id).writeBoolean(bool(bodyDef['dynamic']) if bodyDef.has_key('dynamic') else False).writeByte(int(bodyDef['type']) if bodyDef.has_key('type') else 0).writeShort(x).writeShort(y).writeShort(int(bodyDef['width']) if bodyDef.has_key('width') else 0).writeShort(int(bodyDef['height']) if bodyDef.has_key('height') else 0).writeBoolean(bool(bodyDef['foreground']) if bodyDef.has_key('foreground') else False).writeShort(int(bodyDef['friction']) if bodyDef.has_key('friction') else 0).writeShort(int(bodyDef['restitution']) if bodyDef.has_key('restitution') else 0).writeShort(int(bodyDef['angle']) if bodyDef.has_key('angle') else 0).writeBoolean(bodyDef.has_key('color')).writeInt(int(bodyDef['color']) if bodyDef.has_key('color') else 0).writeBoolean(bool(bodyDef['miceCollision']) if bodyDef.has_key('miceCollision') else True).writeBoolean(bool(bodyDef['groundCollision']) if bodyDef.has_key('groundCollision') else True).writeBoolean(bool(bodyDef['fixedRotation']) if bodyDef.has_key('fixedRotation') else False).writeShort(int(bodyDef['mass']) if bodyDef.has_key('mass') else 0).writeShort(int(bodyDef['linearDamping']) if bodyDef.has_key('linearDamping') else 0).writeShort(int(bodyDef['angularDamping']) if bodyDef.has_key('angularDamping') else 0).writeBoolean(False).writeUTF('').toByteArray())

    def removeObject(this, objectId):
        this.sendAll(Identifiers.send.Remove_Object, ByteArray().writeInt(objectId).writeBoolean(True).toByteArray())

    def bindKeyBoard(this, playerName, key, down, yes):
        client = this.clients.get(playerName)
        if client != None:
            client.sendPacket(Identifiers.send.Bind_Key_Board, ByteArray().writeShort(key).writeBoolean(down).writeBoolean(yes).toByteArray())
        return

    def movePlayer(this, playerName, xPosition, yPosition, pOffSet, xSpeed, ySpeed, sOffSet):
        client = this.clients.get(playerName)
        if client != None:
            client.sendPacket(Identifiers.send.Move_Player, ByteArray().writeShort(xPosition).writeShort(yPosition).writeBoolean(pOffSet).writeShort(xSpeed).writeShort(ySpeed).writeBoolean(sOffSet).toByteArray())
        return

    def setNameColor(this, playerName, color):
        if this.clients.has_key(playerName):
            this.sendAll(Identifiers.send.Set_Name_Color, ByteArray().writeInt(this.clients.get(playerName).playerCode).writeInt(color).toByteArray())

    def addPopup(this, id, type, text, targetPlayer, x, y, width, fixedPos):
        p = ByteArray().writeInt(id).writeByte(type).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeBoolean(fixedPos)
        if targetPlayer == '':
            this.sendAllBin([29, 23], p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket([29, 23], p.toByteArray())
        return

    def addTextArea(this, id, text, targetPlayer, x, y, width, height, backgroundColor, borderColor, backgroundAlpha, fixedPos):
        p = ByteArray().writeInt(id).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeShort(height).writeInt(backgroundColor).writeInt(borderColor).writeByte(100 if backgroundAlpha > 100 else backgroundAlpha).writeBoolean(fixedPos)
        if targetPlayer == '':
            this.sendAll(Identifiers.send.Add_Text_Area, p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Add_Text_Area, p.toByteArray())
        return

    def removeTextArea(this, id, targetPlayer):
        p = ByteArray().writeInt(id)
        if targetPlayer == '':
            this.sendAll(Identifiers.send.Remove_Text_Area, p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Remove_Text_Area, p.toByteArray())
        return

    def updateTextArea(this, id, text, targetPlayer):
        p = ByteArray().writeInt(id).writeUTF(text)
        if targetPlayer == '':
            this.sendAllBin([29, 21], p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket([29, 21], p.toByteArray())
        return

    def bindMouse(this, playerName, yes):
        client = this.clients.get(playerName)
        if client != None:
            client.sendPacket(Identifiers.send.Bind_Mouse, ByteArray().writeBoolean(yes).toByteArray())
        return

    def showColorPicker(this, id, targetPlayer, defaultColor, title):
        packet = ByteArray().writeInt(id).writeInt(defaultColor).writeUTF(title)
        if targetPlayer == '':
            this.sendAll(Identifiers.send.Show_Color_Picker, packet.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Show_Color_Picker, packet.toByteArray())
        return

    def startSnowSchedule(this, power):
        if this.isSnowing:
            this.startSnow(0, power, False)

    def startSnow(this, millis, power, enabled):
        this.isSnowing = enabled
        this.sendAll(Identifiers.send.Snow, ByteArray().writeBoolean(enabled).writeShort(power).toByteArray())
        if enabled:
            this.endSnowTimer = reactor.callLater(millis, lambda : this.startSnowSchedule(power))

    def giveSurvivorStats(this):
        for player in this.clients.values():
            player.survivorStats[0] += 1
            if player.isShaman:
                player.survivorStats[1] += 1
                player.survivorStats[2] += this.getDeathCountNoShaman()
            elif not player.isDead:
                player.survivorStats[3] += 1

    def giveRacingStats(this):
        for player in this.clients.values():
            player.racingStats[0] += 1
            if player.hasCheese or player.hasEnter:
                player.racingStats[1] += 1
            if player.hasEnter:
                if player.currentPlace <= 3:
                    player.racingStats[2] += 1
                if player.currentPlace == 1:
                    player.racingStats[3] += 1

    def send20SecRemainingTimer(this):
        if not this.changed20secTimer:
            if not this.never20secTimer and this.roundTime + (this.gameStartTime - Utils.getTime()) > 21:
                this.changed20secTimer = True
                this.changeMapTimers(20)
                for client in this.clients.values():
                    client.sendRoundTime(20)

    def changeMapTimers(this, seconds):
        if this.changeMapTimer != None:
            this.changeMapTimer.cancel()
        this.changeMapTimer = reactor.callLater(seconds, this.mapChange)
        return

    def newConsumableTimer(this, code):
        this.roomTimers.append(reactor.callLater(10, lambda : this.sendAll(Identifiers.send.Remove_Object, ByteArray().writeInt(code).writeBoolean(False).toByteArray())))


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('./include/configs.properties')
    Database, Cursor = (None, None)
    Database = sqlite3.connect('./database/Users.db', check_same_thread=False)
    Database.text_factory = str
    Database.isolation_level = None
    Database.row_factory = sqlite3.Row
    Cursor = Database.cursor()
    DatabaseCafe, CursorCafe = (None, None)
    DatabaseCafe = sqlite3.connect('./database/Cafe.db', check_same_thread=False)
    DatabaseCafe.text_factory = str
    DatabaseCafe.isolation_level = None
    DatabaseCafe.row_factory = sqlite3.Row
    CursorCafe = DatabaseCafe.cursor()
    DatabaseMaps, CursorMaps = (None, None)
    DatabaseMaps = sqlite3.connect('./database/Maps.db', check_same_thread=False)
    DatabaseMaps.text_factory = str
    DatabaseMaps.isolation_level = None
    DatabaseMaps.row_factory = sqlite3.Row
    CursorMaps = DatabaseMaps.cursor()
    dateNow = datetime.now()
    os.system('title Source TsunaMice - 1.415')
    validPorts = []
    S = Server()
    for port in [443,
     6112,
     5555,
     44440,
     44444,
     3724]:
        try:
            reactor.listenTCP(port, S)
            validPorts.append(port)
        except:
            print 'Portas falharam > ' + str(port)

    if not validPorts == []:
        print '[%s] %s serveur running.' % (time.strftime('%H:%M:%S'), config.get('configGame', 'game.miceName'))
    reactor.run()# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2017.06.19 20:29:16 Hora oficial do Brasil
