http="http://"

while read line; do
	url = "$http$line"
	google-chrome --no-sandbox "$url"
	sleep 8
	killall google-chrome
	sudo rm -rf ~/.cache/google-chrome
done < topsites50.txt