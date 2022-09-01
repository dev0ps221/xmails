from base64 import b64encode as b_encode,b64decode as b_decode

credspath = 'craids'
sfile_ = open(f"{credspath}/_sfile",'r')

_s = int(sfile_.read())
sfile_.close()

def _Ccode(ncDPattern):
    CcdPattern = ""
    for char in ncDPattern: 
        char = ord(f"{char}")+_s
        CcdPattern = f"{CcdPattern}{b_encode('h4ck'.encode()).decode()}{char}"
    return CcdPattern

def _Ncode(pattern):
    ncDPattern = b_encode(pattern.encode())
    return _Ccode(ncDPattern.decode())

def _NDcode(Ccdpattern):
    ncDPattern = _CDcode(Ccdpattern)
    pattern = b_decode(ncDPattern.encode()).decode()
    return pattern

def _CDcode(ncdPattern):
    pattern = ""
    for char in ncdPattern.split(b_encode('h4ck'.encode()).decode()):
        if(char):
            pattern = f"{pattern}{chr(int(char)-_s)}"
    return pattern
    
def code(pattern):
    return _Ncode(pattern)

def d_code(pattern):
    return _NDcode(pattern)

