# Stream Deck Scripts

## Intro:

Helper scripts to use the [StreamDeck](https://www.elgato.com/en/stream-deck) by Elgato for executing custom scripts on macOS or Windows based systems.

Current usage is to create or launch an EC2 instance at the hit of a button.

### Usage:

usage outside of Streamdeck (for testing): instance.py [-h] [-v] [-c COMMAND] [-i INSTANCEID] [-l LAUNCHTEMPLATE] [-s] [-u USERID]

### Options:

    -s, --ssh                                           Launch and open new SSH session
    -h, --help                                          Show this help message and exit
    -v, --verbose                                       Verbose
    -u USERID, --userID USERID                          Username to SSH as
    -c COMMAND, --command COMMAND                       Command to run against ec2
    -i INSTANCEID, --instanceID INSTANCEID              Instance ID
    -l LAUNCHTEMPLATE, --launchTemplate LAUNCHTEMPLATE  Create new instance based off of a Launch Template


### Setup:

In the stream deck UI, place a button with the 'Open' Plugin. for the 'App / File' field, enter (for creating a new instance based off a launch template):

    /<full_path_to_script>/deckScripts/instance_launcher.sh -l lt-abcd1234abcd1234

The 'instance_launcher.sh' is used to call 'instance.py' as the streamdeck does not handle python script execution/redirection well. 
Standard out (STDOUT) and Standard Error (STDERR) are captured from the 'instance_launcher.sh' to `logs/instance_launcher.log`


### SSH Session

Adding the [-s] flag calls `ssh://ec2-user@<public_DNS_name>`

Adding the [-u] flag allows for providing a username besides the default ec2-user (useful for Ubuntu)


### Usage Examples:

In the 'App / File' section after the full path to the 'instance_launcher.sh' script, the followng examples I would use to start and stop known EC2 instances I would use, launch new instances, and disconnect my VPN session (Cisco Anyconnect)

#### Start and connect to EC2

    <path>/instance_launcher.sh -c start -i i-12345abcd -s

#### Stop EC2

    <path>/instance_launcher.sh -c stop -i i-12345abcd

#### launch and connect to a new EC2 Instance based on a launch template:

    <path>/instance_launcher.sh -l lt-abcd5678 -s

#### Launch and connect to a new Ubuntu instance based on a launch template:

    <path>/instance_launcher.sh -l lt-ubuntuLT -s -u ubuntu

#### Disconnect from Cisco Anyconnect VPN

    <path>/vpn.sh