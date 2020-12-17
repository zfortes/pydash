from r2a.ir2a import IR2A
from player.parser import *
import time
from statistics import mean

from base.whiteboard import Whiteboard


class R2AProjeto_luc_otv_jos(IR2A):

    def __init__(self, id):
        IR2A.__init__(self,id)
        self.vazao = []
        self.tempo_request = 0
        self.lista_qi = []

        self.media_qi = []
    
    def handle_xml_request(self, msg):

        self.tempo_request = time.time()
        
        self.send_down(msg)
        


    def handle_xml_response(self, msg):
        
        parser_a = parse_mpd(msg.get_payload())
        self.lista_qi = parser_a.get_qi()

        t = time.time() - self.tempo_request
        self.vazao.append(msg.get_bit_length() / t)

        self.send_up(msg)
    


    def handle_segment_size_request(self, msg):
        self.tempo_request = time.time()
        media_vazao = mean(self.vazao)

        # Verifica o tamanho do Buffer, se for menor que 20 então verifica se é menor que 10
        # Se for menor que 10 ele seta a vazao como tendo apenas 60% da quailidade a fim de 
        # restaurar um tamanho aceitavél do buffer para evitar pausas.
        # Se for entre 10 e 20 ele utiliza 79% da vazão para selecionar a prŕoxima qualidade.
        # Se for maior 20 ele usa a maior qualidade possível entre a média ou o tamanho 
        # máximo da última vazão deisponível.
        if(self.whiteboard.get_amount_video_to_play() < 20):
            if (self.whiteboard.get_amount_video_to_play() < 10):
                    valor_esp_final = self.vazao[-1] * 0.55
            else:
                valor_esp_final = self.vazao[-1] * 0.68
        else: 
            if (media_vazao > self.vazao[-1]):
                valor_esp_final = media_vazao
            else:
                valor_esp_final = self.vazao[-1]

        

        # Busca a qualidade mais próxima que esteja abaixo do valor de vazão esperado.
        qualidade = self.lista_qi[0]
        for i in self.lista_qi:
            if valor_esp_final >= i:
                qualidade = i

        print()
        print("======================================================================")
        print("Vazao atual ----------> {:.0f}".format(self.vazao[-1]))
        print("Vazao esperada -------> {:.0f}".format(valor_esp_final))
        print("Qualidade selecionada = {:.0f}".format(qualidade))
        if valor_esp_final > qualidade :
            print(" Maior vazao")
        else:
            print(" Maior qualidade")
        print("======================================================================")


        # Usar o histórico de vazões para selecionar a qualidade média do streaming.
        # Para que a lista não vicie, apenas as últimas 10 vazões são consideradas 
        # no algoritmo sendo que a vazão mais antiga sempre é descartada.
        tamanho_da_lista = len(self.vazao)
        if (tamanho_da_lista > 9):  ### Limpa a lista quando ela passa do tamanho 10
            self.vazao.pop(0)

        # Adiciona a qualidade mais próxima a vazão escolhida na lista do player.
        msg.add_quality_id(qualidade)
        
        self.send_down(msg)
    


    def handle_segment_size_response(self, msg):

        t = time.time() - self.tempo_request
        self.vazao.append(msg.get_bit_length() / t)

        
        self.send_up(msg)



    def initialize(self):
        pass

    def finalization(self):
        pass