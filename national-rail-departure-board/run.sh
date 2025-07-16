#!/usr/bin/with-contenv bashio

export API_KEY="$(bashio::config 'api_key')"
export START_STATION="$(bashio::config 'start_station')"
export DESTINATION_STATION="$(bashio::config 'destination_station')"
export REFRESH_INTERVAL="$(bashio::config 'refresh_interval')"
export MAX_DEPARTURES="$(bashio::config 'max_departures')"
export TIME_WINDOW="$(bashio::config 'time_window')"

exec python3 app.py 