import os, time, shutil, glob, json
def getkey(): # Credit to https://stackoverflow.com/a/1840
    import sys, tty, termios, select
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    answer = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    return answer


# Initialize Data Directory

datapath = os.path.expanduser('~') + "/Library/Application Support/sdhhhhh.RobloxPatcher"
escdatapath = os.path.expanduser('~') + "/Library/Application\ Support/sdhhhhh.RobloxPatcher"
robloxapp = "/Applications/Roblox.app/Contents"
if not os.path.exists(datapath):
  os.makedirs(datapath)
if not os.path.exists(datapath + "/Modifications"):
  os.makedirs(datapath + "/Modifications")
if not os.path.exists(datapath + "/FastFlags"):
  os.makedirs(datapath + "/FastFlags")


# Menu Sections

def mainmenu():
  os.system('clear')
  print(" ___     _    _         ___      _      _            \n| _ \___| |__| |_____ _| _ \__ _| |_ __| |_  ___ _ _ \n|   / _ \ '_ \ / _ \ \ /  _/ _` |  _/ _| ' \/ -_) '_|\n|_|_\___/_.__/_\___/_\_\_| \__,_|\__\__|_||_\___|_|\n")
  print("Roblox.app Selected: /" + robloxapp.strip("/Contents") + "\n")

  print ("1) Utilities \n2) Mods\n3) FastFlags\n4) Select Roblox.app\n5) Quit\n")
  print("Waiting for input...")
  answer=getkey()
  if "1" in answer: utilities()
  elif "2" in answer: mods()
  elif "3" in answer: fflags()
  elif "4" in answer: chooseapp()
  elif "5" in answer: exit()
  elif answer:
    print("Please enter a valid number.")
    time.sleep(1) 
    mainmenu()

def utilities():
  global mobileapplied
  global olddeathapplied

  if os.path.exists(robloxapp + "/Resources/ExtraContent/places/oldMobile.rbxl"):
    mobileapplied = "[APPLIED]"
  else:
    mobileapplied = ""

  if os.path.exists(robloxapp + "/Resources/content/sounds/oldouch.ogg"):
    olddeathapplied = "[APPLIED]"
  else:
    olddeathapplied = ""

  os.system('clear')
  print(" _   _ _   _ _ _ _   _        \n| | | | |_(_) (_) |_(_)___ ___\n| |_| |  _| | | |  _| / -_|_-<\n \___/ \__|_|_|_|\__|_\___/__/\n")


  print ("1) Disable the Mobile main menu " + mobileapplied, "\n2) Restore the old death sound " + olddeathapplied, "\n3) Go back\n")
  print("Waiting for input...")
  answer=getkey()
  if "1" in answer: mobilemenu()
  if "2" in answer: oldoof()
  if "3" in answer: mainmenu()
  elif answer: 
    print("Please enter a valid number.")
    time.sleep(1) 
    utilities()

def mods():
  os.system('clear')
  print(" __  __         _    \n|  \/  |___  __| |___\n| |\/| / _ \/ _` (_-<\n|_|  |_\___/\__,_/__/\n")

  print ("1) Open mods folder\n2) Apply mods\n3) Remove mods\n4) Go back\n")
  print("Waiting for input...")

  answer=getkey()
  if "1" in answer: openmfolder()
  if "2" in answer: installmods()
  if "3" in answer: removemods()
  if "4" in answer: mainmenu() 
  elif answer: 
    print("Please enter a valid number.")
    time.sleep(1) 
    mods()

def fflags():
  os.system('clear')
  print(" ___        _   ___ _              \n| __|_ _ __| |_| __| |__ _ __ _ ___\n| _/ _` (_-<  _| _|| / _` / _` (_-<\n|_|\__,_/__/\__|_| |_\__,_\__, /__/\n                          |___/\n")

  print ("1) Open FastFlags folder\n2) Import JSON\n3) Apply FastFlags\n4) Remove FastFlags\n5) Go back\n")
  print("Waiting for input...")
  answer=getkey()
  if "1" in answer: openffolder()
  if "2" in answer: importjson()
  if "3" in answer: installfflags()
  if "4" in answer: removefflags()
  if "5" in answer: mainmenu() 
  elif answer: 
    print("Please enter a valid number.")
    time.sleep(1) 
    fflags()


