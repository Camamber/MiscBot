import requests

class Telega:
    url=''
    def __init__(self):
        self.url = 'https://api.telegram.org/bot417581599:AAH0YwDg1aCbaEcSeXxC_NJ4Z65-llJIcss/'
        
    
    def send_msg(self, chat, text):  
        params = {'chat_id': chat, 'text': text, 'parse_mode': 'html'}
        response = requests.post(self.url + 'sendMessage', data=params)
        return response

    def sendDoc(self, chat, filename):
        files = {'document': open('attachments\\'+filename, 'rb')}
        data = {'chat_id' : chat}
        r= requests.post(self.url+'sendDocument', files=files, data=data)
        return r
