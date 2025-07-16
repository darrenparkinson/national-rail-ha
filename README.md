# National Rail Departure Board - Home Assistant Add-on

A beautiful departure board for UK railway stations using National Rail data, designed as a Home Assistant community add-on.

## Features

- 🚂 Real-time departure information from National Rail API
- 🎨 Beautiful National Rail branded interface
- 📱 Responsive design for all devices
- ⚡ Auto-refresh functionality
- 🎯 Station selection with search
- 📊 Status indicators (On Time, Delayed, Cancelled, Platform Change)
- 🔄 Manual refresh option
- 🕐 Live clock display

## Screenshots

The add-on provides a clean, professional departure board interface with:
- National Rail branding and colors
- Real-time departure updates
- Station selection dropdown
- Status indicators with icons
- Responsive design for mobile and desktop

## Installation

### Prerequisites

- Home Assistant (version 2023.8 or later)
- National Rail API key (optional - mock data available for testing)

### Getting a National Rail API Key

1. Visit the [National Rail Data Portal](https://www.nationalrail.co.uk/developers/)
2. Register for an account
3. Apply for API access
4. Once approved, you'll receive your API key

### Installation Steps

1. **Add the repository to Home Assistant:**
   - Go to Settings → Add-ons → Add-on Store
   - Click the three dots in the top right
   - Select "Repositories"
   - Add this repository URL

2. **Install the add-on:**
   - Find "National Rail Departure Board" in the add-on store
   - Click "Install"
   - Wait for installation to complete

3. **Configure the add-on:**
   - Click "Configuration" tab
   - Enter your National Rail API key (optional)
   - Set your preferred start station (default: PAD - London Paddington)
   - Set destination station (optional - for filtered results)
   - Configure refresh interval and other options
   - Click "Save"

4. **Start the add-on:**
   - Click "Start"
   - The departure board will be available at the provided URL

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `api_key` | string | "" | Your National Rail API key (optional) |
| `start_station` | string | "PAD" | Your preferred departure station (CRS code) |
| `destination_station` | string | "" | Filter to specific destination (optional) |
| `refresh_interval` | integer | 60 | Auto-refresh interval in seconds |
| `max_departures` | integer | 10 | Maximum number of departures to display |
| `time_window` | integer | 120 | Time window for departures in minutes |

## Station Codes

The add-on uses CRS (Computer Reservation System) codes for stations. Common examples:

- **PAD** - London Paddington
- **WAT** - London Waterloo
- **VIC** - London Victoria
- **LBG** - London Bridge
- **RDG** - Reading
- **BRI** - Bristol Temple Meads
- **MAN** - Manchester Piccadilly
- **BHM** - Birmingham New Street
- **EDB** - Edinburgh Waverley

A complete list of station codes is included in the `stations.json` file.

## Usage

### Web Interface

1. **Access the departure board:**
   - Open the add-on URL in your browser
   - Or access via Home Assistant sidebar

2. **Select a station:**
   - Use the dropdown in the header to change stations
   - The board will automatically refresh with new data

3. **Refresh data:**
   - Click the refresh button for manual updates
   - Toggle auto-refresh on/off as needed

4. **View departure details:**
   - Time (with delay indicators)
   - Destination
   - Operator
   - Platform
   - Status with color coding

### API Endpoints

The add-on provides several API endpoints:

- `GET /` - Main departure board interface
- `GET /api/departures?station={code}` - Departure data for a station
- `GET /api/stations` - List of all stations
- `GET /health` - Health check endpoint

## Development

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd national-rail-ha
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run locally:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   - Open http://localhost:8123 in your browser

### Testing

The add-on includes mock data for testing without an API key:

- Mock departures are generated automatically
- Realistic train operators and destinations
- Various status conditions (On Time, Delayed, Cancelled)
- Platform assignments and delays

### Building

To build the add-on for Home Assistant:

```bash
docker build -t national-rail-departure-board .
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
- Look for any error messages

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Guidelines

1. Follow the existing code style
2. Add tests for new features
3. Update documentation as needed
4. Test thoroughly before submitting

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- National Rail for providing the API
- Home Assistant community for the add-on framework
- Font Awesome for icons
- Inter font family for typography

## Support

For support and questions:
- Open an issue on GitHub
- Check the Home Assistant community forums
- Review the troubleshooting section above

---

**Note:** This add-on is not officially affiliated with National Rail. Please ensure you comply with National Rail's API terms of service when using this add-on. 