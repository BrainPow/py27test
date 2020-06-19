# -*- coding: utf-8 -*-
import random, time, struct
from twisted.internet import reactor
from ByteArray import ByteArray
class Games:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        this.Cursor = client.Cursor
        this.deathBallonTime = time.time()

    def InvocationEventKeyboard(this, playerName, keyCode, down, xPlayerPosition, yPlayerPosition):
        if keyCode == 32:
            if this.client.invocationpoints >= 1:
                item = [28, 1, 2, 29, 30, 31, 32, 33, 34, 35, 3, 4]
                id = random.choice(item)
                this.client.spawnObject(id, xPlayerPosition+4, yPlayerPosition+16, 1)
                this.client.invocationpoints -= 1
                this.client.sendMessage("<ROSE>[INVOCATION] - <N>Você possui: "+str(this.client.invocationpoints)+" items!")
            else:
                this.client.sendMessage("<ROSE>[INVOCATION] - <N>Você não possui items, aguarde...")

    def sendMessageLoginAventura(this):
        this.client.sendMessage("<J>[EVENTO] <VP>Bem vindo ao <CH>Evento de Aventura, <VP>"+str(this.client.playerName)+"!")
        this.client.sendMessage("<J>[EVENTO] <CH>Como funciona este evento? <N>É simples, você precisa pegar os itens que aparecem no mapa e entrar com ele na toca.")
        this.client.sendMessage("<J>[EVENTO] <N>Se você firstar com o item do evento, ganhará 7 firsts/moedas e acumulará o item no seu perfil em <CH>Pontos de Aventura<N>, com 30/30 você ganhará medalhas e títulos personalizados.")

    def sendMessageLoginTribewar(this):
        this.client.sendMessage("<N>[TRIBEWAR] <ROSE>-> Seja bem-vindo à sala: <N>#tribewar")
        this.client.sendMessage("<N>[TRIBEWAR] <ROSE>-> Ranking TribeWar: <N>/ranktribewar")

    def sendMessageLoginInvocation(this):
        this.client.sendMessage("<ROSE>[INVOCATION] - <N>Seja bem-vindo a sala <ROSE>#Invocation!")
        this.client.sendMessage("<ROSE>[INVOCATION] - <N>Aperte o espaço no seu teclado para usar items")
        this.client.sendMessage("<ROSE>[INVOCATION] - <N>Você possui: "+str(this.client.invocationpoints)+" items!")

    def sendMessageLoginDeath(this):
        this.client.room.bindKeyBoard(this.client.playerName, 3, False, this.client.room.isDeathmatch)
        this.client.room.bindKeyBoard(this.client.playerName, 32, False, this.client.room.isDeathmatch)
        this.client.room.bindKeyBoard(this.client.playerName, 79, False, this.client.room.isDeathmatch)
        this.client.room.bindKeyBoard(this.client.playerName, 80, False, this.client.room.isDeathmatch)
        this.client.sendMessage("<VP>Bem-vindo à sala de minigame <J>#Deathmatch!")
        this.client.sendMessage("<VP>Para usar um cannon utilize a tecla de <J>espaço <VP>ou <J>a seta para baixo!")
        this.client.sendMessage("<CH>Ranking de Deathmatch: <N>Aperte a <J>Letra (L)\n<CH>Abrir o Perfil:<N> Aperte a <J>Letra (P)\n<CH>Abrir o Inventário:<N> Aperte a <J>Letra (O)")

    def deathEventKeyboard(this, _player, key, down, x, y):
        if key == 3 or key == 32 and not this.client.isDead and this.client.PlayerDeathVivo == True:										
            if not this.client.canCN:
                this.client.room.objectID += 1
                idCannon = {15: "149aeaa271c.png", 16: "149af112d8f.png", 17: "149af12c2d6.png", 18: "149af130a30.png", 19: "149af0fdbf7.png", 20: "149af0ef041.png", 21: "149af13e210.png", 22: "149af129a4c.png", 23: "149aeaa06d1.png"}
                if not this.client.isDead:
                    if str(this.client.mDirection) == "0":
                        posXLeft = x+4
                        posYLeft = y+8
                        if this.client.deathStats[0] == 2 and this.client.deathStats[1] == 8:
                            this.client.addShamanObject(1704, int(posXLeft), int(posYLeft), int(1),-90)
                            reactor.callLater(2, this.client.room.removeObject, 1704)
                        else:
                            x = int(posXLeft+this.client.deathStats[0]) if this.client.deathStats[0] < 0 else int(posXLeft+this.client.deathStats[0])
                            y = int(posYLeft+this.client.deathStats[1]) if this.client.deathStats[1] < 0 else int(posYLeft+this.client.deathStats[1])
                            this.client.sendPlaceObjectDeath(this.client.room.objectID, 17, x, y, -90, 0, 0, True, True)
                            reactor.callLater(2, this.client.room.removeObject, this.client.room.objectID)
                            if this.client.deathStats[4] in [15, 16, 17, 18, 19, 20, 21, 22, 23]:
                                if not this.client.deathStats[3] == 1:
                                    this.client.room.sendAll([29, 19], ByteArray().writeInt(this.client.playerCode).writeUTF(idCannon[this.client.deathStats[4]]).writeByte(1).writeInt(this.client.room.objectID).toByteArray()+"\xff\xf0\xff\xf0")
                if not this.client.isDead:
                    if str(this.client.mDirection) == "1":
                        posXRight = x-8
                        posYRight = y+4
                        if this.client.deathStats[0] == 2 and this.client.deathStats[1] == 8:  
                            this.client.addShamanObject(1704, int(posXRight), int(posYRight), int(1),90)
                            reactor.callLater(2, this.client.room.removeObject, 1704)
                        else:
                            x = int(posXRight+this.client.deathStats[0]) if this.client.deathStats[0] < 0 else int(posXRight+this.client.deathStats[0])
                            y = int(posYRight+this.client.deathStats[1]) if this.client.deathStats[1] < 0 else int(posYRight+this.client.deathStats[1])
                            this.client.sendPlaceObjectDeath(this.client.room.objectID, 17, x, y, 90, 0, 0, True, True)
                            reactor.callLater(2, this.client.room.removeObject, this.client.room.objectID)
                            if this.client.deathStats[4] in [15, 16, 17, 18, 19, 20, 21, 22, 23]:
                                if not this.client.deathStats[3] == 1:
                                    this.client.room.sendAll([29, 19], ByteArray().writeInt(this.client.playerCode).writeUTF(idCannon[this.client.deathStats[4]]).writeByte(1).writeInt(this.client.room.objectID).toByteArray()+"\xff\xf0\xff\xf0")

                this.client.canCN = True
                this.canCCN = reactor.callLater(0.7, this.client.cnTrueOrFalse) 


    def ballonEventKeyboard(this, playerName, keyCode, down, xPlayerPosition, yPlayerPosition):
        if keyCode == 32:
            if this.client.ballons >= 1:
                this.client.spawnObject(28, xPlayerPosition+2, yPlayerPosition-25, 1)
                this.client.room.sendAll([8, 16], [this.client.playerCode])
                this.client.ballons -= 1
                this.client.sendMessage("<ROSE>[BALLON] - <N>Você possui: "+str(this.client.ballons)+" ballons!")
            else:
                this.client.sendMessage("<ROSE>[BALLON] - <N>Você não possui ballons, aguarde...")

    def sendMessageLoginBallonRace(this):
        this.client.sendMessage("<ROSE>[BALLON] - <N>Seja bem-vindo a sala <ROSE>#BallonRace!")
        this.client.sendMessage("<ROSE>[BALLON] - <N>Aperte o espaço no seu teclado para usar <ROSE>#Ballons.")
        this.client.sendMessage("<ROSE>[BALLON] - <N>Você possui: "+str(this.client.ballons)+" ballon's!")

    def explosionEventKeyboard(this, playerName, keyCode, down, xPlayerPosition, yPlayerPosition):
        if keyCode == 32:
            if this.client.explosion >= 1:
                this.client.spawnObject(24, xPlayerPosition+4, yPlayerPosition+16, 0)
                this.client.explosion -= 1
                this.client.sendMessage("<ROSE>[EXPLOSION] - <N>Você possui: "+str(this.client.explosion)+" explosion's!")
            else: this.client.sendMessage("<ROSE>[EXPLOSION] - <N>Você não possui explosion, aguarde...")

    def sendMessageLoginExplosion(this):
        this.client.sendMessage("<ROSE>[EXPLOSION] - <N>Seja bem-vindo a sala <ROSE>#Explosion!")
        this.client.sendMessage("<ROSE>[EXPLOSION] - <N>Aperte o espaço no seu teclado para usar <ROSE>#Explosion.")
        this.client.sendMessage("<ROSE>[EXPLOSION] - <N>Você possui: "+str(this.client.explosion)+" explosion's!")

    def pokeEventKeyboard(this, player, key, down, x, y):
        if key == 39:
            # Posição Direita
            this.client.room.addImage(0, this.client.pokeSelect[0], 3, this.client.playerCode, -26, -45, "")
            this.client.room.removeImage(1, "")
        elif key == 37:
            this.client.room.addImage(1, this.client.pokeSelect[1], 3, this.client.playerCode, -26, -45, "")
            this.client.room.removeImage(0, "")
            # Posição Esquerda
            
    def pokeCommand(this, pokemon):
        if this.client.pokeList.has_key(pokemon):
            this.client.pokeSelect = this.client.pokeList[pokemon]
            
    def sendMessageLoginPokeLua(this):
        this.client.sendMessage("<ROSE>[POKELUA] - <N>Seja bem-vindo a sala <ROSE>#PokeLua!")
        this.client.sendMessage("<ROSE>[POKELUA] - <N>Poke Animes numeros: [Poke 0-50].")
        this.client.sendMessage("<ROSE>[POKELUA] - <N>Use o comando <ROSE>/poke (numero [0-50]).")

    def sendMessageLoginFly(this):
        this.client.sendMessage("<ROSE>[FLY] - <N>Seja bem-vindo a sala de <ROSE>#Fly!")
        this.client.sendMessage("<ROSE>[FLY] - <N>Aperte o Espaço no seu teclado para voar.")
        this.client.sendMessage("<ROSE>[FLY] - <N>Você possui: "+str(this.client.flypoints)+" fly's.")           
