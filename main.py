import os, sys, time, subprocess, json, shutil, glob, plistlib, zipfile, stat, warnings
warnings.filterwarnings("ignore", module="urllib3") # annoying modern macos quirk with phython

try:
  import requests, wget
except ImportError:
  os.system('python3 -m pip install requests')
  os.system('python3 -m pip install wget')
  import requests, wget


def getkey(): # Credit to https://stackoverflow.com/a/1840
    import sys, tty, termios, select
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    answer = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    return answer

firstrun = False
datapath = os.path.expanduser('~') + '/Library/Application Support/sdhEmily.BloxMgr'
robloxapp = '/Applications/Roblox.app/Contents' # u can change this if u want 
if not os.path.exists(datapath):
  firstrun = True

if not firstrun:
  config = json.load(open(datapath + '/applied.json'))

def exec(cmd, args, path=None, sh=False):
  if path != None:
    subprocess.call([cmd, args, path], shell=sh)
  else:
    subprocess.call([cmd, args], shell=sh)

with open('/Applications/Roblox.app/Contents/info.plist', 'rb') as infile:
  localversion = plistlib.load(infile)['CFBundleShortVersionString']
clientsettings = requests.get('https://clientsettingscdn.roblox.com/v2/client-version/MacPlayer/channel/LIVE').json()
version = clientsettings['version']

# Menu Sections

def setup():
  exec('clear', '.')
  print(' ___      _             \n/ __| ___| |_ _  _ _ __ \n\__ \/ -_)  _| || | \'_ \\\n|___/\___|\__|\_,_| .__/\n                  |_|   ')

  print('\nWelcome to BloxMgr!\nTo use BloxMgr you have to disable ROBLOX\'s auto updating as BloxMgr breaks it.\nYou can update ROBLOX through BloxMgr.')

  print ('\n1) Install BloxMgr\n2) Quit\n')
  print('Waiting for input...')
  answer=getkey()
  if '1' in answer: install()
  elif '2' in answer: exit()
  elif answer:
    print('Please enter a valid number.')
    time.sleep(1) 
    mainmenu()

def mainmenu():
  exec('clear', '.')
  print(' ___ _         __  __          \n| _ ) |_____ _|  \/  |__ _ _ _ \n| _ \ / _ \ \ / |\/| / _` | \'_|\n|___/_\___/_\_\_|  |_\__, |_|  \n                     |___/     ')
  print('\nInstalled ROBLOX Version: ' + localversion + '\nLatest ROBLOX Version: ' + version)

  print ('\n1) Mods\n2) FastFlags\n3) Update/Reinstall ROBLOX\n4) Quit\n')
  print('Waiting for input...')
  answer=getkey()
  if '1' in answer: mods()
  elif '2' in answer: fflags()
  elif '3' in answer: update()
  elif '4' in answer: exit()
  elif answer:
    print('Please enter a valid number.')
    time.sleep(1) 
    mainmenu()

def mods():
  exec('clear', '.')
  print(' __  __         _    \n|  \/  |___  __| |___\n| |\/| / _ \/ _` (_-<\n|_|  |_\___/\__,_/__/\n')
  print ('1) Open mods folder\n2) Apply mods\n3) Remove mods\n4) Go back\n')
  print('Waiting for input...')

  answer=getkey()
  if '1' in answer: openmfolder()
  if '2' in answer: installmods()
  if '3' in answer: removemods()
  if '4' in answer: mainmenu() 
  elif answer: 
    print('Please enter a valid number.')
    time.sleep(1) 
    mods()

def fflags():
  exec('clear', '.')
  print(' ___        _   ___ _              \n| __|_ _ __| |_| __| |__ _ __ _ ___\n| _/ _` (_-<  _| _|| / _` / _` (_-<\n|_|\__,_/__/\__|_| |_\__,_\__, /__/\n                          |___/\n')

  print ('1) Open FastFlags folder\n2) Import JSON\n3) Apply FastFlags\n4) Remove FastFlags\n5) Go back\n')
  print('Waiting for input...')
  answer=getkey()
  if '1' in answer: openffolder()
  if '2' in answer: importjson()
  if '3' in answer: installfflags()
  if '4' in answer: removefflags()
  if '5' in answer: mainmenu() 
  elif answer: 
    print('Please enter a valid number.')
    time.sleep(1) 
    fflags()

