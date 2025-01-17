import random
from abc import ABC, abstractmethod
from typing import Union, Dict, Optional, List


class Board:
    def __init__(self):
        self.tiles = []
        self.initialize_board()

    def initialize_board(self):
        self.tiles: Block = [
            Block("go"),  # GO
            Street(
                name="Mediterranean Avenue",
                price=60,
                rent=[2, 10, 30, 90, 160, 250],
                mortgage=30,
                unmortgage=30,
                house_price=50,
                group="brown",
            ),
            CommunityChest(),
            Street(
                "Baltic Avenue", 60, [4, 20, 60, 180, 320, 450], 30, 30, 50, "brown"
            ),
            Tax("Income Tax", 200),
            RailRoad("Reading Railroad", 200, [25, 50, 100, 200], 100, 100),
            Street(
                "Oriental Avenue",
                100,
                [6, 30, 90, 270, 400, 550],
                50,
                50,
                50,
                "light blue",
            ),
            Chance(),
            Street(
                "Vermont Avenue",
                100,
                [6, 30, 90, 270, 400, 550],
                50,
                50,
                50,
                "light blue",
            ),
            Street(
                "Connecticut Avenue",
                120,
                [8, 40, 100, 300, 450, 600],
                60,
                60,
                50,
                "light blue",
            ),
            Block("na"),  # Jail
            Street(
                "St. Charles Place",
                140,
                [10, 50, 150, 450, 625, 750],
                70,
                70,
                100,
                "pink",
            ),
            Utility("Electric Company", 150, 0, 75, 75),
            Street(
                "States Avenue", 140, [10, 50, 150, 450, 625, 750], 70, 70, 100, "pink"
            ),
            Street(
                "Virginia Avenue",
                160,
                [12, 60, 180, 500, 700, 900],
                80,
                80,
                100,
                "pink",
            ),
            RailRoad("Pennsylvania Railroad", 200, [25, 50, 100, 200], 100, 100),
            Street(
                "St. James Place",
                180,
                [14, 70, 200, 550, 750, 950],
                90,
                90,
                100,
                "orange",
            ),
            CommunityChest(),
            Street(
                "Tennessee Avenue",
                180,
                [14, 70, 200, 550, 750, 950],
                90,
                90,
                100,
                "orange",
            ),
            Street(
                "New York Avenue",
                200,
                [16, 80, 220, 600, 800, 1000],
                100,
                100,
                100,
                "orange",
            ),
            Block("na"),  # Free Parking
            Street(
                "Kentucky Avenue",
                220,
                [18, 90, 250, 700, 875, 1050],
                110,
                110,
                150,
                "red",
            ),
            Chance(),
            Street(
                "Indiana Avenue",
                220,
                [18, 90, 250, 700, 875, 1050],
                110,
                110,
                150,
                "red",
            ),
            Street(
                "Illinois Avenue",
                240,
                [20, 100, 300, 750, 925, 1100],
                120,
                120,
                150,
                "red",
            ),
            RailRoad("B&O Railroad", 200, [25, 50, 100, 200], 100, 100),
            Street(
                "Atlantic Avenue",
                260,
                [22, 110, 330, 800, 975, 1150],
                130,
                130,
                150,
                "yellow",
            ),
            Street(
                "Ventnor Avenue",
                260,
                [22, 110, 330, 800, 975, 1150],
                130,
                130,
                150,
                "yellow",
            ),
            Utility("Water Works", 150, 0, 75, 75),
            Street(
                "Marvin Gardens",
                280,
                [24, 120, 360, 850, 1025, 1200],
                140,
                140,
                150,
                "yellow",
            ),
            Block("jail"),  # Go to Jail
            Street(
                "Pacific Avenue",
                300,
                [26, 130, 390, 900, 1100, 1275],
                150,
                150,
                200,
                "green",
            ),
            Street(
                "North Carolina Avenue",
                300,
                [26, 130, 390, 900, 1100, 1275],
                150,
                150,
                200,
                "green",
            ),
            CommunityChest(),
            Street(
                "Pennsylvania Avenue",
                320,
                [28, 150, 450, 1000, 1200, 1400],
                160,
                160,
                200,
                "green",
            ),
            RailRoad("Short Line", 200, [25, 50, 100, 200], 100, 100),
            Chance(),
            Street(
                "Park Place",
                350,
                [35, 175, 500, 1100, 1300, 1500],
                175,
                175,
                200,
                "dark blue",
            ),
            Tax("Luxury Tax", 100),
            Street(
                "Boardwalk",
                400,
                [50, 200, 600, 1400, 1700, 2000],
                200,
                200,
                200,
                "dark blue",
            ),
        ]


