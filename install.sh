#!/bin/sh

#pio platform uninstall cs-microapps
#pio platform install https://github.com/mPlagge/platform-crownstone-microapps.git
#pio platform install .

rm -rf ~/.platformio/platforms/cs-microapps
mkdir ~/.platformio/platforms/cs-microapps
cp -r . ~/.platformio/platforms/cs-microapps
rm ~/.platformio/platforms/cs-microapps/install.sh
