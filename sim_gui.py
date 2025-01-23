import tkinter as tk
from tkinter import ttk
import random
from abc import ABC, abstractmethod
from typing import Dict, Optional, List, Tuple, Union
from enum import Enum
from collections import deque


###############################################################################
#                             MONOPOLY CLASSES                                #
###############################################################################


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
    NEAREST_UTILITY = (
        "Advance token to the nearest Utility. If unowned, you may buy it."
    )
    NEAREST_RAILROAD = (
        "Advance token to the nearest Railroad and pay owner twice the rental."
    )
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


class Chance(Block):
    chance_deque = deque(ChanceCards)

    def __init__(self, number):
        super().__init__("chance", number)

    @classmethod
    def get_chance_card(cls):
        card = cls.chance_deque.pop()
        if card != ChanceCards.GET_OUT_OF_JAIL_FREE:
            cls.chance_deque.appendleft(card)
        return card

    @classmethod
    def put_jail_free_card_back(cls):
        cls.chance_deque.appendleft(ChanceCards.GET_OUT_OF_JAIL_FREE)


class CommunityChest(Block):
    community_chest_deque = deque(CommunityChestCards)

    def __init__(self, number):
        super().__init__("community_chest", number)

    @classmethod
    def get_community_chest_card(cls):
        card = cls.community_chest_deque.pop()
        if card != CommunityChestCards.GET_OUT_OF_JAIL_FREE:
            cls.community_chest_deque.appendleft(card)
        return card

    @classmethod
    def put_jail_free_card_back(cls):
        cls.community_chest_deque.appendleft(CommunityChestCards.GET_OUT_OF_JAIL_FREE)


class Tax(Block):
    def __init__(self, name, amount, number):
        super().__init__("tax", number)
        self.name = name
        self.amount = amount


class Property(Block):
    def __init__(self, name, price, number):
        super().__init__("property", number)
        self.name = name
        self.price = price
        self.mortgage = self.price // 2
        self.unmortgage = self.mortgage * 1.1
        self.mortgaged = False
        self.owner = None

    @abstractmethod
    def calculate_rent(self):
        pass


class Utility(Property):
    def __init__(self, name, price, number):
        super().__init__(name, price, number)

    def calculate_rent(self, dice_roll, player):
        if self.owner is None or self.mortgaged or self.owner == player:
            return 0
        return dice_roll * (10 if len(self.owner.utilities) == 2 else 4)


class RailRoad(Property):
    def __init__(self, name: str, price: int, rent: List[int], number: int):
        super().__init__(name, price, number)
        self.rent = rent

    def calculate_rent(self, player):
        if self.owner is None or self.mortgaged or self.owner == player:
            return 0
        railroads_owned = len(self.owner.railroads)
        return self.rent[railroads_owned - 1]


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

    def __init__(self, name, group, price, rent, house_price, number):
        super().__init__(name, price, number)
        self.group = group
        self.rent = rent
        self.house_price = house_price
        self.level = 0  # 0=unimproved, 1=owned, 2..5=houses, 6=hotel

    def calculate_rent(self, player):
        if self.owner is None or self.mortgaged or self.owner == player:
            return 0
        return self.rent[self.level]


