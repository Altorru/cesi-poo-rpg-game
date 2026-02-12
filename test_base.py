import pytest
from base import Hero, Enemy, Boss
from observer import GameObserver

@pytest.fixture
def hero():
    """Fixture pour créer un héros de test"""
    return Hero("John", "warrior", 100, 20)

@pytest.fixture
def enemy():
    """Fixture pour créer un ennemi de test"""
    return Enemy("Goblin", "beast", 50, 10)

@pytest.fixture
def boss():
    """Fixture pour créer un boss de test"""
    return Boss("Dragon", 200, 30)

# ----- Tests pour Hero -----
def test_hero_initialization(hero):
    """Test de l'initialisation du héros"""
    assert hero.name == "John"
    assert hero._pv == 100
    assert hero.damage == 20

def test_hero_take_damage(hero):
    """Test de la prise de dégâts du héros"""
    hero.take_damage(30)
    assert hero._pv == 70

def test_hero_heal(hero):
    """Test de la guérison du héros"""
    hero.take_damage(50)
    hero.heal(20)
    assert hero._pv == 70

def test_hero_max_heal(hero):
    """Test que les PV du héros ne dépassent pas le maximum lors de la guérison"""
    hero.take_damage(30)
    hero.heal(50)
    assert hero._pv == 100  # Ne doit pas dépasser les _pv max

def test_hero_death(hero):
    """Test que le héros meurt correctement et PV ne devient pas négatif"""
    hero.take_damage(100)
    assert hero._pv == 0
    assert hero.is_alive() == False

def test_hero_attack(hero, enemy): # randomize(weapon.damage + self.damage) qui random entre 0.9 et 1.1
    """Test de l'attaque du héros sur un ennemi"""
    damage_min = int(20 * 0.9)  # damage de base 20, randomisé à 90%
    damage_max = int(20 * 1.1)  # damage de base 20, randomisé à 110%
    hero.attack(enemy)
    assert enemy._pv <= 50 - damage_min
    assert enemy._pv >= 50 - damage_max