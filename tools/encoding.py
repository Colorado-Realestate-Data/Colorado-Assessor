# needs https://github.com/chardet

# I have used this to explore encoding/decoding issues with the data.
# I have seen ¬ and ¢ cause issues.

import chardet

#choose data file
dfile = "DATA/ATSDTA_ATSP600.csv"
with open(dfile, 'rb') as f:
    for line in f:
        code = chardet.detect(line)
        #if code == {'confidence': 0.5, 'encoding': 'windows-1252'}:
        if code != {'encoding': 'ascii', 'confidence': 1.0}:
            print(code)
        win = line.decode('windows-1252').split(',') #windows-1252
        norm = line.decode('utf-8', 'ignore').split(',')
        ascii = line.decode('ascii', "ignore").split(',')
        ascii2 = line.decode('ISO-8859-1').split(',')
        
        for w, n, a, a2 in zip(win, norm, ascii, ascii2):
            if not(w == n == a == a2):
                print(w)
                print(n)
                print(a)
                print(a2)
                print(win[0])
