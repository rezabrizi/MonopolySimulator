import random
import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from typing import Dict, Optional, List, Tuple, Union
from enum import Enum
from collections import deque

# We'll keep a global (or module-level) logger list. Every method appends
# to this list with a message. At the end, we write it out to a file.
GAME_LOGS = []


class Board:
    def __init__(self):
        GAME_LOGS.append("Initializing Board...")
        self.tiles = []
        self.initialize_board()

    def initialize_board(self):
        GAME_LOGS.append("Board.initialize_board() called.")
        self.tiles: list[Block] = [
            Block(type="go", number=1),  # GO
            Street(
                name="Mediterranean Avenue",
                group=StreetGroups.BROWN,
                price=60,
                rent=[2, 4, 10, 30, 90, 250],  # Regular, All owned, 1-4 houses, hotel
                house_price=50,
                number=2,
            ),
            CommunityChest(number=3),
            Street(
                name="Baltic Avenue",
                group=StreetGroups.BROWN,
                price=60,
                rent=[4, 8, 20, 60, 180, 450],
                house_price=50,
                number=4,
            ),
            Tax(name="Income Tax", amount=200, number=5),
            RailRoad(
                name="Reading Railroad",
                price=200,
                rent=[25, 50, 100, 200],  # Rent for 1-4 railroads owned
                number=6,
            ),
            Street(
                name="Oriental Avenue",
                group=StreetGroups.LIGHT_BLUE,
                price=100,
                rent=[6, 12, 30, 90, 270, 550],
                house_price=50,
                number=7,
            ),
            Chance(number=8),
            Street(
                name="Vermont Avenue",
                group=StreetGroups.LIGHT_BLUE,
                price=100,
                rent=[6, 12, 30, 90, 270, 550],
                house_price=50,
                number=9,
            ),
            Street(
                name="Connecticut Avenue",
                group=StreetGroups.LIGHT_BLUE,
                price=120,
                rent=[8, 16, 40, 100, 300, 600],
                house_price=50,
                number=10,
            ),
            Block(type="jail", number=11),  # Jail
            Street(
                name="St. Charles Place",
                group=StreetGroups.PINK,
                price=140,
                rent=[10, 20, 50, 150, 450, 750],
                house_price=100,
                number=12,
            ),
            Utility(name="Electric Company", price=150, number=13),
            Street(
                name="States Avenue",
                group=StreetGroups.PINK,
                price=140,
                rent=[10, 20, 50, 150, 450, 750],
                house_price=100,
                number=14,
            ),
            Street(
                name="Virginia Avenue",
                group=StreetGroups.PINK,
                price=160,
                rent=[12, 24, 60, 180, 500, 900],
                house_price=100,
                number=15,
            ),
            RailRoad(
                name="Pennsylvania Railroad",
                price=200,
                rent=[25, 50, 100, 200],
                number=16,
            ),
            Street(
                name="St. James Place",
                group=StreetGroups.ORANGE,
                price=180,
                rent=[14, 28, 70, 200, 550, 950],
                house_price=100,
                number=17,
            ),
            CommunityChest(number=18),
            Street(
                name="Tennessee Avenue",
                group=StreetGroups.ORANGE,
                price=180,
                rent=[14, 28, 70, 200, 550, 950],
                house_price=100,
                number=19,
            ),
            Street(
                name="New York Avenue",
                group=StreetGroups.ORANGE,
                price=200,
                rent=[16, 32, 80, 220, 600, 1000],
                house_price=100,
                number=20,
            ),
            Block(type="free_parking", number=21),  # Free Parking
            Street(
                name="Kentucky Avenue",
                group=StreetGroups.RED,
                price=220,
                rent=[18, 36, 90, 250, 700, 1050],
                house_price=150,
                number=22,
            ),
            Chance(number=23),
            Street(
                name="Indiana Avenue",
                group=StreetGroups.RED,
                price=220,
                rent=[18, 36, 90, 250, 700, 1050],
                house_price=150,
                number=24,
            ),
            Street(
                name="Illinois Avenue",
                group=StreetGroups.RED,
                price=240,
                rent=[20, 40, 100, 300, 750, 1100],
                house_price=150,
                number=25,
            ),
            RailRoad(
                name="B&O Railroad",
                price=200,
                rent=[25, 50, 100, 200],
                number=26,
            ),
            Street(
                name="Atlantic Avenue",
                group=StreetGroups.YELLOW,
                price=260,
                rent=[22, 44, 110, 330, 800, 1150],
                house_price=150,
                number=27,
            ),
            Street(
                name="Ventnor Avenue",
                group=StreetGroups.YELLOW,
                price=260,
                rent=[22, 44, 110, 330, 800, 1150],
                house_price=150,
                number=28,
            ),
            Utility(name="Water Works", price=150, number=29),
            Street(
                name="Marvin Gardens",
                group=StreetGroups.YELLOW,
                price=280,
                rent=[24, 48, 120, 360, 850, 1200],
                house_price=150,
                number=30,
            ),
            Block(type="go_to_jail", number=31),  # Go to Jail
            Street(
                name="Pacific Avenue",
                group=StreetGroups.GREEN,
                price=300,
                rent=[26, 52, 130, 390, 900, 1275],
                house_price=200,
                number=32,
            ),
            Street(
                name="North Carolina Avenue",
                group=StreetGroups.GREEN,
                price=300,
                rent=[26, 52, 130, 390, 900, 1275],
                house_price=200,
                number=33,
            ),
            CommunityChest(number=34),
            Street(
                name="Pennsylvania Avenue",
                group=StreetGroups.GREEN,
                price=320,
                rent=[28, 56, 150, 450, 1000, 1400],
                house_price=200,
                number=35,
            ),
            RailRoad(
                name="Short Line",
                price=200,
                rent=[25, 50, 100, 200],
                number=36,
            ),
            Chance(number=37),
            Street(
                name="Park Place",
                group=StreetGroups.DARK_BLUE,
                price=350,
                rent=[35, 70, 175, 500, 1100, 1500],
                house_price=200,
                number=38,
            ),
            Tax(name="Luxury Tax", amount=100, number=39),
            Street(
                name="Boardwalk",
                group=StreetGroups.DARK_BLUE,
                price=400,
                rent=[50, 100, 200, 600, 1400, 2000],
                house_price=200,
                number=40,
            ),
        ]