# Mods Functions

def openmfolder():
  exec('open', datapath + '/Modifications')
  mods()

def installmods():
  exec('clear', '.')
  print('ℹ️  Applying mods...\n')
  if os.path.exists(robloxapp + '/oldResources'):
    shutil.rmtree(robloxapp + '/Resources')
    os.rename(robloxapp + '/oldResources', robloxapp + '/Resources')
  shutil.copytree(robloxapp + '/Resources', robloxapp + '/oldResources')
  shutil.copytree(datapath + '/Modifications', robloxapp + '/Resources', dirs_exist_ok=True)
  print('✅ Successfully applied mods')
  config['modsapplied'] = True
  saveconfig()
  print('\nPress any key to return to the menu.')
  if not getkey():
    time.sleep()
  mods()

def removemods():
  exec('clear', '.')
  print('ℹ️  Removing mods...\n')
  if os.path.exists(robloxapp + '/oldResources'):
    shutil.rmtree(robloxapp + '/Resources')
    os.rename(robloxapp + '/oldResources', robloxapp + '/Resources')
  print('ℹ️  Successfully removed mods')
  config['modsapplied'] = False
  saveconfig()
  print('\nPress any key to return to the menu.')
  if not getkey():
    time.sleep()
  mods()


# FastFlags Functions

def openffolder():
  exec('open', datapath + '/FastFlags')
  fflags()

def installfflags():
  exec('clear', '.')
  print('ℹ️  Applying FastFlags...\n')
  os.chdir(datapath + '/FastFlags/')
  finaljson = {}
  for f in glob.glob('*.json'):
      with open(f, 'r', encoding='utf-8') as infile:
        file_content = json.load(infile)
        for key, value in file_content.items():
          finaljson[key] = value
  jsonfile = json.dumps(finaljson, indent=1)
  if os.path.exists(robloxapp + '/MacOS/ClientSettings'):
    shutil.rmtree(robloxapp + '/MacOS/ClientSettings')
    os.makedirs(robloxapp + '/MacOS/ClientSettings')
  else:
    os.makedirs(robloxapp + '/MacOS/ClientSettings')
  os.chdir(robloxapp + '/MacOS/ClientSettings')
  with open('ClientAppSettings.json', 'w') as outfile:
    outfile.write(jsonfile)
  print('✅ Successfully applied FastFlags')
  config['fflagsapplied'] = True
  saveconfig()
  print('\nPress any key to return to the menu.')
  if not getkey():
    time.sleep()
  fflags()

def removefflags():
  exec('clear', '.')
  print('ℹ️  Removing FastFlags...\n')
  if os.path.exists(robloxapp + '/MacOS/ClientSettings'):
    shutil.rmtree(robloxapp + '/MacOS/ClientSettings')
  print('✅ Successfully removed FastFlags!')
  config['fflagsapplied'] = False
  saveconfig()
  print('\nPress any key to return to the menu.')
  if not getkey():
    time.sleep()
  fflags()

def importjson():
  lines = []
  exec('clear', '.')
  print('Paste the JSON you want to import below:\n')
  while True:
    importing = input()
    if importing == '':
      break
    else:
      lines.append(importing + '\n')
  try:
    json.loads(''.join(lines))
  except ValueError as error:
    exec('clear', '.')
    print('⚠️  An error occured imporitng this JSON!')
    print(error)
    print('\nPress any key to return to the menu.')
    if not getkey():
      time.sleep()
    fflags()
  def savejson():
    exec('clear', '.')
    name = input('What do you want to name this JSON? > ')
    if not os.path.exists(datapath + '/FastFlags/' + name + '.json'):
      os.chdir(datapath + '/FastFlags/')
      with open(name + '.json', 'w') as outfile:
        outfile.write(''.join(lines))
      print('\n✅ Successfully saved ' + name + '.json')
      print('\nPress any key to return to the menu.')
      if not getkey():
        time.sleep()
      fflags()
    else:
      print('\n⚠️  File already exists. Please try another name.')
      time.sleep(1)
      savejson()
  savejson()

