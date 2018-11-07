#usage:	read user input then judge yes or no

#in the case option, "" is for the default
read -p "do you want to install xxx in xxx?(default is yes)"

case "$REPLY" in
	[Yy]es | [Yy] | "" )
		echo "your choice is yes"
		#do something
		;;
	[Nn]o | [Nn])
		echo "your choice is no"
		#do something
		;;
	*)
		echo "this is default option"
		#do something
esac
