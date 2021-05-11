#! /usr/bin/env sh
echo " .:|:.:|:. "
echo " C I S C O "
echo "  SecureX "
echo
echo " Development Dockerfile build script."
echo

module_name="CTIM-STIX Converter"
image_name="tr-05-ctim-stix-translator"

CONFIG_FILE=code/container_settings.json
if [ -f $CONFIG_FILE ]; then
   echo
   echo "The configuration file (container_settings.json) already exists."
   echo
   version=`jq -r .VERSION code/container_settings.json`
else
   read -p 'Version: ' version
   echo {\"VERSION\": \"$version\",\"NAME\": \"$module_name\"} > code/container_settings.json
fi

echo " Module: $module_name"
echo " Version: $version"
echo
echo "Starting build process ..."
echo
docker build -t "$image_name:$version" .

echo