class ChanceCards(Enum):
    ADVANCE_TO_GO = "Advance to Go (Collect $200)"
    BANK_DIVIDEND = "Bank pays you dividend of $50"
    GO_TO_JAIL = (
        "Go to Jail - Go directly to Jail - Do not pass Go - Do not collect $200"
    )
    ADVANCE_TO_ILLINOIS = "Advance to Illinois Ave. - If you pass Go, collect $200"
    ADVANCE_TO_ST_CHARLES = (
        "Advance to St. Charles Place - If you pass Go, collect $200"
    )
    NEAREST_UTILITY = "Advance token to the nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total ten times the amount thrown."
    NEAREST_RAILROAD = "Advance token to the nearest Railroad and pay owner twice the rental to which they are otherwise entitled. If Railroad is unowned, you may buy it from the Bank."
    READING_RAILROAD = "Take a trip to Reading Railroad - If you pass Go, collect $200"
    BOARDWALK = "Take a walk on the Boardwalk - Advance token to Boardwalk"
    CHAIRMAN = "Elected Chairman of the Board - Pay each player $50"
    BUILDING_LOAN = "Your building loan matures - Collect $150"
    STREET_REPAIRS = (
        "You have been assessed for street repairs - $40 per house, $115 per hotel"
    )
    POOR_TAX = "Pay poor tax of $15"
    GENERAL_REPAIRS = "Make general repairs on all your property - For each house pay $25, for each hotel pay $100"
    GET_OUT_OF_JAIL_FREE = (
        "Get out of Jail Free - This card may be kept until needed, or sold"
    )
    GO_BACK_THREE = "Go back three spaces"


class CommunityChestCards(Enum):
    ADVANCE_TO_GO = "Advance to Go (Collect $200)"
    BANK_ERROR = "Bank error in your favor - Collect $200"
    DOCTOR_FEE = "Doctor's fee - Pay $50"
    STOCK_SALE = "From sale of stock, you get $50"
    GO_TO_JAIL = (
        "Go to Jail - Go directly to Jail - Do not pass Go - Do not collect $200"
    )
    GET_OUT_OF_JAIL_FREE = (
        "Get out of Jail Free - This card may be kept until needed, or sold"
    )
    HOLIDAY_FUND = "Holiday fund matures - Receive $100"
    INCOME_TAX_REFUND = "Income tax refund - Collect $20"
    BIRTHDAY = "It is your birthday - Collect $10 from every player"
    LIFE_INSURANCE = "Life insurance matures - Collect $100"
    HOSPITAL_FEES = "Pay hospital fees of $100"
    SCHOOL_FEES = "Pay school fees of $50"
    CONSULTANCY_FEE = "Receive $25 consultancy fee"
    STREET_REPAIRS = (
        "You are assessed for street repairs - $40 per house, $115 per hotel"
    )
    BEAUTY_CONTEST = "You have won second prize in a beauty contest - Collect $10"
    INHERITANCE = "You inherit $100"


class Block(ABC):
    def __init__(self, type, number):
        self.type = type
        self.number = number
        GAME_LOGS.append(f"Created Block: {self.type}, number={self.number}")


class Chance(Block):
    chance_deque = deque([chance for chance in ChanceCards])

    def __init__(self, number):
        super().__init__("chance", number)

    @classmethod
    def get_chance_card(cls):
        card = cls.chance_deque.pop()
        GAME_LOGS.append(f"Chance Card Drawn: {card.value}")
        if card != ChanceCards.GET_OUT_OF_JAIL_FREE:
            cls.chance_deque.appendleft(card)
        return card

    @classmethod
    def put_jail_free_card_back(cls):
        GAME_LOGS.append("Putting Chance Jail Free Card back on top of deck.")
        cls.chance_deque.appendleft(ChanceCards.GET_OUT_OF_JAIL_FREE)


class CommunityChest(Block):
    community_chest_deque = deque(
        [community_chest for community_chest in CommunityChestCards]
    )

    def __init__(self, number):
        super().__init__("community_chest", number)

    @classmethod
    def get_community_chest_card(cls):
        card = cls.community_chest_deque.pop()
        GAME_LOGS.append(f"Community Chest Card Drawn: {card.value}")
        if card != CommunityChestCards.GET_OUT_OF_JAIL_FREE:
            cls.community_chest_deque.appendleft(card)
        return card

    @classmethod
    def put_jail_free_card_back(cls):
        GAME_LOGS.append("Putting Community Chest Jail Free Card back on top of deck.")
        cls.community_chest_deque.appendleft(CommunityChestCards.GET_OUT_OF_JAIL_FREE)


class Tax(Block):
    def __init__(self, name, amount, number):
        super().__init__("tax", number)
        self.name = name
        self.amount = amount

    def apply_tax(self, player: "Player"):
        GAME_LOGS.append(
            f"{player.name} landed on Tax: {self.name}, must pay {self.amount}"
        )
        player.pay(self.amount)


class Property(Block):
    def __init__(self, name, price, number):
        super().__init__("property", number=number)
        self.name = name
        self.price = price
        self.mortgage = self.price // 2
        self.unmortgage = self.mortgage * 1.1
        self.mortgaged = False
        self.owner: Optional["Player"] = None

    @abstractmethod
    def calculate_rent(self):
        pass


class Utility(Property):
    def __init__(self, name, price, number):
        super().__init__(name, price, number)

    def calculate_rent(self, dice_roll, player):
        if self.owner is None or self.mortgaged or self.owner == player:
            return 0
        rent_val = dice_roll * (10 if len(self.owner.utilities) == 2 else 4)
        GAME_LOGS.append(f"Utility rent calculated: {rent_val} (dice={dice_roll})")
        return rent_val


class RailRoad(Property):
    def __init__(self, name: str, price: int, rent: List[int], number: int):
        super().__init__(name, price, number)
        self.rent = rent

    def calculate_rent(self, player):
        if self.owner is None or self.mortgaged or self.owner == player:
            return 0
        railroads_owned = len(self.owner.railroads)
        rent_val = self.rent[railroads_owned - 1]
        GAME_LOGS.append(
            f"Railroad rent calculated: {rent_val} (RRs owned={railroads_owned})"
        )
        return rent_val


class StreetGroups(Enum):
    BROWN = "Brown"
    LIGHT_BLUE = "Light Blue"
    PINK = "Pink"
    ORANGE = "Orange"
    RED = "Red"
    YELLOW = "Yellow"
    GREEN = "Green"
    DARK_BLUE = "Dark Blue"


