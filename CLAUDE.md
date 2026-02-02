# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CasE InSensitIVE is a Django-based fantasy trading game platform for NCAA tournament and NFL season competitions. Players trade cards/stocks representing sports teams in a marketplace with real-time order book matching.

## Development Commands

```bash
# Install dependencies (uses uv package manager)
uv sync

# Run development server
uv run python manage.py runserver

# Database migrations
uv run python manage.py makemigrations
uv run python manage.py migrate

# Create admin user
uv run python manage.py createsuperuser

# Data import/update commands
uv run python manage.py update_standings      # Update team scores from real results
uv run python manage.py ncaa_schedule_scraper # Fetch NCAA game schedule
uv run python manage.py nfl_schedule_scraper  # Fetch NFL game schedule
uv run python manage.py estimate_scores       # Calculate estimated positions
uv run python manage.py check_games           # Process completed games
uv run python manage.py set_next_games        # Update next game cache

# Add new dependencies
uv add <package-name>
```

## Architecture

### Django Apps

- **cix/** - Core project config, authentication views, URL routing
- **ncaacards/** - Main game logic: games, entries, teams, card trading
- **trading/** - Order book matching engine for stock trading
- **profiles/** - User profiles and verification

### Two Trading Systems

1. **Cards** (`supports_cards=True`): Peer-to-peer trade offers with bid/ask components (`TradeOffer`, `TradeSide`, `TradeComponent`)
2. **Stocks** (`supports_stocks=True`): Continuous order book matching (`Market`, `Security`, `Order`, `Execution`)

### Key Model Hierarchy

```
GameType (NCAA/NFL)
└── NcaaGame (individual game instance)
    ├── GameTeam (team in a game, tracks score/volume)
    ├── UserEntry (player participation)
    │   └── UserTeam (player's holdings per team)
    └── Market → Security → Order → Execution
```

### Signal-Driven Updates

The codebase uses Django signals extensively (`ncaacards/models.py:393-517`):
- `TeamScoreCount` changes → recalculate all team and entry scores
- `Execution` created → update buyer/seller positions and points
- `Order` created → trigger order matching via `process_order()`
- `NcaaGame` created → auto-create Market, Securities, GameTeams

### Caching

Heavy Memcached usage for bid/ask prices, market data, and next game lookups. Cache invalidation happens in signal handlers.

## API

All endpoints under `/ncaa/api/` are CSRF-exempt and require `apid` (UUID) parameter for authentication:
- `positions` - User positions and raw points
- `executions` - Execution history
- `open_orders` / `place_order` / `cancel_order` - Order management
- `make_market` / `my_markets` - Market maker operations
- `market_data` / `get_book` - Market data

## Configuration

- **Package Manager**: uv (see `pyproject.toml`)
- **Database**: PostgreSQL (configured in `cix/settings.py`)
- **Cache**: Memcached on localhost:11211
- **Admin**: Django admin at `/yodawg/`
- **Python**: 3.12 (see `.python-version`)
- **Django**: 4.2 LTS

## Code Patterns

- `@transaction.atomic()` for database consistency
- `is_active` flag for soft deletes on orders/trades
- `Decimal(2)` precision for all prices/points
- UUIDs for order IDs, API IDs
- Entry names stored as strings in execution records (`placer` field)
