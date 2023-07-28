import sqlite3 



class Requests:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('wallet.db')
        self.main =  self.conn.cursor()



    def new_wallet(self,data:str, id:int):
        requests_data = f"""UPDATE useres SET wallet_link = wallet_link || ' {data} ' WHERE users_id = {id}"""
        self.main.execute(requests_data)
        self.conn.commit()


    def new_users(self, users_id:int, name:str, wallet_link:str = ''):    
        requests_data = f"""INSERT OR IGNORE INTO useres (users_id,name,wallet_link) VALUES ({users_id},"{name}","{wallet_link}");"""
        self.main.execute(requests_data)
        self.conn.commit()
        

    def _look_nick(self) -> list:
        data_nick = []
        requests_data = f"""SELECT name FROM useres"""
        result =  self.main.execute(requests_data).fetchall()
        for i in result:
            generator_data = [j for j in i]
            data_nick += generator_data
        return data_nick

    def _look_wallet(self, id):
        data_nick =''
        requests_data = f"""SELECT wallet_link FROM useres WHERE {id}"""
        result =  self.main.execute(requests_data).fetchone()
        for reg in result:
            data_nick += reg
        return data_nick.split(' ')

    def _look_id_chat(self) -> list:
        data_id_chat = []
        requests_data = f"""SELECT users_id FROM useres"""
        result =  self.main.execute(requests_data).fetchall()
        for i in result:
            generator_data = [j for j in i]
            data_id_chat += generator_data
        return data_id_chat

    def look_data_id_name(self):
        requests_data_nick = self._look_nick()
        requests_data_id_chat = self._look_id_chat()
        data_all = dict(zip(requests_data_nick, requests_data_id_chat))
        return data_all

    def delet_entry(self):
        requests_data = f"""DELETE FROM useres """
        self.main.execute(requests_data)
        self.conn.commit()



if __name__ == '__main__':
    start = Requests()
    result = start.new_users(922161621,'Petr','0x903b80141b4cf6804d0fa33b0b6e5ea9ca0d3e1d')