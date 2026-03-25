# Tennis Court Availability Checker

## Overview
Web app that checks availability of public tennis courts in North London (within ~3 miles of Tewkesbury Road, N15) via the ClubSpark/LTA public API.

## Technical Approach
- ClubSpark provides a public JSON API — no scraping needed
- Key endpoint: `GET /v0/VenueBooking/{slug}/GetVenueSessions?startDate=YYYY-MM-DD&endDate=YYYY-MM-DD`
- No authentication required
- Times returned as minutes from midnight (e.g. 420 = 07:00)
- `Capacity=0` or `Name="Booking"/"Closed"` means unavailable

## Project Structure (Vercel)
- `api/availability.py` — serverless function (proxies ClubSpark API)
- `public/index.html` — static frontend
- `courts.py` — venue slugs and metadata
- `scraper.py` — ClubSpark API client
- `vercel.json` — routing config
- `requirements.txt` — Python deps (requests only)

## Deployment
- Hosted on Vercel (free tier)
- Push to GitHub, connect repo in Vercel dashboard
- `vercel dev` for local testing
