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
        if(self.whiteboard.get_amount_video_to_play() < 20):
            if (self.whiteboard.get_amount_video_to_play() < 10):
                    valor_esp_final = self.vazao[-1] * 0.60
            else:
                valor_esp_final = self.vazao[-1] * 0.79
            # print(f'>>>>>>>>>>>>>>>>>>>>>>>>>> Lista de Vazoes - {self.vazao}')
            # print('')

            # print(f'>>>>>>>>>>>>>>>>>>>>>>>>>> Valor Inicial Provável = {valor_esperado}')
            # print('')

            # tamanho_da_lista = len(self.vazao)
            # print(f'>>>>>>>>>>>>>>>>>>>>>>>>>> Tamanho da lista = {tamanho_da_lista}')
            # print('')

            # print(f'>>>>>>>>>>>>>>>>>>>>>>>>>> Tamanho da Buffer = {self.whiteboard.get_amount_video_to_play()}')
            # print('')

            # if( tamanho_da_lista > 2 ):
            #     diferenca = self.vazao[tamanho_da_lista-1] - self.vazao[tamanho_da_lista-3]
            #     print(f'>>>>>> Ultimo valor da Lista Subtraido do Antepenúltimo -- Diferença = {diferenca}')
            # else:
            #     diferenca = 0
            
            # print('')

            # if( tamanho_da_lista > 5 ):  ### Limpa a lista quando ela passa do tamanho 10
            #     self.vazao.clear() 
            

            # if( diferenca < 0 ):
            #     diferenca = diferenca * (-1)
            #     valor_esp_final = (valor_esperado - diferenca) - valor_esperado * 0.2
            # else:
            #     if(diferenca == 0):
            #         valor_esp_final = valor_esperado - (valor_esperado * 0.3)
            #     else:
            #         if( tamanho_da_lista <= 3 ):
            #             valor_esp_final = (valor_esperado - diferenca) - (valor_esperado * 0.3)
            #         else:
            #             valor_esp_final = (valor_esperado - diferenca) - (valor_esperado * 0.2)
        
        else: 
            if (media_vazao > self.vazao[-1]):
                valor_esp_final = media_vazao
            else:
                valor_esp_final = self.vazao[-1]
            
                
        #     print(f'>>>>>>>>>>>>>>>>>>>>>>>>>> Tamanho da Buffer else = {self.whiteboard.get_amount_video_to_play()}')
        #     print('')
            


        # print(f'>>>>>>>>>>>>>>>>>>>>>>>>>> Valor Final Provável = {valor_esp_final}')
        # print('')

        qualidade = self.lista_qi[0]
        for i in self.lista_qi:
            if valor_esp_final >= i:
                qualidade = i



        index1 = 0
        for index, i in enumerate(self.lista_qi):
            if qualidade == i:
                index1 = index

        # print('')
        # print(f'>>>>>>>>>> Qualidade Selecionada {index1} - VALOR FINAL =  {qualidade}')
        self.media_qi.append(index1)
        # print(f'>>>>>>>>>> Media Qualidade =  {mean(self.media_qi)}')
        # print('')

        tamanho_da_lista = len(self.vazao)
        # print
        if( tamanho_da_lista > 9 ):  ### Limpa a lista quando ela passa do tamanho 10
            self.vazao.pop(0)



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