class Street(Property):
    GROUP_COUNTS = {
        StreetGroups.BROWN: 2,
        StreetGroups.LIGHT_BLUE: 3,
        StreetGroups.PINK: 3,
        StreetGroups.ORANGE: 3,
        StreetGroups.RED: 3,
        StreetGroups.YELLOW: 3,
        StreetGroups.GREEN: 3,
        StreetGroups.DARK_BLUE: 2,
    }

    def __init__(
        self,
        name: str,
        group: StreetGroups,
        price: int,
        rent: List[int],
        house_price: int,
        number: int,
    ):
        super().__init__(name, price, number)
        self.house_price = house_price
        self.group = group
        self.rent = rent
        self.level = 0  # 0=normal,1=own group,2..5=houses,5=full houses, or so

    def __repr__(self):
        return (
            f"Street(name='{self.name}', group='{self.group.name}', price={self.price}, "
            f"rent={self.rent}, house_price={self.house_price}, level={self.level}, "
            f"mortgaged={self.mortgaged}, owner={self.owner.name if self.owner else None})"
        )

    def calculate_rent(self, player):
        if self.owner is None or self.mortgaged or self.owner == player:
            return 0
        rent_val = self.rent[self.level]
        GAME_LOGS.append(f"Street rent calculated: {rent_val} (level={self.level})")
        return rent_val


class Bank:
    def __init__(self):
        GAME_LOGS.append("Bank created.")

    def earn(self, amount):
        # The bank in Monopoly doesn't exactly "track" its money, so no effect.
        GAME_LOGS.append(
            f"Bank earned {amount}, but bank funds are unlimited in normal Monopoly."
        )


