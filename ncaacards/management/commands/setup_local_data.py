"""
Setup script to populate the database with realistic test data.

Creates:
- 2 game types: NCAA Basketball 2025, NFL 2025
- Teams for each game type with proper names
- Score types with realistic point values
- 4 users (1 superuser, 3 regular users, 1 designated market maker)
- One market/game for each game type
- Market maker bid/ask orders for each team
- Historical executions (0-5 per team)
"""

import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from ncaacards.models import (
    GameType, Team, ScoreType, NcaaGame, UserEntry, GameTeam
)
from trading.models import Security, Order


# NCAA Tournament teams (2025 field - 68 teams)
NCAA_TEAMS = [
    # 1 seeds
    ("Duke", "DUKE"), ("Auburn", "AUB"), ("Florida", "FLA"), ("Houston", "HOU"),
    # 2 seeds
    ("Alabama", "BAMA"), ("Tennessee", "TENN"), ("Michigan State", "MSU"), ("St. John's", "STJ"),
    # 3 seeds
    ("Wisconsin", "WISC"), ("Texas A&M", "TAMU"), ("Iowa State", "ISU"), ("Kentucky", "UK"),
    # 4 seeds
    ("Arizona", "ARIZ"), ("Purdue", "PUR"), ("Texas Tech", "TTU"), ("Maryland", "UMD"),
    # 5 seeds
    ("Clemson", "CLEM"), ("Michigan", "MICH"), ("Oregon", "ORE"), ("Memphis", "MEM"),
    # 6 seeds
    ("Missouri", "MIZZ"), ("Illinois", "ILL"), ("BYU", "BYU"), ("UCLA", "UCLA"),
    # 7 seeds
    ("Kansas", "KU"), ("Florida State", "FSU"), ("UConn", "CONN"), ("St. Mary's", "SMC"),
    # 8 seeds
    ("Louisville", "LOU"), ("Gonzaga", "GONZ"), ("Mississippi State", "MSST"), ("Baylor", "BAY"),
    # 9 seeds
    ("Creighton", "CREI"), ("Georgia", "UGA"), ("Oklahoma", "OU"), ("USC", "USC"),
    # 10 seeds
    ("Arkansas", "ARK"), ("Vanderbilt", "VAN"), ("New Mexico", "UNM"), ("Utah State", "USU"),
    # 11 seeds
    ("VCU", "VCU"), ("NC State", "NCST"), ("Xavier", "XAV"), ("San Diego State", "SDSU"),
    ("Drake", "DRAK"), ("Texas", "TEX"),
    # 12 seeds
    ("Liberty", "LIB"), ("McNeese", "MCN"), ("Colorado State", "CSU"), ("Grand Canyon", "GCU"),
    # 13 seeds
    ("Yale", "YALE"), ("High Point", "HPU"), ("Akron", "AKR"), ("Vermont", "UVM"),
    # 14 seeds
    ("Troy", "TROY"), ("Lipscomb", "LIP"), ("Montana", "MONT"), ("Wofford", "WOF"),
    # 15 seeds
    ("Robert Morris", "RMU"), ("Omaha", "OMA"), ("SIU Edwardsville", "SIUE"), ("Norfolk State", "NSU"),
    # 16 seeds / First Four
    ("Bryant", "BRY"), ("Mount St. Mary's", "MSM"), ("American", "AU"), ("Alabama State", "ALST"),
]

# NFL teams (32 teams)
NFL_TEAMS = [
    # AFC East
    ("Buffalo Bills", "BUF"), ("Miami Dolphins", "MIA"), ("New England Patriots", "NE"), ("New York Jets", "NYJ"),
    # AFC North
    ("Baltimore Ravens", "BAL"), ("Cincinnati Bengals", "CIN"), ("Cleveland Browns", "CLE"), ("Pittsburgh Steelers", "PIT"),
    # AFC South
    ("Houston Texans", "HOU"), ("Indianapolis Colts", "IND"), ("Jacksonville Jaguars", "JAX"), ("Tennessee Titans", "TEN"),
    # AFC West
    ("Denver Broncos", "DEN"), ("Kansas City Chiefs", "KC"), ("Las Vegas Raiders", "LV"), ("Los Angeles Chargers", "LAC"),
    # NFC East
    ("Dallas Cowboys", "DAL"), ("New York Giants", "NYG"), ("Philadelphia Eagles", "PHI"), ("Washington Commanders", "WAS"),
    # NFC North
    ("Chicago Bears", "CHI"), ("Detroit Lions", "DET"), ("Green Bay Packers", "GB"), ("Minnesota Vikings", "MIN"),
    # NFC South
    ("Atlanta Falcons", "ATL"), ("Carolina Panthers", "CAR"), ("New Orleans Saints", "NO"), ("Tampa Bay Buccaneers", "TB"),
    # NFC West
    ("Arizona Cardinals", "ARI"), ("Los Angeles Rams", "LAR"), ("San Francisco 49ers", "SF"), ("Seattle Seahawks", "SEA"),
]

