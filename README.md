# ftd_bulk_cli

A proof of concept script where one can run a CLI command against all Cisco Firewall  Threat Defense devices managed by a Security Cloud Control Firewall Management manager using this API https://developer.cisco.com/docs/cisco-security-cloud-control-firewall-manager/create-bulk-command/

The script assumes you have provided your SCC Firewall Manager token as an environment variable 

```
export export API_TOKEN="yJraWQiOiIwIiwidHlwIjoiSldUIiwiY..."
```

Run the script by providing the cli command that you wish to run against all of your FTDs. See the above create-bulk-command link for any restrictions or limitations


`python ftd_bulk_cli.py show version`

```
Manager: cisco-xxxxxx.app.us.cdo.cisco.com:443
Retrieved 2 FTD device(s).
Command: show version

Device: Hacks-Home
-------------[ FPR1150.hacksbrain.com ]-------------
Model                     : Cisco Firepower 1150 Threat Defense (78) Version 10.0.0 (Build 140)
UUID                      : 9b8eb11a-e932-11ec-96ae-xxxxxxxx
LSP version               : lsp-rel-20260430-1252
VDB version               : 422
----------------------------------------------------

Cisco Adaptive Security Appliance Software Version 9.24(1)
SSP Operating System Version 2.18(0.520)

Compiled on Mon 01-Dec-25 23:40 GMT by fpbesprd
System image file is "disk0:/installables/switch/fxos-k8-fp1k-lfbff.2.18.0.520.SPA"
Config file at boot was "startup-config"

FPR1150 up 41 days 20 hours
Start-up time 34 secs

Hardware:   FPR-1150, 5652 MB RAM, CPU Atom C3000 series 2000 MHz, 1 CPU (16 cores)

Encryption hardware device : Cisco FP Crypto on-board accelerator (revision 0x11)
                             Driver version        : 4.14.0
                             Number of accelerators: 6

 1: Int: Internal-Data0/0    : address is 00a0.c900.0002, irq 10
 3: Ext: Management1/1       : address is 08ec.f5f6.5a01, irq 0
 4: Int: Internal-Data1/1    : address is 0000.0100.0001, irq 0
 5: Int: Internal-Data1/2    : address is 0000.0300.0001, irq 0
 6: Int: Internal-Control1/1 : address is 0000.0001.0001, irq 0

Serial Number: JAD22xxxxx
Configuration last modified by enable_1 at 05:42:12.616 UTC Fri May 1 2026

Device: Paradise
------------[ paradise.hacksbrain.com ]-------------
Model                     : Cisco Firepower 1010 Threat Defense (78) Version 7.6.2 (Build 329)
UUID                      : 4f973622-192a-11ef-b86d-xxxxxxxx
LSP version               : lsp-rel-20260430-1252
VDB version               : 422
----------------------------------------------------

Cisco Adaptive Security Appliance Software Version 9.22(1)127
SSP Operating System Version 2.16(0.4006)

Compiled on Fri 08-Aug-25 00:57 GMT by fpbesprd
System image file is "disk0:/installables/switch/fxos-k8-fp1k-lfbff.2.16.0.4006.SPA"
Config file at boot was "startup-config"

paradise up 21 hours 17 mins
Start-up time 51 secs

Hardware:   FPR-1010, 2544 MB RAM, CPU Atom C3000 series 2200 MHz, 1 CPU (4 cores)

Encryption hardware device : Cisco FP Crypto on-board accelerator (revision 0x11)
                             Driver version        : 4.12.0
                             Number of accelerators: 6

 1: Int: Internal-Data0/0    : address is 00a0.c900.0000, irq 10
 3: Ext: Management1/1       : address is e8eb.3421.f401, irq 0
 4: Int: Internal-Data1/1    : address is 0000.0100.0001, irq 0
 5: Int: Internal-Data1/2    : address is 0000.0300.0001, irq 0
 6: Int: Internal-Control1/1 : address is 0000.0001.0001, irq 0

Serial Number: JAD2xxxxxx
Configuration last modified by enable_1 at 05:45:12.968 UTC Fri May 1 2026
