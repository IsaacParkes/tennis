# Tennis Court Availability Checker

## Overview
Web app that checks availability of public tennis courts in London from two booking platforms: ClubSpark (LTA) and Better.org (GLL). Hosted on Vercel (free tier). Live at: https://tennis-teal.vercel.app

## How It Works
- User enters a location (postcode, outcode like N15, or area name) and radius
- Frontend geocodes the location and calls our serverless API proxy (`api/availability.py`)
- The proxy fetches availability from ClubSpark and Better.org concurrently, merges and sorts by distance
- Results show venue cards with available 1-hour slots, price, floodlight indicator, and source badge (ClubSpark / Better)
- Each slot/venue links directly to the relevant booking page

## Project Structure
```
Tennis/
├── api/
│   ├── availability.py      # Vercel serverless function (HTTP handler)
│   └── requirements.txt     # Python deps (requests only)
├── public/
│   └── index.html           # Static frontend (vanilla HTML/CSS/JS, no framework)
├── courts.py                # VENUES (ClubSpark) and BETTER_VENUES (Better.org) lists
├── scraper.py               # ClubSpark API client + availability parser
├── better_scraper.py        # Better.org API client + availability parser
├── scripts/
│   └── discover_better_venues.py  # Admin helper to find Better.org tennis venues
├── vercel.json              # Vercel routing + file bundling config
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
  - Slot fields: `starts_at.format_24_hour`, `ends_at.format_24_hour`, `price.formatted_amount` (e.g. "£14.85"), `spaces` (0 = unavailable), `action_to_show.status` ("BOOK"/"SOLD_OUT")
- Booking URL: `https://bookings.better.org.uk/location/{slug}/tennis-activities/{date}/by-time`
- `allows_anonymous_bookings: false` on all slots — users must log in on Better.org to complete a booking

## File Details

### `courts.py`
- `VENUES` — 24 ClubSpark venues across North/East London (Haringey, Hackney, Islington, Enfield, Waltham Forest, Tower Hamlets, Camden, Southwark). Each has: `name`, `slug`, `borough`, `lat`, `lng`
- `BETTER_VENUES` — 2 confirmed Better.org venues with tennis: Britannia Leisure Centre (Hackney) and Islington Tennis Centre (Islington). Each has: `name`, `slug`, `booking_slug`, `tennis_slugs` (list), `borough`, `lat`, `lng`, `source: "better"`

### `scraper.py`
- `fetch_sessions(slug, date_str)` — ClubSpark API call
- `parse_availability(api_data, start_time, end_time)` — extracts slots, splits multi-hour blocks
- `filter_by_radius(venues, lat, lng, radius_miles)` — haversine distance filter
- `get_availability(venues, date_str, start_time, end_time, user_lat, user_lng, radius_miles)` — concurrent fetch via ThreadPoolExecutor

### `better_scraper.py`
- `fetch_tennis_slugs(venue_slug)` — discovers parent + leaf tennis activity slugs for a venue
- `fetch_better_times(venue_slug, activity_slug, date_str)` — fetches /times endpoint, normalises list/dict response
- `parse_better_times(times_data, court_name, start_time, end_time)` — parses price/spaces/times into standard slot format
- `get_better_availability(venues, date_str, start_time, end_time)` — concurrent fetch, embeds `booking_url` in venue dict

### `api/availability.py`
- Vercel serverless function using `BaseHTTPRequestHandler`
- Query params: `date` (YYYY-MM-DD, required), `start_time` (HH:MM), `end_time` (HH:MM), `lat`, `lng`, `radius` (miles)
- Defaults to N15 (51.5805, -0.0760) and 3-mile radius if no location provided
- Merges ClubSpark + Better results, re-sorts by distance
- Returns JSON array of `{venue, slots}` objects

### `public/index.html`
- Single-file frontend — all CSS and JS inline, no build step
- Location input with geocoding (postcodes.io for full/outcodes, Nominatim fallback) + GPS button
- Geocoding priority: (1) postcodes.io full postcode, (2) postcodes.io outcode (N15, SW1, etc.), (3) Nominatim — this order matters because Nominatim misidentifies outcodes
- Radius selector: 1/2/3/5/10 miles
- Date picker with arrows and quick-pick buttons (Today/Tomorrow/day names)
- Time range dropdowns (06:00–22:00)
- Collapsible venue cards sorted by distance; collapsed by default if no slots
- Source badge on each venue: blue "Better" or purple "ClubSpark"
- Booking links use `v.booking_url` (Better) or constructed ClubSpark URL
- Floodlight indicator (💡), price display (£ or Free)

### `vercel.json`
- `framework: null` — prevents auto-detection
- `includeFiles: "{courts,scraper,better_scraper}.py"` — bundles all Python modules with the serverless function

## Deployment
- Hosted on Vercel (free tier), auto-deploys from GitHub: https://github.com/IsaacParkes/tennis
- Push to `main` triggers deploy (~30–60 seconds)
- `vercel dev` for local testing
- Vercel free tier: 10-second function timeout, 1GB memory

## Known Constraints
- PythonAnywhere free tier blocks outbound requests to clubspark.lta.org.uk — do not use
- Render free tier has 30-second cold starts — not suitable
- Must remain a simple Vercel deployment (serverless function + static HTML)
- Better.org BETTER_VENUES list is small (2 venues) — only venues confirmed to have tennis via the categories API are included. Run `python scripts/discover_better_venues.py` to find more (requires Better.org API to be up)

## Testing the App
- Live URL: https://tennis-teal.vercel.app
- API endpoint: `GET https://tennis-teal.vercel.app/api/availability?date=YYYY-MM-DD&start_time=HH:MM&end_time=HH:MM&lat=51.58&lng=-0.08&radius=3`
- Key test cases:
  - N15 postcode outcode → should resolve to ~51.5827, -0.0811 (not Stratford)
  - Full postcode e.g. N15 5PQ → postcodes.io full lookup
  - Named location e.g. "Hackney" → Nominatim fallback
  - Today's date → Better.org API returns dict format (handled)
  - Future date → Better.org API returns list format
  - Both ClubSpark and Better venues should appear in results (when within radius)
  - Better venue booking links → bookings.better.org.uk/location/{slug}/tennis-activities/{date}/by-time
  - ClubSpark booking links → clubspark.lta.org.uk/{slug}/Booking/BookByDate#?date=...