# Utilities Functions

def mobilemenu():
  if os.path.exists(robloxapp + "/Resources/ExtraContent/places/oldMobile.rbxl"):
    global mobileapplied
    os.rename(robloxapp + "/Resources/ExtraContent/places/oldMobile.rbxl", robloxapp + "/Resources/ExtraContent/places/Mobile.rbxl")
    if os.path.exists(robloxapp + "/oldResources/ExtraContent/places/oldMobile.rbxl"):
      os.rename(robloxapp + "/oldResources/ExtraContent/places/oldMobile.rbxl", robloxapp + "/oldResources/ExtraContent/places/Mobile.rbxl")
    utilities()
    mobileapplied = ""
  else:
    os.rename(robloxapp + "/Resources/ExtraContent/places/Mobile.rbxl", robloxapp + "/Resources/ExtraContent/places/oldMobile.rbxl")
    if os.path.exists(robloxapp + "/oldResources/ExtraContent/places/Mobile.rbxl"):
      os.rename(robloxapp + "/oldResources/ExtraContent/places/Mobile.rbxl", robloxapp + "/oldResources/ExtraContent/places/oldMobile.rbxl")
    utilities()
    mobileapplied = "[APPLIED]"

def oldoof():
  if os.path.exists(robloxapp + "/Resources/content/sounds/oldouch.ogg"):
    global olddeathapplied
    os.remove(robloxapp + "/Resources/content/sounds/ouch.ogg")
    os.rename(robloxapp + "/Resources/content/sounds/oldouch.ogg", robloxapp + "/Resources/content/sounds/ouch.ogg")
    if os.path.exists(robloxapp + "/oldResources/content/sounds/oldouch.ogg"):
      os.remove(robloxapp + "/oldResources/content/sounds/ouch.ogg")
      os.rename(robloxapp + "/oldResources/content/sounds/oldouch.ogg", robloxapp + "/oldResources/content/sounds/ouch.ogg")
    olddeathapplied = ""
    utilities()
  else:
    os.rename(robloxapp + "/Resources/content/sounds/ouch.ogg", robloxapp + "/Resources/content/sounds/oldouch.ogg")
    os.system("clear")
    print("ℹ️  Downloading old death sound, please wait...\n")
    if os.path.exists(robloxapp + "/oldResources"):
      if os.path.exists(robloxapp + "/oldResources/content/sounds/oldouch.ogg"):
        os.rename(robloxapp + "/oldResources/content/sounds/ouch.ogg", robloxapp + "/oldResources/content/sounds/oldouch.ogg")
        os.system("curl https://github.com/sdhhhhh/RobloxPatcher-MacOS/raw/main/ouch.ogg -Lo " + robloxapp + "/oldResources/content/sounds/ouch.ogg")
    os.system("curl https://github.com/sdhhhhh/RobloxPatcher-MacOS/raw/main/ouch.ogg -Lo " + robloxapp + "/Resources/content/sounds/ouch.ogg")
    olddeathapplied = "[APPLIED]"
    print("\n✅  Successfully installed old death sound!")
    print("\nPress any key to return to the menu.")
    if not getkey():
      time.sleep()
    utilities()


# Mods Functions

def openmfolder():
  os.system("open \'" + datapath + "/Modifications\'")
  mods()