# Misc Functions

def update():
  exec('clear', '.')
  print('ℹ️  Downloading ROBLOX...')
  try:
    os.remove('/tmp/RobloxPlayer.zip')
  except OSError:
    pass
  downloadlink = 'https://roblox-setup.cachefly.net/mac/' + clientsettings['clientVersionUpload'] + '-RobloxPlayer.zip'
  wget.download(downloadlink, out = '/tmp/RobloxPlayer.zip')
  print('ℹ️  Extracting...')
  with zipfile.ZipFile('/tmp/RobloxPlayer.zip') as zip:
    zip.extractall('/tmp/')
  os.remove('/tmp/RobloxPlayer.zip')
  shutil.rmtree(robloxapp)
  shutil.copytree('/tmp/RobloxPlayer.app', '/Applications/Roblox.app', dirs_exist_ok=True)
  dir = glob.glob(robloxapp + '/MacOS/*')
  for file in dir:
    if not file.endswith('.app'):
      current = os.stat(file)
      os.chmod(file, current.st_mode | stat.S_IEXEC)
      dir = glob.glob(robloxapp + '/MacOS/Roblox.app/Contents/MacOS/*')
      for file in dir:
        if not file.endswith('.app'):
          current = os.stat(file)
          os.chmod(file, current.st_mode | stat.S_IEXEC)
  shutil.rmtree(robloxapp + '/MacOS/RobloxPlayerInstaller.app')
  if config['modsapplied']:
    print('ℹ️  Applying Mods...')
    shutil.copytree(robloxapp + '/Resources', robloxapp + '/oldResources')
    shutil.copytree(datapath + '/Modifications', robloxapp + '/Resources', dirs_exist_ok=True)
  if config['fflagsapplied']:
    print('ℹ️  Applying FFlags...')
    os.chdir(datapath + '/FastFlags/')
    finaljson = {}
    for f in glob.glob('*.json'):
        with open(f, 'r', encoding='utf-8') as infile:
          file_content = json.load(infile)
          for key, value in file_content.items():
            finaljson[key] = value
    jsonfile = json.dumps(finaljson, indent=1)
    os.makedirs(robloxapp + '/MacOS/ClientSettings')
    os.chdir(robloxapp + '/MacOS/ClientSettings')
    with open('ClientAppSettings.json', 'w') as outfile:
      outfile.write(jsonfile)
  print('\n✅ Successfully updated ROBLOX')
  print('\nPress any key to go to the main menu.')
  if not getkey():
    time.sleep()
  mainmenu()

def install():
  exec('clear', '.')
  print('ℹ️  Installing BloxMgr...\n')
  
  os.makedirs(datapath)
  if not os.path.exists(datapath + '/Modifications'):
    os.makedirs(datapath + '/Modifications')
  if not os.path.exists(datapath + '/FastFlags'):
    os.makedirs(datapath + '/FastFlags')
  settingsdict = {
    'modsapplied': False,
    'fflagsapplied': False
  }
  jsonfile = json.dumps(settingsdict, indent=1)
  os.chdir(datapath)
  with open('applied.json', 'w') as outfile:
    outfile.write(jsonfile)
  config = json.load(open(datapath + '/applied.json'))


  if os.path.exists(robloxapp + '/MacOS/RobloxPlayerInstaller.app'):
    shutil.rmtree(robloxapp + '/MacOS/RobloxPlayerInstaller.app')

  print('\n✅ Successfully installed BloxMgr')
  print('\nPress any key to go to the main menu.')
  if not getkey():
    time.sleep()
  mainmenu()


def saveconfig():
  jsonfile = json.dumps(config, indent=1)
  os.chdir(datapath)
  with open('applied.json', 'w') as outfile:
    outfile.write(jsonfile)

# Load the main menu or the setup

if firstrun:
  setup()
else:
  mainmenu()