# NCAA scoring types (tournament rounds)
NCAA_SCORE_TYPES = [
    ("Round of 64 Win", Decimal("1.00"), 1),
    ("Round of 32 Win", Decimal("1.00"), 2),
    ("Sweet 16 Win", Decimal("2.00"), 3),
    ("Elite 8 Win", Decimal("2.00"), 4),
    ("Final Four Win", Decimal("2.00"), 5),
    ("Championship Win", Decimal("3.00"), 6),
]

# NFL scoring types
NFL_SCORE_TYPES = [
    ("Regular Season Win", Decimal("1.00"), 1),
    ("Playoff Berth", Decimal("1.00"), 2),
    ("Playoff Win or Byte", Decimal("1.00"), 3),
    ("Super Bowl Win", Decimal("2.00"), 4),
]

# User data
USERS = [
    {"username": "admin", "email": "admin@example.com", "password": "admin123", "is_superuser": True},
    {"username": "marketmaker", "email": "mm@example.com", "password": "mm123", "is_superuser": False},
    {"username": "trader1", "email": "trader1@example.com", "password": "trader123", "is_superuser": False},
    {"username": "trader2", "email": "trader2@example.com", "password": "trader123", "is_superuser": False},
]


class Command(BaseCommand):
    help = "Populate the database with realistic test data"

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing data before creating new data',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write("Resetting existing data...")
            self.reset_data()

        self.stdout.write("Creating game types...")
        ncaa_type, nfl_type = self.create_game_types()

        self.stdout.write("Creating score types...")
        self.create_score_types(ncaa_type, nfl_type)

        self.stdout.write("Creating teams...")
        self.create_teams(ncaa_type, nfl_type)

        self.stdout.write("Creating users...")
        users = self.create_users()

        self.stdout.write("Creating games/markets...")
        ncaa_game, nfl_game = self.create_games(ncaa_type, nfl_type)

        self.stdout.write("Creating user entries...")
        entries = self.create_entries(users, ncaa_game, nfl_game)

        self.stdout.write("Creating market maker orders...")
        mm_entries = {
            ncaa_game: entries[(users[1], ncaa_game)],
            nfl_game: entries[(users[1], nfl_game)],
        }
        self.create_market_maker_orders(mm_entries)

        self.stdout.write("Creating execution history...")
        self.create_execution_history(entries, ncaa_game, nfl_game, users)

        self.stdout.write(self.style.SUCCESS("\nSetup complete!"))
        self.stdout.write(f"\nUsers created:")
        for user_data in USERS:
            role = "superuser" if user_data["is_superuser"] else ("market maker" if user_data["username"] == "marketmaker" else "trader")
            self.stdout.write(f"  - {user_data['username']} / {user_data['password']} ({role})")
        self.stdout.write(f"\nGames created:")
        self.stdout.write(f"  - {ncaa_game.name}")
        self.stdout.write(f"  - {nfl_game.name}")

    def reset_data(self):
        """Delete existing test data."""
        from trading.models import Execution, Order, Market

        # Delete in order of dependencies
        Execution.objects.all().delete()
        Order.orders.all().delete()
        UserEntry.objects.all().delete()
        NcaaGame.objects.all().delete()
        Market.objects.all().delete()
        Team.objects.all().delete()
        ScoreType.objects.all().delete()
        GameType.objects.all().delete()
        User.objects.filter(username__in=[u["username"] for u in USERS]).delete()

    def create_game_types(self):
        ncaa_type, _ = GameType.objects.get_or_create(name="NCAA Basketball 2025")
        nfl_type, _ = GameType.objects.get_or_create(name="NFL 2025")
        return ncaa_type, nfl_type

    def create_score_types(self, ncaa_type, nfl_type):
        for name, default_score, ordering in NCAA_SCORE_TYPES:
            ScoreType.objects.get_or_create(
                name=name,
                game_type=ncaa_type,
                defaults={"default_score": default_score, "ordering": ordering}
            )

        for name, default_score, ordering in NFL_SCORE_TYPES:
            ScoreType.objects.get_or_create(
                name=name,
                game_type=nfl_type,
                defaults={"default_score": default_score, "ordering": ordering}
            )

    def create_teams(self, ncaa_type, nfl_type):
        for full_name, abbrev in NCAA_TEAMS:
            Team.objects.get_or_create(
                abbrev_name=abbrev,
                game_type=ncaa_type,
                defaults={"full_name": full_name}
            )

        for full_name, abbrev in NFL_TEAMS:
            Team.objects.get_or_create(
                abbrev_name=abbrev,
                game_type=nfl_type,
                defaults={"full_name": full_name}
            )

    def create_users(self):
        users = []
        for user_data in USERS:
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                defaults={"email": user_data["email"]}
            )
            if created:
                user.set_password(user_data["password"])
                if user_data["is_superuser"]:
                    user.is_superuser = True
                    user.is_staff = True
                user.save()
            users.append(user)
        return users

    def create_games(self, ncaa_type, nfl_type):
        ncaa_game, _ = NcaaGame.objects.get_or_create(
            name="March Madness 2025",
            defaults={
                "game_type": ncaa_type,
                "supports_stocks": True,
                "supports_cards": False,
            }
        )

        nfl_game, _ = NcaaGame.objects.get_or_create(
            name="NFL Season 2025",
            defaults={
                "game_type": nfl_type,
                "supports_stocks": True,
                "supports_cards": False,
            }
        )

        return ncaa_game, nfl_game

    def create_entries(self, users, ncaa_game, nfl_game):
        entries = {}
        entry_names = ["AdminEntry", "MarketMaker", "Trader1", "Trader2"]

        for user, entry_name in zip(users, entry_names):
            for game in [ncaa_game, nfl_game]:
                entry, _ = UserEntry.objects.get_or_create(
                    user=user,
                    game=game,
                    defaults={"entry_name": f"{entry_name}_{game.name[:4]}"}
                )
                entries[(user, game)] = entry

        return entries

    def create_market_maker_orders(self, mm_entries):
        """Create bid/ask orders for each team by the market maker."""
        for game, entry in mm_entries.items():
            securities = Security.objects.filter(market__game=game)

            for security in securities:
                # Generate a base price between 5 and 50
                base_price = Decimal(random.randint(5, 50))
                # Spread of 0.5 to 2.0 points
                spread = Decimal(random.randint(50, 200)) / Decimal(100)

                bid_price = base_price - spread / 2
                ask_price = base_price + spread / 2

                # Create bid order
                Order.orders.create(
                    placer=entry.entry_name,
                    entry=entry,
                    security=security,
                    quantity=random.randint(5, 20),
                    quantity_remaining=random.randint(5, 20),
                    price=bid_price.quantize(Decimal("0.01")),
                    is_buy=True,
                    is_active=True,
                )

                # Create ask order
                Order.orders.create(
                    placer=entry.entry_name,
                    entry=entry,
                    security=security,
                    quantity=random.randint(5, 20),
                    quantity_remaining=random.randint(5, 20),
                    price=ask_price.quantize(Decimal("0.01")),
                    is_buy=False,
                    is_active=True,
                )

    def create_execution_history(self, entries, ncaa_game, nfl_game, users):
        """Create 0-5 historical executions per team using crossing orders."""
        from trading.models import Execution

        # Get non-market-maker entries for trading
        traders = users[2:]  # trader1 and trader2
        mm_user = users[1]  # marketmaker

        for game in [ncaa_game, nfl_game]:
            securities = Security.objects.filter(market__game=game)
            mm_entry = entries[(mm_user, game)]
            trader_entries = [entries[(t, game)] for t in traders]

            for security in securities:
                num_executions = random.randint(0, 5)

                for _ in range(num_executions):
                    # Pick a random trader to trade with the market maker
                    trader_entry = random.choice(trader_entries)

                    # Randomly decide if trader buys or sells
                    trader_buys = random.choice([True, False])

                    # Get a price for execution
                    price = Decimal(random.randint(500, 5000)) / Decimal(100)
                    quantity = random.randint(1, 5) * 100

                    if trader_buys:
                        buy_entry = trader_entry
                        sell_entry = mm_entry
                    else:
                        buy_entry = mm_entry
                        sell_entry = trader_entry

                    # Create sell order first at the execution price
                    Order.orders.create(
                        placer=sell_entry.entry_name,
                        entry=sell_entry,
                        security=security,
                        quantity=quantity,
                        quantity_remaining=quantity,
                        price=price,
                        is_buy=False,
                        is_active=True,
                    )

                    # Create buy order at same price - this will cross and execute
                    Order.orders.create(
                        placer=buy_entry.entry_name,
                        entry=buy_entry,
                        security=security,
                        quantity=quantity,
                        quantity_remaining=quantity,
                        price=price,
                        is_buy=True,
                        is_active=True,
                    )

        # Fudge timestamps to spread executions over the past 30 days
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE trading_execution
                SET time = NOW() - (random() * INTERVAL '30 days')
            """)
