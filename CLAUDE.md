# Tennis Court Availability Checker

## Overview
Web app that checks availability of public tennis courts across London from two booking platforms: ClubSpark (LTA) and Better.org (GLL). Hosted on Vercel (free tier). Live at: https://tennis-teal.vercel.app

## How It Works
- User enters a location (postcode, outcode like N15, or area name) and radius
- Frontend geocodes the location and calls our serverless API proxy (`api/availability.py`)
- The proxy fetches availability from ClubSpark and Better.org concurrently, merges and sorts by distance
- Results shown in a **list view** (venue cards with slots) or **map view** (Leaflet/OpenStreetMap)
- Each slot/venue links directly to the relevant booking page
- When searching today's date, past slots are automatically hidden (API start_time clamped to current hour + client-side hour-boundary filter)

## Project Structure
```
Tennis/
├── api/
│   ├── availability.py           # Vercel serverless function (HTTP handler)
│   └── requirements.txt          # Python deps (requests only)
├── public/
│   └── index.html                # Static frontend (vanilla HTML/CSS/JS + Leaflet map)
├── courts.py                     # VENUES (ClubSpark) and BETTER_VENUES (Better.org) lists
├── scraper.py                    # ClubSpark API client + availability parser
├── better_scraper.py             # Better.org API client + availability parser
├── scripts/
│   └── discover_better_venues.py # CLI tool to check if a Better.org venue has tennis
├── vercel.json                   # Vercel routing + file bundling config
└── CLAUDE.md
```

## ClubSpark API
- Endpoint: `GET https://clubspark.lta.org.uk/v0/VenueBooking/{slug}/GetVenueSessions?startDate=YYYY-MM-DD&endDate=YYYY-MM-DD`
- No auth required, no special headers needed
- Times in minutes from midnight (420 = 07:00)
- `Capacity=0` or `Name="Booking"/"Closed"` = unavailable
- Cost from `GuestPrice`, `CourtCost`, or `CostFrom` fields
- Multi-hour blocks split into 1-hour slots in `scraper.py`
- Booking URL: `https://clubspark.lta.org.uk/{slug}/Booking/BookByDate#?date=YYYY-MM-DD&role=guest`

## Better.org API
- All endpoints require `Origin: https://bookings.better.org.uk` and `Referer: https://bookings.better.org.uk/` headers — without these every endpoint returns 404
- Categories: `GET https://better-admin.org.uk/api/activities/venue/{slug}/categories`
- Tennis children: `GET https://better-admin.org.uk/api/activities/venue/{slug}/categories/tennis-activities`
- Times: `GET https://better-admin.org.uk/api/activities/venue/{slug}/activity/{leaf-slug}/times?date=YYYY-MM-DD`
  - Leaf slugs: `tennis-court-outdoor`, `tennis-court-indoor` (varies per venue)
  - **Important**: returns `data` as a **list** for future dates but a **dict** (keyed by index string) for today — `better_scraper.py` normalises both
  - `action_to_show` can be `null` — guarded with `(t.get("action_to_show") or {})` in parser
  - Slot fields: `starts_at.format_24_hour`, `ends_at.format_24_hour`, `price.formatted_amount` (e.g. "£14.85"), `spaces` (0 = unavailable), `action_to_show.status` ("BOOK"/"SOLD_OUT")
- Booking URL: `https://bookings.better.org.uk/location/{slug}/tennis-activities/{date}/by-time`
- `allows_anonymous_bookings: false` on all slots — users must log in on Better.org to complete a booking

## File Details

### `courts.py`
- `VENUES` — ~46 ClubSpark venues across London. Boroughs covered: Haringey, Hackney, Enfield, Waltham Forest, Tower Hamlets, Southwark, Lambeth, Lewisham, Greenwich, Wandsworth, Merton. Each has: `name`, `slug`, `borough`, `lat`, `lng`
- `BETTER_VENUES` — 3 Better.org venues: Britannia Leisure Centre (Hackney), Hackney Parks GLL (Hackney), Islington Tennis Centre (Islington). Each has: `name`, `slug`, `booking_slug`, `tennis_slugs` (list), `borough`, `lat`, `lng`, `source: "better"`
- All lat/lng coordinates point to the actual tennis courts within each park (sourced from Spin Tennis App, Global Tennis Network, and OpenStreetMap)

### `scraper.py`
- `_haversine(lat1, lng1, lat2, lng2)` — distance in miles between two coordinates
- `filter_by_radius(venues, lat, lng, radius_miles)` — haversine distance filter, also used by `availability.py` for Better venues
- `fetch_sessions(slug, date_str)` — ClubSpark API call
- `parse_availability(api_data, start_time, end_time)` — extracts slots, splits multi-hour blocks
- `get_availability(venues, date_str, start_time, end_time, user_lat, user_lng, radius_miles)` — concurrent fetch via ThreadPoolExecutor

