http="http://"

while read line; do
	url = "$http$line"
	google-chrome --no-sandbox "$url"
	sleep 8
	killall google-chrome
	sudo rm -rf ~/.cache/google-chrome
	sudo systemd-resolve --flush-caches #flushdnscache
	#ping the above site five times and get average RTT
	x=1
	declare -a lines
	while [ $x -le 5 ]
	do
  		ping -c 1 $line 2>&1 | awk -F'/' 'END{ print (/^rtt/? ""$5"":"FAIL") }' >> ping.txt
  		x=$(( $x + 1 ))
	done

	IFS=$'\n' read -d '' -r -a lines < /home/ubuntu/ping.txt
	sum=$( IFS="+"; bc <<< "${lines[*]}" )
	temp=$(echo "$sum / 5" | bc -l )
	echo $temp >> avgping.txt #write avg ping for the site to a new file
	> ping.txt #clear file contents
done < topsites50.txt