class Board:
    def __init__(self):
        self.tiles = []
        self.initialize_board()

    def initialize_board(self):
        self.tiles: List[Block] = [
            Block("go", 0),
            Street(
                "Mediterranean Avenue",
                StreetGroups.BROWN,
                60,
                [2, 4, 10, 30, 90, 250],
                50,
                1,
            ),
            CommunityChest(2),
            Street(
                "Baltic Avenue", StreetGroups.BROWN, 60, [4, 8, 20, 60, 180, 450], 50, 3
            ),
            Tax("Income Tax", 200, 4),
            RailRoad("Reading Railroad", 200, [25, 50, 100, 200], 5),
            Street(
                "Oriental Avenue",
                StreetGroups.LIGHT_BLUE,
                100,
                [6, 12, 30, 90, 270, 550],
                50,
                6,
            ),
            Chance(7),
            Street(
                "Vermont Avenue",
                StreetGroups.LIGHT_BLUE,
                100,
                [6, 12, 30, 90, 270, 550],
                50,
                8,
            ),
            Street(
                "Connecticut Avenue",
                StreetGroups.LIGHT_BLUE,
                120,
                [8, 16, 40, 100, 300, 600],
                50,
                9,
            ),
            Block("jail", 10),
            Street(
                "St. Charles Place",
                StreetGroups.PINK,
                140,
                [10, 20, 50, 150, 450, 750],
                100,
                11,
            ),
            Utility("Electric Company", 150, 12),
            Street(
                "States Avenue",
                StreetGroups.PINK,
                140,
                [10, 20, 50, 150, 450, 750],
                100,
                13,
            ),
            Street(
                "Virginia Avenue",
                StreetGroups.PINK,
                160,
                [12, 24, 60, 180, 500, 900],
                100,
                14,
            ),
            RailRoad("Pennsylvania Railroad", 200, [25, 50, 100, 200], 15),
            Street(
                "St. James Place",
                StreetGroups.ORANGE,
                180,
                [14, 28, 70, 200, 550, 950],
                100,
                16,
            ),
            CommunityChest(17),
            Street(
                "Tennessee Avenue",
                StreetGroups.ORANGE,
                180,
                [14, 28, 70, 200, 550, 950],
                100,
                18,
            ),
            Street(
                "New York Avenue",
                StreetGroups.ORANGE,
                200,
                [16, 32, 80, 220, 600, 1000],
                100,
                19,
            ),
            Block("free_parking", 20),
            Street(
                "Kentucky Avenue",
                StreetGroups.RED,
                220,
                [18, 36, 90, 250, 700, 1050],
                150,
                21,
            ),
            Chance(22),
            Street(
                "Indiana Avenue",
                StreetGroups.RED,
                220,
                [18, 36, 90, 250, 700, 1050],
                150,
                23,
            ),
            Street(
                "Illinois Avenue",
                StreetGroups.RED,
                240,
                [20, 40, 100, 300, 750, 1100],
                150,
                24,
            ),
            RailRoad("B&O Railroad", 200, [25, 50, 100, 200], 25),
            Street(
                "Atlantic Avenue",
                StreetGroups.YELLOW,
                260,
                [22, 44, 110, 330, 800, 1150],
                150,
                26,
            ),
            Street(
                "Ventnor Avenue",
                StreetGroups.YELLOW,
                260,
                [22, 44, 110, 330, 800, 1150],
                150,
                27,
            ),
            Utility("Water Works", 150, 28),
            Street(
                "Marvin Gardens",
                StreetGroups.YELLOW,
                280,
                [24, 48, 120, 360, 850, 1200],
                150,
                29,
            ),
            Block("go_to_jail", 30),
            Street(
                "Pacific Avenue",
                StreetGroups.GREEN,
                300,
                [26, 52, 130, 390, 900, 1275],
                200,
                31,
            ),
            Street(
                "North Carolina Avenue",
                StreetGroups.GREEN,
                300,
                [26, 52, 130, 390, 900, 1275],
                200,
                32,
            ),
            CommunityChest(33),
            Street(
                "Pennsylvania Avenue",
                StreetGroups.GREEN,
                320,
                [28, 56, 150, 450, 1000, 1400],
                200,
                34,
            ),
            RailRoad("Short Line", 200, [25, 50, 100, 200], 35),
            Chance(36),
            Street(
                "Park Place",
                StreetGroups.DARK_BLUE,
                350,
                [35, 70, 175, 500, 1100, 1500],
                200,
                37,
            ),
            Tax("Luxury Tax", 100, 38),
            Street(
                "Boardwalk",
                StreetGroups.DARK_BLUE,
                400,
                [50, 100, 200, 600, 1400, 2000],
                200,
                39,
            ),
        ]


