# Quick Setup Guide

## 🚀 Getting Started

### Local Development

1. **Install dependencies:**
   ```bash
   cd national-rail-departure-board
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Access the departure board:**
   - Open http://localhost:8124 in your browser
   - The app will show mock data by default

4. **Test the application:**
   ```bash
   python test_app.py
   ```

### Home Assistant Add-on

1. **Add to Home Assistant:**
   - Copy all files to your Home Assistant add-ons directory
   - Or create a repository with these files

2. **Install the add-on:**
   - Go to Settings → Add-ons → Add-on Store
   - Add your repository
   - Install "National Rail Departure Board"

3. **Configure:**
   - Enter your National Rail API key (optional)
   - Set your preferred station
   - Start the add-on

## 📁 Project Structure

```
national-rail-ha/
├── national-rail-departure-board/  # Home Assistant add-on
│   ├── app.py                      # Main Flask application
│   ├── config.yaml                 # Add-on configuration
│   ├── Dockerfile                  # Container definition
│   ├── requirements.txt            # Python dependencies
│   ├── templates/                  # HTML templates
│   ├── static/                     # CSS, JS, images
│   ├── stations.json               # UK station data
│   ├── ldbws.json                  # National Rail API spec
│   └── README.md                   # Add-on documentation
├── repository.yaml                 # Add-on repository config
├── README.md                       # Main documentation
├── SETUP_GUIDE.md                  # This file
└── Brand Guidelines/, Logos/       # Branding assets (optional)
```

## 🎯 Key Features

- **Mock Data**: Works without API key for testing
- **Real API Integration**: Uses National Rail API when configured
- **Responsive Design**: Works on mobile and desktop
- **Auto-refresh**: Updates every 60 seconds
- **Station Selection**: Dropdown with all UK stations
- **Status Indicators**: Visual status for delays, cancellations, etc.

## 🔧 Configuration

The add-on supports these configuration options:

- `api_key`: Your National Rail API key
- `start_station`: Default station (CRS code)
- `destination_station`: Filter to specific destination
- `refresh_interval`: Auto-refresh interval in seconds
- `max_departures`: Number of departures to show
- `time_window`: Time window for departures in minutes

## 🧪 Testing

The application includes comprehensive testing:

- **Health Check**: `/health` endpoint
- **API Endpoints**: `/api/departures` and `/api/stations`
- **Mock Data**: Realistic departure data for testing
- **Error Handling**: Graceful fallbacks and error messages

## 🚂 Next Steps

1. **Get API Key**: Apply for National Rail API access
2. **Customize**: Modify colors, layout, or add features
3. **Deploy**: Install as Home Assistant add-on
4. **Share**: Contribute to the community

## 📞 Support

- Check the logs in Home Assistant
- Review the troubleshooting section in README.md
- Test locally first before deploying

---

**Ready to go!** 🎉 