from enum import Enum

class CityEnum(Enum):
    bialystok = 0
    bydgoszcz = 1
    czestochowa = 2
    gdansk = 3
    gdynia = 4
    katowice = 5
    krakow = 6
    lodz = 7
    lublin = 8
    poznan = 9
    radom = 10
    rzeszow = 11
    szczecin = 12
    warszawa = 13
    wroclaw = 14

class TypeEnum(Enum):
    apartmentBuilding = 0
    blockOfFlats = 1
    tenement = 2

class ClassPremium(Enum):
    normal = 0
    premium = 1