class Bank:
    def earn(self, amount: int):
        pass


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
        self.name = name
        self.w_buy_building = w_buy_building
        self.w_buy_railroad = w_buy_railroad
        self.w_buy_utility = w_buy_utility
        self.w_use_jail_free_card = w_use_jail_free_card
        self.w_roll_double_in_jail = w_roll_double_in_jail
        self.min_cash = min_cash
        self.min_cash_to_unmortgage = min_cash_to_unmortgage
        self.is_in_jail = False
        self.is_in_game = True
        self.jail_roll_attempts = 0
        self.consecutive_doubles = 0
        self.position = 0
        self.cash = 1500
        self.liquidity = 1500
        self.last_dice_roll = 0
        self.community_chest_jail_free_card = False
        self.chance_jail_free_card = False
        self.streets: Dict[StreetGroups, List[Street]] = {}
        self.railroads: List[RailRoad] = []
        self.utilities: List[Utility] = []

    def has_jail_free_card(self):
        return self.community_chest_jail_free_card or self.chance_jail_free_card

    def decide_to_use_jail_free_card(self):
        return random.random() < self.w_use_jail_free_card

    def use_jail_free_card(self):
        if self.chance_jail_free_card:
            self.chance_jail_free_card = False
            Chance.put_jail_free_card_back()
        elif self.community_chest_jail_free_card:
            self.community_chest_jail_free_card = False
            CommunityChest.put_jail_free_card_back()

    def reset_jail_roll_attempts(self):
        self.jail_roll_attempts = 0

    def decide_to_roll_for_doubles(self):
        return random.random() < self.w_roll_double_in_jail

    def earn(self, amount):
        self.cash += amount
        self.liquidity += amount

    def pay(self, amount, to):
        if self.liquidity < amount:
            self.is_in_game = False
            self.transfer_ownership_of_all_assets(to)
            return
        if self.cash < amount:
            self.raise_fund(amount)
        if self.is_in_game:
            to.earn(amount)

    def transfer_ownership_of_all_assets(self, to):
        if isinstance(to, Player):
            self.transfer_ownership_of_all_assets_to_another_player(to)
        else:
            self.transfer_ownership_of_all_assets_to_the_bank(to)

    def transfer_ownership_of_all_assets_to_another_player(self, other: "Player"):
        other.earn(self.cash)
        self.cash = 0
        self.liquidity = 0

        for group, streets in self.streets.items():
            for s in streets:
                s.owner = other
                other.receive_street(s)
        self.streets.clear()

        while self.railroads:
            rr = self.railroads.pop()
            rr.owner = other
            other.railroads.append(rr)

        while self.utilities:
            u = self.utilities.pop()
            u.owner = other
            other.utilities.append(u)

        if self.community_chest_jail_free_card:
            other.community_chest_jail_free_card = True
        if self.chance_jail_free_card:
            other.chance_jail_free_card = True

    def transfer_ownership_of_all_assets_to_the_bank(self, bank: Bank):
        self.cash = 0
        self.liquidity = 0

        for group, streets in self.streets.items():
            for s in streets:
                s.owner = None
        self.streets.clear()

        while self.railroads:
            rr = self.railroads.pop()
            rr.owner = None

        while self.utilities:
            u = self.utilities.pop()
            u.owner = None

        if self.community_chest_jail_free_card:
            CommunityChest.put_jail_free_card_back()
        if self.chance_jail_free_card:
            Chance.put_jail_free_card_back()

    def raise_fund(self, amount):
        def sell_houses():
            with_houses = []
            for g, props in self.streets.items():
                for s in props:
                    if s.level >= 2:
                        with_houses.append(s)
            with_houses.sort(key=lambda x: x.house_price, reverse=True)

            while self.cash < amount and with_houses:
                prop = with_houses.pop()
                self.cash += prop.house_price // 2
                self.liquidity -= prop.house_price // 2
                prop.level -= 1

        def mortgage_props():
            props_list = []
            for g, props in self.streets.items():
                props_list.extend(props)
            props_list.extend(self.railroads)
            props_list.extend(self.utilities)
            # Filter out already mortgaged
            not_mortgaged = [p for p in props_list if not p.mortgaged]
            not_mortgaged.sort(key=lambda p: p.mortgage)
            for p in not_mortgaged:
                p.mortgaged = True
                self.cash += p.mortgage
                self.liquidity -= p.mortgage
                if self.cash >= amount:
                    return

        sell_houses()
        if self.cash < amount:
            mortgage_props()

    def receive_street(self, street: "Street"):
        if street.group not in self.streets:
            self.streets[street.group] = []
        self.streets[street.group].append(street)

    def decide_to_buy_property_random(self, prop):
        if isinstance(prop, Street):
            return random.random() < self.w_buy_building
        elif isinstance(prop, RailRoad):
            return random.random() < self.w_buy_railroad
        elif isinstance(prop, Utility):
            return random.random() < self.w_buy_utility
        return False

    def decide_to_buy_property(self, prop):
        return self.decide_to_buy_property_random(prop)

    def buy_property(self, prop):
        if prop.owner is not None:
            return
        self.cash -= prop.price
        self.liquidity -= prop.price
        self.liquidity += prop.mortgage
        prop.owner = self
        if isinstance(prop, Street):
            self.receive_street(prop)
        elif isinstance(prop, RailRoad):
            self.railroads.append(prop)
        elif isinstance(prop, Utility):
            self.utilities.append(prop)

    def buy_house(self, street: "Street"):
        street.level += 1
        self.cash -= street.house_price
        self.liquidity -= street.house_price
        self.liquidity += street.house_price // 2

    def go_to_jail(self):
        self.is_in_jail = True
        self.position = 10

    def move(self, steps, board_size):
        self.last_dice_roll = steps
        self.position += steps
        if self.position >= board_size:
            self.cash += 200
            self.liquidity += 200
        self.position %= board_size

    def get_valid_expandable_sets(self):
        sets = {}
        for group, props in self.streets.items():
            if (
                len(props) == Street.GROUP_COUNTS[group]
                and not all(p.level == 5 for p in props)
                and all(not p.mortgaged for p in props)
            ):
                sets[group] = props
        return sets

    def buy_houses_and_hotels(self):
        # simple approach
        sets = self.get_valid_expandable_sets()
        # sort by "lowest total improvements" first
        sorted_groups = sorted(sets.items(), key=lambda kv: sum(p.level for p in kv[1]))
        for group, props in sorted_groups:
            while True:
                min_level = min(p.level for p in props)
                if min_level == 5:
                    break
                candidates = [p for p in props if p.level == min_level]
                made_purchase = False
                for c in candidates:
                    if self.cash - c.house_price >= self.min_cash:
                        self.buy_house(c)
                        made_purchase = True
                if not made_purchase:
                    break

    def unmortgage_properties(self):
        # trivial approach
        all_mortgaged = []
        for g, props in self.streets.items():
            for s in props:
                if s.mortgaged:
                    all_mortgaged.append(s)
        all_mortgaged += [r for r in self.railroads if r.mortgaged]
        all_mortgaged += [u for u in self.utilities if u.mortgaged]
        all_mortgaged.sort(key=lambda x: x.unmortgage)
        for p in all_mortgaged:
            if self.cash - p.unmortgage >= self.min_cash_to_unmortgage:
                self.cash -= p.unmortgage
                self.liquidity -= p.unmortgage
                p.mortgaged = False


