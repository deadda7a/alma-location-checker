#!/usr/bin/env bash
dotnet publish ./alma-location-checker --configuration Release --framework net5.0 --output ./release --self-contained true --runtime linux-x64
#osslsigncode sign -pkcs12 "/mnt/c/path/to/certificate.p12" -pass "certificate password" -n "My Application Name" -i "https://www.mywebsite.com" -t "http://timestamp.comodoca.com/authenticode" -in "/mnt/c/path/to/executable.exe" -out "/mnt/c/path/to/executable.exe"
