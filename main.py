import os, sys, time, subprocess, json, shutil, glob

def getkey(): # Credit to https://stackoverflow.com/a/1840
    import sys, tty, termios, select
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    answer = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    return answer

datapath = os.path.expanduser('~') + '/Library/Application Support/sdhEmily.BloxMgr'
robloxapp = '/Applications/Roblox.app/Contents' # not to e removed im too lazy to do allat rn.
if not os.path.exists(datapath):
  os.makedirs(datapath)
if not os.path.exists(datapath + '/Modifications'):
  os.makedirs(datapath + '/Modifications')
if not os.path.exists(datapath + '/FastFlags'):
  os.makedirs(datapath + '/FastFlags')

def exec(cmd, args, path=None, sh=False):
  if path != None:
    subprocess.call([cmd, args, path], shell=sh)
  else:
    subprocess.call([cmd, args], shell=sh)

# Menu Sections

def mainmenu():
  exec('clear', '.')
  print(' ___ _         __  __          \n| _ ) |_____ _|  \/  |__ _ _ _ \n| _ \ / _ \ \ / |\/| / _` | \'_|\n|___/_\___/_\_\_|  |_\__, |_|  \n                     |___/     ')

  print ('1) Mods\n2) FastFlags\n3) Quit\n')
  print('Waiting for input...')
  answer=getkey()
  if '1' in answer: mods()
  elif '2' in answer: fflags()
  elif '3' in answer: exit()
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
  print('ℹ️  Applying mods, please wait...\n')
  if os.path.exists(robloxapp + '/oldResources'):
    shutil.rmtree(robloxapp + '/Resources')
    os.rename(robloxapp + '/oldResources', robloxapp + '/Resources')
  shutil.copytree(robloxapp + '/Resources', robloxapp + '/oldResources')
  shutil.copytree(datapath + '/Modifications', robloxapp + '/Resources', dirs_exist_ok=True)
  print('✅ Successfully applied mods')
  print('\nPress any key to return to the menu.')
  if not getkey():
    time.sleep()
  mods()

def removemods():
  exec('clear', '.')
  print('ℹ️  Removing mods, Please wait...\n')
  if os.path.exists(robloxapp + '/oldResources'):
    shutil.rmtree(robloxapp + '/Resources')
    os.rename(robloxapp + '/oldResources', robloxapp + '/Resources')
  print('ℹ️  Successfully removed mods')
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
  print('ℹ️  Applying FastFlags, please wait...\n')
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
  print('\nPress any key to return to the menu.')
  if not getkey():
    time.sleep()
  fflags()

def removefflags():
  exec('clear', '.')
  print('ℹ️  Removing FastFlags, please wait...\n')
  if os.path.exists(robloxapp + '/MacOS/ClientSettings'):
    shutil.rmtree(robloxapp + '/MacOS/ClientSettings')
  print('✅ Successfully removed FastFlags!')
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

# Load the main menu

mainmenu()