### `better_scraper.py`
- `fetch_tennis_slugs(venue_slug)` — discovers parent + leaf tennis activity slugs for a venue
- `fetch_better_times(venue_slug, activity_slug, date_str)` — fetches /times endpoint, normalises list/dict response
- `parse_better_times(times_data, court_name, start_time, end_time)` — parses price/spaces/times into standard slot format
- `get_better_availability(venues, date_str, start_time, end_time)` — concurrent fetch; returns discovered `booking_slug` from `_fetch_one` so the booking URL is built correctly even for auto-discovered venues

### `api/availability.py`
- Vercel serverless function using `BaseHTTPRequestHandler`
- Query params: `date` (YYYY-MM-DD, required), `start_time` (HH:MM), `end_time` (HH:MM), `lat`, `lng`, `radius` (miles)
- Defaults to N15 (51.5805, -0.0760) and 3-mile radius if no location provided
- Merges ClubSpark + Better results, re-sorts by distance
- Returns JSON array of `{venue, slots}` objects

### `public/index.html`
- Single-file frontend — all CSS and JS inline, no build step, plus Leaflet.js from cdnjs CDN
- Location input with geocoding (postcodes.io for full/outcodes, Nominatim fallback) + GPS button
- Geocoding priority: (1) postcodes.io full postcode, (2) postcodes.io outcode (N15, SW1, etc.), (3) Nominatim — this order matters because Nominatim misidentifies outcodes
- Radius selector: 1/2/3/5/10 miles
- Date picker with arrows and quick-pick buttons (Today/Tomorrow/day names)
- Time range dropdowns (06:00–22:00); past-slot filtering for today (API clamp + hour-boundary render filter)
- **List view**: collapsible venue cards sorted by distance; collapsed by default if no slots
- **Map view**: Leaflet.js with OpenStreetMap tiles; blue dot for user location, green dots for venues with slots, grey for venues without; click popup shows venue info + booking link. Border-radius is on a wrapper div (not the `#map` div) to avoid Leaflet's hardware-accelerated tile rendering conflict
- Toggle between list/map via buttons shown after first search
- Source badge on each venue: blue "Better" or purple "ClubSpark"
- Booking links use `v.booking_url` (Better) or constructed ClubSpark URL
- Floodlight indicator, price display (£ or Free)

### `vercel.json`
- `framework: null` — prevents auto-detection
- `includeFiles: "{courts,scraper,better_scraper}.py"` — bundles Python modules with the serverless function

### `scripts/discover_better_venues.py`
- CLI tool: `python scripts/discover_better_venues.py <slug>` checks if a Better.org venue has tennis
- `--all` flag checks a built-in list of common London GLL leisure centre slugs

## Deployment
- Hosted on Vercel (free tier), auto-deploys from GitHub: https://github.com/IsaacParkes/tennis
- Push to `main` triggers deploy (~30–60 seconds)
- `vercel dev` for local testing (or `npx vercel dev --yes`)
- Vercel free tier: 10-second function timeout, 1GB memory

## Known Constraints
- PythonAnywhere free tier blocks outbound requests to clubspark.lta.org.uk — do not use
- Render free tier has 30-second cold starts — not suitable
- Must remain a simple Vercel deployment (serverless function + static HTML)
- Better.org venues list is small (3 venues) — only venues confirmed to have tennis via the categories API are included
- `filter_by_radius` lives in `scraper.py` but is also used by `availability.py` for Better venue filtering — shared utility, not ClubSpark-specific despite its location
- Both `scraper.py` and `better_scraper.py` define their own `_time_to_minutes` helper (identical 2-line function)
- Default location constants (N15) are defined in both `scraper.py` and `api/availability.py`
- No server-side logging — errors in Better.org/ClubSpark API calls are caught silently

## Adding New Venues

### ClubSpark
1. Find the venue slug from the ClubSpark URL: `clubspark.lta.org.uk/{slug}/Booking`
2. Verify the API works: `GET https://clubspark.lta.org.uk/v0/VenueBooking/{slug}/GetVenueSessions?startDate=YYYY-MM-DD&endDate=YYYY-MM-DD` — must return non-empty `Resources` array
3. Get accurate tennis court coordinates (not park centre) — check OpenStreetMap or Spin Tennis App
4. Add to `VENUES` list in `courts.py`

### Better.org
1. Run `python scripts/discover_better_venues.py <slug>` to check for tennis
2. If found, add to `BETTER_VENUES` in `courts.py` with the returned `booking_slug` and `tennis_slugs`

## Testing
- Live URL: https://tennis-teal.vercel.app
- API: `GET https://tennis-teal.vercel.app/api/availability?date=YYYY-MM-DD&start_time=HH:MM&end_time=HH:MM&lat=51.58&lng=-0.08&radius=3`
- Key test cases:
  - N15 outcode → should resolve to ~51.5827, -0.0811 (not Stratford)
  - Full postcode e.g. N15 5PQ → postcodes.io full lookup
  - Named location e.g. "Hackney" → Nominatim fallback
  - Today's date → Better.org API returns dict format (handled); past slots hidden
  - Future date → Better.org API returns list format
  - Both ClubSpark and Better venues should appear in results (when within radius)
  - Map view → tiles render, markers positioned at actual courts, popups work
  - 10-mile radius from central London → should show venues across all covered boroughs
