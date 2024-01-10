#!/usr/bin/with-contenv bashio
set -e


bashio::log.info "Preparing to start..."
bashio::log.info "Checking internet..."
test=bing.com
if nc -zw1 $test 443 && echo | openssl s_client -connect $test:443 2>&1 | awk '
  handshake && $1 == "Verification" { if ($2=="OK") exit; exit 1 }
  $1 $2 == "SSLhandshake" { handshake = 1 }'; then
    bashio::log.info "Internet Working..."
    data=$(curl -sSL -H "Authorization: Bearer $SUPERVISOR_TOKEN" http://supervisor/core/info | jq .data)
    arch=$(echo $data | jq -r .arch)
    ip=$(echo $data | jq -r .ip_address)
    port=$(echo $data | jq -r .port)
    key=$(bashio::config 'key')
    bashio::log.info "Home Assistant Arch ${arch}..."
    bashio::log.info "Get Home Assistant Running address..."
else
    exit 1
fi
length=${#key}

if [ ${length} -le 15 ]; then
    bashio::log.info "Key Length Wrong Exiting..."
    exit 1
else
    bashio::log.info "Key Length Correct..."
    bashio::log.info "Starting Agent..."
    /usr/bin/npc -vkey=${key} -coreip=${ip} -coreport=${port} -debug=true
fi

bashio::log.info "Something Wrong Exiting..."
