# National Rail Departure Board - Home Assistant Add-on

A beautiful departure board for UK railway stations using National Rail data, designed as a Home Assistant community add-on.

## 🚂 Features

- 🎨 Beautiful National Rail branded interface
- 📱 Responsive design for all devices
- ⚡ Auto-refresh functionality
- 🎯 Station selection with search
- 📊 Status indicators (On Time, Delayed, Cancelled, Platform Change)
- 🔄 Manual refresh option
- 🕐 Live clock display
- 🧪 Mock data for testing (no API key required)

## 📦 Installation

### Home Assistant

1. **Add this repository to Home Assistant:**
   - Go to **Settings** → **Add-ons** → **Add-on Store**
   - Click the three dots (⋮) in the top right
   - Select **"Repositories"**
   - Add: `https://github.com/darrenparkinson/national-rail-ha`
   - Click **"Add"**

2. **Install the add-on:**
   - Find "National Rail Departure Board" in the add-on store
   - Click **"Install"**
   - Wait for installation to complete

3. **Configure and start:**
   - Click **"Configuration"** tab
   - Set your preferred station (default: PAD - London Paddington)
   - Optionally add your National Rail API key
   - Click **"Save"**
   - Click **"Start"**

### Local Development

```bash
# Clone the repository
git clone https://github.com/darrenparkinson/national-rail-ha.git
cd national-rail-ha

# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r national-rail-departure-board/requirements.txt

# Run locally
cd national-rail-departure-board
python app.py
```

Then visit: http://localhost:8123

## ⚙️ Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `api_key` | string | "" | Your National Rail API key (optional) |
| `start_station` | string | "PAD" | Your preferred departure station (CRS code) |
| `destination_station` | string | "" | Filter to specific destination (optional) |
| `refresh_interval` | integer | 60 | Auto-refresh interval in seconds |
| `max_departures` | integer | 10 | Maximum number of departures to display |
| `time_window` | integer | 120 | Time window for departures in minutes |

## 🚉 Station Codes

Common station codes:
- **PAD** - London Paddington
- **WAT** - London Waterloo
- **VIC** - London Victoria
- **RDG** - Reading
- **BRI** - Bristol Temple Meads
- **MAN** - Manchester Piccadilly

A complete list is included in the add-on.

## 🎯 Usage

1. **Access the departure board** via the add-on URL or Home Assistant sidebar
2. **Select a station** using the dropdown in the header
3. **View departures** with real-time updates every 60 seconds
4. **Monitor status** with color-coded indicators for delays and cancellations

## 🧪 Testing

The add-on includes comprehensive testing:

```bash
# Test the application
python test_app.py
```

## 📁 Repository Structure

```
national-rail-ha/
├── national-rail-departure-board/  # Home Assistant add-on
│   ├── app.py                      # Main Flask application
│   ├── config.yaml                 # Add-on configuration
│   ├── Dockerfile                  # Container definition
│   ├── requirements.txt            # Python dependencies
│   ├── templates/                  # HTML templates
│   ├── static/                     # CSS, JS, images
│   └── stations.json              # UK station data
├── README.md                       # This file
├── SETUP_GUIDE.md                 # Detailed setup guide
└── test_app.py                    # Test script
```

## 🔧 Troubleshooting

### Common Issues

1. **"Not a valid add-on repository"**
   - Ensure you're using the correct repository URL
   - Check that the repository is public

2. **No departures showing**
   - Check the add-on logs for errors
   - Verify station codes are correct
   - Try with mock data first (no API key)

3. **API errors**
   - Ensure your API key is valid
   - Check internet connectivity
   - Verify National Rail API access

### Logs

View add-on logs in Home Assistant:
- Go to Settings → Add-ons → National Rail Departure Board
- Click "Logs" tab

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- National Rail for providing the API
- Home Assistant community for the add-on framework
- Font Awesome for icons
- Inter font family for typography

---

**Note:** This add-on is not officially affiliated with National Rail. Please ensure you comply with National Rail's API terms of service when using this add-on. 