class Player:
    def __init__(
        self,
        name,
        w_buy_building,
        w_buy_railroad,
        w_buy_utility,
        w_roll_double_in_jail,
        w_use_jail_free_card,
        min_cash,
        min_cash_to_unmortgage,
    ):
        self.name: str = name
        self.w_buy_building: float = w_buy_building
        self.w_buy_railroad: float = w_buy_railroad
        self.w_buy_utility: float = w_buy_utility
        self.w_use_jail_free_card: float = w_use_jail_free_card
        self.w_roll_double_in_jail: float = w_roll_double_in_jail
        self.min_cash: int = min_cash
        self.min_cash_to_unmortgage: int = min_cash_to_unmortgage
        self.jail_roll_attempts: int = 0
        self.consecutive_doubles: int = 0
        self.is_in_jail: bool = False
        self.cash: int = 1500
        self.streets: Dict[str, List[Street]] = {}
        self.railroads: List[RailRoad] = []
        self.utilities: List[Utility] = []
        self.is_in_game: bool = True
        self.position: int = 0
        self.last_dice_roll: int = 0
        self.community_chest_jail_free_card: bool = False
        self.chance_jail_free_card: bool = False

        GAME_LOGS.append(f"Created Player {self.name} with ${self.cash}.")

    def __repr__(self):
        return (
            f"P('{self.name}', cash={self.cash}, position={self.position}, "
            f"is_in_jail={self.is_in_jail}, jail_roll_attempts={self.jail_roll_attempts}, "
            f"streets_owned={len(self.streets)}, railroads_owned={len(self.railroads)}, "
            f"utilities_owned={len(self.utilities)}, is_in_game={self.is_in_game})"
        )

    def has_jail_free_card(self) -> bool:
        return self.community_chest_jail_free_card or self.chance_jail_free_card

    def decide_to_use_jail_free_card(self) -> bool:
        val = random.random() < self.w_use_jail_free_card
        GAME_LOGS.append(f"{self.name} deciding to use Jail Free Card: {val}")
        return val

    def use_jail_free_card(self) -> None:
        if self.chance_jail_free_card:
            GAME_LOGS.append(f"{self.name} used CHANCE Jail Free Card.")
            self.chance_jail_free_card = False
            Chance.put_jail_free_card_back()
        elif self.community_chest_jail_free_card:
            GAME_LOGS.append(f"{self.name} used COMMUNITY CHEST Jail Free Card.")
            self.community_chest_jail_free_card = False
            CommunityChest.put_jail_free_card_back()
        else:
            raise Exception(
                "Should only call this when the player has a jail free card"
            )

    def reset_jail_roll_attempts(self):
        GAME_LOGS.append(
            f"{self.name} reset jail roll attempts from {self.jail_roll_attempts} to 0."
        )
        self.jail_roll_attempts = 0

    def decide_to_roll_for_doubles(self) -> bool:
        val = random.random() < self.w_roll_double_in_jail
        GAME_LOGS.append(f"{self.name} deciding to roll for doubles: {val}")
        return val

    def advance_to_illinois(self) -> None:
        GAME_LOGS.append(f"{self.name} advanced to Illinois Ave.")
        if self.position > 24:
            self.earn(200)
        self.position = 24

    def advance_to_st_charles(self) -> None:
        GAME_LOGS.append(f"{self.name} advanced to St. Charles Place.")
        if self.position > 11:
            self.earn(200)
        self.position = 11

    def advance_to_nearest_utility(self):
        GAME_LOGS.append(f"{self.name} advanced to nearest Utility.")
        if self.position < 12:
            self.position = 12
        else:
            self.position = 28

    def advance_to_nearest_railroad(self):
        GAME_LOGS.append(f"{self.name} advanced to nearest Railroad.")
        # Replaced the multiple if's with if/elif to avoid skipping to 35 each time:
        if self.position < 5 or self.position > 35:
            self.position = 5
        elif self.position < 15:
            self.position = 15
        elif self.position < 25:
            self.position = 25
        elif self.position < 35:
            self.position = 35

    def advance_to_reading_railroad(self):
        GAME_LOGS.append(f"{self.name} advanced to Reading Railroad.")
        if self.position > 5:
            self.earn(200)
        self.position = 5

    def advance_to_go(self):
        GAME_LOGS.append(f"{self.name} advanced to GO, collecting 200.")
        self.position = 0
        self.earn(200)

    def advance_to_boardwalk(self):
        GAME_LOGS.append(f"{self.name} advanced to Boardwalk.")
        self.position = 39

    def determine_street_repair_fee(self):
        total = 0
        for _group, streets in self.streets.items():
            for street in streets:
                if street.level == 5:
                    total += 115
                elif street.level >= 2:
                    num_houses = street.level - 1
                    total += 40 * num_houses
        GAME_LOGS.append(f"{self.name} must pay a street repair fee of {total}.")
        return total

    def determine_general_repair_fee(self):
        total = 0
        for _group, streets in self.streets.items():
            for street in streets:
                if street.level == 5:
                    total += 100
                elif street.level >= 2:
                    num_houses = street.level - 1
                    total += 25 * num_houses
        GAME_LOGS.append(f"{self.name} must pay a general repair fee of {total}.")
        return total

    def go_back_three(self, board_size: int):
        oldpos = self.position
        self.position = (self.position - 3 + board_size) % board_size
        GAME_LOGS.append(
            f"{self.name} goes back 3 spaces from {oldpos} to {self.position}."
        )

    def get_valid_expandable_sets(self) -> Dict[str, List[Street]]:
        sets: Dict[str, List[Street]] = {}
        for group, properties in self.streets.items():
            if (
                len(properties) == Street.GROUP_COUNTS[group]
                and not all(prop.level == 5 for prop in properties)
                and all(not prop.mortgaged for prop in properties)
            ):
                sets[group] = properties
        return sets

    def buy_houses_and_hotels(self, priority: str = "quantity_price"):
        from random import shuffle

        GAME_LOGS.append(
            f"{self.name} is attempting to buy houses/hotels with priority={priority}."
        )
        completed_sets = self.get_valid_expandable_sets()

        def get_groups_based_on_random():
            groups = list(completed_sets.keys())
            shuffle(groups)
            return groups

        def get_groups_based_on_house_quantity_price_priority():
            groups = [
                item[0]
                for item in sorted(
                    completed_sets.items(),
                    key=lambda item: (
                        sum(prop.level for prop in item[1]),
                        min(prop.house_price for prop in item[1]),
                    ),
                )
            ]
            return groups

        if priority == "random":
            groups = get_groups_based_on_random()
        elif priority == "quantity_price":
            groups = get_groups_based_on_house_quantity_price_priority()
        else:
            raise ValueError("Invalid priority. Use 'random' or 'quantity_price'.")

        while self.cash > self.min_cash:
            built_any = False
            for group in groups:
                properties = completed_sets[group]
                min_level = min(prop.level for prop in properties)
                if min_level == 5:
                    continue
                target_props = [pr for pr in properties if pr.level == min_level]
                for pr in target_props:
                    if self.cash - pr.house_price >= self.min_cash:
                        GAME_LOGS.append(
                            f"{self.name} buys a house on {pr.name} for {pr.house_price}."
                        )
                        self.buy_house(pr)
                        built_any = True
                    else:
                        GAME_LOGS.append(
                            f"{self.name} cannot afford a house on {pr.name}."
                        )
                        break
            if not built_any:
                break

    def unmortgage_properties(self):
        GAME_LOGS.append(f"{self.name} attempts to unmortgage properties.")
        mortgaged_groups = {
            group: props
            for group, props in self.streets.items()
            if any(prop.mortgaged for prop in props)
        }
        sorted_groups = sorted(
            mortgaged_groups.items(),
            key=lambda item: len(item[1]),
            reverse=True,
        )

        for group, props in sorted_groups:
            for pr in props:
                if (
                    pr.mortgaged
                    and self.cash - pr.unmortgage >= self.min_cash_to_unmortgage
                ):
                    GAME_LOGS.append(
                        f"{self.name} unmortgages {pr.name} for {pr.unmortgage}."
                    )
                    self.cash -= pr.unmortgage
                    pr.mortgaged = False

    def transfer_ownership_of_all_assets_to_another_player(self, other: "Player"):
        GAME_LOGS.append(f"{self.name} is transferring all assets to {other.name}.")
        other.earn(self.cash)
        self.cash = 0

        for group, streets in self.streets.items():
            for st in streets:
                st.owner = other
                other.receive_street(st)
        self.streets.clear()

        while self.railroads:
            rr = self.railroads.pop()
            rr.owner = other
            other.railroads.append(rr)

        while self.utilities:
            ut = self.utilities.pop()
            ut.owner = other
            other.utilities.append(ut)

        if self.community_chest_jail_free_card:
            GAME_LOGS.append(
                f"{self.name} also gives COMMUNITY CHEST Jail Free card to {other.name}."
            )
            other.community_chest_jail_free_card = True
        if self.chance_jail_free_card:
            GAME_LOGS.append(
                f"{self.name} also gives CHANCE Jail Free card to {other.name}."
            )
            other.chance_jail_free_card = True

    def transfer_ownership_of_all_assets_to_the_bank(self, to: Bank):
        GAME_LOGS.append(f"{self.name} is transferring all assets back to the Bank.")
        self.cash = 0
        for group, streets in self.streets.items():
            for st in streets:
                st.owner = None
        self.streets.clear()
        while self.railroads:
            rr = self.railroads.pop()
            rr.owner = None
        while self.utilities:
            ut = self.utilities.pop()
            ut.owner = None
        if self.community_chest_jail_free_card:
            GAME_LOGS.append(
                f"{self.name} returns COMMUNITY CHEST Jail Free card to deck."
            )
            CommunityChest.put_jail_free_card_back()
        if self.chance_jail_free_card:
            GAME_LOGS.append(f"{self.name} returns CHANCE Jail Free card to deck.")
            Chance.put_jail_free_card_back()

    def receive_street(self, street: Street) -> None:
        if street.group not in self.streets:
            self.streets[street.group] = []
        self.streets[street.group].append(street)

    def transfer_ownership_of_all_assets(self, to: Union["Player", Bank]):
        if isinstance(to, Player):
            self.transfer_ownership_of_all_assets_to_another_player(to)
        elif isinstance(to, Bank):
            self.transfer_ownership_of_all_assets_to_the_bank(to)

    def pay(self, amount, to: Union["Player", Bank]):
        GAME_LOGS.append(f"{self.name} must pay {amount} to {to.__class__.__name__}.")
        if self.cash < amount:
            self.raise_fund(amount=amount)
        if self.cash < amount:
            GAME_LOGS.append(f"{self.name} cannot pay and is going bankrupt!")
            self.is_in_game = False
            self.transfer_ownership_of_all_assets(to)
            return
        GAME_LOGS.append(
            f"{self.name} pays {amount}. Remaining cash={self.cash - amount}."
        )
        self.cash -= amount
        to.earn(amount=amount)

    def earn(self, amount: int):
        GAME_LOGS.append(f"{self.name} earns {amount}. Old cash={self.cash}.")
        self.cash += amount

    def decide_to_buy_property_random(
        self, property: Union[Street, RailRoad, Utility]
    ) -> bool:
        val = False
        if isinstance(property, Street):
            val = random.random() < self.w_buy_building
        elif isinstance(property, RailRoad):
            val = random.random() < self.w_buy_railroad
        elif isinstance(property, Utility):
            val = random.random() < self.w_buy_utility
        GAME_LOGS.append(f"{self.name} random buy-decision for {property.name}: {val}")
        return val

    def decide_to_buy_property(self, property: Union[Street, RailRoad, Utility]):
        if self.cash - property.price < self.min_cash:
            GAME_LOGS.append(
                f"{self.name} cannot buy {property.name}, not enough cash after min_cash check."
            )
            return False
        return self.decide_to_buy_property_random(property)

    def buy_property(self, property: "Property"):
        if property.owner is not None:
            return
        GAME_LOGS.append(f"{self.name} buys {property.name} for {property.price}.")
        self.cash -= property.price
        property.owner = self
        if isinstance(property, Street):
            if property.group not in self.streets:
                self.streets[property.group] = []
            self.streets[property.group].append(property)
            # If this completes a set of 3 for that color, set all to level=1
            if len(self.streets[property.group]) == Street.GROUP_COUNTS[property.group]:
                for st in self.streets[property.group]:
                    st.level = 1
                GAME_LOGS.append(
                    f"{self.name} now owns the full set for {property.group.name}; all set to level=1."
                )
        elif isinstance(property, RailRoad):
            self.railroads.append(property)
        elif isinstance(property, Utility):
            self.utilities.append(property)

    def buy_house(self, property: "Street"):
        GAME_LOGS.append(
            f"{self.name} is buying a house on {property.name}, cost {property.house_price}."
        )
        property.level += 1
        self.cash -= property.house_price

    def get_streets_with_houses(self):
        # All that have level >=2 means at least 1 house built
        return [
            p
            for _g, props in self.streets.items()
            if len(props) == Street.GROUP_COUNTS[_g]
            for p in props
            if p.level >= 2
        ]

    def raise_fund(self, amount):
        GAME_LOGS.append(
            f"{self.name} is trying to raise funds to pay {amount}. Current cash={self.cash}."
        )

        def raise_fund_by_selling_houses():
            streets_with_houses = self.get_streets_with_houses()
            streets_with_houses = sorted(
                streets_with_houses, key=lambda pr: pr.house_price, reverse=True
            )
            while self.cash < amount and streets_with_houses:
                pr = streets_with_houses.pop()
                # Sell one house => earn half
                GAME_LOGS.append(
                    f"{self.name} sells house on {pr.name}, gets {pr.house_price//2} back."
                )
                self.cash += pr.house_price // 2
                pr.level -= 1

        def raise_fund_by_mortgaging_properties():
            GAME_LOGS.append(f"{self.name} tries mortgaging properties to raise funds.")
            property_freq: Dict[int, List[Property]] = {}
            for _g, props in self.streets.items():
                freq = len(props)
                property_freq.setdefault(freq, []).extend(props)
            if self.railroads:
                property_freq.setdefault(len(self.railroads), []).extend(self.railroads)
            if self.utilities:
                property_freq.setdefault(len(self.utilities), []).extend(self.utilities)
            if not property_freq:
                return
            property_freq = dict(
                sorted(
                    property_freq.items(),
                    key=lambda item: (item[0], min(pr.mortgage for pr in item[1])),
                )
            )
            for _freq, props in property_freq.items():
                for pr in props:
                    if not pr.mortgaged:
                        pr.mortgaged = True
                        GAME_LOGS.append(
                            f"{self.name} mortgages {pr.name} for {pr.mortgage}."
                        )
                        self.cash += pr.mortgage
                    if self.cash >= amount:
                        return

        raise_fund_by_selling_houses()
        if self.cash >= amount:
            return
        raise_fund_by_mortgaging_properties()

    def move(self, steps, board_size):
        GAME_LOGS.append(f"{self.name} moves {steps} steps from {self.position}.")
        self.last_dice_roll = steps
        self.position += steps
        if self.position // board_size >= 1:
            # Passed GO
            GAME_LOGS.append(f"{self.name} passed GO, +200.")
            self.cash += 200
        self.position %= board_size
        GAME_LOGS.append(f"{self.name} new position: {self.position}.")

    def get_position(self):
        return self.position

    def go_to_jail(self):
        GAME_LOGS.append(f"{self.name} goes to Jail!")
        self.is_in_jail = True
        self.position = 10


