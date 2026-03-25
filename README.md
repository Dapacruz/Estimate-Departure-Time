# Estimate Departure Time

A command-line tool that calculates what time you need to leave in order to arrive at your destination by a desired time, using real-time traffic data from the Google Maps Directions API.

## How It Works

Given an origin, destination, and desired arrival time, `travest.py` iteratively queries the Google Maps Directions API (with traffic) to converge on the departure time that results in arriving at your target time. It accounts for real-world traffic conditions, not just raw distance.

## Requirements

- Python 3.6+
- A [Google Maps API key](#getting-a-google-maps-api-key) with the **Directions API** enabled

## Installation

1. Clone the repository:

```bash
git clone https://github.com/dacruz/Estimate-Departure-Time.git
cd Estimate-Departure-Time
```

2. Install the dependency:

```bash
pip install googlemaps
```

## Getting a Google Maps API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Enable the **Directions API**
4. Navigate to **APIs & Services > Credentials** and create an API key
5. (Recommended) Restrict the key to the Directions API

## Usage

### Interactive Mode

Run the script without arguments and follow the prompts:

```bash
python travest.py
```

You will be prompted for:
- **Google Maps API Key** (first run only — saved for future use)
- **Start Address** (default: `Roseville, CA`)
- **Destination Address** (default: `Marriott Marquis, San Francisco`)
- **Arrival Date** (default: tomorrow, format `MM/DD/YYYY`)
- **Desired Arrival Time** (default: `8:00`)

### Command-Line Mode

Pass all parameters directly:

```bash
python travest.py -o "Roseville, CA" -d "San Francisco, CA" -ad 03/26/2026 -at 9:00
```

### Example Output

```
Start Address: Roseville, CA, USA
Destination Address: San Francisco, CA 94103, USA

Estimated Departure: 5:45
Estimated Arrival: 9:00

Travel Time: 3 hours 15 mins
Distance: 94.3 mi
```

## CLI Reference

| Argument | Short | Type | Default | Description |
|---|---|---|---|---|
| `--origin` | `-o` | string | *(prompted)* | Start location |
| `--destination` | `-d` | string | *(prompted)* | End location |
| `--arrival-date` | `-ad` | string | *(prompted)* | Arrival date (`MM/DD/YYYY`) |
| `--arrival-time` | `-at` | string | *(prompted)* | Desired arrival time (`H:MM`) |
| `--api-key` | `-k` | string | *(from settings)* | Google Maps API key |
| `--max_iterations` | `-mi` | int | `25` | Max refinement iterations |
| `--update` | `-u` | flag | — | Update saved API key |

## Configuration

On first run, you will be prompted for your Google Maps API key. It is saved to:

- **macOS/Linux:** `~/.travest-settings.json`
- **Windows:** `%USERPROFILE%\.travest-settings.json`

The file is created with `600` permissions (owner read/write only). To update the saved key:

```bash
python travest.py --update
```

## Troubleshooting

**`ModuleNotFoundError: No module named 'googlemaps'`**
Run `pip install googlemaps`.

**`ApiError` or empty directions result**
- Verify your API key is valid and the Directions API is enabled in your Google Cloud project.
- Ensure the origin and destination are recognizable addresses.

**Departure time doesn't converge**
The default of 25 iterations handles most routes. For very long or unusual routes, increase it with `-mi 50`.

**API key is rejected**
Run `python travest.py --update` to replace the stored key.

## License

MIT License — Copyright (c) 2018 David Cruz. See [LICENSE](LICENSE) for details.
