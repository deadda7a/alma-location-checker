SELF_CONTAINED = false

all: clean linux windows

clean:
	rm -rf release

debug:
	dotnet build --configuration Debug --framework net5.0 --output ./debug

linux:
	dotnet publish ./alma-location-checker --configuration Release --framework net5.0 --output ./release/linux --self-contained ${SELF_CONTAINED} --runtime linux-x64

windows:
	dotnet publish ./alma-location-checker --configuration Release --framework net5.0 --output ./release/win10 --self-contained ${SELF_CONTAINED} --runtime win10-x64

sign: windows
	osslsigncode sign -pkcs12 "/home/spfeifer/tmp/user.p12" -pass "1337" -n "Hello Workd App" -i "https://sebastian-elisa-pfeifer.eu" -t "http://timestamp.sectigo.com" -in "./release/win10/alma-location-checker.exe" -out "./release/win10/alma-location-checker_signed.exe"
