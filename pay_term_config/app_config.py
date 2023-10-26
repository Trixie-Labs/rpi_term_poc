from flask import Flask, request, render_template
import re

app = Flask(__name__)

# File to store settings
#settings_config_file = "/home/vitor/pay_term_config/settings.txt"
settings_config_file = "settings.txt"
#pay_config_file = "/home/vitor/pay_term_config/pay.txt"
pay_config_file = "pay.txt"

def read_pay():
    try:
        with open(pay_config_file, "r") as file:
            return file.read()
    except FileNotFoundError:
        return ""

def update_pay_variable(variable_name, new_value):
    # Update the .env file with the new value
    with open(pay_config_file, 'r') as env_file:
        lines = env_file.readlines()

    updated_lines = []
    updated = False

    for line in lines:
        if line.startswith(variable_name):
            updated_lines.append(f'{variable_name}={new_value}\n')
            updated = True
        else:
            updated_lines.append(line)

    if not updated:
        updated_lines.append(f'{variable_name}={new_value}\n')

    with open(pay_config_file, 'w') as env_file:
        env_file.writelines(updated_lines)

    print(f'{variable_name} has been updated to: {new_value}')


def read_settings():
    try:
        with open(settings_config_file, "r") as file:
            return file.read()
    except FileNotFoundError:
        return ""

def write_settings_config(settings):
    with open(settings_config_file, "w") as file:
        file.write(settings)

@app.route('/')
def config_page():
    current_settings = read_settings()
    ssid=re.search(r'ssid="([^"]+)"', current_settings).group(1)
    psk=re.search(r'psk="([^"]+)"', current_settings).group(1)
    current_pay = read_pay()
    contractAdress=re.search(r'CONTRACT_ADDRESS=(\w+)', current_pay).group(1)
    termAddress=re.search(r'TERM_ADDRESS=(\w+)', current_pay).group(1)
    return render_template('config.html', ssid=ssid, psk=psk, contractAdress=contractAdress, termAddress=termAddress)

@app.route('/update_settings_config', methods=['POST'])
def update_settings_config():
    wifiName = request.form.get('wifiName')
    wifiPass = request.form.get('wifiPass')

    network_config = f"""network={{
    ssid="{wifiName}"
    psk="{wifiPass}"
    key_mgmt=WPA-PSK
}}
"""

    write_settings_config(network_config)
    return "Configuration Updated"

@app.route('/update_pay_config', methods=['POST'])
def update_pay_config():
    eventContractAddress = request.form.get('eventContractAddress')
    termAddress = request.form.get('termAddress')

    update_pay_variable("CONTRACT_ADDRESS", eventContractAddress)
    update_pay_variable("TERM_ADDRESS", termAddress)

    return "Configuration Updated"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
    #app.run(host='192.168.4.1', port=5000)
    #Move to config file