class Game:
    def __init__(self, p1, p2, p3=None, p4=None):
        GAME_LOGS.append("Initializing Game with players.")
        self.board = Board()
        self.players: List[Player] = [p1, p2]
        if p3:
            self.players.append(p3)
        if p4:
            self.players.append(p4)
        self.bank = Bank()
        self.current_player_index = 0

    def roll_dice(self):
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        GAME_LOGS.append(f"Dice rolled => ({d1}, {d2})")
        return d1, d2

    def next_player(self):
        old_index = self.current_player_index
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        GAME_LOGS.append(
            f"Next player: from index {old_index} to index {self.current_player_index}."
        )

    def check_win_condition(self) -> Optional[Player]:
        active_players = [p for p in self.players if p.is_in_game]
        if len(active_players) == 1:
            GAME_LOGS.append(
                f"WIN CONDITION MET: {active_players[0].name} is the last active player."
            )
            return active_players[0]
        return None

    def play_turn(self):
        logs = []
        player = self.players[self.current_player_index]
        GAME_LOGS.append(f"--- TURN START :: {player.name} ---")
        if not player.is_in_game:
            GAME_LOGS.append(f"{player.name} is out of the game, skipping.")
            self.next_player()
            return logs

        d1, d2 = self.roll_dice()
        if player.is_in_jail:
            GAME_LOGS.append(f"{player.name} is in jail; attempting to get out.")
            skip, d1_j, d2_j = self.attempt_jail_break(player)
            if skip:
                GAME_LOGS.append(f"{player.name} remains in jail, end turn.")
                self.next_player()
                return logs
            player.is_in_jail = False
            if d1_j and d2_j:
                d1, d2 = d1_j, d2_j
                GAME_LOGS.append(
                    f"{player.name} got out of jail & rolled => ({d1},{d2})."
                )

        # logs.append(f"{player.name} rolled dice ({d1}, {d2}) => {d1+d2}")
        old_position = player.get_position()
        player.move(d1 + d2, len(self.board.tiles))
        # logs.append(
        #    f"{player.name} moved from {old_position} to {player.get_position()}."
        # )
        tile = self.board.tiles[player.position]
        self.handle_tile_landing(player, tile)

        # Double checks
        if d1 == d2:
            GAME_LOGS.append(f"{player.name} rolled a double.")
            player.consecutive_doubles += 1
            if player.consecutive_doubles == 3:
                GAME_LOGS.append(f"{player.name} rolled 3 consecutive doubles => Jail!")
                player.go_to_jail()
                player.consecutive_doubles = 0
                self.next_player()
        else:
            player.consecutive_doubles = 0
            self.next_player()

        # Post Move
        if player.is_in_game:
            player.unmortgage_properties()
            player.buy_houses_and_hotels()
        self.add_player_states_to_logs()
        GAME_LOGS.append(f"--- TURN END :: {player.name} ---\n")
        return logs

    def add_player_states_to_logs(self):
        for player in self.players:
            GAME_LOGS.append(player.__repr__())

    def handle_tile_landing(self, player: Player, tile: Block):
        GAME_LOGS.append(f"{player.name} landed on tile #{tile.number} ({tile.type}).")
        if isinstance(tile, Street):
            self.handle_street_landing(player, tile)
        elif isinstance(tile, RailRoad):
            self.handle_railroad_landing(player, tile)
        elif isinstance(tile, Utility):
            self.handle_utility_landing(player, tile)
        elif isinstance(tile, Chance):
            self.handle_chance_landing(player, tile)
        elif isinstance(tile, CommunityChest):
            self.handle_community_chest_landing(player, tile)
        elif isinstance(tile, Tax):
            self.handle_tax_landing(player, tile)
        elif tile.type == "go_to_jail":
            GAME_LOGS.append(f"{player.name} must go to jail from tile {tile.number}.")
            player.go_to_jail()

    def handle_street_landing(self, player: Player, street: Street):
        if street.owner is None:
            GAME_LOGS.append(f"{player.name} can buy {street.name} if desired.")
            if player.decide_to_buy_property(street):
                player.buy_property(street)
        elif street.owner != player and street.owner.is_in_game:
            rent = street.calculate_rent(player)
            if rent > 0:
                GAME_LOGS.append(
                    f"{player.name} pays rent {rent} to {street.owner.name} for {street.name}."
                )
            player.pay(rent, street.owner)

    def handle_railroad_landing(self, player: Player, railroad: RailRoad):
        if railroad.owner is None:
            GAME_LOGS.append(
                f"{player.name} can buy Railroad {railroad.name} if desired."
            )
            if player.decide_to_buy_property(railroad):
                player.buy_property(railroad)
        elif railroad.owner != player and railroad.owner.is_in_game:
            rent = railroad.calculate_rent(player)
            if rent > 0:
                GAME_LOGS.append(
                    f"{player.name} pays rent {rent} to {railroad.owner.name} for {railroad.name}."
                )
            player.pay(rent, railroad.owner)

    def handle_utility_landing(self, player: Player, utility: Utility):
        if utility.owner is None:
            GAME_LOGS.append(
                f"{player.name} can buy Utility {utility.name} if desired."
            )
            if player.decide_to_buy_property(utility):
                player.buy_property(utility)
        elif utility.owner != player and utility.owner.is_in_game:
            dice_roll = player.last_dice_roll
            rent = utility.calculate_rent(dice_roll, player)
            if rent > 0:
                GAME_LOGS.append(
                    f"{player.name} pays {rent} to {utility.owner.name} (Utility rent)."
                )
            player.pay(rent, utility.owner)

    def handle_chance_landing(self, player: Player, chance: Chance):
        card = Chance.get_chance_card()
        self.resolve_card_effect(player, card)

    def handle_community_chest_landing(
        self, player: Player, community_chest: CommunityChest
    ):
        card = CommunityChest.get_community_chest_card()
        self.resolve_card_effect(player, card)

    def handle_tax_landing(self, player: Player, tax: Tax):
        GAME_LOGS.append(f"{player.name} landed on tax {tax.name}, cost {tax.amount}.")
        player.pay(tax.amount, self.bank)

    def resolve_card_effect(self, player: Player, card: Enum):
        GAME_LOGS.append(f"Resolving card effect for {player.name}: {card.value}")
        if (
            card == ChanceCards.ADVANCE_TO_GO
            or card == CommunityChestCards.ADVANCE_TO_GO
        ):
            player.advance_to_go()
        elif card == ChanceCards.BANK_DIVIDEND:
            player.earn(amount=50)
        elif card == ChanceCards.GO_TO_JAIL or card == CommunityChestCards.GO_TO_JAIL:
            player.go_to_jail()
        elif card == ChanceCards.ADVANCE_TO_ILLINOIS:
            player.advance_to_illinois()
        elif card == ChanceCards.ADVANCE_TO_ST_CHARLES:
            player.advance_to_st_charles()
        elif card == ChanceCards.NEAREST_UTILITY:
            player.advance_to_nearest_utility()
            utility: Utility = self.board.tiles[player.get_position()]

            def handle_advance_to_utility():
                if utility.owner is None:
                    if player.decide_to_buy_property(utility):
                        player.buy_property(utility)
                elif utility.owner != player and utility.owner.is_in_game:
                    d1, d2 = self.roll_dice()
                    rent = (d1 + d2) * 10
                    GAME_LOGS.append(
                        f"{player.name} must pay 10x dice to Utility => {rent}."
                    )
                    player.pay(rent, utility.owner)

            handle_advance_to_utility()
        elif card == ChanceCards.NEAREST_RAILROAD:
            player.advance_to_nearest_railroad()
            railroad: RailRoad = self.board.tiles[player.get_position()]

            def handle_advance_to_railroad():
                if railroad.owner is None:
                    if player.decide_to_buy_property(railroad):
                        player.buy_property(railroad)
                elif railroad.owner != player and railroad.owner.is_in_game:
                    rent = railroad.calculate_rent(player) * 2
                    GAME_LOGS.append(f"{player.name} must pay 2x RR rent => {rent}.")
                    player.pay(rent, railroad.owner)

            handle_advance_to_railroad()
        elif card == ChanceCards.READING_RAILROAD:
            player.advance_to_reading_railroad()
            railroad: RailRoad = self.board.tiles[player.get_position()]
            self.handle_railroad_landing(player, railroad)
        elif card == ChanceCards.BOARDWALK:
            player.advance_to_boardwalk()
            boardwalk: Street = self.board.tiles[player.get_position()]
            self.handle_street_landing(player, boardwalk)
        elif card == ChanceCards.CHAIRMAN:
            for i, pl in enumerate(self.players):
                if i != self.current_player_index:
                    GAME_LOGS.append(
                        f"{player.name} pays 50 to {pl.name} (Chairman card)."
                    )
                    player.pay(50, pl)
        elif card == ChanceCards.BUILDING_LOAN:
            GAME_LOGS.append(f"{player.name} collects building loan of 150.")
            player.earn(150)
        elif (
            card == ChanceCards.STREET_REPAIRS
            or card == CommunityChestCards.STREET_REPAIRS
        ):
            fee = player.determine_street_repair_fee()
            player.pay(fee, self.bank)
        elif card == ChanceCards.POOR_TAX:
            GAME_LOGS.append(f"{player.name} pays poor tax of 15.")
            player.pay(15, self.bank)
        elif card == ChanceCards.GENERAL_REPAIRS:
            fee = player.determine_general_repair_fee()
            player.pay(fee, self.bank)
        elif card == ChanceCards.GET_OUT_OF_JAIL_FREE:
            GAME_LOGS.append(f"{player.name} receives GET OUT OF JAIL FREE (Chance).")
            player.chance_jail_free_card = True
        elif card == ChanceCards.GO_BACK_THREE:
            player.go_back_three(len(self.board.tiles))
        elif CommunityChestCards.BANK_ERROR == card:
            GAME_LOGS.append(f"{player.name} collects bank error of 200.")
            player.earn(200)
        elif CommunityChestCards.DOCTOR_FEE == card:
            player.pay(50, self.bank)
        elif CommunityChestCards.STOCK_SALE == card:
            player.earn(50)
        elif CommunityChestCards.GO_TO_JAIL == card:
            player.go_to_jail()
        elif CommunityChestCards.GET_OUT_OF_JAIL_FREE == card:
            GAME_LOGS.append(
                f"{player.name} receives GET OUT OF JAIL FREE (CommChest)."
            )
            player.community_chest_jail_free_card = True
        elif CommunityChestCards.HOLIDAY_FUND == card:
            player.earn(100)
        elif CommunityChestCards.INCOME_TAX_REFUND == card:
            player.earn(20)
        elif CommunityChestCards.BIRTHDAY == card:
            for i, pl in enumerate(self.players):
                if i != self.current_player_index:
                    GAME_LOGS.append(f"{pl.name} pays 10 to {player.name} (Birthday).")
                    pl.pay(10, player)
        elif CommunityChestCards.LIFE_INSURANCE == card:
            player.earn(100)
        elif CommunityChestCards.SCHOOL_FEES == card:
            player.pay(50, self.bank)
        elif CommunityChestCards.CONSULTANCY_FEE == card:
            player.earn(25)
        elif CommunityChestCards.BEAUTY_CONTEST == card:
            player.earn(10)
        elif CommunityChestCards.INHERITANCE == card:
            player.earn(100)

    def attempt_jail_break(
        self, player: Player
    ) -> Tuple[bool, Optional[int], Optional[int]]:
        GAME_LOGS.append(
            f"{player.name} attempts jail break. So far tried {player.jail_roll_attempts} times."
        )
        if player.has_jail_free_card():
            use_card = player.decide_to_use_jail_free_card()
            if use_card:
                player.use_jail_free_card()
                player.reset_jail_roll_attempts()
                d1, d2 = self.roll_dice()
                GAME_LOGS.append(
                    f"{player.name} used a Jail Free card and rolled => ({d1},{d2})."
                )
                return (False, d1, d2)

        if player.jail_roll_attempts < 3:
            roll_doubles = player.decide_to_roll_for_doubles()
            if roll_doubles:
                d1, d2 = self.roll_dice()
                GAME_LOGS.append(
                    f"{player.name} tries for doubles => rolled ({d1},{d2})."
                )
                if d1 == d2:
                    GAME_LOGS.append(
                        f"{player.name} rolled doubles & is free from jail."
                    )
                    player.reset_jail_roll_attempts()
                    return (False, d1, d2)
                else:
                    player.jail_roll_attempts += 1
                    GAME_LOGS.append(
                        f"{player.name} did NOT roll doubles, attempt={player.jail_roll_attempts}."
                    )
                    return (True, None, None)

        GAME_LOGS.append(
            f"{player.name} paying 50 to get out of jail, or is bankrupt if they can't."
        )
        player.pay(50, to=self.bank)
        if player.is_in_game:
            player.reset_jail_roll_attempts()
            d1, d2 = self.roll_dice()
            GAME_LOGS.append(
                f"{player.name} leaves jail after paying 50 => rolled ({d1},{d2})."
            )
            return (False, d1, d2)
        else:
            GAME_LOGS.append(f"{player.name} is bankrupt trying to leave jail.")
            return (True, -1, -1)

    def simulate_game(self):
        GAME_LOGS.append("Starting simulate_game() with 10,000 turn cutoff.")
        turn_count = 0
        max_turns = 10000
        winner = None

        # Run the normal loop, but break if too many turns.
        while not winner and turn_count < max_turns:
            logs = self.play_turn()
            if logs:
                GAME_LOGS.extend(logs)
            winner = self.check_win_condition()
            turn_count += 1

        if winner == None:
            winner = -1

        if winner == -1:
            GAME_LOGS.append(f"No winner after {max_turns} turns => stopping.")
        else:
            GAME_LOGS.append(f"WINNER after {turn_count} turns: {winner.name}.")

        # Once done, dump all logs to a text file
        # with open("full_detailed_logs.txt", "w", encoding="utf-8") as f:
        #     for line in GAME_LOGS:
        #         f.write(line + "\n")

        return winner


