import requests
import sys
import string

from collections import Counter

def url_for(f, sig):
    return 'http://localhost:5000/?file=%s&signature=%s' % (f, sig)

def timedelta_ms(td):
    return td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6

def sorted_dict(d):
    return sorted(d, key=d.get)

if __name__ == '__main__':
    f = '/etc/passwd'

    hash_len = 40

    prefix = ''
    for i in range(hash_len):
        ''' This is similar to the previous solution, except for the following change:

                Instead of one iteration, we do multiple iterations and take the
                3 digits with the maximum time (instead of the one in previous). Idea
                is that over multiple iterations and taking multiple top values instead
                of one, the small unequalilty will smooth over the multiple iterations
        '''

        top_3 = Counter()
        time = {}

        iterations = 10
        ''' I did some analsis on the value of iterations,
            as the server sleep interval decreases, the value required to get the correct
            result increases in a similar manner:
                0.001 -> 10 iterations
                0.0001 -> 200 iterations
                0.00001 -> >1000 iterations
        '''
        for i in xrange(iterations):
            for c in sorted_dict(time)[-3:]:
                top_3[c] += 1

            time = {}
            for c in string.hexdigits:
                s = prefix + c
                s = s + (hash_len - len(s)) * 'z'

                url = url_for(f, s)

                r = requests.get(url)

                if r.text == 'true':
                    print(s)
                    sys.exit(0)

                time[c] = timedelta_ms(r.elapsed)
        match = top_3.most_common(1)[0][0]
        prefix += match
        print prefix
