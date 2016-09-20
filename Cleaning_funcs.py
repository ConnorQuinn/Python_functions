'''
Helper functions for cleaning text inputs.
'''


def AlphabetOnly(input_string, inc=None):
    # Remove any text that is not an alphabet letter
    # Can also pass a different list of chars 
    if inc is None:
        inc = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        # note that white-space also allowed (start of string)
    input_string = ''.join([ch for ch in input_string if ch in inc])
    return input_string



def RemoveForbidden(input_string, forbidden=None): 
    # Removes forbidden characters
    # Can pass a new list of forbidden chars
    # e.g. new_forbidden = ['[','\'']
    # RemoveForbidden('reth8n [cc  d]-3nf', new_forbidden)
    if forbidden is None:
        forbidden = ['!', '?', '&','(',')','$','@','#', 
                    '%','/',':',';','[',']','{','}','~' ]
    input_string = ''.join([c for c in input_string if c not in forbidden])
    return input_string


    
def UniqueChars(input_string):
    # Returns a string with the sorted unique characters
    # This is useful to see what special characters may need to be stripped
    myChars = ''
    myChars = myChars.join(sorted(set(input_string)))
    return myChars
    
