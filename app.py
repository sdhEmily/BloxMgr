import warnings
warnings.filterwarnings('ignore', message='.*https://github.com/urllib3/urllib3/issues/3020.*') # annoying warning and doesnt really do anything

try:
  import requests
except ImportError:
  subprocess.call(['python3', '-m', 'pip install requests'])


import sys, os, shutil, zipfile, glob, subprocess, plistlib, stat
import json, requests
import time

datapath = os.path.expanduser('~') + '/Library/Application Support/sdhEmily.RobloxPatcher'
config = json.load(open(datapath + '/applied.json')) # could be buggy if never loaded the actual tool (the config wouldnt exist) (fix later)

clientsettings = requests.get('https://clientsettingscdn.roblox.com/v2/client-version/MacPlayer/channel/LIVE').json() # the channel fluctuates (???) (sometimes its zLIVE its very confusing) (fix later!!!!)
version = clientsettings['version']
downloadlink = 'https://setup.rbxcdn.com/mac/' + clientsettings['clientVersionUpload'] + '-RobloxPlayer.zip'

if os.path.exists('/tmp/RobloxPlayer.zip'):
  os.remove('/tmp/RobloxPlayer.zip')

def exec(cmd, args, path=None, sh=False):
  if path != None:
    subprocess.call([cmd, args, path], shell=sh)
  else:
    subprocess.call([cmd, args], shell=sh)

def echo(txt): # ICKY WORKAROUND FOR A PLATYPUS BUG!!!
   exec('echo', txt) 
echo('DETAILS:HIDE')
echo('PROGRESS:0\nPlease Wait....') 

try:
  if sys.argv[1].startswith("roblox-player:"):
    with open('/Applications/Roblox.app/Contents/info.plist', 'rb') as infile:
        localversion = plistlib.load(infile)['CFBundleShortVersionString']

    if localversion != version:
      echo('PROGRESS:1\nDownloading updates... ') 
      dl = requests.get(downloadlink, allow_redirects=True)
      open('/tmp/RobloxPlayer.zip', 'wb').write(dl.content)

      echo('PROGRESS:25\nExtracting...')
      with zipfile.ZipFile('/tmp/RobloxPlayer.zip') as zip:
        zip.extractall('/tmp/')
      os.remove('/tmp/RobloxPlayer.zip')
      shutil.copytree('/tmp/RobloxPlayer.app', '/Applications/Roblox.app', dirs_exist_ok=True)
      if os.path.exists('/Applications/Roblox.app/Contents/oldResources'):
        shutil.rmtree('/Applications/Roblox.app/Contents/oldResources')
      if os.path.exists('/Applications/Roblox.app/Contents/Resources/ExtraContent/places/oldMobile.rbxl'):
        os.remove('/Applications/Roblox.app/Contents/Resources/ExtraContent/places/oldMobile.rbxl')
      if os.path.exists('/Applications/Roblox.app/Contents/Resources/ExtraContent/places/oldMobile.rbxl'):
        os.remove('/Applications/Roblox.app/Contents/Resources/ExtraContent/places/oldMobile.rbxl')
      dir = glob.glob('/Applications/Roblox.app/Contents/MacOS/*')
      for file in dir:
        if not file.endswith('.app'):
          current = os.stat(file)
          os.chmod(file, current.st_mode | stat.S_IEXEC)
      dir = glob.glob('/Applications/Roblox.app/Contents/MacOS/Roblox.app/Contents/MacOS/*')
      for file in dir:
        if not file.endswith('.app'):
          current = os.stat(file)
          os.chmod(file, current.st_mode | stat.S_IEXEC)

      echo('PROGRESS:50\nUpdated! Applying mods...') 

      if config['rmbeta']:
        if os.path.exists('/Applications/Roblox.app/Contents/Resources/ExtraContent/places/Mobile.rbxl'):
          os.rename('/Applications/Roblox.app/Contents/Resources/ExtraContent/places/Mobile.rbxl', '/Applications/Roblox.app/Contents/Resources/ExtraContent/places/oldMobile.rbxl')

      if config['olddeath']:
        if os.path.exists('/Applications/Roblox.app/Contents/Resources'):
          if os.path.exists('/Applications/Roblox.app/Contents/Resources/content/sounds/oldouch.ogg'):
            os.rename('/Applications/Roblox.app/Contents/Resources/content/sounds/ouch.ogg', '/Applications/Roblox.app/Contents/Resources/content/sounds/oldouch.ogg')
            dl = requests.get('https://github.com/sdhEmily/RobloxPatcher/raw/main/ouch.ogg', allow_redirects=True)
            open('/Applications/Roblox.app/Contents/Resources/content/sounds/ouch.ogg', 'wb').write(dl.content)

      if config['modsapplied']:
        shutil.copytree('/Applications/Roblox.app/Contents/Resources', '/Applications/Roblox.app/Contents/oldResources')
        shutil.copytree(datapath + '/Modifications', datapath + '/Resources')
        shutil.copytree(datapath + '/Resources', '/Applications/Roblox.app/Contents/Resources', dirs_exist_ok=True)
        shutil.rmtree(datapath + '/Resources')
      echo('PROGRESS:85\nMods applied!')

      if config['fflagsapplied']:
        os.chdir(datapath + '/FastFlags/')
        finaljson = {}
        for f in glob.glob('*.json'):
            with open(f, 'r', encoding='utf-8') as infile:
              file_content = json.load(infile)
              for key, value in file_content.items():
                finaljson[key] = value
        jsonfile = json.dumps(finaljson, indent=1)
        if os.path.exists('/Applications/Roblox.app/Contents/MacOS/ClientSettings'):
          shutil.rmtree('/Applications/Roblox.app/Contents/MacOS/ClientSettings')
          os.makedirs('/Applications/Roblox.app/Contents/MacOS/ClientSettings')
        else:
          os.makedirs('/Applications/Roblox.app/Contents/MacOS/ClientSettings')
        os.chdir('/Applications/Roblox.app/Contents/MacOS/ClientSettings')
        with open('ClientAppSettings.json', 'w') as outfile:
          outfile.write(jsonfile)

      exec('open', sys.argv[1])
      echo('PROGRESS:100\nFinished!') 
      time.sleep(1)
      echo('QUITAPP\n')
    else:
      echo('PROGRESS:100\nRoblox is up to date.')
      exec('open', sys.argv[1])
      time.sleep(1)
      echo('QUITAPP\n')
  else: 
    echo('DETAILS:SHOW')
    echo('Arguments are not for "roblox-player:"!\nArguments given: ' + sys.argv[1])

except IndexError:
  # VVV - icky impelementation (to be replaced (eventually (i hope)))
  os.system("osascript -e 'tell application \"Terminal\"' -e  'do script \"curl https://github.com/sdhEmily/RobloxPatcher/raw/main/main.py -Lo /tmp/RobloxPatcher.py && python3 /tmp/RobloxPatcher.py; rm /tmp/RobloxPatcher.py && exit\"' -e 'end tell'")
  echo('QUITAPP\n')