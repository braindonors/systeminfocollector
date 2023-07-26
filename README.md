# sysinfo.app

Sysinfo Python app to store system data in a python database

# Usage: 
use pip -r requirements.txt to install the correct subordinate components.

Start in Docker or via Apache web (Both of these need additional configuration which I haven't built out yet.

From the app folder

```bash
system: ~$ cd ./systeminfocollector
system: ~/systeminfocollector$ pip install -r requirements.txt
system: ~/systeminfocollector$ python3 ./app.py
```

# Primary usage from a client machine
## *nix systems
```bash
curl http://webserver/sysinfo.sh | bash

curl http://webserver/sysinfo.py | python3

```
## Windows Systems
```powershell
PS> iex (iwr "http://webserver/sysinfo.ps1").Content

```
* Either will work with their respective languages
* Internally, the app generates the python file with the correct url to post the data to, the bash version does the same, except encodes the python script as base64 and injects it into a bash wrapper.

use **pip -r requirements.txt** to install the correct subordinate components.

the script will prefer that dmidecode is on the system, but will not install it if missing.