class Block(ABC):
    def __init__(self, type):
        self.type = type


class Chance(Block):
    def __init__(self):
        super().__init__("chance")

    @staticmethod
    def get_chance_card():
        cards = ["Advance to Go", "Bank pays you dividend of $50", "Go to Jail"]
        return random.choice(cards)


class CommunityChest(Block):
    def __init__(self):
        super().__init__("community_chest")

    @staticmethod
    def get_community_chest_card():
        # Simplified example of community chest cards
        cards = ["Doctor's fees: Pay $50", "You inherit $100", "Go to Jail"]
        return random.choice(cards)


class Player:
    def __init__(
        self, name, w_buy_building, w_buy_railroad, w_buy_utility, w_roll_double_in_jail
    ):
        self.name = name
        self.w_buy_building = w_buy_building
        self.w_buy_railroad = w_buy_railroad
        self.w_buy_utility = w_buy_utility
        self.w_roll_double_in_jail = w_roll_double_in_jail
        self.tries_in_jail = 3
        self.consecutive_doubles = 0
        self.is_in_jail = False
        self.cash = 1500
        self.total_assets = 1500
        self.streets: Dict[str, List[Street]] = {}
        self.railroads = []
        self.utilities = []
        self.in_game = True
        self.position = 0

    def should_buy(self, property_type):
        if property_type == "building":
            return random.random() < self.w_buy_building
        elif property_type == "railroad":
            return random.random() < self.w_buy_railroad
        elif property_type == "utility":
            return random.random() < self.w_buy_utility
        return False

    def buy_property(self, property: "Property"):
        self.cash -= property.price
        self.total_assets -= property.price
        if isinstance(property, Street):
            if property.group not in self.streets:
                self.streets[property.group] = []
            self.streets[property.group].append(property)
        elif isinstance(property, RailRoad):
            self.railroads.append(property)
        elif isinstance(property, Utility):
            self.utilities.append(property)
        self.total_assets += property.mortgage

    def get_valid_expandable_sets(self):
        """Get a dictionary of all the compeleted sets that still have capacity to build houses on"""
        sets: Dict[str, List[Street]] = {}
        for group, properties in self.streets.items():
            if len(properties) == 3 and not all(prop.level == 6 for prop in properties):
                sets[group] = properties
        sorted_sets = dict(
            sorted(
                sets.items(),
                key=lambda item: (
                    sum(prop.level for prop in item[1]),
                    min(prop.house_price for prop in item[1]),
                ),
            )
        )
        return sorted_sets

    def buy_house(self, property: "Street"):
        property.level += 1
        self.cash -= property.house_price
        self.total_assets -= property.house_price
        self.total_assets += property.house_price // 2

    def get_streets_with_houses(self):
        return [
            property
            for _group, properties in self.streets.items()
            if len(properties) == 3
            for property in properties
            if property.level >= 2
        ]

    def raise_fund(self, amount):
        """This is one a hell of a function. It tries to raise funds by
        1. Selling houses based on the cheapest house prices
        2. Mortgaging properties with the least number of houses owned in the group and the cheapest price to mortgage
        NOTE: It is assumed this function is only called if it is actually possible to achieve amount
        """
        if self.cash >= amount:
            return

        def raise_fund_by_selling_houses():
            streets_with_houses = self.get_streets_with_houses()
            streets_with_houses = sorted(
                streets_with_houses,
                key=lambda property: property.house_price,
                reverse=True,
            )

            while self.cash < amount and streets_with_houses:
                property = streets_with_houses[-1]
                self.cash += property.house_price // 2
                self.total_assets -= property.house_price // 2
                property.level -= 1
                if property.level == 1:
                    streets_with_houses.pop()

        def raise_fund_by_mortgaging_properties():
            property_frequency: Dict[int, List[Property]] = {}
            for _group, properties in self.streets.items():
                if len(properties) not in property_frequency:
                    property_frequency[len(properties)] = []
                property_frequency[len(properties)].extend(properties)
            if len(self.railroads) not in property_frequency:
                property_frequency[len(self.railroads)] = []
            property_frequency[len(self.railroads)].extend(self.railroads)
            if len(self.utilities) not in property_frequency:
                property_frequency[len(self.utilities)] = []
            property_frequency[len(self.utilities)].extend(self.utilities)

            property_frequency = dict(
                sorted(
                    property_frequency.items(),
                    key=lambda item: (
                        item[0],
                        min(property.mortgage for property in item[1]),
                    ),
                )
            )
            while self.cash < amount and property_frequency:
                for _freq, properties in property_frequency.items():
                    for property in properties:
                        if not property.mortgaged:
                            self.cash += property.mortgage
                            self.total_assets -= property.mortgage
                            property.mortgaged = True
                        if self.cash >= amount:
                            return

        raise_fund_by_selling_houses()
        if self.cash >= amount:
            return

        raise_fund_by_mortgaging_properties()

    def update_position(self, steps, board_size):
        self.position = (self.position + steps) % (board_size)

    def go_to_jail(self):
        self.is_in_jail = True
        self.position = 10

    def pay_rent(self, rent):
        if self.cash < rent:
            self.in_game = False
        else:
            self.cash -= rent


