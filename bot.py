from imaplib import IMAP4, IMAP4_SSL
import time
import email
import email.parser
from decoder import Decoder
from telega import Telega

#Mail section
def Get_msg(id): 
    typ, msg_data = server.fetch(id, '(RFC822)')
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            email_parser = email.parser.BytesFeedParser()
            email_parser.feed(response_part[1])
            msg = email_parser.close()
            #print(msg)
            return(Parse_msg(msg))

def Parse_msg(message):
    arr = []
    files =[]
    dec = Decoder()
    text =''
    text+='\n<b>{}:</b> {}'.format('DATE', message['date'].replace('<','').replace('>',''))
    text+='\n<b>{}:</b> {}'.format('FROM', dec.dc(message['from']).replace('<','').replace('>',''))
    text+='\n<b>{}:</b> {}'.format('SUBJECT', dec.dc(message['subject']).replace('<','').replace('>',''))
    if message.is_multipart():
        for part in message.get_payload():
            res=dec.decode(part)
            if res[0]=='txt':
                text+=res[1].replace('<','').replace('>','')
            elif res[0]=='file':
                files.append(res[1])
    else:
        print(message.get_payload())
    arr.append(text)
    arr.append(files)
    return arr

def Check_MailBox(mailbox):
    result,data = server.status(mailbox, '(MESSAGES)')
    if result=='OK':
        num =int((str(data[0]).split(' ')[2])[:-2])
        print(num)
        return True
    else:
        return False
    

    
#MAIN
def main():
    bot = Telega()
    #send_msg('-1001134469469', 'Я родился!')339018008
    result, data = server.login('iasa_da61@ukr.net','iasasai2016')
    print('Logging...',)
    if result=='OK':
        print(str(data[0]).split('\'')[1])
        result, data = server.select(mailbox, readonly=True)
        if result == 'OK':
            while(True):
                result, data = server.search(None, 'UNSEEN')
                for id in data[0].split():
                    mesadge=Get_msg(id)
                    print(bot.send_msg('339018008', mesadge[0]))
                    if mesadge[1][0]!='':
                        for file in mesadge[1]:
                            print(bot.sendDoc('339018008', file))
                    print(mesadge)
                time.sleep(60)



if __name__ == '__main__':
    mailbox='INBOX' 
    server=IMAP4_SSL('imap.ukr.net')
    main()
