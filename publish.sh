#!/usr/bin/env bash
dotnet publish ./alma-location-checker --configuration Release --framework net5.0 --output ./release/linux --self-contained false --runtime linux-x64
dotnet publish ./alma-location-checker --configuration Release --framework net5.0 --output ./release/win10 --self-contained false --runtime win10-x64
#osslsigncode sign -pkcs12 "/mnt/c/path/to/certificate.p12" -pass "certificate password" -n "My Application Name" -i "https://www.mywebsite.com" -t "http://timestamp.comodoca.com/authenticode" -in "/mnt/c/path/to/executable.exe" -out "/mnt/c/path/to/executable.exe"
