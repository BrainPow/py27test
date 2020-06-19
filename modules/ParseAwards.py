# -*- coding: UTF-8 -*-
import os, struct, urllib
from datetime import datetime
from twisted.internet import reactor
from ByteArray import ByteArray
from Identifiers import Identifiers

class AwardsPlayers:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server

    def sendMenu(this):
        bg = ""
        text = "<a href='event:fullMenu:open'><font size='15'><N>?</N></font></a>"
        this.client.sendAddPopupText(11000, 777, 24, 18, 20, '3C5064', '3C5064', 100, str(bg))
        this.client.sendAddPopupText(11001, 780, 24, 18, 20, '000000', '000000', 100, str(text))
            
    def sendPremio(this):
        if os.path.exists('./include/premiados.txt'):
            BadUsers = str(open('./include/premiados.txt', 'r').read()).split(', ')
        else:
            fo = open('./include/premiados.txt', 'wb')
            fo.write('10.0.0.1')
            fo.close()
        now = datetime.now()
        if not this.client.playerName in BadUsers:
            with open('./include/premiados.txt', 'r+') as f:
                old = f.read()
                f.seek(0)
                f.write('' + (this.client.playerName) + ', ' + old)
            this.client.firstCount += 5000
            this.client.cheeseCount += 5000
            this.client.XDCoins += 3000
            this.client.sendClientMessage("<S>Você recebeu <J>5.000 <S>firsts e <J>3.000 <S>moedas!")  

    def sendpremiohours(this):
        if this.client.privLevel >= 1:
            this.client.rebootTimer = reactor.callLater(900, this.sendAnuncioConstante1)
            this.client.rebootTimer = reactor.callLater(1200, this.sendAnuncioConstante1)
            this.client.rebootTimer = reactor.callLater(2500, this.sendAnuncioConstante1)
            this.client.rebootTimer = reactor.callLater(4000, this.sendAnuncioConstante1)
            this.client.rebootTimer = reactor.callLater(1600, this.sendAnuncioConstante1)
            this.client.rebootTimer = reactor.callLater(3600, this.sendAnuncioConstante1)
            this.client.rebootTimer = reactor.callLater(6000, this.sendAnuncioConstante1)
            this.client.rebootTimer = reactor.callLater(160, this.sendpremiomessage)
            this.client.rebootTimer = reactor.callLater(360, this.shopMessage)
            this.client.rebootTimer = reactor.callLater(3600, this.sendpremio1hora)
            this.client.rebootTimer = reactor.callLater(7200, this.sendpremio2horas)
            this.client.rebootTimer = reactor.callLater(10800, this.sendpremio3horas)
            this.client.rebootTimer = reactor.callLater(14400, this.sendpremio4horas)
            this.client.rebootTimer = reactor.callLater(18000, this.sendpremio5horas)
            this.client.rebootTimer = reactor.callLater(600, this.eventMessage)
            
    def shopMessage(this):
        this.client.sendMessage("<BL>Olá, <J>"+str(this.client.playerName)+"<BL>. Vendemos cargo de Mod/Admin por apenas <J>R$30,00! <BL>Agora você pode comprar por <J>boleto<BL>,<J> cartão de crédito <BL>e<J> depósito<BL>. Ao comprar, você terá diversos comandos: <VP>Banir<N>,<VP> mover jogadores da sala<BL>,<VP> expulsar<BL>,<VP> ganhar moedas<BL>,<VP> ajudar a fazer eventos <BL>e<VP> muito mais<BL>! Acesse a nossa lojinha e saiba mais: <J>http://www.transforvida.com.br/lojinha")
        reactor.callLater(1200, this.shopMessage)

    def eventMessage(this):
        this.client.sendMessage("<J>[EVENTO] <N>Participe do nosso <CH>Evento de Aventura<N> coletando o item do evento e firstando você ganhará 7 firsts/moedas e podendo ganhar até mesmo medalhas e títulos que ninguém possuí. <CH>Digite: /sala #eventoaventura1")
        reactor.callLater(3600, this.eventMessage)
        
    def sendpremiomessage(this):
        this.client.sendMessage("<ROSE>Prêmios por ficar online:\n<J> 1 hora <VP>= <J> 5 <V>firsts/queijos/moedas e <J>1000<V> queijos/morangos.\n<J> 2 horas <VP>= <J> 10 <V>firsts/queijos/moedas e <J>2000<V> queijos/morangos.\n<J> 3 horas <VP>= <J> 20 <V>firsts/queijos/moedas e <J>3000<V> queijos/morangos.\n<J> 4 horas <VP>= <J> 30 <V>firsts/queijos/moedas e <J>4000<V> queijos/morangos.\n<J> 5 horas <VP>= <J> 50 <V>firsts/queijos/moedas e <J>5000<V> queijos/morangos.")

    def sendpremio1hora(this):
        this.client.shopCheeses += 1000
        this.client.shopFraises += 1000
        this.client.firstCount += 5
        this.client.cheeseCount += 5
        this.client.shamanSaves += 5
        this.client.XDCoins += 5
        this.client.XDFichas += 5
        this.client.sendMessage('<R><b>Você ganhou o prêmio de uma hora online:</b> <VP>+1000 queijos e morangos na loja e +5 fichas, +5 firsts, queijos, saves no perfil e moedas.')

    def sendpremio2horas(this):
        this.client.shopCheeses += 2000
        this.client.shopFraises += 2000
        this.client.firstCount += 10
        this.client.cheeseCount += 10
        this.client.shamanSaves += 10
        this.client.XDCoins += 10
        this.client.XDFichas += 6

    def sendpremio3horas(this):
        this.client.shopCheeses += 3000
        this.client.shopFraises += 3000
        this.client.firstCount += 20
        this.client.cheeseCount += 20
        this.client.shamanSaves += 20
        this.client.XDCoins += 20
        this.client.XDFichas += 7

    def sendpremio4horas(this):
        this.client.shopCheeses += 4000
        this.client.shopFraises += 4000
        this.client.firstCount += 30
        this.client.cheeseCount += 30
        this.client.shamanSaves += 30
        this.client.XDCoins += 30
        this.client.XDFichas += 8

    def sendpremio5horas(this):
        this.client.shopCheeses += 5000
        this.client.shopFraises += 5000
        this.client.firstCount += 50
        this.client.cheeseCount += 50
        this.client.shamanSaves += 50
        this.client.XDCoins += 50
        this.client.XDFichas += 10

    def sendAnuncioConstante1(this):
        this.client.sendMessage("<VP>[Anúncio] <ROSE>Adquira <VP><b>[MOD]</b> <ROSE>e faça eventos, ganhe 20 mil moedas, título de MOD, comandos, respeito, etc. Saiba mais acessando: <u><b>http://www.transforvida.com.br/lojinha/</b></u>")

    def sendAdsense(this):
        reactor.callLater(600, this.client.sendMessage, "<BL>Compre agora mesmo cargo de <J>MOD<BL> do <J>Realmice<BL>, basta você acessar <J>www.realmice.ml<BL> e seguir as instruções.")
        reactor.callLater(2000, this.sendAdsense)
