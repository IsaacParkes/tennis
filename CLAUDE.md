# Tennis Court Availability Checker

## Overview
Web app that checks availability of public tennis courts in North London via the ClubSpark/LTA public API. Hosted on Vercel (free tier). Live at: https://tennis-teal.vercel.app

## How It Works
- ClubSpark provides a public JSON API — no scraping or authentication needed
- The frontend (`public/index.html`) calls our serverless API proxy (`api/availability.py`)
- The proxy fetches availability from ClubSpark for all venues concurrently, parses the data, and returns structured JSON
- The frontend renders results with clickable time slots that link directly to the ClubSpark booking page

## Key API Details
- ClubSpark endpoint: `GET https://clubspark.lta.org.uk/v0/VenueBooking/{slug}/GetVenueSessions?startDate=YYYY-MM-DD&endDate=YYYY-MM-DD`
- No auth required
- Times returned as minutes from midnight (e.g. 420 = 07:00)
- `Capacity=0` or `Name="Booking"/"Closed"` means unavailable
- Cost comes from `GuestPrice`, `CourtCost`, or `CostFrom` fields (checked in that order)
- Multi-hour availability blocks are split into individual 1-hour slots in `scraper.py`

## Project Structure
```
Tennis/
├── api/
│   ├── availability.py    # Vercel serverless function (HTTP handler)
│   └── requirements.txt   # Python deps (requests only)
├── public/
│   └── index.html         # Static frontend (vanilla HTML/CSS/JS, no framework)
├── courts.py              # Venue slugs, names, boroughs, distances
├── scraper.py             # ClubSpark API client + availability parser
├── vercel.json            # Vercel routing config
├── .gitignore
└── CLAUDE.md
```

## File Details

### `courts.py`
- Contains `VENUES` list — each venue is a dict with: `name`, `slug`, `borough`, `distance_miles`
- Currently 15 parks across Haringey and Hackney (within ~3 miles of Tewkesbury Road, N15)
- The `slug` is the ClubSpark URL identifier (e.g. `FinsburyPark` → `clubspark.lta.org.uk/FinsburyPark`)

### `scraper.py`
- `fetch_sessions(slug, date_str)` — calls ClubSpark API for a single venue/date
- `parse_availability(api_data, start_time, end_time)` — extracts available slots, splits multi-hour blocks into 1-hour slots, applies time filter
- `get_availability(venues, date_str, start_time, end_time)` — fetches all venues concurrently using ThreadPoolExecutor (10 workers), returns sorted by distance

### `api/availability.py`
- Vercel serverless function using `BaseHTTPRequestHandler`
- Query params: `date` (required, YYYY-MM-DD), `start_time` (optional, HH:MM), `end_time` (optional, HH:MM)
- Returns JSON array of `{venue, slots}` objects
- Uses `sys.path.insert(0, os.getcwd())` to import from project root

### `public/index.html`
- Single-file frontend — all CSS and JS inline, no build step
- Features: date picker with arrow nav and quick-pick buttons (Today/Tomorrow/day names), time range dropdowns, collapsible venue cards
- Each time slot is a clickable link to the ClubSpark booking page for that venue/date
- Shows: slot time, price (£ or Free), floodlight indicator (💡)
- Responsive layout for mobile

### `vercel.json`
- `framework: null` — prevents Vercel from auto-detecting a framework
- `includeFiles` config ensures `courts.py` and `scraper.py` are bundled with the serverless function

## Deployment
- Hosted on Vercel (free tier), auto-deploys from GitHub: https://github.com/IsaacParkes/tennis
- Push to `main` branch triggers deploy
- `vercel dev` for local testing
- Git tag `v1.0` marks the first stable working version

## Current Status / Next Steps
The app was working and deployed as of v1.0. The next planned feature is:
- **Location-based search**: Allow users to enter any London location and choose a radius (1-5 miles) to find nearby parks, rather than hardcoding parks near Tewkesbury Road
- This requires: geocoding the user's input, having a comprehensive list of all ClubSpark tennis venues in London, and filtering by distance
- Better.org also has tennis courts using OpenActive RPDE 1.0/2.0 APIs — could be integrated as an additional data source

## Important Notes
- PythonAnywhere free tier does NOT work — it blocks outbound requests to clubspark.lta.org.uk
- Render free tier has 30-second cold starts — user rejected this option
- The app must remain a simple Vercel deployment (serverless function + static HTML)
- User prefers clean, user-friendly UI with buttons/dropdowns, not text input for dates/times
- Each time slot should be individually clickable and link to the booking page
- Show pricing in output
