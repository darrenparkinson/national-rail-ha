# National Rail Departure Board

A beautiful departure board for UK railway stations using National Rail data.

## Features

- 🚂 Real-time departure information
- 🎨 Beautiful National Rail branded interface
- 📱 Responsive design for all devices
- ⚡ Auto-refresh functionality
- 🎯 Station selection with search
- 📊 Status indicators (On Time, Delayed, Cancelled, Platform Change)
- 🔄 Manual refresh option
- 🕐 Live clock display
- 🧪 Mock data for testing (no API key required)

## Screenshots

The add-on provides a clean, professional departure board interface with:
- National Rail branding and colors
- Real-time departure updates
- Station selection dropdown
- Status indicators with icons
- Responsive design for mobile and desktop

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `api_key` | string | "" | Your National Rail API key (optional) |
| `start_station` | string | "PAD" | Your preferred departure station (CRS code) |
| `destination_station` | string | "" | Filter to specific destination (optional) |
| `refresh_interval` | integer | 60 | Auto-refresh interval in seconds |
| `max_departures` | integer | 10 | Maximum number of departures to display |
| `time_window` | integer | 120 | Time window for departures in minutes |

## Station Codes

Common station codes:
- **PAD** - London Paddington
- **WAT** - London Waterloo
- **VIC** - London Victoria
- **RDG** - Reading
- **BRI** - Bristol Temple Meads
- **MAN** - Manchester Piccadilly

A complete list of station codes is included in the add-on.

## Usage

1. **Access the departure board** via the add-on URL or Home Assistant sidebar
2. **Select a station** using the dropdown in the header
3. **View departures** with real-time updates every 60 seconds
4. **Monitor status** with color-coded indicators for delays and cancellations

## API Endpoints

The add-on provides several API endpoints:

- `GET /` - Main departure board interface
- `GET /api/departures?station={code}` - Departure data for a station
- `GET /api/stations` - List of all stations
- `GET /health` - Health check endpoint

## Development

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

Then visit: http://localhost:8123

### Testing

```bash
# Test the application
python test_app.py
```

## Troubleshooting

### Common Issues

1. **No departures showing:**
   - Check your API key is correct
   - Verify the station code is valid
   - Check the add-on logs for errors

2. **API errors:**
   - Ensure your API key is valid and active
   - Check your internet connection
   - Verify the National Rail API is accessible

3. **Interface not loading:**
   - Check the add-on is running
   - Verify the port configuration
   - Check browser console for JavaScript errors

### Logs

View add-on logs in Home Assistant:
- Go to Settings → Add-ons → National Rail Departure Board
- Click "Logs" tab

## License

This add-on is licensed under the MIT License.

## Acknowledgments

- National Rail for providing the API
- Home Assistant community for the add-on framework
- Font Awesome for icons
- Inter font family for typography

---

**Note:** This add-on is not officially affiliated with National Rail. Please ensure you comply with National Rail's API terms of service when using this add-on. 