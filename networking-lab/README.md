# YemoLab — Cisco home networking lab

## Goal

Practice switch administration and network segmentation using a physical Cisco Catalyst WS-C2960-24TT-L and a Windows laptop.

## Documented work

The existing Day 1 lab notes record console access using PuTTY at 9600 baud, hostname configuration, saved startup configuration, two VLANs, a management interface, and SSH access.

| VLAN | Name | Access port | Purpose |
| --- | --- | --- | --- |
| 10 | HOME | Fa0/1 | Laptop and switch management |
| 20 | LAB | Fa0/2 | Reserved for a future lab device |

```text
Windows laptop ── Fa0/1 / VLAN 10 ── Cisco 2960
                                     └── Fa0/2 / VLAN 20 (reserved)
```

## Configuration example

```text
configure terminal
vlan 10
 name HOME
vlan 20
 name LAB
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 10
interface FastEthernet0/2
 switchport mode access
 switchport access vlan 20
end
copy running-config startup-config
```

## Verification and troubleshooting

The notes record verification with `show vlan brief` and `show ip interface brief`, plus four successful ping replies with no packet loss between the laptop and management SVI. They also record a successful SSH login after resolving compatibility with legacy algorithms on the older IOS version.

These results are reported from the original lab write-up; fresh screenshots and terminal captures are not yet included. Legacy SSH compatibility is a limitation of this training device, not a recommended production configuration.

## Next experiments

Inter-VLAN routing, DHCP, ACLs, and additional services are planned, not completed. A useful next milestone is to demonstrate traffic isolation with before/after test results and add equipment photos.

## Attribution

Adapted from David Yemoh's existing Day 1 home-lab documentation. This portfolio write-up was organized with AI assistance. No hardware was reconfigured during preparation of this repository.
