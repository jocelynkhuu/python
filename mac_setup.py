#!/usr/bin/env python3

# Personal script to quickly set up new Macs
#
# Installs shell themes: powerlevel10k and lsd
# Creates/adds aliases to .zshrc and .vimrc
# 
# Installs apps: Rectangle, VSCode, Spotify
#
# Tested with Python 3.9.6 on Ventura

import os
import shutil
import subprocess
import platform
import requests
import logging
import sys
from datetime import datetime

# Send logs to /tmp as well as stdout
file_handler = logging.FileHandler(filename=datetime.now().strftime('/tmp/computersetup_%m%d%Y_%H%M%S.log'))
stdout_handler = logging.StreamHandler(sys.stdout) 
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=handlers
) 

logger = logging.getLogger('LOGGER_NAME')

### VARIABLES
HOME = os.path.expanduser('~')
DOWNLOADS = f"{HOME}/Downloads"

xcode = "/Library/Developer/CommandLineTools"

zshrc = f"{HOME}/.zshrc"
def_zsh = "/bin/zsh"

vimrc = f"{HOME}/.vimrc"
def_vim = "/usr/bin/vim"

font_loc = f"{HOME}/Library/Fonts"

rec = "/Applications/Rectangle.app"
loc_rec = f"{DOWNLOADS}/Rectangle.dmg"
down_rec = "https://api.github.com/repos/rxhanson/Rectangle/releases/latest"

code = "/Applications/Visual Studio Code.app"
loc_code = f"{DOWNLOADS}/VSCode.zip"
down_code = "https://code.visualstudio.com/sha/download\?build\=stable\&os\=darwin-universal"

betterdisplay = "/Applications/BetterDisplay.app"
loc_betterdisplay = f"{DOWNLOADS}/Betterdisplay.dmg"
bd_latest_down_link = "https://api.github.com/repos/waydabber/BetterDisplay/releases/latest"
vol_betterdisplay = "/Volumes/BetterDisplay"

firefox = "/Applications/Firefox.app"
loc_firefox = f"{DOWNLOADS}/Firefox.dmg"
vol_firefox = "/Volumes/Firefox"
down_firefox = "https://download.mozilla.org/\?product=firefox-latest-ssl\&os=osx\&lang=en-US"

chrome = "/Applications/Google Chrome.app"
loc_chrome = f"{DOWNLOADS}/googlechrome.dmg"
vol_chrome = "/Volumes/Google\ Chrome"
down_chrome = "https://dl.google.com/chrome/mac/universal/stable/GGRO/googlechrome.dmg"

spotify = "/Applications/Spotify.app"
loc_spotify = f"{DOWNLOADS}/SpotifyInstaller.zip"
app_spotify = f"{DOWNLOADS}/Install\ Spotify.app"
down_spotify = "https://download.scdn.co/SpotifyInstaller.zip"

iterm = "/Applications/iTerm.app"
loc_iterm = f"{DOWNLOADS}/iTerm2.zip"
down_iterm = "https://iterm2.com/downloads/stable/latest"

### DOTFILE CONFIGS
alias = """
## LS & TREE
alias ls='lsd'

### Colorize commands
alias grep='grep --color=auto'
alias ip='ip --color=auto'
alias vi='vim'
alias cp="cp -i"
alias ll='ls -la'

"""

m1_alias = """
## LS & TREE
alias ls='lsd'

### Colorize commands
alias grep='grep --color=auto'
alias ip='ip --color=auto'
alias vi='vim'
alias cp="cp -i"
alias ll='ls -la'

export PATH=/opt/homebrew/bin:$PATH
export PATH=/opt/homebrew/sbin:$PATH
"""

vim_text = """
set number
syntax on
set smartindent
set tabstop=4
set hlsearch
cmap w!! w !sudo tee > /dev/null %

"""

# Install xcode-select
def install_xcode():
    if not os.path.isdir(xcode):
        subprocess.run("xcode-select --install", shell=True, stdout=True)

