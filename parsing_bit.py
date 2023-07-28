
# импортируем все нужные библеотеки
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent
from parsing_site import Parsing_transactions



# сощдаем класс
class Parsing:
    def __init__(self,url:str,driver:str) -> None: # созлдаем объект
        self.url = url # прописываем все переменнные в нутри класса
        self.opp = webdriver.ChromeOptions() # создаем опцию для веб драйвера
        self.driver = Service(driver)
        self.ua = UserAgent()
        user_agent = self.ua.random
        self.opp.add_argument(f'--user-agent={user_agent}')
        self.opp.add_argument('--disable-blink-features=AutomationControlled')
        # # self.opp.headless = False # прописываем методу headless параметр который обозначает что драйвер будет работать в фоновом режиме и мы его видеть не будем
        self.web = webdriver.Chrome(service= self.driver,options=self.opp) # сощдаем веб драйвер и передаем ему нашу опцию
        self.web.get(self.url)
        


        
    
    # Сощдаем методы класса для прасинга 
    def one_teg(self, teg): # делаем метод который будет паристь только по одному названию тега
        element = self.web.find_element(By.TAG_NAME, teg)
        return element
        
                                               
    def all_teg_name(self,teg):# делаем метод который будет паристь все теги с один именем 
        elements = self.web.find_elements(By.TAG_NAME, teg)
        result = [i.text for i in elements]
        return result


    def paht_x(self,xpath):# делаем метод который будет паристь только один тег по его xpath(пути)
        element = self.web.find_element(By.XPATH, xpath)
        return element.text

    def classe(self,_class):# делаем метод который будет паристь тег по его классу
        element = self.web.find_element(By.CLASS_NAME, _class)
        return element.text

    def cliced(self,xpath):# делаем метод который будет восоздавать нажатие по какому то тегу при этом мы прописываем путь до этого тега(xpath)
        element = self.web.find_element(By.XPATH, xpath).click()

    def cliced_class(self,_class):
        element = self.web.find_element(By.XPATH, _class)    
        ActionChains(self.web).move_to_element(element).click(element).perform() 


    def vvod(self,key:str,xpath:str):# делаем метод который будет восоздавать ввод в поле по его пути на этот тег(xpath)
        element = self.web.find_element(By.XPATH, xpath).send_keys(key)

   



# точка входа проверям  класс на работо способность 
if __name__ == '__main__':
    pass
























