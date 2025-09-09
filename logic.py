import aiohttp
import random
from random import randint
from datetime import datetime, timedelta
import asyncio


class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.img = None
        self.power = random.randint(30, 60)
        self.hp = random.randint(200, 400)
        self.last_feed_time = datetime.now()
        if pokemon_trainer not in self.pokemons:
            self.pokemons[pokemon_trainer] = self

    async def feed(self, feed_interval=60, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"HP pokemon meningkat. HP pokemon sekarang: {self.hp}"
        else:
            return f"Waktu makan pokemon berikutnya: {current_time+delta_time}"

    async def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['forms'][0]['name']
                else:
                    return "Pikachu"

    async def info(self):
        if not self.name:
            self.name = await self.get_name()
        return f"""Nama pokemon anda: {self.name}
ATK pokemon anda: {self.power}
HP pokemon anda: {self.hp}"""

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    img_url = data['sprites']['front_default']
                    return img_url 
                else:
                    return None

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = randint(1, 5)
            if chance == 1:
                return "Pokemon Penyihir menggunakan perisai dalam pertempuran"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pertempuran @{self.pokemon_trainer} dengan @{enemy.pokemon_trainer}\nHP @{enemy.pokemon_trainer} sekarang {enemy.hp}"
        else:
            enemy.hp = 0
            return f"@{self.pokemon_trainer} menang lawan @{enemy.pokemon_trainer}!"

# Move subclasses into the same file
class Wizard(Pokemon):
    async def feed(self):
        return await super().feed(hp_increase=20)

class Fighter(Pokemon):
    async def attack(self, enemy):
        super_power = randint(5, 15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nPokemon petarung menggunakan kekuatan serangan super:{super_power}"
    
    async def feed(self):
        return await super().feed(feed_interval=10)

class Healer(Pokemon):
    async def feed(self):
        return await super().feed(hp_increase=30)

    async def heal(self, target, hp_increase=100):
        self.hp -= 50
        target.hp += hp_increase
        if self.hp <= 0:
            self.hp = 0
            return f"@{self.pokemon_trainer} telah mengorbankan diri untuk menyembuhkan @{target.pokemon_trainer}!"
        
        return f"@{self.pokemon_trainer} menyembuhkan @{target.pokemon_trainer}.\nHP @{target.pokemon_trainer} sekarang: {target.hp}."

class Trapper(Pokemon):
    async def attack(self, enemy):
        power_decrease = randint(1, 10)
        enemy.power -= power_decrease
        result = await super().attack(enemy)
        return result + f"\nPokemon trapper milik @{self.pokemon_trainer} mengurangi Power pokemon @{enemy.pokemon_trainer} (-{power_decrease} ATK)!"