class Tax(Block):
    def __init__(self, name, amount):
        super().__init__("tax")
        self.name = name
        self.amount = amount

    def apply_tax(self, player: Player):
        player.cash -= self.amount
        if player.cash < 0:
            player.in_game = False


class Property(Block):
    def __init__(self, name, price, rent, mortgage, unmortgage):
        super().__init__("property")
        self.name = name
        self.price = price
        self.rent = rent
        self.mortgage = self.price // 2
        self.unmortgage = self.mortgage * 1.1
        self.mortgaged = False
        self.owner: Optional[Player] = None

    @abstractmethod
    def calculate_rent(self):
        pass


class Street(Property):
    def __init__(self, name, price, rent, mortgage, unmortgage, house_price, group):
        super().__init__(name, price, rent, mortgage, unmortgage)
        self.house_price = house_price
        self.group = group
        # level 0 - normal rent
        # level 1 - all cards owned
        # level 2:5 - houses 1 to 4
        # level 6 - hotel
        self.level = 0

    def calculate_rent(self, player):
        if self.owner is None:
            return 0
        if self.mortgaged == True:
            return 0
        if self.owner == player:
            return 0
        return self.rent[self.level]


class Utility(Property):
    def __init__(self, name, price, rent, mortgage, unmortgage):
        super().__init__(name, price, rent, mortgage, unmortgage)

    def calculate_rent(self, dice_roll, player):
        if self.owner is None:
            return 0
        if self.mortgaged == True:
            return 0
        if self.owner == player:
            return 0
        return dice_roll * (10 if len(self.owner.utilities) == 2 else 4)


class RailRoad(Property):
    def __init__(self, name, price, rent, mortgage, unmortgage):
        super().__init__(name, price, rent, mortgage, unmortgage)

    def calculate_rent(self, player):
        if self.owner is None:
            return 0
        if self.mortgaged == True:
            return 0
        if self.owner == player:
            return 0
        railroads_owned = len(self.owner.railroads)
        return self.rent[railroads_owned - 1]


