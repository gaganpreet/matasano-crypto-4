from hashlib import sha1

def string_xor(x, y):
    ''' Xor two equal length strings character by character '''
    return ''.join([chr(ord(a) ^ ord(b)) for a, b in zip(x,y)])

def hmac(key, message):
    ''' SHA1 HMAC
        Arguments:
            key -> Key to use
            message -> Message to generate auth hash for
    '''
    blocksize = 64 # Block size of SHA1

    # Keys > blocksize are shortened
    if len(key) > blocksize:
        key = sha1(key).digest()

    key += '\x00' * (blocksize - len(key))

    o_key_pad = string_xor(len(key) * chr(0x5C), key)
    i_key_pad = string_xor(len(key) * chr(0x36), key)

    return sha1(o_key_pad + sha1(i_key_pad + message).digest()).hexdigest()

def main():
    print(hmac('', ''))

if __name__ == '__main__':
    main()
