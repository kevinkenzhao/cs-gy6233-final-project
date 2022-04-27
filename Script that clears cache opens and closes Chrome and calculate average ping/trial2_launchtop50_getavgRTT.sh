http="http://"
rm -rf ~/.cache/google-chrome
systemd-resolve --flush-caches
while read line || [[ -n $line ]]; do
	echo "$line"
	url="${http}${line}"
	echo "$url"
	timeout 15 google-chrome --no-sandbox "${url}"
	pkill chrome
	rm -rf ~/.cache/google-chrome
	systemd-resolve --flush-caches #flushdnscache
	#ping the above site twenty five times and get average RTT
	x=1
	declare -a lines
	a=$line
	pings=$(echo $a | sed -e 's/\n//g')
	while [ $x -le 25 ]
	do
  		ping -c 1 $line 2>&1 | awk -F'/' 'END{ print (/^rtt/? ""$5"":"FAIL") }' >> "$pings.txt"
		#systemd-resolve --flush-caches
  		x=$(( $x + 1 ))
	done
	IFS=$'\n' read -d '' -r -a lines < "$pings.txt"
	sum=$( IFS="+"; bc <<< "${lines[*]}" )
	temp=$(echo "$sum / 25" | bc -l )
	echo $temp >> avgping.txt #write avg ping for the site to a new file
	#> "$pings.txt"  #clear file contents
done < topsites50.txt
