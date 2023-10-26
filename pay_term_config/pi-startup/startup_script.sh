#!/bin/bash

source /home/vitor/pay_term_config/venv/bin/activate

STARTUP_VARIABLES_FILE="/home/vitor/pay_term_config/pi-startup/startup_variables.txt"
PAY_VARIABLES_FILE="/home/vitor/pay_term_config/pay.txt"

write_var() {
    echo "MODE=$MODE" > "$STARTUP_VARIABLES_FILE"
    echo "NEXT_MODE=$NEXT_MODE" >> "$STARTUP_VARIABLES_FILE"
}

read_var() {
    if [ -e "$STARTUP_VARIABLES_FILE" ]; then
        source "$STARTUP_VARIABLES_FILE"
    fi
}

read_var

echo "mode: $MODE nextmode: $NEXT_MODE"

# Check MODE
if [ "$MODE" = "config" ]; then
    echo "Running in $MODE mode"
    MODE=""
    NEXT_MODE="term"
    write_var
    ./home/vitor/pay_term_config/pi-startup/config_script.sh
    sudo reboot
elif [ "$MODE" = "term" ]; then
    echo "Running in $MODE mode"
    MODE=""
    NEXT_MODE="config"
    write_var
    ./home/vitor/pay_term_config/pi-startup/term_script.sh
    sudo reboot
else
    echo "Next mode $NEXT_MODE"
    MODE=$NEXT_MODE
    write_var
    if [ "$NEXT_MODE" = "term" ]; then
        # Run config app
        echo "Run config app"
        python3 /home/vitor/pay_term_config/app_config.py
    else
        # Run term app
        echo "Run term app"
        python3 /home/vitor/pay_term_config/pi-rfid/read.py
    fi
fi


