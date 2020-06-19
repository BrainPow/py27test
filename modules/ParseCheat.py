# -*- coding: cp1252 -*-
import json
class AntiCheat:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        
    def update(self):
        ac = ("[F.A.C] ")
        this.ac_config = open('./cheat/anticheat_config.txt', 'r').read()
        this.ac_c = json.loads(this.ac_config)
        this.learning = this.ac_c['learning']
        this.bantimes = this.ac_c['ban_times']
        this.s_list = open('./cheat/anticheat_allow', 'r').read()
        if this.s_list != "":
            this.s_list = this.s_list.split(',')
            this.s_list.remove("")
        else: this.s_list = []
            
    def readPacket(this, packet, pd=None):
        ac = ("[R.A.C] ")
        if packet == " " or packet == "":
            this.list.remove(packet)
        if str(packet) not in this.server.s_list and str(packet) != "":
            if this.server.learning == "true":
                this.server.sendModMessage(4, "<V>[Anti-Hack] Eu encontrei um novo pacote vindo de "+this.client.playerName+" ["+str(packet)+"]")
                this.server.s_list.append(str(packet))
                w = open('./cheat/anticheat_allow', 'a')
                w.write(str(packet) + ",")
                w.close()
            else:
                if this.client.privLevel != 11:
                    if packet == 55 or packet == 31 or packet == 51:
                        this.client.dac += 1
                        this.server.sendModMessage(5, "<ROSE>[Anti-Hack]<V> O jogador <J>"+this.client.playerName+" <V>é suspeito de cheat! <J>"+str(3-this.client.dac)+" <V>alertas ele será banido automaticamente.")
                        this.client.sendMessage("<V>Caro <J>"+this.client.playerName+"<V>, detectamos Cheat Engine no seu Standalone, por favor, desative-o ou será banido dentro de segundos.")
                    else: this.client.dac = 3
                    if this.client.dac >= 0 and this.client.dac <= 2:
                        this.client.dac += 1
                    else:
                        bans_done = 0
                        bl = open('./cheat/anticheat_bans.txt', 'r').read()
                        lista = bl.split('=')
                        lista.remove("")
                        for listas in lista:
                            data = listas.split(" ")
                            data.remove("")
                            name = data[1]
                            if name == this.client.playerName:
                                bans_done += 1
                        if bans_done == 0:
                            tb = int(this.server.bantimes)
                        elif bans_done == 1:
                            tb = int(this.server.bantimes)*2
                        elif bans_done == 2:
                            tb = int(this.server.bantimes)*3
                        elif bans_done >= 3:
                            tb = int(this.server.bantimes)*4
                        if int(packet) == 31:
                            info = "Fly hack"
                        elif int(packet) == 51 or int(packet) == 55:
                            info = "Speed"
                        else: info = "Unknown"
                            
                        bans_done += 1
                        x = open('./cheat/anticheat_bans.txt', 'a')
                        x.write("= Jogador: "+this.client.playerName+" | Tempo: "+str(tb)+" hora(s) | Banido por: "+str(packet)+" | Data: "+info+" | +Info: "+repr(pd)+"\n")
                        x.close()
                        this.server.sendModMessage(5, "<V>[Anti-Hack]<J> O jogador "+this.client.playerName+" foi banido por cheat por "+str(tb)+" hora(s). ["+info+"]")
                        if int(packet) == 51 or int(packet) == 55 or int(packet) == 31:
                            this.server.banPlayer(this.client.playerName, int(tb), "Cheat Engine Detectado [Ban #"+str(bans_done)+" - "+info+"]", "Anti-Hack", False)
                        else: this.server.banPlayer(this.client.playerName, 0, "Atividade Suspeita Detectada [Ban #"+str(bans_done)+" - "+info+"]", "Anti-Hack", False)
                else:
                    if int(packet) == 31:
                        info = "Fly hack"
                    elif int(packet) == 51 or int(packet) == 55:
                        info = "Speed"
                    else: info = "Unknown"
                    this.client.dac += 1
