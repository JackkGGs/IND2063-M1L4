import discord
from discord.ext import commands
import random
from config import token
from logic import Pokemon, Wizard, Fighter, Healer, Trapper

# Mengatur intents untuk bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True 
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Event yang terpicu saat bot siap dan terhubung ke Discord."""
    print(f'Logged in as {bot.user.name}')
    print('Bot siap dimainkan!')

@bot.command()
async def go(ctx):
    """
    Perintah untuk membuat Pokémon bagi pengguna.
    Seorang pengguna hanya dapat membuat satu Pokémon per sesi bot.
    """
    author = ctx.author.name
    if author not in Pokemon.pokemons.keys():
        # Secara acak memilih jenis Pokémon untuk pengguna
        pokemon_types = [Pokemon, Wizard, Fighter, Healer, Trapper]
        chosen_type = random.choice(pokemon_types)
        
        # Membuat instance baru dari kelas Pokémon yang dipilih
        pokemon = chosen_type(author)
        
        # Mengirim informasi dan gambar Pokémon awal
        await ctx.send(f"Anda telah membuat Pokémon baru dengan tipe: {chosen_type.__name__}!")
        await ctx.send(await pokemon.info())
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Gagal mengunggah gambar Pokémon.")
    else:
        await ctx.send("Anda sudah membuat Pokémon Anda.")
        
@bot.command()
async def start(ctx):
    """
    Menyediakan pesan sambutan sederhana dan instruksi tentang cara memulai permainan.
    """
    await ctx.send("Hai, saya adalah bot game Pokémon! Untuk membuat pokemon Anda sendiri, masukkan !go")

@bot.command()
async def info(ctx):
    """
    Menampilkan statistik saat ini (nama, kekuatan, hp) dari Pokémon pengguna.
    """
    author = ctx.author.name
    if author in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[author]
        await ctx.send(await pokemon.info())
    else:
        await ctx.send("Anda belum memiliki Pokémon! Gunakan `!go` untuk membuatnya.")

@bot.command()
async def feed(ctx):
    """
    Memberi makan Pokémon pengguna, meningkatkan HP-nya.
    """
    author = ctx.author.name
    if author in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[author]
        await ctx.send(await pokemon.feed())
    else:
        await ctx.send("Anda belum memiliki Pokémon! Gunakan `!go` untuk membuatnya.")

@bot.command()
async def attack(ctx, member: discord.Member):
    """
    Memulai serangan pada Pokémon pengguna lain.
    Penggunaan: !attack @<sebutan_pengguna>
    """
    attacker_name = ctx.author.name
    target_name = member.name
    
    if attacker_name not in Pokemon.pokemons.keys():
        await ctx.send("Anda belum memiliki Pokémon! Gunakan `!go` untuk membuatnya.")
        return

    if target_name not in Pokemon.pokemons.keys():
        await ctx.send(f"Target, {target_name}, tidak memiliki Pokémon untuk diserang!")
        return

    attacker = Pokemon.pokemons[attacker_name]
    target = Pokemon.pokemons[target_name]
    
    await ctx.send(await attacker.attack(target))
    
@bot.command()
async def heal(ctx, member: discord.Member):
    """
    Menyembuhkan Pokémon pengguna lain. Hanya dapat digunakan oleh Pokémon Healer.
    Penggunaan: !heal @<sebutan_pengguna>
    """
    healer_name = ctx.author.name
    target_name = member.name

    if healer_name not in Pokemon.pokemons.keys():
        await ctx.send("Kamu belum punya Pokemon! inisiasi `!go` untuk membuat pokemon baru.")
        return

    healer = Pokemon.pokemons[healer_name]
    
    # Check if the user's Pokémon is a Healer type
    if not isinstance(healer, Healer):
        await ctx.send("Pokemon anda bukan healer, command ini tidak dapat digunakan.")
        return
        
    if target_name not in Pokemon.pokemons.keys():
        await ctx.send(f"Target, {target_name}, tidak memiliki pokemon!")
        return

    target = Pokemon.pokemons[target_name]
    
    await ctx.send(await healer.heal(target))

bot.run(token)
