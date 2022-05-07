from netmiko import ConnectHandler

device_ip = '10.0.15.110'
username = 'admin'
password = 'cisco'

device_params = {
    'device_type': 'cisco_ios',
    'ip': device_ip,
    'username': username,
    'password': password
}

cmd_createlo = [
        "int lo62070154",
        "ip add 192.168.1.1 255.255.255.0",
        "no shut",
    ]

cmd_deletelo = ["no int lo62070154"]

with ConnectHandler(**device_params) as ssh:
    result = ssh.send_command('sh ip int lo 62070154')
    lines = result.strip().split('\n')
    words = lines[1].split()

    # if not found loopback with ip 192.168.1.1/24
    if words[3] != "192.168.1.1/24":
        # create loopback
        result = ssh.send_config_set(cmd_createlo)
    else:
        # delete loopback
        result = ssh.send_config_set(cmd_deletelo)
    ssh.save_config()
        