class MonteCarloSimulation:
    def __init__(self, runs: int):
        self.runs = runs

    def run(self):
        win_count = {}
        for _ in range(self.runs):
            # Create players
            players = [
                Player(
                    name="Player 1",
                    w_buy_building=0.8,
                    w_buy_railroad=0.7,
                    w_buy_utility=0.6,
                    w_roll_double_in_jail=0.5,
                    w_use_jail_free_card=0.5,
                    min_cash=200,
                    min_cash_to_unmortgage=300,
                ),
                Player(
                    name="Player 2",
                    w_buy_building=0.6,
                    w_buy_railroad=0.8,
                    w_buy_utility=0.7,
                    w_roll_double_in_jail=0.4,
                    w_use_jail_free_card=0.6,
                    min_cash=200,
                    min_cash_to_unmortgage=300,
                ),
                Player(
                    name="Player 3",
                    w_buy_building=0.7,
                    w_buy_railroad=0.6,
                    w_buy_utility=0.8,
                    w_roll_double_in_jail=0.6,
                    w_use_jail_free_card=0.7,
                    min_cash=200,
                    min_cash_to_unmortgage=300,
                ),
                Player(
                    name="Player 4",
                    w_buy_building=0.5,
                    w_buy_railroad=0.5,
                    w_buy_utility=0.5,
                    w_roll_double_in_jail=0.5,
                    w_use_jail_free_card=0.5,
                    min_cash=200,
                    min_cash_to_unmortgage=300,
                ),
            ]
            game = Game(*players)
            w = game.simulate_game()
            if w == -1:
                if "no_winner" in win_count:
                    win_count["no_winner"] += 1
                else:
                    win_count["no_winner"] = 0
            elif w and w.name not in win_count:
                win_count[w.name] = 0
            elif w:
                win_count[w.name] += 1
        return win_count


