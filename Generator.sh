#!/bin/bash

# To be used with python script 
# $1 Ninja first name
# $2 Ninja last name
# $3 Index ninja info is stored in array
# The output certificate will be called <ninjaArrayIndex>.pdf, this allows for easy validation 

# Python script will create then delete tmp folder
cp Template.tex "tmp/"
cd tmp

newFileName="$3.tex"
mv Template.tex  $newFileName

newString="$1 $2"

#Reduce font size if name is greater than 20 characters long
if [ ${#newString} -ge 20 ]; then 
    sed -i -e "s/{60}{70}/{40}{50}/g" $newFileName
fi

sed -i -e "s/InsertName/$newString/g" $newFileName
#need to compile twice for some reason fucking latex
lualatex $newFileName
lualatex $newFileName

newFileName="$3.pdf"
mv "$newFileName" "../Certs/"
cd ..

