#!/bin/bash

if [[ "$1" =~ ^(-h|--help)$ ]]
then
    echo "Usage:"
    echo "\$ cd <directory you want to backup>"
    echo "\$ backup.sh"
    echo "Follow instructions on the screen"
    exit 0
fi

[[ "$1" =~ ^(-y|--yes|--dont-ask|no-ask)$ ]] && dontask=true

source=`pwd`/

red=$'\e[1m\e[31m'
green=$'\e[1m\e[32m'
reset=$'\e[0m'

rsync_opts="-a --groupmap=*:users --chmod=Dg+rwxs,g+rw,o-w --info=progress2 --stats"
rsync_opts+=" --exclude=_OUT_ --exclude=lost+found --exclude=.Trash* --exclude=tytan-backup --exclude=kolos-backup --exclude=tmp --exclude=temp --exclude=.git"
#rsync_opts+=" --dry-run"
#rsync_opts+=" --delete"

function monitor-start {
    monitor.py working Backup $source 24h
}

function monitor-error {
    monitor.py error Backup $source 24h
}

function monitor-finished {
    monitor.py finished Backup $source 24h
}

function kill-jobs {
    trap 'echo KILLING JOBS... && kill $(jobs -p)' SIGINT SIGTERM
}

function backup {
	source="$1"
	target="$2"
	echo "$green======== ======== ======== BACKUP ======== ======== ======== "
	#     Zrodlo:                      /tytan/raid/x
	#     Cel:    /kolos/storage/tytan-backup/raid/x
	echo "${green}Zrodlo:$reset                      $source"
	echo "${green}Cel:$reset    $target"
	if [[ "$dontask" == "true" ]] ; then
		echo "${green}Wykonuje backup...$reset"
	else
		read -p "${green}Czy chcesz umiescic backup w oddzielnym katalogu [t/N]?$reset " yn
		if [[ "$yn" =~ ^[YyTt] ]] ; then
    	    now=`date +"%Y%m%d"`
		    target=${target::-1}_$now/
        	echo "${green}Cel:$reset    $target"
		fi
#		read -p "${green}Czy chcesz usunac pliki z poprzedniego backupu (tryb 'mirror') [t/n]?$reset " yn
#		if [[ "$yn" =~ ^[YyTt] ]] ; then
#		    echo "${red}UWAGA! Usuwam stary backup!!!$reset"
            #rsync_opts+=" --delete"
#		fi
		read -p "${green}Czy na pewno chcesz zrobic backup [t/n]?$reset " yn
		[[ "$yn" =~ ^[YyTt] ]] || exit 2
	fi
	mkdir -p "$target"
	if [ $? -ne 0 ]; then
		echo "${red}Nie mozna utworzyc katalogu docelowego:$reset $target"
		monitor-error
		exit 1
	fi
	monitor-start
	ionice -c 3 rsync $rsync_opts "$source" "$target"
	if [ $? -eq 0 ]; then
		echo "${green}Backup OK.$reset"
		echo "`date`    $source    ->   $target" >> /kolos/m2/home/backup.log
	    monitor-finished
	else
		echo "${red}Cos poszlo nie tak.$reset"
		monitor-error
		exit 1
	fi
}

if [[ "$source" =~ ^/(kolos|tytan)/storage/(kolos|tytan)-backup/.*$ ]]; then
	echo "${red}Nie mozna zrobic backupu z backupu!$reset"
	exit 1

elif [[ "$source" =~ ^/(kolos|tytan)/(.+/)?_OUT_/.*$ ]]; then
	echo "${red}Nie mozna zrobic backupu katalogu _OUT_!$reset"
	exit 1

#elif [[ "$source" =~ ^/(kolos|tytan)/storage/$ ]]; then
#	echo "${red}Nie mozna zrobic backupu calego storage!$reset"
#	exit 1

elif [[ "$source" =~ ^/kolos/(m2|ssd|storage)/.*$ ]]; then
	# /kolos/XXX/... -> /tytan/storage/kolos-backup/XXX/...
	target=${source/kolos/tytan\/storage\/kolos-backup}
	backup "$source" "$target"

elif [[ "$source" =~ ^/tytan/(raid|storage)/.*$ ]]; then
	# /tytan/XXX/... -> /kolos/storage/tytan-backup/XXX/...
	target=${source/tytan/kolos\/storage\/tytan-backup}
	backup "$source" "$target"

else
	echo "${red}Nie potrafie zrobic backupu tego katalogu:$reset $source"
	exit 1
fi


