#!/bin/sh

#*********************************************************************************************************
#*   __     __               __     ______                __   __                      _______ _______   *
#*  |  |--.|  |.---.-..----.|  |--.|   __ \.---.-..-----.|  |_|  |--..-----..----.    |       |     __|  *
#*  |  _  ||  ||  _  ||  __||    < |    __/|  _  ||     ||   _|     ||  -__||   _|    |   -   |__     |  *
#*  |_____||__||___._||____||__|__||___|   |___._||__|__||____|__|__||_____||__|      |_______|_______|  *
#* http://www.blackpantheros.eu | http://www.blackpanther.hu - kbarcza[]blackpanther.hu * Charles Barcza *
#*************************************************************************************(c)2002-2016********
 . /etc/blackPanther-default-apps.conf
# Different style:
# landscape format

name=$1
format=$2
name2=$3
landscape=0
redline=1

if [ "$format" != "png" ]&&[ "$format" != "svg" ];then
 # print help if not entered format
 name=""
fi

if [ "x$name" = "x" ];then
  echo -e "$GRN
  Missing paramter as rpm name. Run script with parameter ! 
    $YEL Example:$MAG $basename $0 install$GRN  (for install dependency)
  And for generate RPM-Map

Description: | generator name|appliaction|map format |map name |
$YEL    Example:$MAG $basename $0 gimp svg$GRN
  OR
$YEL    Example:$MAG $basename $0 full $GRN/for full system mapping/
  OR 
$YEL    Example:$MAG $basename $0 gimp svg Different_SCREENSHOTNAME$GRN
$DEF"
  exit

fi

if [ "$name" = "install" ];then
  installing perl graphviz rpmorphan
  echo -e "$GRN
  Okay! $CYN
  Now run script simple! Example: $basename $0 gimp
  $DEF"
  exit
fi


[ "x$name" = "x" ]&&echo -e "$RED => Missing packname! Example: $basename $0 gimp$DEF" && exit

gendot () {
if [ -n "$(rpm -q --quiet $name || echo 1)" ];then
    echo -e "$RED => The $name package is missing! Wrong name or not installed package...$DEF"
    exit
fi
echo -e "$CYN => Run:$MAG rpmdep -dot $name.dot $name "
echo -e "$CYN => Listing$YEL $name$MAG package dependencies:$BLU"
rpmdep -dot $name.dot $name 2>/dev/null
ret=$?
[ "$ret" = "1" ]&& echo -e "$RED ERROR 1$DEF" && exit
[ ! -n "$name" ]&& echo -e "$RED ERROR 2$DEF" && exit
[ ! -n "$name2" ]&& name2=$name
}

systemmap () {
name=Out
rpm --queryformat '%{NAME} \n' -qa | sort > pack_names.tmp 
cat pack_names.tmp | while read FILE; do $basename $0 $FILE 2>/dev/null ; done
}

gensysmap () {
awk '{if (!a[$0]++) print}' *.dot > ${name}.tmp
mv -f ${name}.tmp ${name}.dot

#perl -pi -e 's|;| [color=red,penwidth=1.0];|' ${name}.dot
perl -pi -e 's|;| minlen=30; splines=line; overlap = false; rankdir=LR ; nodesep=0.1; margin=0;|' ${name}.dot 2>/dev/null

genpng
rm -rf *.tmp
rm -rf *.dot
}
coloring () {
echo -e "$CYN => Run:$MAG Coloring $name.dot $DEF"
# Red line
if [ "$redline" = "1" ];then
perl -pi -e 's|;| [color=red,penwidth=1.0];|g' $name.dot
fi
# Gren conainer
if [ "$landscape" != "1" ];then
perl -pi -e 's|digraph "rpmdep" {|digraph "rpmdep" {
node [width = 0.95, fixedsize = false, style = filled, fillcolor = palegreen];|g' $name.dot 2>/dev/null
else
perl -pi -e 's|digraph "rpmdep" {|digraph "rpmdep" {
minlen=30; splines=line; overlap = false; rankdir=LR ; nodesep=0.1; margin=0;
node [fontname=Helvetica; fontsize=9; height=0.1; color=lightgray; style=filled; shape=record];|g' $name.dot 2>/dev/null
fi
genpng
}

genpng () {
if [ "$format" = "svg" ];then
    echo -e "$CYN => Run:$MAG dot -Tsvg $name.dot -o $name2.svg"
    dot -Tsvg $name.dot -o $name2.svg 2>/dev/null
elif [ $format = png ];then
    echo -e "$CYN => Run:$MAG dot -Tpng $name.dot -o $name2.png"
    dot -Tpng $name.dot -o $name2.png 2>/dev/null
else
    echo -e "$YEL - First package name: $1 Second: $2 Third ADD: svg or png forma ?????"
fi
}

if [ "$name" = "full" ];then
echo -e "$GRN => Generating full system MAP"
    systemmap
    gensysmap
    exit

fi

[ ! -x "$(which rpmdep 2>/dev/null)" ]&& echo "Please run >$(basename $0) install< first because rpmorphan package is missing !" && exit 
[ ! -x "$(which dot 2>/dev/null)" ]&& echo "Please run >$(basename $0) install< first because graphviz package is missing!" && exit 
[ ! -x "$(which perl 2>/dev/null)" ]&& echo "Please run >$(basename $0) install< first because perl package is missing!" && exit 
gendot
coloring
echo -e "$GRN => Generating finished."

#finish
