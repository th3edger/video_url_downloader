#!/bin/bash
#Programa que sirve para descargar de manera automatica los videos de las listas .txt
#Autor: Edgar Alberto Pérez


if [ -d videos/ ]
then
    echo "Ya existe una carptea contenedora"
else
    mkdir -m 755 videos/
    echo "Se creo la carpeta que contendra los archivos"
fi

echo ""
echo "se procedera a descargar los videos en su respectiva carpeta"
echo ""

for arch_txt in $(ls *.txt)
do
    nom_carp=$(echo "$arch_txt" |  awk -F .txt '{print $1}')

    if [ -d ./videos/$nom_carp ]
    then
        echo "Ya existe una carpeta para $nom_carp"
    else
        echo "Se creo una carpeta para $nom_carp"
        mkdir -m 755 ./videos/$nom_carp
    fi

    wget -tries=5 -P ./videos/$nom_carp/ -i $arch_txt

done
