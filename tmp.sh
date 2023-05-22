tst() {
	i=1
	mkfifo pipe-$$
	exec 3<>pipe-$$
	rm pipe-$$
	for j in {1..3};{ echo "xxx" >&3 ;}
	while [[ $i -le 10 ]]; do
		read -u 3 line 
		(echo "$i enters"
		sleep $i
		echo "$i exits" 
		echo "xxx" >&3 )&
		i=$(($i+1))
	done
	wait
}
tst2() {
	i=0
	for id in $(cat $1 | head); do
		echo $i
		if [[ $(($i%2)) = 0 ]]; then
			f=$id
			echo "set f=$id for $(($i%2))"
		else
			echo "$f $id"
		fi
		i=$(($i+1))
	done
}

