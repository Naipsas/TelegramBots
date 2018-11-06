#!/bin/bash
# Naipsas - Btc Sources
# This script takes a bot, replaces the token string it has in GitHub, puts
# instead the actual token from ./TelegramBots/PrivateData and copies it to
# tmp folder, where it's launched.

# FUNCTIONS
function menu {

  echo "#####################"
  echo "####             ####"
  echo "# 1.- Install API   #"
  echo "# 2.- Deploy bot    #"
  echo "# 3.- Exit          #"
  echo "####             ####"
  echo "#####################"

  echo ""
  echo -n "Select an option: "
  read Option

  case $Option in
    1 )
      InstallAPI
      ;;
    2 )
      DeployBot
      ;;
    3 )
      clear
      exit
      ;;
    * )
      # Non valid option
      menu
      ;;

  esac

}

function backtoMenu()
{

  echo ""
	echo -n "Do you want to return to the menu? (Y/N) : "
  read Option

  if [ "$Option" = "Y" ] || [ "$Option" = "y" ]; then
    menu
  else
    exit
  fi

}

function InstallAPI()
{

  clear
  echo "Getting ready to install Telegram-Bot-API (Python)..."

  sudo -H pip install python-telegram-bot --upgrade -y > /dev/null
  if [ "$?" -eq "0" ]; then
    echo -e "\tAPI installed!"
  else
    echo -e "\tWe couldn't install the API!"
  fi

  backtoMenu

}

function DeployBot()
{

  clear
  echo "Deploy bot selected! Let's see how many are available:"
  #ls -d */
  for f in *; do
    if [[ -d $f  ]]; then
      echo -e "\t$f";
    fi;
  done

  echo -n "Introduce the name of the desired bot: "
  read Bot

  LaunchBot $Bot

  backtoMenu

}

function LaunchBot()
{

  clear
  echo "Starting Bot $1..."

  sudo cp -r "./$1" "/tmp/$1"

  # Token extraction
  line=$(grep $1 ./PrivateData)
  read -ra splited <<< "$line"
  actualToken=${splitted[1]}
  sed -i -e "s/BotFather_provided_token/$actualToken/g" "/tmp/$1/$1.py"

  python "/tmp/$1/$1.py"

  backtoMenu

}

#source ./Deploy_vars
menu