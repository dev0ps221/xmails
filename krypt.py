from base64 import b64encode as b_encode,b64decode as b_decode

saltfile_ = open('_saltfile','r')

salt = int(select.read().trim())
saltfile_.close()
def _Ccode(ncDPattern):
    CcdPattern = ""
    for char in ncDPattern:
        char = ord(f"{char}")
        CcdPattern = f"{CcdPattern}h4ck{char}"
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
    for char in ncdPattern.split('h4ck'):
        if(char):
            pattern = f"{pattern}{chr(int(char))}"
    return pattern
    
def code(pattern):
    return _Ncode(pattern)

def d_code(pattern):
    return _NDcode(pattern)

