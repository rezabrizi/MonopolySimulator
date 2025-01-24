import random
import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from typing import Dict, Optional, List, Tuple, Union
from enum import Enum
from collections import deque

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
            f"rent={self.calculate_rent()}, level={self.get_street_building()}, "
            f"mortgaged={self.mortgaged}, owner={self.owner.name if self.owner else None})"
        )

    def get_street_building(self):
        if self.level == 0:
            return "Empty"
        elif self.level == 1:
            return "Complete Set"
        elif self.level < 5:
            return f"#({self.level-1}) Houses"
        else:
            return "Hotel"

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

    def reset_jail_roll_attempts(self):
        GAME_LOGS.append(
            f"{self.name} reset jail roll attempts from {self.jail_roll_attempts} to 0."
        )
        self.jail_roll_attempts = 0

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
            # TODO: self.raise_fund(amount=amount)
            pass
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