class Game:
    def __init__(self, *players):
        self.board = Board()
        self.players: List[Player] = list(players)
        self.bank = Bank()
        self.current_player_index = 0

    def roll_dice(self):
        return random.randint(1, 6), random.randint(1, 6)

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def check_win_condition(self):
        active = [p for p in self.players if p.is_in_game]
        if len(active) == 1:
            return active[0]
        return None

    def play_turn(self):
        """
        Returns a list of log lines describing what happened.
        """
        logs = []
        p = self.players[self.current_player_index]
        if not p.is_in_game:
            self.next_player()
            return logs

        # If in jail
        if p.is_in_jail:
            logs.append(f"{p.name} is in jail. Attempting to get out...")
            skip, d1, d2 = self.attempt_jail_break(p, logs)
            if skip:
                self.next_player()
                return logs
            # If actually rolled out or used card, dice might be replaced
            if d1 is not None and d2 is not None:
                dice = (d1, d2)
            else:
                # If code logic didn't fill them, roll fresh now
                dice = self.roll_dice()
        else:
            dice = self.roll_dice()

        d1, d2 = dice
        logs.append(f"{p.name} rolled dice ({d1}, {d2}) => {d1+d2}")

        total = d1 + d2
        old_position = p.position
        p.move(total, len(self.board.tiles))
        logs.append(f"{p.name} moved from {old_position} to {p.position}.")

        tile = self.board.tiles[p.position]
        logs += self.handle_tile_landing(p, tile)

        # Doubles check
        if d1 == d2:
            p.consecutive_doubles += 1
            if p.consecutive_doubles == 3:
                logs.append(f"{p.name} rolled 3 doubles in a row -> GO TO JAIL.")
                p.go_to_jail()
                p.consecutive_doubles = 0
                self.next_player()
                return logs
        else:
            p.consecutive_doubles = 0
            self.next_player()

        if p.is_in_game:
            p.unmortgage_properties()
            p.buy_houses_and_hotels()

        return logs

    def attempt_jail_break(
        self, p: Player, logs
    ) -> Tuple[bool, Optional[int], Optional[int]]:
        # returns (skipTurn, dice1, dice2)
        if p.has_jail_free_card():
            if p.decide_to_use_jail_free_card():
                logs.append(f"{p.name} used a 'Get Out Of Jail Free' card.")
                p.use_jail_free_card()
                p.reset_jail_roll_attempts()
                p.is_in_jail = False
                d1, d2 = self.roll_dice()
                logs.append(f"After using card, {p.name} rolls dice ({d1}, {d2}).")
                return (False, d1, d2)

        if p.jail_roll_attempts < 3:
            if p.decide_to_roll_for_doubles():
                d1, d2 = self.roll_dice()
                logs.append(f"{p.name} tries for doubles in jail: rolled ({d1}, {d2}).")
                if d1 == d2:
                    logs.append(f"{p.name} rolled doubles -> Freed from jail.")
                    p.is_in_jail = False
                    p.reset_jail_roll_attempts()
                    return (False, d1, d2)
                else:
                    p.jail_roll_attempts += 1
                    logs.append(
                        f"No doubles -> remain in jail. Attempts so far = {p.jail_roll_attempts}."
                    )
                    return (True, None, None)

        # if we get here, must pay
        logs.append(f"{p.name} pays $50 to get out of jail.")
        p.pay(50, self.bank)
        if p.is_in_game:
            p.is_in_jail = False
            p.reset_jail_roll_attempts()
            d1, d2 = self.roll_dice()
            logs.append(f"After paying, {p.name} rolls dice ({d1}, {d2}).")
            return (False, d1, d2)
        else:
            logs.append(f"{p.name} went bankrupt while trying to pay jail fee!")
            return (True, None, None)

    def handle_tile_landing(self, p: Player, tile: Block) -> List[str]:
        logs = []
        if isinstance(tile, Street):
            if tile.owner is None:
                decide = p.decide_to_buy_property(tile)
                logs.append(f"{p.name} lands on {tile.name}. Decides to buy? {decide}")
                if decide:
                    p.buy_property(tile)
                    if tile.owner == p:
                        logs.append(f"{p.name} bought {tile.name} for ${tile.price}.")
            else:
                if tile.owner != p and tile.owner.is_in_game:
                    rent = tile.calculate_rent(p)
                    if rent > 0:
                        logs.append(
                            f"{p.name} pays ${rent} rent to {tile.owner.name} for {tile.name}."
                        )
                    p.pay(rent, tile.owner)
        elif isinstance(tile, RailRoad):
            if tile.owner is None:
                decide = p.decide_to_buy_property(tile)
                logs.append(f"{p.name} lands on {tile.name} (Railroad). Buy? {decide}")
                if decide:
                    p.buy_property(tile)
                    if tile.owner == p:
                        logs.append(f"{p.name} bought {tile.name} for ${tile.price}.")
            else:
                if tile.owner != p and tile.owner.is_in_game:
                    rent = tile.calculate_rent(p)
                    if rent > 0:
                        logs.append(
                            f"{p.name} pays ${rent} railroad rent to {tile.owner.name}."
                        )
                    p.pay(rent, tile.owner)
        elif isinstance(tile, Utility):
            if tile.owner is None:
                decide = p.decide_to_buy_property(tile)
                logs.append(f"{p.name} lands on {tile.name} (Utility). Buy? {decide}")
                if decide:
                    p.buy_property(tile)
                    if tile.owner == p:
                        logs.append(f"{p.name} bought {tile.name} for ${tile.price}.")
            else:
                if tile.owner != p and tile.owner.is_in_game:
                    rent = tile.calculate_rent(p.last_dice_roll, p)
                    if rent > 0:
                        logs.append(
                            f"{p.name} pays ${rent} utility rent to {tile.owner.name}."
                        )
                    p.pay(rent, tile.owner)
        elif isinstance(tile, Chance):
            card = Chance.get_chance_card()
            logs.append(f"{p.name} lands on Chance -> {card.value}")
            self.resolve_card_effect(p, card, logs)
        elif isinstance(tile, CommunityChest):
            card = CommunityChest.get_community_chest_card()
            logs.append(f"{p.name} lands on Community Chest -> {card.value}")
            self.resolve_card_effect(p, card, logs)
        elif isinstance(tile, Tax):
            logs.append(f"{p.name} lands on {tile.name} -> pays ${tile.amount} tax.")
            p.pay(tile.amount, self.bank)
        elif tile.type == "go_to_jail":
            logs.append(f"{p.name} hits GO TO JAIL!")
            p.go_to_jail()
        return logs

    def resolve_card_effect(self, p: Player, card: Enum, logs: List[str]):
        if card in (ChanceCards.ADVANCE_TO_GO, CommunityChestCards.ADVANCE_TO_GO):
            logs.append(f"{p.name} advances to GO (+$200).")
            p.advance_to_go()
        elif card == ChanceCards.BANK_DIVIDEND:
            logs.append(f"{p.name} gets $50 from Bank Dividend.")
            p.earn(50)
        elif card in (ChanceCards.GO_TO_JAIL, CommunityChestCards.GO_TO_JAIL):
            logs.append(f"{p.name} goes directly to Jail!")
            p.go_to_jail()
        elif card == ChanceCards.ADVANCE_TO_ILLINOIS:
            logs.append(f"{p.name} advances to Illinois (24).")
            p.advance_to_illinois()
        elif card == ChanceCards.ADVANCE_TO_ST_CHARLES:
            logs.append(f"{p.name} advances to St. Charles (11).")
            p.advance_to_st_charles()
        elif card == ChanceCards.NEAREST_UTILITY:
            logs.append(f"{p.name} moves to nearest Utility.")
            old_pos = p.position
            p.advance_to_nearest_utility()
            if p.position < old_pos:
                logs.append(f"Passed GO -> +200!")
            tile = self.board.tiles[p.position]
            if isinstance(tile, Utility):
                if tile.owner is None:
                    decided = p.decide_to_buy_property(tile)
                    logs.append(f"Decided to buy utility? {decided}")
                    if decided:
                        p.buy_property(tile)
                elif tile.owner != p and tile.owner.is_in_game:
                    d1, d2 = self.roll_dice()
                    rent = (d1 + d2) * 10
                    logs.append(
                        f"{p.name} rolled ({d1},{d2}) -> pays ${rent} to {tile.owner.name}."
                    )
                    p.pay(rent, tile.owner)
        elif card == ChanceCards.NEAREST_RAILROAD:
            logs.append(f"{p.name} moves to nearest Railroad.")
            old_pos = p.position
            p.advance_to_nearest_railroad()
            if p.position < old_pos:
                logs.append(f"Passed GO -> +200!")
            tile = self.board.tiles[p.position]
            if isinstance(tile, RailRoad):
                if tile.owner is None:
                    decided = p.decide_to_buy_property(tile)
                    logs.append(f"Decided to buy RR? {decided}")
                    if decided:
                        p.buy_property(tile)
                elif tile.owner != p and tile.owner.is_in_game:
                    rent = tile.calculate_rent(p) * 2
                    logs.append(
                        f"{p.name} pays double RR rent ${rent} to {tile.owner.name}."
                    )
                    p.pay(rent, tile.owner)
        elif card == ChanceCards.READING_RAILROAD:
            logs.append(f"{p.name} moves to Reading RR (5).")
            old_pos = p.position
            p.advance_to_reading_railroad()
            if p.position < old_pos:
                logs.append(f"Passed GO -> +200!")
            tile = self.board.tiles[p.position]
            self.handle_railroad_landing(p, tile, logs)
        elif card == ChanceCards.BOARDWALK:
            logs.append(f"{p.name} advances to Boardwalk (39).")
            p.advance_to_boardwalk()
            tile = self.board.tiles[p.position]
            if isinstance(tile, Street):
                logs += self.handle_tile_landing(p, tile)
        elif card == ChanceCards.CHAIRMAN:
            logs.append(f"CHAIRMAN: {p.name} pays each other player $50.")
            for pl in self.players:
                if pl != p and pl.is_in_game:
                    p.pay(50, pl)
        elif card == ChanceCards.BUILDING_LOAN:
            logs.append(f"{p.name} gets $150 from building loan.")
            p.earn(150)
        elif card in (ChanceCards.STREET_REPAIRS, CommunityChestCards.STREET_REPAIRS):
            fee = p.determine_street_repair_fee()
            logs.append(f"{p.name} must pay street repair: ${fee}.")
            p.pay(fee, self.bank)
        elif card == ChanceCards.POOR_TAX:
            logs.append(f"{p.name} pays poor tax of $15.")
            p.pay(15, self.bank)
        elif card == ChanceCards.GENERAL_REPAIRS:
            fee = p.determine_general_repair_fee()
            logs.append(f"{p.name} pays general repairs: ${fee}.")
            p.pay(fee, self.bank)
        elif card == ChanceCards.GET_OUT_OF_JAIL_FREE:
            logs.append(f"{p.name} receives a Get Out of Jail Free (Chance).")
            p.chance_jail_free_card = True
        elif card == ChanceCards.GO_BACK_THREE:
            logs.append(f"{p.name} goes back 3 spaces.")
            p.go_back_three(len(self.board.tiles))
        elif card == CommunityChestCards.BANK_ERROR:
            logs.append(f"{p.name} gets $200 from Bank Error.")
            p.earn(200)
        elif card == CommunityChestCards.DOCTOR_FEE:
            logs.append(f"{p.name} pays $50 Doctor Fee.")
            p.pay(50, self.bank)
        elif card == CommunityChestCards.STOCK_SALE:
            logs.append(f"{p.name} gets $50 from Stock Sale.")
            p.earn(50)
        elif card == CommunityChestCards.GET_OUT_OF_JAIL_FREE:
            logs.append(f"{p.name} receives a Get Out of Jail Free (Chest).")
            p.community_chest_jail_free_card = True
        elif card == CommunityChestCards.HOLIDAY_FUND:
            logs.append(f"{p.name} receives $100 from Holiday Fund.")
            p.earn(100)
        elif card == CommunityChestCards.INCOME_TAX_REFUND:
            logs.append(f"{p.name} collects $20 from Income Tax Refund.")
            p.earn(20)
        elif card == CommunityChestCards.BIRTHDAY:
            logs.append(f"Birthday: each other player pays $10 to {p.name}.")
            for pl in self.players:
                if pl != p and pl.is_in_game:
                    pl.pay(10, p)
        elif card == CommunityChestCards.LIFE_INSURANCE:
            logs.append(f"{p.name} gets $100 from Life Insurance.")
            p.earn(100)
        elif card == CommunityChestCards.HOSPITAL_FEES:
            logs.append(f"{p.name} pays $100 Hospital Fees.")
            p.pay(100, self.bank)
        elif card == CommunityChestCards.SCHOOL_FEES:
            logs.append(f"{p.name} pays $50 School Fees.")
            p.pay(50, self.bank)
        elif card == CommunityChestCards.CONSULTANCY_FEE:
            logs.append(f"{p.name} gets $25 Consultancy Fee.")
            p.earn(25)
        elif card == CommunityChestCards.BEAUTY_CONTEST:
            logs.append(f"{p.name} wins $10 from Beauty Contest.")
            p.earn(10)
        elif card == CommunityChestCards.INHERITANCE:
            logs.append(f"{p.name} inherits $100.")
            p.earn(100)

    def handle_railroad_landing(self, p: Player, tile: RailRoad, logs: List[str]):
        if tile.owner is None:
            decide = p.decide_to_buy_property(tile)
            logs.append(f"{p.name} lands on {tile.name}, decides to buy? {decide}")
            if decide:
                p.buy_property(tile)
                if tile.owner == p:
                    logs.append(f"{p.name} bought {tile.name} for ${tile.price}.")
        else:
            if tile.owner != p and tile.owner.is_in_game:
                rent = tile.calculate_rent(p)
                logs.append(f"{p.name} pays ${rent} RR rent to {tile.owner.name}.")
                p.pay(rent, tile.owner)


