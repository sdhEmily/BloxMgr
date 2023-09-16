import sys, os, json, plistlib, zipfile, shutil, glob, warnings
os.system("echo Please Wait....") # ICKY WORKAROUND FOR A PLATYPUS BUG!!!
warnings.filterwarnings("ignore", message=".*https://github.com/urllib3/urllib3/issues/3020.*") # annoying warning and doesnt really do anything
try:
  import requests
except ImportError:
  os.system('python3 -m pip install requests')

import requests


try:
  sys.argv[1]
  robloxapp = "/Applications/Roblox.app/Contents"
  datapath = os.path.expanduser('~') + "/Library/Application Support/sdhEmily.RobloxPatcher"
  escdatapath = os.path.expanduser('~') + "/Library/Application\ Support/sdhEmily.RobloxPatcher"
  config = json.load(open(datapath + "/applied.json"))
  clientsettings = requests.get('https://clientsettingscdn.roblox.com/v2/client-version/MacPlayer/channel/LIVE').json()
  version = clientsettings["version"]
  downloadlink = "https://setup.rbxcdn.com/mac/" + clientsettings["clientVersionUpload"] + "-RobloxPlayer.zip"

  with open(robloxapp + "/info.plist", 'rb') as infile:
      localversion = plistlib.load(infile)["CFBundleShortVersionString"]

  if localversion != version:
    os.system("echo Updating Roblox...") # ICKY WORKAROUND FOR A PLATYPUS BUG!!!
    os.system("curl " + downloadlink + " -Lo /tmp/RobloxPlayer.zip > /dev/null 2>&1")
    with zipfile.ZipFile("/tmp/RobloxPlayer.zip") as zip:
      zip.extractall("/tmp/")
    shutil.rmtree("/Applications/Roblox.app") 
    os.rename("/tmp/RobloxPlayer.app", "/Applications/Roblox.app")
    os.system("echo Updated Roblox! Applying mods...") # ICKY WORKAROUND FOR A PLATYPUS BUG!!!
    os.system("chmod +x /Applications/Roblox.app/Contents/MacOS/*")
    os.system("chmod +x /Applications/Roblox.app/Contents/MacOS/Roblox.app/Contents/MacOS/*")
    if config["rmbeta"]:
      if os.path.exists(robloxapp + "/Resources/ExtraContent/places/Mobile.rbxl"):
        os.rename(robloxapp + "/Resources/ExtraContent/places/Mobile.rbxl", robloxapp + "/Resources/ExtraContent/places/oldMobile.rbxl")
    if config["olddeath"]:
      if os.path.exists(robloxapp + "/Resources"):
        if os.path.exists(robloxapp + "/Resources/content/sounds/oldouch.ogg"):
          os.rename(robloxapp + "/Resources/content/sounds/ouch.ogg", robloxapp + "/Resources/content/sounds/oldouch.ogg")
          os.system("curl https://github.com/sdhEmily/RobloxPatcher/raw/main/ouch.ogg -Lo " + robloxapp + "/Resources/content/sounds/ouch.ogg > /dev/null 2>&1")
    if config["modsapplied"]:
      shutil.copytree(robloxapp + "/Resources", robloxapp + "/oldResources")
      shutil.copytree(datapath + "/Modifications", datapath + "/Resources")
      os.system('/bin/cp -rf ' + escdatapath + '/Resources/. \"' + robloxapp + '/Resources\"')
      shutil.rmtree(datapath + "/Resources")
    if config["fflagsapplied"]:
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
    os.system("open " + sys.argv[1])
    os.system("echo Finished!") # ICKY WORKAROUND FOR A PLATYPUS BUG!!!
    os.system("exit")
  else:
    os.system("echo Roblox is up to date!") # ICKY WORKAROUND FOR A PLATYPUS BUG!!!
    os.system("open " + sys.argv[1])
    os.system("exit")
except IndexError:
  os.system("osascript -e 'tell application \"Terminal\"' -e  'do script \"curl https://github.com/sdhEmily/RobloxPatcher/raw/main/main.py -Lo /tmp/RobloxPatcher.py && python3 /tmp/RobloxPatcher.py; rm /tmp/RobloxPatcher.py && exit\"' -e 'end tell'") # this is really gross i feel and i want to replace it with something better later (send help)
  os.system("exit")