upload() {
	curl --request POST \
	     --url https://www.virustotal.com/api/v3/files \
	     --header 'accept: application/json' \
	     --header 'content-type: multipart/form-data' \
	     --header 'x-apikey: 6f6e2614ff76622e955450f99af7676229f6740b7810d54e6334a9317fe71e09' \
	     --form file=@"$1"
	wait $!
}

getReport() {
	curl --request GET \
	  --url https://www.virustotal.com/api/v3/files/{$1} \
	  --header 'x-apikey: 6f6e2614ff76622e955450f99af7676229f6740b7810d54e6334a9317fe71e09' 
	wait
}

getCloakReports() {
	inFile="$1"
	outDir="$2"
	entries=$(sort "$inFile" | uniq -u)
	total=$(sort "$inFile" | uniq | wc -l)
	count=$(sort "$inFile" | uniq -d | wc -l)
    subtotal=$(echo $entries | wc --words)
	if [[ ! -d "$outDir" ]]; then
		mkdir "$outDir"
        echo "created dir: $outDir"
	fi
	echo "starting from ($count/$total) getting ($subtotal) reports"
	for entry in $(echo "$entries"); do
		file=$(echo $entry | grep -Po "^.+(?=:)")
		path=$(echo $entry | grep -Po "(?<=:).+$")
        sum=$(sha256sum $path)
		count=$(($count+1))
		echo "reteriving file ($count/$total): $outDir/$file.rpt"
        #echo "             sha256 sum        : {$sum}"
        (getReport $sum) 1> "$outDir"/"$file".rpt
		grep last_analysis_stats "$outDir"/"$file".rpt > /dev/null
        if [[ $? -ne 0 ]]; then
            echo "error in report for: $file" >&2
            exit 2
        fi
		echo "reterived file ($count/$total): $outDir/$file.rpt"
        echo "$entry" >> "$inFile"
	done
	echo "done"
}

uploadCloaks() {
	toUpload=$(sort virusTotal/toUploadUniq.txt | uniq -u)
	total=$(wc -l <(echo $toUpload))
	count=$(($(sort virusTotal/toUploadUniq.txt | uniq -d | wc -l)+1))
	counti=$count
	for ff in $(echo $toUpload); do
		(f=$(echo $ff | grep -Po "(?<=/)[\w.]+$")
		upload $ff 1> virusTotal/uploadResponses/$f.out 2>virusTotal/uploadResponses/$f.err
		echo $ff >> virusTotal/toUploadUniq.txt
		echo "uploaded ($count/$total): $f")
		count=$(($count+1))
	done
	echo "done uploading $(($counti-$count)) files"

}
