#nie ustawiamy 'shebang line', zeby mozna bylo uzyc tego w roznych shellach

# helpery
function add_dir {
    export PATH=$PATH:$1
	export PYTHONPATH=$PYTHONPATH:$1
}
[ -z "$REPOS" ] && export REPOS=$HOME/repos
[ -z "$SCRIPTS" ] && export REPOS=$HOME/repos/vision-tools/vision/scripts

# ALIASY DO NASZYCH SKRYPTOW

alias backup=$SCRIPTS/backup.sh
alias monitor=$SCRIPTS/monitor.py
alias smi="watch nvidia-smi"
alias vctl="v4l2-ctl"
alias monitor-resources="$REPOS/vision-tools/vision/monitor/monitor_resources.py"
alias iotop="sudo iotop"

# CALE KATALOGI

add_dir $REPOS/vision-tools/vision/scripts
add_dir $REPOS/ocr/ocr/data
add_dir $REPOS/tfmodels/research
add_dir $REPOS/tfmodels/research/slim


