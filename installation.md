# Installation
First, you will need to access the Home Assistant files, for example, using ssh.
An useful tutorial is available here: [https://www.wundertech.net/how-to-ssh-into-home-assistant/](https://www.wundertech.net/how-to-ssh-into-home-assistant/)

1. Access the terminal and paste the commands bellow:
```
cd ~/config/custom_components/
download_url=$(wget -q -O - https://api.github.com/repos/darkxst/ihost_indicator/releases/latest | jq -r '.assets[] | select(.name | contains("tar.xz")) | .browser_download_url')
wget "$download_url"
filename="${download_url##*/}"
tar -xf "$filename"
```
This command will download and extract the latest release in the folder `~/config/custom_components/`

2. Restart

3. then go to `Settings` > `Devices & Services` > + `ADD INTEGRATION`

4. Find `iHost indicator` and install it