def tile_to_grid_position(tile_index: int) -> Tuple[int, int]:
    if tile_index == 0:
        return (10, 0)
    elif 1 <= tile_index <= 9:
        return (10 - tile_index, 0)
    elif tile_index == 10:
        return (0, 0)
    elif 11 <= tile_index <= 19:
        return (0, tile_index - 10)
    elif tile_index == 20:
        return (0, 10)
    elif 21 <= tile_index <= 29:
        return (tile_index - 20, 10)
    elif tile_index == 30:
        return (10, 10)
    elif 31 <= tile_index <= 39:
        return (10, 40 - tile_index)
    else:
        raise ValueError("Invalid tile index")


class MonopolyGUI:
    def __init__(self, root):
        GAME_LOGS.append("Starting Monopoly GUI.")
        self.root = root
        self.root.title("Monopoly Board with Logs")

        self.players = [
            Player("Alice", 0.8, 0.7, 0.6, 0.5, 0.5, 200, 300),
            Player("Bob", 0.6, 0.8, 0.7, 0.4, 0.6, 200, 300),
        ]
        self.game = Game(*self.players)

        self.board_frame = ttk.Frame(self.root, padding=5)
        self.board_frame.grid(row=0, column=0, sticky="nwes")
        self.info_frame = ttk.Frame(self.root, padding=5)
        self.info_frame.grid(row=0, column=1, sticky="nwes")

        self.board_labels = []
        for r in range(11):
            row_list = []
            self.board_frame.grid_rowconfigure(r, weight=1)
            for c in range(11):
                self.board_frame.grid_columnconfigure(c, weight=1)
                lbl = ttk.Label(
                    self.board_frame,
                    text="",
                    borderwidth=1,
                    relief="solid",
                    width=12,
                    anchor="nw",
                )
                lbl.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")
                row_list.append(lbl)
            self.board_labels.append(row_list)

        self.player_info_text = tk.Text(self.info_frame, width=35, height=30)
        self.player_info_text.pack(side="top", fill="both", expand=True)

        self.next_button = ttk.Button(
            self.info_frame, text="Next Turn", command=self.next_turn
        )
        self.next_button.pack(side="bottom", pady=10)

        self.update_gui()

    def update_gui(self):
        self.update_board_labels()
        self.update_player_info()

    def update_board_labels(self):
        for r in range(11):
            for c in range(11):
                self.board_labels[r][c].config(text="", background="#dddddd")

        for i, tile in enumerate(self.game.board.tiles):
            row, col = tile_to_grid_position(i)
            txt = f"#{i} {tile.type}"
            if isinstance(tile, Property):
                txt = f"#{i}\n{tile.name}"
                if tile.owner:
                    txt += f"\nOwner: {tile.owner.name}"
                if isinstance(tile, Street):
                    txt += f"\nLvl:{tile.level}"
            plrs = [p.name for p in self.players if p.is_in_game and p.position == i]
            if plrs:
                txt += "\n[" + ", ".join(plrs) + "]"

            self.board_labels[row][col].config(text=txt, background="#ffffff")

    def update_player_info(self):
        self.player_info_text.delete("1.0", tk.END)
        for p in self.players:
            self.player_info_text.insert(tk.END, f"{p.name}:\n")
            self.player_info_text.insert(tk.END, f"  Cash: {p.cash}\n")
            self.player_info_text.insert(tk.END, f"  Position: {p.position}\n")
            self.player_info_text.insert(tk.END, f"  In Jail?: {p.is_in_jail}\n")
            if p.is_in_game:
                all_props = []
                for g, st_list in p.streets.items():
                    for st in st_list:
                        all_props.append(st.name)
                for rr in p.railroads:
                    all_props.append(rr.name)
                for ut in p.utilities:
                    all_props.append(ut.name)
                if not all_props:
                    all_props = ["(none)"]
                self.player_info_text.insert(tk.END, f"  Owned: {all_props}\n\n")
            else:
                self.player_info_text.insert(tk.END, "  [BANKRUPT]\n\n")

    def next_turn(self):
        winner = self.game.check_win_condition()
        if not winner:
            turn_logs = self.game.play_turn()
            self.update_gui()
            if turn_logs:
                self.player_info_text.insert(tk.END, "----- Turn Log -----\n")
                for line in turn_logs:
                    self.player_info_text.insert(tk.END, line + "\n")
                self.player_info_text.insert(tk.END, "--------------------\n\n")
            winner = self.game.check_win_condition()
        if winner:
            self.player_info_text.insert(tk.END, f"WINNER = {winner.name}\n")
            self.next_button.config(state="disabled")


def main():
    root = tk.Tk()
    app = MonopolyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
