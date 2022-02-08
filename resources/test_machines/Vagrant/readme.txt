Vagrant files for easy deployment of test virtual machine in Virtualbox using Vagrant. Specific Domoticz version is built from source code. Different port-forwarding host port is defined for Domoticz http port in each VM to enable running all 3 VMs at the same time, if needed.

I have been inspired by Vagrant file found in Domoticz wiki: https://www.domoticz.com/wiki/Build_Domoticz_from_source_with_Vagrant

Domoticz - https://github.com/domoticz/domoticz
Domoticz-Volumio-Plugin - https://github.com/frepkovsky/Domoticz-Volumio-Plugin


ubuntu-domoticz-latest:
    - VM Name: Domoticz-latest
    - Ubuntu 20.04.3 LTS (Focal Fossa) VM
    - Domoticz version: latest available from github development branch from
    - Domoticz-Volumio-Plugin
    - Domoticz is reachable from host http://localhost:8080

ubuntu-domoticz-2021.1:
    - VM Name: Domoticz-2021.1
    - Ubuntu 20.04.3 LTS (Focal Fossa) VM
    - Domoticz version: 2021.1 (2021.1 tagged release from github)
    - Domoticz-Volumio-Plugin
    - Domoticz is reachable from host: http://localhost:8081

ubuntu-domoticz-2022.1:
    - VM Name: Domoticz-2022.1
    - Ubuntu 20.04.3 LTS (Focal Fossa) VM
    - Domoticz version: 2022.1 (2022.1 tagged release from github)
    - Domoticz-Volumio-Plugin
    - Domoticz is reachable from host: http://localhost:8082

