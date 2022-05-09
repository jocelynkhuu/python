#!/usr/bin/env python3

#
# Personal script to quickly set up new Macs
#
# Installs shell themes: powerlevel10k and lsd
# Creates/adds aliases to .zshrc and .vimrc
# 
# Installs apps: Rectangle & VSCode
#
# Tested with Python 3.8.9 on Monterey 12.3.1

import os
import shutil
import subprocess

HOME = os.path.expanduser('~')
zshrc = f"{HOME}/.zshrc"
def_zsh = "/bin/zsh"

vimrc = f"{HOME}/.vimrc"
def_vim = "/usr/bin/vim"

font_loc = f"{HOME}/Library/Fonts"
font_file = str(f"{font_loc}/'MesloLGS NF Regular'.ttf")
loc_file = str(f"{font_loc}/MesloLGS NF Regular.ttf")

rec = "/Applications/Rectangle.app"
loc_rec = f"{HOME}/Downloads/Rectangle.dmg"
vol_rec = "/Volumes/Rectangle0.56"

code = "/Applications/Visual Studio Code.app"
loc_code = f"{HOME}/Downloads/VSCode.zip"

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

vim_text = """
set number
syntax on
set smartindent
set tabstop=4
set hlsearch
cmap w!! w !sudo tee > /dev/null %

"""

def create_zsh():
    print(f"Searching for {zshrc}")
    if os.path.isfile(zshrc):
        print(".zshrc already exists. Checking file.")
        check_alias = "ls='lsd'"
        with open(f"{zshrc}", "r+") as file:
            file.seek(0)
            lines = file.read()
            if check_alias in lines:
                    print('Alias already exist in file. Not creating')
            else:
                print("Alias does not exist. Appending file")
                file.write(alias)
    else: 
        print(".zshrc does not exist. Creating new file")
        with open(zshrc, "a") as file:
            file.write(alias)
    # To doublecheck that file is actually there
    if os.path.isfile(zshrc):
        print("woohoo!")
    else:
        print(f"could not create {zshrc}")

def install_homebrew():
    cmd = f'/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    subprocess.run(cmd, shell=True, stdout=True)

def check_homebrew():
    print("Checking if homebrew is installed.")
    if shutil.which('brew') is None:
        print("Installing Homebrew")
        install_homebrew()
    else:
        print("Homebrew installed")

# Only installed MesloLGS NF Regular to make p10k work
def check_fonts():
    print("Check if font is installed.")
    down_font = f'https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf'
    if os.path.isfile(loc_file):
        print(f"{font_file} exists. Don't forget to change Terminal font!")
    else:
        print(f"{font_file} does not exist. Downloading fonts to {font_loc}.")
        subprocess.run(f"curl -L {down_font} -o {font_file}", shell=True, stdout=True)
        if os.path.isfile(loc_file):
            print("File has been downloaded. Don't forget to change Terminal font!")
        else:
            print("File was not downloaded. Please manually download from https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf")

def install_plvl():
    cmd = f'brew install romkatv/powerlevel10k/powerlevel10k && echo "source $(brew --prefix)/opt/powerlevel10k/powerlevel10k.zsh-theme" >>~/.zshrc'
    subprocess.run(cmd, shell=True, stdout=True)

def check_plvl():
    print("Checking if powerlevel10k is installed: https://github.com/romkatv/powerlevel10k")
    powlevel = subprocess.call(['brew list | grep powerlevel10k'], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    if powlevel != 0:
        print("Not installed. Installing p10k.")
        install_plvl()
    else:
        print("Powerlevel10k is installed.")

def install_lsd():
    cmd = f'brew install lsd'
    subprocess.run(cmd, shell=True, stdout=True)

def check_lsd():
    print("Checking if lsd is installed: https://github.com/Peltoche/lsd")
    if shutil.which('lsd') is None:
        print("Not installed. Installing lsd.")
        install_lsd()
    else:
        print("lsd is installed.")

def check_shell():
    print("Checking shell environment")
    shell = os.environ['SHELL']
    if shell == def_zsh:
        print(f"Shell is {def_zsh}. Right on!")
    else:
        print(f"Shell is not {def_zsh}. Updating shell.")
        cmd = f'chsh -s {def_zsh}' 
        subprocess.run(cmd, shell=True, stdout=True)

# Source .zshrc to apply updates
def source_zsh():
    cmd = f'source {zshrc} >& /dev/null'
    subprocess.run(cmd, shell=True)

def check_vimrc():
    print(f"Searching for {vimrc}")
    if os.path.isfile(vimrc):
        print(f"{vimrc} exists. Checking config.")
        check_vimrc = "set number"
        with open(f"{vimrc}", "r+") as file:
            file.seek(0)
            lines = file.read()
            if check_vimrc in lines:
                print("Config already exists in file.")
            else:
                print("Config does not exist in file. Appending file.")
                file.write(f"{vim_text}")
    else:
        print(f"{vimrc} does not exist. Creating file.")
        with open(vimrc, "a") as file:
            file.write(f"{vim_text}")
    # To doublecheck if file is there
    if os.path.isfile(vimrc):
        print("woohoo!")
    else:
        print(f"could not create {vimrc}")

def install_rec():
    print("Checking to see if Rectangle is installed: https://rectangleapp.com/")
    if os.path.isdir(rec):
        print("Rectangle is installed!")
    else:
        down_rec = "https://github.com/rxhanson/Rectangle/releases/download/v0.56/Rectangle0.56.dmg"
        print("Rectangle not installed. Installing now.")
        cmds = [ 
            f"curl -L {down_rec} -o {loc_rec}", 
            f"sudo hdiutil attach {loc_rec} && cd {vol_rec}",
            f"sudo cp -R {vol_rec}/Rectangle.app /Applications",
            f"sudo hdiutil unmount {vol_rec}"
        ]
        for i in cmds:
            subprocess.run(i, shell=True, stdout=True)
        if os.path.isdir(rec):
            print("Successfully installed Rectangle!")
        else:
            print("Unable to install. Please check Downloads for file.")

def install_code():
    print("Checking if VS Code is installed: https://code.visualstudio.com/Download")
    if os.path.isdir(code):
        print("VS Code is installed!")
    else:
        down_code = "https://code.visualstudio.com/sha/download\?build\=stable\&os\=darwin-universal"
        print("VS Code is not installed. Installing now.")
        cmds = [ 
            f"curl -L {down_code} -o {loc_code}",
            f"unzip {loc_code} -d {HOME}/Downloads/",
            f"sudo mv {HOME}/Downloads/Visual\ Studio\ Code.app /Applications"
        ]   
        for i in cmds:
            subprocess.run(i, shell=True, stdout=True)
        if os.path.isdir(code):
            print("Successfully installed VS Code!")
        else: 
            print("Unable to install VS Code. Please check Downloads for file.")

def main():
    print("Setting up laptop with your configs!")
    create_zsh()
    check_homebrew()
    check_plvl()
    check_lsd()
    check_shell()
    source_zsh()
    check_fonts()
    check_vimrc()
    install_rec()
    install_code()
    print("Setup complete! Please open new terminal. Goodbye! :)")

if __name__ == "__main__":
    main()
