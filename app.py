from flask import Flask, json, render_template, request
from rgb import RGB
from config import config
import datetime, re

app = Flask(__name__)
light = RGB(18, 23, 24)

value = 'initial value'

@app.route("/")
def hello():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'HELLO',
        'time'  : timeString
        }
    return render_template('main.html', **templateData)

@app.route("/set",methods=['POST'])
def set_values():
    try:
        response = request.get_json()
        if response['token'] != config['user-token']:
            return 'Invalid user token'
        else:
            print(response['value'])
            msg = runCmd(response['value'])
        return msg
    except Exception:
        return 'an error occurred'

def runCmd(command):
    command = command.lower().split(' ')
    if command[0] in commands:
        status = commands[command[0]]()
    elif command[0] == 'rgb' and len(command) == 4:
        status = light.setColor(command[1:])
    else:
        status = light.setColor(command[0])
    print(status)
    return status+'\n'

def showHelp():
    return 'Commands are "HELP"; "STATUS"; "STOP", or a color name as either\
 "RGB 255 255 255"; "#09fFfF"; or a CSS color keyword, "white".'

def stopLED():
    light.stop()
    return 'stopped'

def showStatus():
    return 'status page'

def showAbout():
    return 'http://github.com/begillespie/pilight'

commands = {
        'help':showHelp,
        'stop':stopLED,
        'status':showStatus,
        'about':showAbout
        }

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

