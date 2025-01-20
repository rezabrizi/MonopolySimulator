import random
from abc import ABC, abstractmethod
from typing import Dict, Optional, List, Tuple, Union
from enum import Enum
from collections import deque


class Board:
    def __init__(self):
        self.tiles = []
        self.initialize_board()

    def initialize_board(self):
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


class Chance(Block):
    chance_deque = deque([chance for chance in ChanceCards])

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
    community_chest_deque = deque(
        [community_chest for community_chest in CommunityChestCards]
    )

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

    def apply_tax(self, player: "Player"):
        player.pay(self.amount)


class Property(Block):
    def __init__(self, name, price, number):
        super().__init__("property", number=number)
        self.name = name
        self.price = price
        self.mortgage = self.price // 2
        self.unmortgage = self.mortgage * 1.1
        self.mortgaged = False
        self.owner: Optional[Player] = None

    @abstractmethod
    def calculate_rent(self):
        pass


class Utility(Property):
    def __init__(self, name, price, number):
        super().__init__(name, price, number)

    def calculate_rent(self, dice_roll, player):
        if self.owner is None:
            return 0
        if self.mortgaged == True:
            return 0
        if self.owner == player:
            return 0
        return dice_roll * (10 if len(self.owner.utilities) == 2 else 4)


class RailRoad(Property):
    def __init__(self, name: str, price: int, rent: List[int], number: int):
        super().__init__(name, price, number)
        self.rent = rent

    def calculate_rent(self, player):
        if self.owner is None:
            return 0
        if self.mortgaged == True:
            return 0
        if self.owner == player:
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
        # level 0 - normal rent
        # level 1 - all cards owned
        # level 2:5 - houses 1 to 4
        # level 6 - hotel
        self.level = 0

    def __repr__(self):
        return (
            f"Street(name='{self.name}', group='{self.group.name}', price={self.price}, "
            f"rent={self.rent}, house_price={self.house_price}, level={self.level}, "
            f"mortgaged={self.mortgaged}, owner={self.owner.name if self.owner else None})"
        )

    def calculate_rent(self, player):
        if self.owner is None:
            return 0
        if self.mortgaged == True:
            return 0
        if self.owner == player:
            return 0
        return self.rent[self.level - 1]