###############################################################################
#                               GUI LAYOUT                                    #
###############################################################################


def tile_to_grid_position(tile_index: int) -> Tuple[int, int]:
    # corners: 0 => bottom-left, 10 => top-left, 20 => top-right, 30 => bottom-right
    # The board is an 11×11 grid, perimeter only
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
        self.root = root
        self.root.title("Monopoly Board with Logs")

        # Create example players
        self.players = [
            Player("Alice", 0.8, 0.7, 0.6, 0.5, 0.5, 200, 300),
            Player("Bob", 0.6, 0.8, 0.7, 0.4, 0.6, 200, 300),
        ]
        self.game = Game(*self.players)

        # Frames: board on left, info/log on right
        self.board_frame = ttk.Frame(self.root, padding=5)
        self.board_frame.grid(row=0, column=0, sticky="nwes")
        self.info_frame = ttk.Frame(self.root, padding=5)
        self.info_frame.grid(row=0, column=1, sticky="nwes")

        # 11×11 grid for board
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

        # Text area for player info + logs
        self.player_info_text = tk.Text(self.info_frame, width=45, height=30)
        self.player_info_text.pack(side="top", fill="both", expand=True)

        # Next Turn button
        self.next_button = ttk.Button(
            self.info_frame, text="Next Turn", command=self.next_turn
        )
        self.next_button.pack(side="bottom", pady=10)

        self.update_gui()

    def update_gui(self):
        self.update_board_labels()
        self.update_player_info()

    def update_board_labels(self):
        # Clear all
        for r in range(11):
            for c in range(11):
                self.board_labels[r][c].config(text="", background="#dddddd")

        # Fill perimeter
        for i, tile in enumerate(self.game.board.tiles):
            row, col = tile_to_grid_position(i)
            txt = f"#{i} {tile.type}"
            if isinstance(tile, Property):
                txt = f"#{i}\n{tile.name}"
                if tile.owner:
                    txt += f"\nOwner: {tile.owner.name}"
                if isinstance(tile, Street):
                    txt += f"\nLvl:{tile.level}"
            # which players
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
            # Print logs after current status
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