# Creates ~/.zshrc with aliases
def create_zsh():
    logging.info(f"Searching for {zshrc}")
    if os.path.isfile(zshrc):
        logging.info(f"{zshrc} already exists. Checking file.")
        check_alias = "ls='lsd'"
        with open(f"{zshrc}", "r+") as file:
            file.seek(0)
            lines = file.read()
            if check_alias in lines: 
                    logging.info('Alias already exists in file. Not creating.')
            else:
                logging.info("Alias does not exist. Appending file")
                if platform.processor() == "arm":
                    file.write(m1_alias)
                else:
                    file.write(alias)
    else:
        logging.info(f"{zshrc} does not exist. Creating new file")
        with open(zshrc, "a") as file:
            if platform.processor() == "arm":
                file.write(m1_alias)
            else:
                file.write(alias)

    # To doublecheck that file is actually there
    if os.path.isfile(zshrc):
        logging.info("Woohoo!")
    else:
        logging.debug(f"Could not create {zshrc}.")

# Installs Homebrew
def install_homebrew():
    url = "https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh"
    script_path = "/tmp/install.sh"

    try:
        # Download the script
        response = response.get(url)
        response.raise_for_status()

        with open(script_path, 'wb') as file:
            file.write(response.content)
        print("Homebrew script downloaded.")

        # Make the script executable
        os.chmod(script_path, 0o755)

        # Run the script
        subprocess.run(['/bin/bash', script_path], check=True)
        print("Homebrew installed successfully")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading script: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally: # this block is always executed regardless of exception status
        if os.path.exists(script_path):
             os.remove(script_path)

def check_homebrew():
    logging.info("Checking if homebrew is installed.")
    if shutil.which('brew') is None:
        logging.info("Installing Homebrew")
        install_homebrew()
    else:
        logging.info("Homebrew installed")