def installmods():
  os.system("clear")
  print("ℹ️  Applying mods, please wait...\n")
  if os.path.exists(robloxapp + "/oldResources"):
    shutil.rmtree(robloxapp + "/Resources")
    os.rename(robloxapp + "/oldResources", robloxapp + "/Resources")
  shutil.copytree(robloxapp + "/Resources", robloxapp + "/oldResources")
  shutil.copytree(datapath + "/Modifications", datapath + "/Resources")
  os.system('/bin/cp -rf ' + escdatapath + '/Resources/. \"' + robloxapp + '/Resources\"')
  shutil.rmtree(datapath + "/Resources")
  print("✅ Successfully applied mods")
  print("\nPress any key to return to the menu.")
  if not getkey():
    time.sleep()
  mods()

def removemods():
  os.system("clear")
  print("ℹ️  Removing mods, Please wait...\n")
  if os.path.exists(robloxapp + "/oldResources"):
    shutil.rmtree(robloxapp + "/Resources")
    os.rename(robloxapp + "/oldResources", robloxapp + "/Resources")
  print("ℹ️  Successfully removed mods")
  print("\nPress any key to return to the menu.")
  if not getkey():
    time.sleep()
  mods()


# FastFlags Functions

def openffolder():
  os.system("open \'" + datapath + "/FastFlags\'")
  fflags()

def installfflags():
  os.system("clear")
  print("ℹ️  Applying FastFlags, please wait...\n")
  os.chdir(datapath + "/FastFlags/")
  finaljson = {}
  for f in glob.glob("*.json"):
      with open(f, "r", encoding='utf-8') as infile:
        file_content = json.load(infile)
        for key, value in file_content.items():
          finaljson[key] = value
  jsonfile = json.dumps(finaljson, indent=1)
  if os.path.exists(robloxapp + "/MacOS/ClientSettings"):
    shutil.rmtree(robloxapp + "/MacOS/ClientSettings")
    os.makedirs(robloxapp + "/MacOS/ClientSettings")
  else:
    os.makedirs(robloxapp + "/MacOS/ClientSettings")
  os.chdir(robloxapp + "/MacOS/ClientSettings")
  with open("ClientAppSettings.json", "w") as outfile:
    outfile.write(jsonfile)
  print("✅ Successfully applied FastFlags")
  print("\nPress any key to return to the menu.")
  if not getkey():
    time.sleep()
  fflags()

def removefflags():
  os.system("clear")
  print("ℹ️  Removing FastFlags, please wait...\n")
  if os.path.exists(robloxapp + "/MacOS/ClientSettings"):
    shutil.rmtree(robloxapp + "/MacOS/ClientSettings")
  print("✅ Successfully removed FastFlags!")
  print("\nPress any key to return to the menu.")
  if not getkey():
    time.sleep()
  fflags()

def importjson():
  lines = []
  os.system("clear")
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
    os.system("clear")
    print("⚠️  An error occured imporitng this JSON!")
    print(error)
    print("\nPress any key to return to the menu.")
    if not getkey():
      time.sleep()
    fflags()
  def savejson():
    os.system("clear")
    name = input("What do you want to name this JSON? > ")
    if not os.path.exists(datapath + "/FastFlags/" + name + ".json"):
      os.chdir(datapath + "/FastFlags/")
      with open(name + ".json", "w") as outfile:
        outfile.write(''.join(lines))
      print("\n✅ Successfully saved " + name + ".json")
      print("\nPress any key to return to the menu.")
      if not getkey():
        time.sleep()
      fflags()
    else:
      print("\n⚠️  File already exists. Please try another name.")
      time.sleep(1)
      savejson()
  savejson()


# Choose app if it isnt detected

def chooseapp():
  os.system("clear")
  newroblox = input('Drag the Roblox.app into the terminal (Enter : to cancel) > ')
  global robloxapp
  if ":" in newroblox: 
    mainmenu()
  if os.path.exists(newroblox.rstrip() + "/Contents/MacOS/RobloxPlayer"):
    robloxapp = newroblox.rstrip() + "/Contents"
    mainmenu()
  else:
    print("This is not a valid Roblox.app!")
    time.sleep(1)
    chooseapp()

if not os.path.exists(robloxapp):
  chooseapp()


# Load the main menu

mainmenu()