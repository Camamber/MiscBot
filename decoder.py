import base64
import re
import translit


class Decoder:
    
    def decode_base64(self, _str, coding):
        msg = base64.b64decode(_str).decode(coding, 'ignore')
        return msg

    def save_file(self, data, filename):
        with open(filename, 'wb') as fh:
            fh.write(base64.decodebytes(bytes(data, 'utf-8')))

    def decode(self, part):
        ctype = part.get_content_type()
        cdispo = str(part.get('Content-Disposition'))
        if ctype=='text/plain':
            charset = part.get_content_charset()
            return('txt',self.decode_base64(part.get_payload(), charset))
        elif 'attachment' in cdispo:
            filename=translit.transliterate(self.dc(part.get_filename())).replace(' ','_')
            self.save_file(part.get_payload(), 'attachments\\'+filename)
            return('file', filename)
        else:
            return('null','null')


    def dc(self, parse_str):
        ref=''
        coding =self.Get_Coding(parse_str)
        p = re.compile(r'\=\?'+coding+'\?(?i)b\?(.*?)\?')
        splited = parse_str.split()
        for _str in splited:
            m = p.match(_str)
            if m:
                ref+= self.decode_base64(m.group(1), coding)
            else:
                ref+=' '+_str+' '
        return ref

    def Get_Coding(self,_str):
        ref='UTF-8'
        p = re.compile(r'\=\?(.*?)\?(?i)b\?')
        m = p.match(_str)
        if m:
            ref = m.group(1)
        return ref