class Bank:
    def __init__(self):
        pass

    def earn(self, amount):
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
        self.liquidity: int = 1500
        self.streets: Dict[str, List[Street]] = {}
        self.railroads: List[RailRoad] = []
        self.utilities: List[Utility] = []
        self.is_in_game: bool = True
        self.position: int = 0
        self.last_dice_roll: int = 0
        self.community_chest_jail_free_card: bool = False
        self.chance_jail_free_card: bool = False

    def __repr__(self):
        return (
            f"Player("
            f"name='{self.name}', "
            f"cash={self.cash}, "
            f"position={self.position}, "
            f"is_in_jail={self.is_in_jail}, "
            f"jail_roll_attempts={self.jail_roll_attempts}, "
            f"streets_owned={len(self.streets)}, "
            f"railroads_owned={len(self.railroads)}, "
            f"utilities_owned={len(self.utilities)}, "
            f"is_in_game={self.is_in_game}"
            f")"
        )

    def has_jail_free_card(self) -> bool:
        return self.community_chest_jail_free_card or self.chance_jail_free_card

    def decide_to_use_jail_free_card(self) -> bool:
        return random.random() < self.w_use_jail_free_card

    def use_jail_free_card(self) -> None:
        if self.chance_jail_free_card:
            self.chance_jail_free_card = False
            Chance.put_jail_free_card_back()
        elif self.community_chest_jail_free_card:
            self.community_chest_jail_free_card = False
            CommunityChest.put_jail_free_card_back()
        else:
            raise Exception(
                "Should only call this when the player has a jail free card"
            )

    def reset_jail_roll_attempts(self):
        self.jail_roll_attempts = 0

    def decide_to_roll_for_doubles(self) -> bool:
        return random.random() < self.w_roll_double_in_jail

    def advance_to_illinois(self) -> None:
        if self.position > 24:
            self.earn(200)
        self.position = 24

    def advance_to_st_charles(self) -> None:
        if self.position > 11:
            self.earn(200)
        self.position = 11

    def advance_to_nearest_utility(self):
        if self.position < 12:
            self.position = 12
        else:
            self.position = 28

    def advance_to_nearest_railroad(self):
        if self.position < 5 or self.position > 35:
            self.position = 5
        if self.position < 15:
            self.position = 15
        if self.position < 25:
            self.position = 25
        if self.position < 35:
            self.position = 35

    def advance_to_reading_railroad(self):
        if self.position > 5:
            self.earn(200)
        self.position = 5

    def advance_to_go(self):
        self.position = 0
        self.earn(200)

    def advance_to_boardwalk(self):
        self.position = 39

    def determine_street_repair_fee(self):
        total = 0
        for _group, streets in self.streets.items():
            for street in streets:
                if street.level == 6:
                    total += 115
                elif street.level >= 2:
                    num_houses = street.level - 1
                    total += 40 * num_houses
        return total

    def determine_general_repair_fee(self):
        total = 0
        for _group, streets in self.streets.items():
            for street in streets:
                if street.level == 6:
                    total += 100
                elif street.level >= 2:
                    num_houses = street.level - 1
                    total += 25 * num_houses
        return total

    def go_back_three(self, board_size: int):
        self.position = (self.position - 3 + board_size) % board_size

    def get_valid_expandable_sets(self) -> Dict[str, List[Street]]:
        """Get a dictionary of all the compeleted sets that still have capacity to build houses on"""
        sets: Dict[str, List[Street]] = {}
        for group, properties in self.streets.items():
            if (
                len(properties) == Street.GROUP_COUNTS[group]
                and not all(prop.level == 6 for prop in properties)
                and all(not prop.mortgaged for prop in properties)
            ):
                sets[group] = properties

        return sets

    def buy_houses_and_hotels(self, priority: str = "quantity_price"):
        """
        Buy houses and hotels based on the specified priority:
        - "random": Randomize the order of groups.
        - "quantity_price": Sort groups based on total house levels and minimum house price.
        """
        from random import shuffle

        # Get all completed sets that can still be expanded (not maxed out)
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
                        sum(
                            prop.level for prop in item[1]
                        ),  # Total house levels in the group
                        min(
                            prop.house_price for prop in item[1]
                        ),  # Minimum house price
                    ),
                )
            ]
            return groups

        # Determine group order based on the priority
        if priority == "random":
            groups = get_groups_based_on_random()
        elif priority == "quantity_price":
            groups = get_groups_based_on_house_quantity_price_priority()
        else:
            raise ValueError("Invalid priority. Use 'random' or 'quantity_price'.")

        # Continue building while there is cash above min_cash
        while self.cash > self.min_cash:
            built = False  # Track if any house was built in this iteration

            # Iterate through the prioritized groups
            for group in groups:
                properties = completed_sets[group]

                # Find the properties with the minimum house level in the group
                min_level = min(property.level for property in properties)
                # If the group has hotels built on all of the streets then go to the next group
                if min_level == 6:
                    continue

                target_properties = [
                    property for property in properties if property.level == min_level
                ]

                # Attempt to build one house on each property with the least houses in the group
                for property in target_properties:
                    if self.cash - property.house_price >= self.min_cash:
                        self.buy_house(property)
                        built = True
                    else:
                        break  # Stop if funds are insufficient for further houses

            # Break the loop if no houses were built in this iteration
            if not built:
                break

    def unmortgage_properties(self):
        # Filter mortgaged properties by group
        mortgaged_groups = {
            group: properties
            for group, properties in self.streets.items()
            if any(prop.mortgaged for prop in properties)
        }

        sorted_groups = sorted(
            mortgaged_groups.items(),
            key=lambda item: len(item[1]),
            reverse=True,
        )

        for group, properties in sorted_groups:
            for property in properties:
                if (
                    property.mortgaged
                    and self.cash - property.unmortgage >= self.min_cash_to_unmortgage
                ):
                    self.cash -= property.unmortgage
                    self.liquidity -= property.unmortgage
                    property.mortgaged = False

    def transfer_ownership_of_all_assets_to_another_player(self, other: "Player"):
        # CASH
        other.earn(self.cash)
        self.cash = 0
        self.liquidity = 0

        # STREETS
        for group, streets in self.streets.items():
            for street in streets:
                street.owner = other
                other.receive_street(street)
        self.streets.clear()

        # RAILROADS
        while self.railroads:
            current_railroad = self.railroads.pop()
            current_railroad.owner = other
            other.railroads.append(current_railroad)

        # UTILITIES
        while self.utilities:
            current_utility = self.utilities.pop()
            current_utility.owner = other
            other.utilities.append(current_utility)

        # JAIL FREE CARDS
        if self.community_chest_jail_free_card:
            other.community_chest_jail_free_card = True
        if self.chance_jail_free_card:
            other.chance_jail_free_card = True

    def transfer_ownership_of_all_assets_to_the_bank(self, to: Bank):
        ## TODO: Technically bank should auction everything
        ## However for now this implementation just frees the cards so they can be repurchased
        self.cash = 0
        self.liquidity = 0

        for group, streets in self.streets.items():
            for street in streets:
                street.owner = None
        self.streets.clear()

        # RAILROADS
        while self.railroads:
            current_railroad = self.railroads.pop()
            current_railroad.owner = None

        # UTILITIES
        while self.utilities:
            current_utility = self.utilities.pop()
            current_utility.owner = None

        # JAIL FREE CARDS
        if self.community_chest_jail_free_card:
            CommunityChest.put_jail_free_card_back()
        if self.chance_jail_free_card:
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
        if self.liquidity < amount:
            self.is_in_game = False
            self.transfer_ownership_of_all_assets(to)
            return
        if self.cash < amount:
            self.raise_fund(amount=amount)
        to.earn(amount=amount)

    def earn(self, amount: int):
        self.cash += amount
        self.liquidity += amount

    def decide_to_buy_property_random(
        self, property: Union[Street, RailRoad, Utility]
    ) -> bool:
        if isinstance(property, Street):
            return random.random() < self.w_buy_building
        elif isinstance(property, RailRoad):
            return random.random() < self.w_buy_railroad
        elif isinstance(property, Utility):
            return random.random() < self.w_buy_utility
        return False

    def decide_to_buy_property(self, property: Union[Street, RailRoad, Utility]):
        return self.decide_to_buy_property_random(property)

    def buy_property(self, property: "Property"):
        if property.owner is not None:
            return
        self.cash -= property.price
        self.liquidity -= property.price
        self.liquidity += property.mortgage
        property.owner = self
        if isinstance(property, Street):
            if property.group not in self.streets:
                self.streets[property.group] = []
            self.streets[property.group].append(property)
        elif isinstance(property, RailRoad):
            self.railroads.append(property)
        elif isinstance(property, Utility):
            self.utilities.append(property)

    def buy_house(self, property: "Street"):
        property.level += 1
        self.cash -= property.house_price
        self.liquidity -= property.house_price
        self.liquidity += property.house_price // 2

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
        NOTE: It is assumed this function is only called if it is actually possible to achieve amount (total_assets > amount)
        """

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
                self.liquidity -= property.house_price // 2
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

            if not property_frequency:
                return
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
                            self.liquidity -= property.mortgage
                            property.mortgaged = True
                        if self.cash >= amount:
                            return

        raise_fund_by_selling_houses()
        if self.cash >= amount:
            return

        raise_fund_by_mortgaging_properties()

    def move(self, steps, board_size):
        self.last_dice_roll = steps
        self.position = self.position + steps
        if self.position / board_size >= 1:
            self.cash += 200
            self.liquidity += 200
        self.position %= board_size

    def get_position(self):
        return self.position

    def go_to_jail(self):
        self.is_in_jail = True
        self.position = 10


class Game:
    def __init__(self, p1, p2, p3=None, p4=None):
        # Create a game board
        self.board = Board()
        self.players: List[Player] = [p1, p2]
        if p3:
            self.players.append(p3)
        if p4:
            self.players.append(p4)
        self.bank = Bank()
        self.current_player_index = 0

    def roll_dice(self):
        return random.randint(1, 6), random.randint(1, 6)

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def check_win_condition(self) -> Optional[Player]:
        active_players = [p for p in self.players if p.is_in_game]
        if len(active_players) == 1:
            return active_players[0]
        return None

    def play_turn(self):
        player = self.players[self.current_player_index]

        if not player.is_in_game:
            self.next_player()
            return

        d1, d2 = self.roll_dice()
        if player.is_in_jail:
            skip, d1_j, d2_j = self.attempt_jail_break(player)
            if skip:
                self.next_player()
                return
            if d1 and d2:
                d1 = d1_j
                d2 = d2_j

        player.move(d1 + d2, len(self.board.tiles))
        tile = self.board.tiles[player.position]
        self.handle_tile_landing(player, tile)

        # DOUBLE DICE CHECKS
        if d1 == d2:
            player.consecutive_doubles += 1
            if player.consecutive_doubles == 3:
                player.go_to_jail()
                player.consecutive_doubles = 0
                self.next_player()
        else:
            player.consecutive_doubles = 0
            self.next_player()

        # POST MOVE ACTIONS
        player.unmortgage_properties()
        player.buy_houses_and_hotels()

    def handle_tile_landing(self, player: Player, tile: Block):
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
        elif isinstance(tile, Block) and tile.type == "go_to_jail":
            player.go_to_jail()

    def handle_street_landing(self, player: Player, street: Street):
        if street.owner is None:
            # Player can buy the property if they have enough money
            if player.decide_to_buy_property(street):
                player.buy_property(street)
        elif street.owner != player and street.owner.is_in_game:
            # Player pays rent if the property is owned
            rent = street.calculate_rent(player)
            player.pay(rent, street.owner)

    def handle_railroad_landing(self, player: Player, railroad: RailRoad):
        if railroad.owner is None:
            # Player can buy the railroad if they have enough money
            if player.decide_to_buy_property(railroad):
                player.buy_property(railroad)
        elif railroad.owner != player and railroad.owner.is_in_game:
            # Player pays rent to the railroad owner
            rent = railroad.calculate_rent(player)
            player.pay(rent, railroad.owner)

    def handle_utility_landing(self, player: Player, utility: Utility):
        if utility.owner is None:
            # Player can buy the utility if they have enough money
            if player.decide_to_buy_property(utility):
                player.buy_property(utility)
        elif utility.owner != player and utility.owner.is_in_game:
            # Player pays rent based on dice roll
            dice_roll = (
                player.last_dice_roll
            )  # Assuming dice roll is stored on the player
            rent = utility.calculate_rent(dice_roll, player)
            player.pay(rent, utility.owner)

    def handle_chance_landing(self, player: Player, chance: Chance):
        card = Chance.get_chance_card()
        # Handle the effect of the chance card
        self.resolve_card_effect(player, card)

    def handle_community_chest_landing(
        self, player: Player, community_chest: CommunityChest
    ):
        card = CommunityChest.get_community_chest_card()
        # Handle the effect of the community chest card
        self.resolve_card_effect(player, card)

    def handle_tax_landing(self, player: Player, tax: Tax):
        # Player pays the tax amount
        player.pay(tax.amount, self.bank)

    def resolve_card_effect(self, player: Player, card: Enum):
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
                    # Player pays rent based on dice roll
                    d1, d2 = self.roll_dice()
                    rent = (d1 + d2) * 10
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
                    rent = railroad.calculate_rent(player)
                    player.pay(rent * 2, railroad.owner)

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
            for i in range(len(self.players)):
                if i != self.current_player_index:
                    player.pay(50, self.players[i])
        elif card == ChanceCards.BUILDING_LOAN:
            player.earn(150)
        elif (
            card == ChanceCards.STREET_REPAIRS
            or card == CommunityChestCards.STREET_REPAIRS
        ):
            player.pay(player.determine_street_repair_fee(), self.bank)
        elif card == ChanceCards.POOR_TAX:
            player.pay(15, self.bank)
        elif card == ChanceCards.GENERAL_REPAIRS:
            player.pay(player.determine_general_repair_fee(), self.bank)
        elif card == ChanceCards.GET_OUT_OF_JAIL_FREE:
            player.chance_jail_free_card = True
        elif card == ChanceCards.GO_BACK_THREE:
            player.go_back_three(len(self.board.tiles))
        elif CommunityChestCards.BANK_ERROR:
            player.earn(200)
        elif CommunityChestCards.DOCTOR_FEE:
            player.pay(50, self.bank)
        elif CommunityChestCards.STOCK_SALE:
            player.earn(50)
        elif CommunityChestCards.GO_TO_JAIL:
            player.go_to_jail()
        elif CommunityChestCards.GET_OUT_OF_JAIL_FREE:
            player.community_chest_jail_free_card = True
        elif CommunityChestCards.HOLIDAY_FUND:
            player.earn(100)
        elif CommunityChestCards.INCOME_TAX_REFUND:
            player.earn(20)
        elif CommunityChestCards.BIRTHDAY:
            for i in range(len(self.players)):
                if i != self.current_player_index:
                    other_player = self.players[i]
                    other_player.pay(10, player)
        elif CommunityChestCards.LIFE_INSURANCE:
            player.earn(100)
        elif CommunityChestCards.SCHOOL_FEES:
            player.pay(50, self.bank)
        elif CommunityChestCards.CONSULTANCY_FEE:
            player.earn(25)
        elif CommunityChestCards.BEAUTY_CONTEST:
            player.earn(10)
        elif CommunityChestCards.INHERITANCE:
            player.earn(100)

    def attempt_jail_break(
        self, player: Player
    ) -> Tuple[bool, Optional[int], Optional[int]]:
        # Check if the player has a "Get Out of Jail Free" card
        if player.has_jail_free_card():
            use_card = player.decide_to_use_jail_free_card()
            if use_card:
                player.use_jail_free_card()
                player.reset_jail_roll_attempts()
                d1, d2 = self.roll_dice()
                return (False, d1, d2)

        # Check if the player has attempted rolling a double less than 3 times
        if player.jail_roll_attempts < 3:
            roll_doubles = player.decide_to_roll_for_doubles()
            if roll_doubles:
                d1, d2 = self.roll_dice()
                if d1 == d2:  # Player rolled a double
                    player.reset_jail_roll_attempts()  # Reset attempts
                    return (False, d1, d2)
                else:  # Double not rolled, increment attempts
                    player.jail_roll_attempts += 1
                    return (True, None, None)

        # If all attempts to roll a double fail, the player pays $50
        player.pay(50, to=self.bank)
        if player.is_in_game:
            player.reset_jail_roll_attempts()
            d1, d2 = self.roll_dice()
            return (False, d1, d2)
        else:
            return (True, -1, -1)

    def simulate_game(self):
        winner = None
        while not winner:
            self.play_turn()
            winner = self.check_win_condition()
        return winner


class MonteCarloSimulation:
    def __init__(self, runs: int):
        """
        Initialize the simulation with the number of runs.
        """
        self.runs = runs

    def run(self):
        """
        Run the Monte Carlo simulation.
        Returns:
            dict: A dictionary mapping player names to the number of wins.
        """
        win_count = {}

        for _ in range(self.runs):
            # Create players with differing strategies
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

            # Initialize the Game with all four players
            game = Game(*players)

            # Simulate the game and retrieve the winner
            winner = game.simulate_game()
            print("Game is done!")

            # Tally the wins
            if winner.name not in win_count:
                win_count[winner.name] = 0
            win_count[winner.name] += 1

        return win_count


# Example usage:
# simulation = MonteCarloSimulation(runs=10000)
# results = simulation.run()
# print("Win counts:", results)
