source embed.sh
timeFrom() {
    now=$2
    if [[ -z $now ]]; then
        now=$(date +%s)
    fi
    date -ud @$(($now - $1)) +%H:%M:%S
}


applyCloak() {
    substart=$SECONDS
    echo "started apply cloak :: $(timeFrom $substart $SECONDS)"
    msk=masked_dir
    par=cloaked_dir
    if [[ -d $par ]]; then
        rm -r $par
    fi
    total=$(ls masked_dir/*/* | grep "nibmask" | wc -l)
    count=0
    mkdir $par
    for dd in $msk/*; do
        d=$(grep -Po "[^/]+$" <(echo $dd))
        mkdir "$par/$d"
        for ff in $msk/$d/*.nibmask; do
            echo "cloaking file: $ff :: $(timeFrom $substart $SECONDS)"
            embed $ff
            f=$(grep -Po "[^/]+$" <(echo $ff))
            mv $ff".cloaked.exe" "$par/$d/$f"".cloaked.exe"
	    count=$(($count+1))
	    echo "cloaked file($count/$total): $par/$d/$f"".cloaked.exe :: $(timeFrom $substart $SECONDS)"
        done
    done
}

applyMask() {
	substart=$SECONDS
	echo "starting apply mask $(date) :: $(timeFrom $substart $SECONDS)"
	basename="[^/]+$"
	source_files=$(ls orig_exes/*.exe)
	prob_files=$(ls active_probs/*.pnp)
	msk_dir=masked_dir
	if [[ -d $msk_dir ]]; then
		rm -r $msk_dir
	fi
	mkdir $msk_dir
	for pp in active_probs/*; do
		mkdir "$msk_dir"/"$(echo $pp | grep -Po $basename)"
	done
	total=$(( $(echo "$source_files" | wc -l) * $(echo "$prob_files" | wc -l)))
	count=0
	mkfifo pipe-$$
	exec 3<>pipe-$$
	rm pipe-$$
	for i in {1..5};{ echo "xxx" >&3; }
	for ee in $source_files; do
		e=$(echo $ee | grep -Po "[^/]+$")
		for pp in $prob_files; do
			read -u 3 line
			(p=$(echo $pp | grep -Po "[^/]+$")
			echo "applying mask($count/$total): $p -> $e :: $(timeFrom $substart $SECONDS)"
			msk_fil=$(python3 applyMask.py "$ee" "$pp")
			if [[ $? -ne 0 ]]; then 
				echo "failed($count/$total): $p -> $e :: $(timeFrom $substart $SECONDS)"; 
				exit [2]; 
			fi
			new_msk_fil="$msk_dir"/"$p"/$(grep -Po "[^/]+$" <(echo $msk_fil))
			mv $msk_fil $new_msk_fil
			echo "applied mask($count/$total): $new_msk_fil :: $(timeFrom $substart $SECONDS)"
			echo "xxx" >&3) &
			count=$(($count+1))
		done
	done
	wait
}


cloakFromActiveProbs() {
    startsec=$(date +%s)
    echo "> Starting at $(date -d @$startsec)  $startsec"
    echo "> Starting Cloak From Active Probabalities :: $(timeFrom $startsec)"
    echo "  > Starting maskApply.py :: $(timeFrom $startsec)"
    python3 maskApply.py
    echo "  > Finished maskApply.py :: $(timeFrom $startsec)"
    echo "  > Starting applyCloak :: $(timeFrom $startsec)"
    applyCloak
    echo "  > Finished applyCloak :: $(timeFrom $startsec)"
    echo "> Finished Cloak From Active Probabalities :: $(timeFrom $startsec)"
}
