#!/usr/bin/env bash

vtc() {
    grep -Po "(?<=$1\": )\d+"
}


sourcefile=$1
destFile=$2
echo -e "\n\n\n\n>>>>>>>>>>>>>>>> Starting generate CSV file from $sourcefile to $destFile <<<<<<<<<\n\n\n\n"

if [[ -z $destFile ]]; then
    read -p "Enter name of CSV file to generate: " destFile
    truncate --size 0 $destFile
fi

h="harmless"
tu="type-unsupported"
s="suspicious"
ct="confirmed-timeout"
t="timeout"
f="failure"
m="malicious"
u="undetected"

echo "/,file,size,$h,$tu,$s,$m,$u" > $destFile

rptFiles=$(cat $sourcefile)

total=$(wc -l $sourcefile | grep -Po "^\d+")
count=1
for f in $rptFiles; do 
    echo
    echo "starting ($count/$total): $f"
    fsize=$(grep -Po "(?<=\"size\": )\d+" $f -m 1)
    if [[ $? -ne 0 ]]; then
        echo -e "error extracting file size from $f \nbraking from loop" >&2
        break
    fi
    statLine=$(grep last_analysis_stats -n $f | grep -Po "^\d+")
    if [[ $? -ne 0 ]]; then
        echo "error, braking from loop" >&2
        break
    fi
    echo $statLine
    stats=$(tail -n +$statLine $f | head -n 10)
    if [[ $? -ne 0 ]]; then
        echo "error, braking from loop" >&2
        break
    fi
    file=$(echo $f | grep -Po "(?<=/)[^/]+$")
    line="$count,$file,$fsize,$(echo $stats | vtc $h),$(echo $stats | vtc $tu),$(echo $stats | vtc $s),$(echo $stats | vtc $m),$(echo $stats | vtc $u)"
    echo "$line" >> $destFile
    echo "$line"



    echo $stats

    echo "finished ($count/$total): $f"
    echo
    count=$((1+$count))
done

echo -e "\n\n\n\n<<<<<<<<<<<<<<<< Done generate CSV file from $file to $destFile >>>>>>>>>>>>>>>\n"