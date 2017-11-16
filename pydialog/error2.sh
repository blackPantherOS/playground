#!/bin/sh


PARTINATOR="kialasztottvalami TEXT_TEXT_TEXT false"
xmsg=kdialog
echo "Start Kdialog - Path $(which $xmsg)"
#ret=$($xmsg --title "System Admin" --yesno "<img src=/usr/share/icons/blackPanther-dark.png><br><big>blackPanther OS</big>")
$xmsg --title "System Admin" --yesnocancel "<img src=/usr/share/icons/blackPanther-dark.png><br><big>blackPanther OS</big>"
ret=$?
#ret=`$xmsg --title "$(gettext 'System Admin')" --radiolist "<img src=/usr/share/icons/blackPanther-dark.png><br><big>blackPanther OS</big><br>$(gettext 'Possible Managing System Partitions with.. <br>[please select]')" ${PARTINATOR}`
echo "Select:$ret"

xmsg=$PWD/pydialog
echo "Start PYdialog - Path: $xmsg"
$xmsg --title "System Admin" --yesnocancel "<img src=/usr/share/icons/blackPanther-dark.png><br><big>blackPanther OS</big>"
ret=$?
#ret=`$xmsg --title "$(gettext 'System Admin')" --radiolist "<img src=/usr/share/icons/blackPanther-dark.png><br><big>blackPanther OS</big><br>$(gettext 'Possible Managing System Partitions with.. <br>[please select]')" ${PARTINATOR}`
echo "Select:$ret"