class Game:
    def __init__(self, p1, p2, p3=None, p4=None):
        self.board = Board()
        self.players = [p1, p2]
        if p3:
            self.players.append(p3)
        if p4:
            self.players.append(p4)
        self.current_player_index = 0

    def roll_dice(self):
        return random.randint(1, 6), random.randint(1, 6)

    def _player_in_jail(self, player: Player):
        # Roll dice to attempt a double
        d1, d2 = self.roll_dsice()

        if (
            player.tries_in_jail > 0 and random.random() < player.w_roll_double_in_jail
        ):  # Player can try rolling for doubles
            if d1 == d2:  # Rolled a double, release player
                player.is_in_jail = False
                player.tries_in_jail = 3  # Reset tries for next jail visit
                return d1, d2
            else:  # Failed to roll a double
                player.tries_in_jail -= 1
                return -1, -1  # Indicates no movement this turn
        else:  # No tries left, or the player just didn't want to role a double; deduct $50 fine
            player.cash -= 50
            player.is_in_jail = False
            player.tries_in_jail = 3  # Reset tries for next jail visit
            return d1, d2

    def play_turn(self):
        player: Player = self.players[self.current_player_index]
        if not player.in_game:
            self.next_player()
            return

        d1, d2 = 0, 0

        if player.is_in_jail:
            d1, d2 = self._player_in_jail(player)
        else:
            d1, d2 = self.roll_dice()

        # Proceed with normal movement if dice rolled successfully
        if d1 > 0 and d2 > 0:
            player.update_position(d1 + d2, len(self.board.tiles))
            self.handle_landing(player)
            self.handle_houses_and_hotels(player)

        if d1 != d2:  # No extra turn unless doubles rolled
            player.consecutive_doubles = 0
            self.next_player()
        else:
            player.consecutive_doubles += 1
            if player.consecutive_doubles == 3:
                player.consecutive_doubles = 0
                player.go_to_jail()

    def handle_landing(self, player: Player):
        current_tile: Block = self.board.tiles[player.position]

        if current_tile.type == "jail":
            player.go_to_jail()
        elif current_tile.type == "go":
            player.cash += 200

        elif isinstance(current_tile, Property):
            if current_tile.owner is None and player.cash >= current_tile.price:
                if player.should_buy(current_tile.type):
                    player.cash -= current_tile.price
                    player.properties.append(current_tile)
                    current_tile.owner = player
            elif current_tile.owner is not None and current_tile.owner != player:
                rent = current_tile.calculate_rent()
                player.pay_rent(rent)

        elif isinstance(current_tile, Tax):
            current_tile.apply_tax(player)

        elif isinstance(current_tile, Chance):
            card = current_tile.get_chance_card()
            print(f"Chance Card: {card}")
            if card == "Advance to Go":
                player.position = 0
                player.cash += 200  # Collect $200 for passing GO
            elif card == "Bank pays you dividend of $50":
                player.cash += 50
            elif card == "Go to Jail":
                player.go_to_jail()

        elif isinstance(current_tile, CommunityChest):
            card = current_tile.get_community_chest_card()
            print(f"Community Chest Card: {card}")
            if card == "Doctor's fees: Pay $50":
                player.cash -= 50
                if player.cash < 0:
                    player.in_game = False
            elif card == "You inherit $100":
                player.cash += 100
            elif card == "Go to Jail":
                player.go_to_jail()

    def handle_houses_and_hotels(self, player: Player):
        # Group properties by set
        sets_owned = {}
        for property in player.properties:
            if isinstance(property, Street):
                if property.group not in sets_owned:
                    sets_owned[property.group] = []
                sets_owned[property.group].append(property)

        # Filter to include only complete sets owned by the player
        complete_sets = {
            group: properties
            for group, properties in sets_owned.items()
            if len(properties)
            == len(
                [
                    t
                    for t in self.board.tiles
                    if isinstance(t, Street) and t.group == group
                ]
            )
        }

        # Sort sets by least houses and then by cheapest house price
        sorted_sets = sorted(
            complete_sets.items(),
            key=lambda x: (
                min(p.houses for p in x[1]),
                min(p.house_price for p in x[1]),
            ),
        )

        # Attempt to build houses or hotels
        for group, properties in sorted_sets:
            while player.cash > 0:
                # Find property with the fewest houses in the set
                min_houses = min(p.houses for p in properties)
                target_properties = [p for p in properties if p.houses == min_houses]

                # Build one house on each property with the least houses, if affordable
                built = False
                for prop in target_properties:
                    if player.cash >= prop.house_price:
                        player.cash -= prop.house_price
                        prop.houses += 1
                        built = True
                    else:
                        return  # Stop if player cannot afford any more houses
                if not built:
                    break

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def check_win_condition(self):
        active_players = [p for p in self.players if p.in_game]
        return len(active_players) == 1

    def simulate_game(self):
        while not self.check_win_condition():
            self.play_turn()
        winner = [p for p in self.players if p.in_game][0]
        return winner


class MonteCarloSimulation:
    def __init__(self, runs):
        self.runs = runs

    def run(self):
        win_count = {}
        for i in range(self.runs):
            players = [
                Player("Player 1", 0.8, 0.7, 0.6, 0.5),
                Player("Player 2", 0.6, 0.8, 0.7, 0.4),
                Player("Player 3", 0.7, 0.6, 0.8, 0.6),
                Player("Player 4", 0.5, 0.5, 0.5, 0.5),
            ]
            game = Game(players)
            winner = game.simulate_game()
            if winner.name not in win_count:
                win_count[winner.name] = 0
            win_count[winner.name] += 1

        return win_count


# Running the Monte Carlo simulation
simulation = MonteCarloSimulation(10000)
results = simulation.run()
print("Win counts:", results)
