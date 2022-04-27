http="http://"

while read line; do
	echo "$line"
	url="${http}${line}"
	echo "$url"
	timeout 15 google-chrome "${url}"
	pkill chrome
	rm -rf ~/.cache/google-chrome
	systemd-resolve --flush-caches #flushdnscache
	#ping the above site five times and get average RTT
	x=1
	declare -a lines
	while [ $x -le 5 ]
	do
  		ping -c 1 "$line" 2>&1 | awk -F'/' 'END{ print (/^rtt/? ""$5"":"FAIL") }' >> ping.txt
  		x=$(( $x + 1 ))
	done

	IFS=$'\n' read -d '' -r -a lines < ping.txt
	sum=$( IFS="+"; bc <<< "${lines[*]}" )
	temp=$(echo "$sum / 5" | bc -l )
	echo $temp >> avgping.txt #write avg ping for the site to a new file
	> ping.txt #clear file contents
done < topsites50.txt