# Installs recommended fonts for p10k to work
def check_fonts():
    logging.info(f"Checking if fonts are installed in {font_loc}")
    down_font = [
        (f'{font_loc}/MesloLGS NF Regular.ttf',f'https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf'),
        (f'{font_loc}/MesloLGS NF Bold.ttf', f'https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf'),
        (f'{font_loc}/MesloLGS NF Italic.ttf', f'https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf'),
        (f'{font_loc}/MesloLGS NF Bold Italic.ttf', f'https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf')
    ]
    for fonts in down_font:
        if os.path.isfile(fonts[0]):
            logging.info(f"{fonts[0]} exists.")
        else:
            logging.info(f"{fonts[0]} does not exist. Downloading fonts to {font_loc}.")

            try:
                response = requests.get(fonts[1])
                response.raise_for_status()

                with open(fonts[0], 'wb') as file:
                    file.write(response.content) 
            except requests.exceptions.RequestException as e:
                 print(f"Error downloading font: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                if os.path.isfile(fonts[0]):
                    logging.info("Font has been downloaded.")
                else:
                    logging.debug("Font was not downloaded. Please manually download from https://github.com/romkatv/powerlevel10k")

# Installs powerlevel10k
def install_plvl():
    cmd = f'brew install romkatv/powerlevel10k/powerlevel10k && echo "source $(brew --prefix)/share/powerlevel10k/powerlevel10k.zsh-theme" >>~/.zshrc'
    subprocess.run(cmd, shell=True, stdout=True)

def check_plvl():
    logging.info("Checking if powerlevel10k is installed: https://github.com/romkatv/powerlevel10k")
    powlevel = subprocess.call(['brew list | grep powerlevel10k'], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    if powlevel != 0:
        logging.info("Not installed. Installing p10k.")
        install_plvl()
    else:
        logging.info("Powerlevel10k is installed.")

# Installs lsd
def install_lsd():
    cmd = f'brew install lsd'
    subprocess.run(cmd, shell=True, stdout=True)

def check_lsd():
    logging.info("Checking if lsd is installed: https://github.com/Peltoche/lsd")
    if shutil.which('lsd') is None:
        logging.info("Not installed. Installing lsd.")
        install_lsd()
    else:
        logging.info("lsd is installed.")

# Install ykman and yubico-piv-tool
def install_ykman():
	cmd = f'brew install ykman'
	subprocess.run(cmd, shell=True, stdout=True)

def check_ykman():
	logging.info("Checking if ykman is installed: brew install ykman")
	if shutil.which('ykman') is None:
		logging.info("Not installed. Install ykman.")
		install_ykman()
	else:
		logging.info("ykman is installed.")

def install_yubico_piv_tool():
	cmd = f'brew install yubico-piv-tool'
	subprocess.run(cmd, shell=True, stdout=True)

def check_yubico_piv_tool():
	logging.info("Checking if yubico-piv-tool is installed: brew install yubico-piv-tool")
	if shutil.which('yubico-piv-tool') is None:
		logging.info("Not installed. Install yubico-piv-tool.")
		install_yubico_piv_tool()
	else:
		logging.info("yubico-piv-tool is installed.")

# Install gopass
def install_gopass():
	cmd = f'brew install gopass'
	subprocess.run(cmd, shell=True, stdout=True)

def check_gopass():
	logging.info("Checking if gopass is installed: brew install gopass")
	if shutil.which('gopass') is None:
		logging.info("Not installed. Install gopass.")
		install_gopass()
	else:
		logging.info("gopass is installed.")

# Installs google-cloud-sdk
def install_gcloud():
	cmd = f'brew install --cask google-cloud-sdk'
	subprocess.run(cmd, shell=True, stdout=True)

def check_gcloud():
	logging.info("Checking if gcloud is installed")
	if shutil.which('gcloud') is None:
		logging.info("Not installed. Install gcloud.")
		install_gopass()
	else:
		logging.info("gcloud is installed.")

# Checks if shell is /bin/zsh
def check_shell():
    logging.info("Checking shell environment")
    shell = os.environ['SHELL']
    if shell == def_zsh:
        logging.info(f"Shell is {def_zsh}. Right on!")
    else:
        logging.info(f"Shell is not {def_zsh}. Updating shell.")
        cmd = f'chsh -s {def_zsh}' 
        subprocess.run(cmd, shell=True, stdout=True)

# Source .zshrc to apply changes
def source_zsh():
    cmd = f'source {zshrc} >& /dev/null'
    subprocess.run(cmd, shell=True)

# Creates .vimrc and adds config
def check_vimrc():
    logging.info(f"Searching for {vimrc}")
    if os.path.isfile(vimrc):
        logging.info(f"{vimrc} exists. Checking config.")
        check_vimrc = "set number" 
        with open(f"{vimrc}", "r+") as file:
            file.seek(0)
            lines = file.read()
            if check_vimrc in lines:
                logging.info("Config already exists in file.")
            else:
                logging.info("Config does not exist in file. Appending file.")
                file.write(f"{vim_text}")
    else:
        logging.info(f"{vimrc} does not exist. Creating file.")
        with open(vimrc, "a") as file:
            file.write(f"{vim_text}")
    # To doublecheck if file is there
    if os.path.isfile(vimrc):
        logging.info("Woohoo!")
    else:
        logging.debug(f"could not create {vimrc}.")

# Installs Rectangle app
def install_rec():
    logging.info("Checking to see if Rectangle is installed: https://rectangleapp.com/")
    if os.path.isdir(rec):
        logging.info("Rectangle is installed!")
    else:
        logging.info("Rectangle not installed. Installing now.")
        response = requests.get(f"{down_rec}").json()
        rec_dmg_name = response.get('assets')[0].get('name')
        rec_vol_name = rec_dmg_name.removesuffix('.dmg')
        vol_rec = f"/Volumes/{rec_vol_name}" 
        rec_down_url = response.get('assets')[0].get('browser_download_url')
        
        try:
            # Download the DMG file
            with requests.get(rec_down_url, stream=True) as r:
                r.raise_for_status()
                with open(loc_rec, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            cmds = [
                f"sudo hdiutil attach {loc_rec} && cd {vol_rec}",
                f"sudo cp -R {vol_rec}/Rectangle.app /Applications",
                f"sudo hdiutil unmount {vol_rec}"
            ]
            for cmd in cmds:
                subprocess.run(cmd, shell=True, stdout=True)

            if os.path.isdir(rec):
                logging.info("Successfully installed Rectangle!")
            else:
                logging.debug(f"Unable to install Rectangle. Please check {DOWNLOADS} for file.")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error downloading Rectangle DMG: {e}")
        except Exception as e:
            logging.error(f"An error occurred during Rectangle installation: {e}")


# Looks for download URL on BetterDisplay release page and install latest version
def install_bd():
    logging.info("Checking if BetterDisplay is installed: https://github.com/waydabber/BetterDisplay")
    if os.path.isdir(betterdisplay):
        logging.info("BetterDisplay is installed!")
    else:
        logging.info("BetterDisplay is not installed. Installing now.")
        response = requests.get(f"{bd_latest_down_link}").json()
        bd_down_url = response.get('assets')[0].get('browser_download_url')
        
        try:
            # Download the DMG file
            with requests.get(bd_down_url, stream=True) as r:
                r.raise_for_status()
                with open(loc_betterdisplay, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
        
            cmds = [
                f"curl -L {bd_down_url} -o {loc_betterdisplay}",
                f"sudo hdiutil attach {loc_betterdisplay} && cd {vol_betterdisplay}",
                f"sudo cp -R {vol_betterdisplay}/BetterDisplay.app /Applications",
                f"sudo hdiutil unmount {vol_betterdisplay}"
            ]
            for i in cmds:
                subprocess.run(i, shell=True, stdout=True)
            if os.path.isdir(betterdisplay):
                logging.info("Successfully installed BetterDisplay!")
            else:
                logging.debug(f"Unable to install BettterDisplay. Please check {DOWNLOADS} for file.")
        
        except requests.exceptions.RequestException as e: 
             logging.error(f"Error downloading BetterDisplay as {e}")
        except Exception as e:
            logging.error(f"An error occurred during BetterDisplay installation: {e}")

# Installs Firefox app
def install_firefox():
    logging.info("Checking if Firefox is installed.")
    if os.path.isdir(firefox):
        logging.info("Firefox is installed!")
    else:
        logging.info("Firefox is not installed. Installing now.")
        
        try:
             # Download the DMG file
            with requests.get(down_firefox, stream=True) as r:
                r.raise_for_status()
                with open(loc_firefox, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        f.write(chunk)
        
            cmds = [
                f"sudo hdiutil attach {loc_firefox} && cd {vol_firefox}",
                f"sudo cp -R {vol_firefox}/Firefox.app /Applications",
                f"sudo hdiutil unmount {vol_firefox}"
            ]
            for i in cmds:
                subprocess.run(i, shell=True, stdout=True)
            if os.path.isdir(firefox):
                logging.info("Successfully installed Firefox!")
            else:
                logging.debug(f"Unable to install Firefox. Please check {DOWNLOADS} for file.")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error downloading Firefox DMG: {e}")
        except Exception as e:
            logging.error(f"An error occurred during Firefox installation: {e}")

# Installs Google Chrome app
def install_chrome():
	logging.info("Checking if Google Chrome is installed.")
	if os.path.isdir(chrome):
		logging.info("Google Chrome is installed!")
	else:
		logging.info("Google Chrome is not installed. Installing now.")
		
        try:
            # Download the DMG file
            with requests.get(down_chrome, stream=True) as r:
                r.raise_for_status()
                with open(loc_firefox, 'wb') as f: 
                     for chunk in r.iter_content(chunk_size=8182):
                          f.write(chunk)
        
            cmds = [
                f"sudo hdiutil attach {loc_chrome} && cd {vol_chrome}",
                f"sudo cp -R {vol_chrome}/Google\ Chrome.app /Applications",
                f"sudo hdiutil unmount {vol_chrome}"
            ]
            for i in cmds:
                subprocess.run(i, shell=True, stdout=True)
            if os.path.isdir(chrome):
                logging.info("Successfully installed Google Chrome!")
            else:
                logging.debug(f"Unable to install Google Chrome. Please check {DOWNLOADS} for file.")
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Error downloading Google Chrome DMG: {e}")
        except Exception as e:
            logging.error(f"An error occurred during Google Chrome installation: {e}")
        
# Installs VS Code
def install_code():
    logging.info("Checking if VS Code is installed: https://code.visualstudio.com/Download")
    if os.path.isdir(code):
        logging.info("VS Code is installed!")
    else:
        logging.info("VS Code is not installed. Installing now.")

        try:
            with requests.get(down_code, stream=True) as r:
                  r.raise_for_status()
                  with open(loc_code, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk) 
            cmds = [ 
                f"curl -L {down_code} -o {loc_code}",
                f"unzip {loc_code} -d {DOWNLOADS}", 
                f"sudo mv {DOWNLOADS}/Visual\ Studio\ Code.app /Applications"
            ]   
            for i in cmds:
                subprocess.run(i, shell=True, stdout=True)
            if os.path.isdir(code):
                logging.info("Successfully installed VS Code!")
            else: 
                logging.debug(f"Unable to install VS Code. Please check {DOWNLOADS} for file.")
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Error downloading VS Code DMG: {e}")
        except Exception as e:
            logging.error(f"An error occurred during VS Code installation: {e}")

# Installs Spotify
def install_spotify():
    logging.info("Checking if Spotify is installed.")
    if os.path.isdir(spotify):
        logging.info("Spotify is installed!")
    else:
        logging.info("Spotify not installed. Installing now.")
        cmds = [
            f"curl -L {down_spotify} -o {loc_spotify}",
            f"unzip {loc_spotify} -d {DOWNLOADS}", 
            f"/usr/bin/open -W {app_spotify}"
        ]
        for i in cmds:
            subprocess.run(i, shell=True, stdout=True)
        if os.path.isdir(spotify):
            logging.info("Successfully installed Spotify!")
        else:
            logging.debug(f"Unable to install Spotify. Please check {DOWNLOADS}.") 

# Installs iTerm2
def install_iterm():
    logging.info("Checking if iTerm2 is installed: https://iterm2.com/")
    if os.path.isdir(iterm):
        logging.info("iTerm2 is installed!")
    else:
        logging.info("iTerm2 is not installed. Installing now.")
        cmds = [ 
            f"curl -L {down_iterm} -o {loc_iterm}",
            f"unzip {loc_iterm} -d {DOWNLOADS}",
            f"sudo mv {DOWNLOADS}/iTerm.app /Applications"
        ]   
        for i in cmds:
            subprocess.run(i, shell=True, stdout=True)
        if os.path.isdir(iterm):
            logging.info("Successfully installed iTerm2!")
        else: 
            logging.debug(f"Unable to install iTerm2. Please check {DOWNLOADS} for file.")


def main():
    logging.info("Setting up laptop with your configs!")
    install_xcode()
    create_zsh()
    check_homebrew()
    check_plvl()
    check_lsd()
    check_ykman()
    check_yubico_piv_tool()
    check_gopass()
    check_gcloud()
    check_shell()
    source_zsh()
    check_fonts() 
    check_vimrc()
    install_rec()
    install_bd()
    install_code()
    install_firefox()
    install_chrome()
    install_spotify()
    install_iterm()
    logging.info("Setup complete! Please open new terminal. Goodbye! :)")

if __name__ == "__main__":
    main()
