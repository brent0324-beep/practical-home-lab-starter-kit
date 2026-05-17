# Troubleshooting

Troubleshooting is faster when the lab has a known shape. Start with the host,
then the topology, then automation.

## Host Checks

```bash
hostnamectl
ip addr
ip route
sudo ufw status verbose
systemctl status ssh
```

Questions:

- Is the host on the expected network?
- Is the firewall allowing the intended traffic?
- Is SSH running?
- Did a recent update change networking or virtualization behavior?

## GNS3 Checks

- Is the project running?
- Are device links up?
- Are management interfaces assigned?
- Is the management bridge or cloud connected correctly?
- Can the Linux host ping the device management IP?

Useful commands:

```bash
ping 10.10.10.11
traceroute 10.10.10.11
arp -n
```

## SSH Checks

```bash
ssh -vvv labadmin@10.10.10.11
```

Look for:

- Wrong username.
- Wrong key.
- Host key mismatch.
- Firewall drop.
- Device SSH service disabled.

## Ansible Checks

Start with inventory parsing:

```bash
ansible-inventory -i ansible/inventory.example.ini --list
```

Then test reachability:

```bash
ansible -i ansible/inventory.example.ini lab_network -m ping
```

Common issues:

- Incorrect `ansible_network_os`.
- Wrong connection plugin.
- Device prompt or privilege mode mismatch.
- SSH key not accepted.
- Inventory points to an old management IP.

## Documentation Checks

When something fails, compare:

- GNS3 topology labels.
- Inventory hostnames.
- IP address plan.
- Firewall rules.
- SSH config.
- Latest change notes.

Most lab issues are mismatches between these sources. Fix the documentation
while fixing the technical problem.
