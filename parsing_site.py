import requests
from tockin import * 


class Parsing_transactions:
    def __init__(self, wallet:str) -> list:
        self.url = f"https://api.zerion.io/v1/wallets/{wallet}/transactions/"
        self.headers = {"accept": "application/json","authorization": f"Basic {Basic}"}
        self.result =  self.__formatting(self.__get_pars())
        
        
        
        
    def __get_pars(self,):    
        response = requests.get(self.url, headers=self.headers)
        return response.text



    def __formatting(self,data_wallet:str):
        data_list = []
        for i in data_wallet.split('"'):
            if i[0:2] == '0x':
                if len(i) == 42:
                    data_list.append(i)
        return data_list
    

if __name__ == '__main__':
    start = Parsing_transactions('0x319bBfD774AB763172E2e9a90ae4eFE2E8b6e32D')
    print(start.result)
