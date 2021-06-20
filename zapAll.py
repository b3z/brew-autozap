from subprocess import Popen, PIPE
import wget

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

def fetchCask(cask):
    print(f'Downloading {cask}.rb')
    url=f'https://raw.githubusercontent.com/Homebrew/homebrew-cask/master/Casks/{cask}.rb'
    wget.download(url, out="Casks")

def fixStyle(cask):
    fixProcess = Popen(["brew", "style", "--fix", f'zappedCasks/{cask}.rb'], stdout=PIPE)
    stdout = fixProcess.communicate()
    print(stdout.decode("UTF-8"))


# ----- Main -------

casks = open('casks-to-zap.txt', 'r')
 
for cask in casks:
    cask = cask.strip()
    print(f'Current cask: {cask}\n')
    zap = generateZap(cask)
    if zap:
        fetchCask(cask)
        
        with open(f'Casks/{cask}.rb', 'r') as caskRead:
            caskContent = caskRead.readlines()
        
        print(caskContent)
        
        caskContent[len(caskContent)-1] = f'{zap}\nend'
    
        caskWrite = open(f'zappedCasks/{cask}.rb', 'w')
        caskWrite.writelines(caskContent)
        caskWrite.close()




    else:
        print(f'No zap for {cask}.\n')

casks.close()

print("Done.")
