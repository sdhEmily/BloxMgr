tell application "Terminal"
	do script "curl https://github.com/sdhEmily/BloxMgr/raw/main/main.py -Lo /tmp/BloxMgr.py && python3 /tmp/BloxMgr.py; rm /tmp/BloxMgr.py"
	activate
end tell