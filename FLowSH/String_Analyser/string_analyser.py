from datasketch import MinHash, MinHashLSH
from MySQLdb import _mysql


def list_to_string(list_: list[str]) -> str:
    '''
        Given the list transforms it into a string

        Parameters:
        list(list[str]): the list to be transformed           

        Returns:
        str: the final string
    '''
    new = ""
    for x in list_:
        new += x
    return new

def from_hexa_to_meta(input: str) -> str:
    '''
        Given the string written, transforms the % into
        metacaracters.

        Parameters:
        input (str): the string 

        Returns:
        str: the string with metacharacters
    '''
    input = list(input) 
    full_input = []
    i = 0
    while(i < len(input)):
        if input[i] == '%':  
            hexa = list_to_string(input[i+1:i+3])
            byte_array = bytes.fromhex(hexa)
            try:
                meta = byte_array.decode()
                full_input.append(meta)
            except:
                full_input.append(hexa)
            i += 3
        else: 
            full_input.append(input[i])
            i += 1

    return list_to_string(full_input)


def string_analyser(string:str, lsh:MinHashLSH, minhash:MinHash) -> bool:
    '''
        Applies a string sanitisation function and checks if the string detected has any metacharacter.
        If there is a sanitisation, check if the string is already on the LSH database, if not insert
        MinHash of string and returns TRUE.
        If there is no sanitisation, returns FALSE.   

        Parameters:
        string(str): string to be sanitised
        lsh(MinHashLSH): the LSH to be used
        minhash(MinHash): the MinHash of the string

        Returns:
        bool: if string is attack or not
    '''
    new_string:str = from_hexa_to_meta(string)

    san_token:bytes = _mysql.escape_string(new_string)
   
    san_str = san_token.decode()
    
    i = 0
    while(i < len(san_str)-1):
        if san_str[i] == '\\':
            if san_str[i+1] != '\\':
                print("Found metacharacter")
                return True
            if san_str[i+1] == '\\':
                print('Found bar')
                i += 1
        i += 1
    return False

