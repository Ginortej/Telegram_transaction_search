import socket
import multiprocessing
import time
from parsing_bit import Parsing
from parsing_site import Parsing_transactions
from sql_requests_1 import Requests
from tockin import *


HOST = "127.0.0.1"  
PORT = 65432  





class Service_parsing_wallet:
    def __init__(self,PORT:int, HOST:str):    
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT)) 
        server.listen(5) 
        print(f'[*] Listening on {HOST}:{PORT}')
        self.data_wallet  = Requests()
        while True:
            self.client, address = server.accept() 
            while True:
                   try:
                    data_wallet_user = self.client.recv(1024)
                    self.watch_wallet(data_wallet_user.decode('utf-8'))
                   except ConnectionResetError as e:
                       print('[*]error in connect')
                       break
        

    def watch_wallet(self,wish:str):
        for i in wish.split(' '):
            if i == 'last':
                self.requsets_link_last(wish)
            elif i == 'full':
                task1 = multiprocessing.Process(target=self.requsets_link, args= [wish]).start()
        



    def requsets_link_last(self, wish:str):
       get_transactions = Parsing_transactions(wish[5::])
       print(get_transactions.result) 
       transaction_request = Parsing(url = f'https://etherscan.io/address/{get_transactions.result[0]}', driver= 'chromedriver.exe')
       result_one_transaction =  transaction_request.paht_x('//*[@id="ContentPlaceHolder1_divSummary"]/div[2]/div[1]/div/div')
       result = f'last {result_one_transaction}'
       self.client.send(bytes(result.encode('utd-8')))

    def reqesets_link(self,id:int):
        while True:
            time.sleep(120)
            url_wallet_users = self.data_wallet._look_wallet(id[5::])
            for i in url_wallet_users.split(' '):
                get_transactions = Parsing_transactions(i)
                transaction_request = Parsing(url = f'https://etherscan.io/address/{get_transactions.result}', driver= 'chromedriver.exe')
                result_one_transaction =  transaction_request.paht_x('//*[@id="ContentPlaceHolder1_divSummary"]/div[2]/div[1]/div/div')
                result = str(result_one_transaction).encode('utf-8')
                return self.client.send(bytes(f'last {result}')) 


if __name__ == '__main__':
    satrt = Service_parsing_wallet(PORT,HOST)
      
    