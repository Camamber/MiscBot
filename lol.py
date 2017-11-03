import imaplib

server = imaplib.IMAP4_SSL('imap.ukr.net')
res , data=server.login('iasa_da61@ukr.net', 'iasasai2016')
print(data)
