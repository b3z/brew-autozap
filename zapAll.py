from subprocess import Popen, PIPE


def generateZap(cask):
    if not cask:
        print("Err: No cask")
        return None

    zapProcess = Popen(["sh", "brew-createzap.sh", cask], stdout=PIPE, stderr=PIPE)
    stdout, stderr = zapProcess.communicate()
    
    err = stderr.decode("UTF-8")
    if err:
        print(f'Error: {err}')
        
    zap = stdout.decode("UTF-8")
    if zap == f'No {cask} settings found.':
        print(f'No settings for {cask}')
        return None
    else:
        return zap

# Testing - all passed as expected.
#print(generateZap("ddnet"))        # There is a zap to be found.
#print(generateZap("mactex"))       # No setting to find (at least for me manually. Same result here).
#print(generateZap("jwgböewlbg"))   # Some nonsense input.
#print(generateZap(""))             # Empty string. 
#print(generateZap(None))           # None arg.


casks = open('casks-to-zap.txt', 'r')
zaps  = open('zaps.txt', 'w')
 
for cask in casks:
    print(f'cask.strip()\n')
    zap = generateZap(cask.strip())
    if zap:
        zaps.writelines(f'{cask}{zap}\n\n')
    else:
        zaps.writelines(f'No zap for {cask}.\n\n')

casks.close()
zaps.close()

print("Done.")
