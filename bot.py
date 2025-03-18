from telethon import TelegramClient, events, Button
import random
import asyncio
import time

# Bot credentials
API_ID = ####
API_HASH = '###'
BOT_TOKEN = '####'

# Initialize bot
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Message store for handling encryption
_message_store = {}

# Encryption classes
class NumberEncryption:
    def __init__(self):
        self.number_replacements = {
            'a': '4', 'b': '8', 'e': '3', 'i': '1', 'l': '1',
            'o': '0', 's': '5', 't': '7', 'z': '2',
            'A': '4', 'B': '8', 'E': '3', 'I': '1', 'L': '1',
            'O': '0', 'S': '5', 'T': '7', 'Z': '2'
        }

    def encrypt(self, text):
        words = text.split()
        encrypted_words = []
        
        for word in words:
            if len(word) < 3:
                encrypted_words.append(word)
                continue
            
            num_chars = max(2, int(len(word) * 0.3))
            positions = random.sample(range(len(word)), num_chars)
            word_list = list(word)
            
            for pos in positions:
                char = word_list[pos]
                if char in self.number_replacements:
                    word_list[pos] = self.number_replacements[char]
            
            encrypted_words.append(''.join(word_list))
        
        return ' '.join(encrypted_words)

class LookAlikeEncryption:
    def __init__(self):
        self.look_alike = {
            'a': ['а', 'α', 'ɑ'], 'b': ['б', 'ḅ', 'ɓ'],
            'c': ['с', 'ϲ', 'ċ'], 'd': ['ԁ', 'ḍ', 'ɗ'],
            'e': ['е', 'ε', 'ẹ'], 'f': ['ḟ', 'ƒ', 'ғ'],
            'g': ['ġ', 'ģ', 'ǵ'], 'h': ['һ', 'ḥ', 'ħ'],
            'i': ['і', 'ḭ', 'ı'], 'j': ['ј', 'ʝ', 'ɉ'],
            'k': ['к', 'ḳ', 'ķ'], 'l': ['ӏ', 'ḷ', 'ļ'],
            'm': ['м', 'ṃ', 'ṁ'], 'n': ['ո', 'ṇ', 'ņ'],
            'o': ['о', 'ο', 'ọ'], 'p': ['р', 'ρ', 'ṗ'],
            'q': ['զ', 'ԛ', 'ʠ'], 'r': ['г', 'ṛ', 'ŗ'],
            's': ['ѕ', 'ṣ', 'ş'], 't': ['т', 'ṭ', 'ţ'],
            'u': ['υ', 'ц', 'ụ'], 'v': ['ν', 'ѵ', 'ṿ'],
            'w': ['ѡ', 'ẉ', 'ẇ'], 'x': ['х', 'ẋ', 'ẍ'],
            'y': ['у', 'ỵ', 'ÿ'], 'z': ['z', 'ẓ', 'ž']
        }
        # Add uppercase variants
        upper_look_alike = {k.upper(): [c.upper() if c.upper() != c else c for c in v] 
                          for k, v in self.look_alike.items()}
        self.look_alike.update(upper_look_alike)

    def encrypt(self, text):
        words = text.split()
        encrypted_words = []
        
        for word in words:
            if len(word) < 3:
                encrypted_words.append(word)
                continue
            
            num_chars = max(2, int(len(word) * 0.3))
            positions = random.sample(range(len(word)), num_chars)
            word_list = list(word)
            
            for pos in positions:
                char = word_list[pos]
                if char in self.look_alike:
                    word_list[pos] = random.choice(self.look_alike[char])
            
            encrypted_words.append(''.join(word_list))
        
        return ' '.join(encrypted_words)

class AccentEncryption:
    def __init__(self):
        self.accents = {
            'a': ['à', 'á', 'â', 'ã', 'ä', 'å'],
            'e': ['è', 'é', 'ê', 'ë'],
            'i': ['ì', 'í', 'î', 'ï'],
            'o': ['ò', 'ó', 'ô', 'õ', 'ö'],
            'u': ['ù', 'ú', 'û', 'ü'],
            'y': ['ý', 'ÿ'],
            'n': ['ñ']
        }
        # Add uppercase variants
        upper_accents = {k.upper(): [c.upper() for c in v] 
                        for k, v in self.accents.items()}
        self.accents.update(upper_accents)

    def encrypt(self, text):
        words = text.split()
        encrypted_words = []
        
        for word in words:
            if len(word) < 3:
                encrypted_words.append(word)
                continue
            
            num_chars = max(2, int(len(word) * 0.3))
            positions = random.sample(range(len(word)), num_chars)
            word_list = list(word)
            
            for pos in positions:
                char = word_list[pos]
                if char in self.accents:
                    word_list[pos] = random.choice(self.accents[char])
            
            encrypted_words.append(''.join(word_list))
        
        return ' '.join(encrypted_words)

# Initialize encryption methods
number_encryption = NumberEncryption()
lookalike_encryption = LookAlikeEncryption()
accent_encryption = AccentEncryption()

# Message handlers
@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    if not event.is_private:
        return
        
    user = await event.get_sender()
    welcome_msg = (
        f"Hello @{user.username}! Welcome to the Text Encryption Bot!\n\n"
        "Simply send me any text message to encrypt it with different options!\n"
        "Use /help to see available commands."
    )
    await event.respond(welcome_msg)

@bot.on(events.NewMessage(pattern='/help'))
async def help_handler(event):
    if not event.is_private:
        return
        
    user = await event.get_sender()
    is_owner = user.id in OWNER_IDS
    
    if is_owner:
        help_msg = (
            f"Hello @{user.username}! Here are all available commands:\n\n"
            "🔑 Available Commands:\n\n"
            "General Commands:\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n\n"
            "Admin Commands:\n"
            "/channel - View channel statistics and controls\n"
            "/group - View channel statistics and group\n"
            "/approve <user_id> - Approve a user to skip message deletion\n"
            "/skip <user_id> - Add user to skip list\n"
            "/unskip <user_id> - Remove user from skip list\n"
            "/unapprove <user_id> - Remove user from approved list\n\n"
            "Simply send me any text message to encrypt it with different options!"
        )
    else:
        help_msg = (
            f"Hello @{user.username}!\n\n"
            "🔑 Available Commands:\n\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n\n"
            "Simply send me any text message to encrypt it with different options!"
        )
    
    await event.respond(help_msg)

@bot.on(events.NewMessage)
async def message_handler(event):
    if not event.is_private:
        return
        
    if event.message.text and event.message.text.startswith('/'):
        return

    # Get text from message or caption
    text = event.message.text or event.message.caption or ""
    if not text:
        return await event.respond("Please send some text to encrypt!")

    # Store the original message
    _message_store[event.message.id] = {
        'text': text,
        'encrypted_msg_id': None
    }

    buttons = [
        [
            Button.inline("Numbers", b"1"),
            Button.inline("Look Alike", b"2"),
            Button.inline("Accents", b"3")
        ],
        [Button.inline("❌ Close", b"close")]
    ]
    
    response = await event.respond("Choose encryption method:", buttons=buttons)
    # Store reference to original message
    _message_store[f"response_{response.id}"] = str(event.message.id)


@bot.on(events.NewMessage)
async def message_handler(event):
    if not event.is_private:
        return
        
    if event.message.text and event.message.text.startswith('/'):
        return

    # Get text from message or caption
    text = event.message.text or event.message.caption or ""
    if not text:
        return await event.respond("Please send some text to encrypt!")

    # Store the original message
    _message_store[event.message.id] = {
        'text': text,
        'encrypted_msg_id': None
    }

    buttons = [
        [
            Button.inline("Numbers", b"1"),
            Button.inline("Look Alike", b"2"),
            Button.inline("Accents", b"3")
        ],
        [Button.inline("❌ Close", b"close")]
    ]
    
    response = await event.respond("Choose encryption method:", buttons=buttons)
    # Store reference to original message
    _message_store[f"response_{response.id}"] = str(event.message.id)


@bot.on(events.CallbackQuery)
async def callback_handler(event):
    data = event.data.decode()
    
    if data == "close":
        # Clean up stored messages only when closing
        original_msg = await event.get_message()
        original_msg_id = _message_store.get(f"response_{original_msg.id}")
        if original_msg_id:
            if int(original_msg_id) in _message_store:
                del _message_store[int(original_msg_id)]
            if f"response_{original_msg.id}" in _message_store:
                del _message_store[f"response_{original_msg.id}"]
        await event.delete()
        return

    if data not in ["1", "2", "3"]:
        return

    # Get the original message
    original_msg = await event.get_message()
    original_msg_id = _message_store.get(f"response_{original_msg.id}")
    
    if not original_msg_id:
        return await event.answer("No text found to encrypt!", alert=True)
    
    msg_data = _message_store.get(int(original_msg_id))
    if not msg_data:
        return await event.answer("No text found to encrypt!", alert=True)

    text = msg_data['text']

    # Process the text while preserving formatting
    words = []
    current_word = ""
    preserve_chars = ['\n', ' ', '\t', 'https://', 'http://', '@', '#']
    
    i = 0
    while i < len(text):
        # Check for URLs
        if text[i:].startswith(('https://', 'http://')):
            if current_word:
                words.append(current_word)
                current_word = ""
            url_end = text.find(' ', i) if ' ' in text[i:] else len(text)
            words.append(text[i:url_end])
            i = url_end
            continue
        
        # Check for special characters
        if any(text[i:].startswith(p) for p in preserve_chars):
            if current_word:
                words.append(current_word)
                current_word = ""
            words.append(text[i])
            i += 1
            continue
        
        current_word += text[i]
        i += 1
    
    if current_word:
        words.append(current_word)

    # Encrypt only words
    encrypted_words = []
    for word in words:
        if any(p in word for p in preserve_chars):
            encrypted_words.append(word)
        else:
            if data == "1":
                encrypted_words.append(number_encryption.encrypt(word))
            elif data == "2":
                encrypted_words.append(lookalike_encryption.encrypt(word))
            elif data == "3":
                encrypted_words.append(accent_encryption.encrypt(word))

    # Combine and send
    encrypted_text = ''.join(encrypted_words)
    
    # Get original message to check for media
    original_message = await event.client.get_messages(
        event.chat_id, 
        ids=int(original_msg_id)
    )

    # Update or send new encrypted message
    buttons = [
        [
            Button.inline("Numbers", b"1"),
            Button.inline("Look Alike", b"2"),
            Button.inline("Accents", b"3")
        ],
        [Button.inline("❌ Close", b"close")]
    ]

    if msg_data['encrypted_msg_id']:
        try:
            # Try to edit existing message
            await event.client.edit_message(
                event.chat_id,
                msg_data['encrypted_msg_id'],
                encrypted_text,
                file=original_message.media if hasattr(original_message, 'media') and original_message.media else None
            )
        except:
            # If edit fails, send new message
            new_msg = await event.respond(
                encrypted_text,
                file=original_message.media if hasattr(original_message, 'media') and original_message.media else None
            )
            msg_data['encrypted_msg_id'] = new_msg.id
    else:
        # Send first encrypted message
        new_msg = await event.respond(
            encrypted_text,
            file=original_message.media if hasattr(original_message, 'media') and original_message.media else None
        )
        msg_data['encrypted_msg_id'] = new_msg.id

    await event.answer("Text encrypted successfully!")

    # Keep the original message data for further encryption
    _message_store[int(original_msg_id)] = msg_data

    # Remove the cleanup code that was here before

# Add these constants at the top
OWNER_IDS = [5847637609, 5847637234, 2033053024]  # Added new admin ID
CHANNEL_ID = -1002690702208

# Add new class for channel encryption
class ChannelEncryption:
    def __init__(self):
        self.special_chars = {
            'A': 'А', 'B': 'В', 'C': 'С', 'D': 'Ð',
            'E': 'Е', 'F': 'Ғ', 'G': 'Ġ', 'H': 'Н',
            'I': 'І', 'J': 'Ј', 'K': 'К', 'L': 'Ł',
            'M': 'М', 'N': 'Н', 'O': 'О', 'P': 'Р',
            'Q': 'Q', 'R': 'Ř', 'S': 'Ѕ', 'T': 'Т',
            'U': 'Ü', 'V': 'Ѵ', 'W': 'Ш', 'X': 'Х',
            'Y': 'Ү', 'Z': 'Ż',
            # Add lowercase characters
            'a': 'а', 'b': 'b', 'c': 'с', 'd': 'ď',
            'e': 'е', 'f': 'ғ', 'g': 'ğ', 'h': 'ħ',
            'i': 'і', 'j': 'ј', 'k': 'к', 'l': 'ł',
            'm': 'м', 'n': 'ń', 'o': 'о', 'p': 'р',
            'q': 'ԛ', 'r': 'я', 's': 'ѕ', 't': 'ț',
            'u': 'ū', 'v': 'ѵ', 'w': 'ш', 'x': 'х',
            'y': 'ү', 'z': 'ź'
        }
        # Create a set of all special characters for faster lookup
        self.special_chars_values = set(self.special_chars.values())

    def is_encrypted(self, text):
        if not text:
            return False
            
        # Count special characters
        special_char_count = sum(1 for char in text if char in self.special_chars_values)
        
        # Calculate percentage (excluding spaces and special characters)
        text_length = sum(1 for char in text if char.isalnum())
        if text_length == 0:
            return False
            
        encryption_percentage = (special_char_count / text_length) * 100
        
        # Return True if at least 10% of characters are special
        return encryption_percentage >= 10

    def encrypt(self, text):
        # Process the text while preserving formatting
        words = []
        current_word = ""
        preserve_chars = ['\n', ' ', '\t']
        
        i = 0
        while i < len(text):
            # Check for URLs (http://, https://, t.me/)
            if i < len(text) - 7 and text[i:i+8].lower().startswith(('https://', 'http://')):
                if current_word:
                    words.append(current_word)
                    current_word = ""
                url_end = text.find(' ', i) if ' ' in text[i:] else len(text)
                words.append(text[i:url_end])
                i = url_end
                continue
            
            # Check for t.me links
            if i < len(text) - 4 and text[i:i+5].lower() == 't.me/':
                if current_word:
                    words.append(current_word)
                    current_word = ""
                url_end = text.find(' ', i) if ' ' in text[i:] else len(text)
                words.append(text[i:url_end])
                i = url_end
                continue
            
            # Check for usernames (@username)
            if i < len(text) and text[i] == '@':
                if current_word:
                    words.append(current_word)
                    current_word = ""
                # Find the end of the username (space or end of text)
                username_end = i
                while username_end < len(text) and text[username_end] != ' ' and text[username_end] != '\n':
                    username_end += 1
                words.append(text[i:username_end])
                i = username_end
                continue
            
            # Check for special characters
            if i < len(text) and text[i] in preserve_chars:
                if current_word:
                    words.append(current_word)
                    current_word = ""
                words.append(text[i])
                i += 1
                continue
            
            current_word += text[i]
            i += 1
        
        if current_word:
            words.append(current_word)

        # Encrypt only words that are not URLs, usernames, or special characters
        encrypted_words = []
        for word in words:
            # Skip encryption for usernames, URLs, and special characters
            if word.startswith('@') or word.lower().startswith(('http', 't.me/')) or word in preserve_chars:
                encrypted_words.append(word)
            else:
                # Apply encryption only to regular words
                num_chars = max(2, int(len(word) * 0.3))
                if len(word) > 2:  # Only encrypt words longer than 2 characters
                    positions = random.sample(range(len(word)), min(num_chars, len(word)))
                    word_list = list(word)
                    
                    for pos in positions:
                        char = word_list[pos]
                        if char in self.special_chars:
                            word_list[pos] = self.special_chars[char]
                    
                    encrypted_words.append(''.join(word_list))
                else:
                    encrypted_words.append(word)
        
        return ''.join(encrypted_words)


# Initialize channel encryption
channel_encryption = ChannelEncryption()

# Load channel state from config
def get_channel_state():
    config = load_config()
    return config['channel_settings']

def save_channel_state(state):
    config = load_config()
    config['channel_settings'].update(state)
    save_config(config)

# Add channel command handler
@bot.on(events.NewMessage(pattern='/channel'))
async def channel_command(event):
    if event.sender_id not in OWNER_IDS:
        usage_text = (
            "📝 Channel Command Usage:\n\n"
            "/channel - View channel statistics and controls\n"
            "/approve <user_id> - Approve a user to skip message deletion\n"
            "/skip <user_id> - Add user to skip list\n"
            "/unskip <user_id> - Remove user from skip list\n"
            "/unapprove <user_id> - Remove user from approved list"
        )
        return await event.respond(usage_text)

    config = load_config()
    try:
        group = await event.client.get_entity(config['group_id'])
        group_name = f"{group.title} (ID: {group.id})"
    except:
        group_name = f"Unknown Group (ID: {config['group_id']})"

    try:
        channel = await event.client.get_entity(config['channel_id'])
        channel_name = f"{channel.title} (ID: {channel.id})"
    except:
        channel_name = f"Unknown Channel (ID: {config['channel_id']})"

    channel_settings = config['channel_settings']
    stats = channel_settings['stats']
    group_stats = config['group_settings']
    skipped_users_count = len(config['skip_user_ids'])
    status_text = (
        f"📊 Statistics for:\n"
        f"📱 Group: {group_name}\n"
        f"📢 Channel: {channel_name}\n\n"
        f"Group Stats:\n"
        f"• Deleted Messages: {group_stats['deleted_count']}\n"
        f"• Skipped Messages: {group_stats['skipped_count']}\n"
        f"• Approved Users: {group_stats['approved_users_count']}\n"
        f"• Skipped Users: {skipped_users_count}\n\n"
        f"Channel Stats:\n"
        f"• Edited Messages: {stats['edited']}\n"
        f"• CoinXpert Mentions: {stats['coinxpert_mentions']}\n"
        f"• Encrypted Messages: {stats['encrypted']}\n\n"
        f"Status: {'🟢 Monitoring' if channel_settings['monitoring'] else '🔴 Stopped'}\n"
        f"CoinXpert: {'🟢 ON' if channel_settings['coinxpert'] else '🔴 OFF'}"
    )
    
    buttons = [
        [
            Button.inline(
                "🔴 Stop Monitor" if channel_settings['monitoring'] else "🟢 Start Monitor",
                b"toggle_monitor"
            )
        ],
        [
            Button.inline(
                "🔴 CoinXpert OFF" if channel_settings['coinxpert'] else "🟢 CoinXpert ON",
                b"toggle_coinxpert"
            )
        ],
        [Button.inline("👥 Show Skipped Users", b"show_skipped")],
        [Button.inline("❌ Close", b"close")]
    ]
    
    await event.respond(status_text, buttons=buttons)

# Add callback handlers for channel controls
@bot.on(events.CallbackQuery(pattern=b"toggle_monitor"))
async def toggle_monitor(event):
    if event.sender_id not in OWNER_IDS:
        return await event.answer("Not authorized!", alert=True)
    
    state = get_channel_state()
    state['monitoring'] = not state['monitoring']
    save_channel_state(state)
    
    stats = state['stats']
    status_text = (
        "📊 Channel Statistics:\n"
        f"• Edited Messages: {stats['edited']}\n"
        f"• CoinXpert Mentions: {stats['coinxpert_mentions']}\n"
        f"• Encrypted Messages: {stats['encrypted']}\n\n"
        f"Status: {'🟢 Monitoring' if state['monitoring'] else '🔴 Stopped'}\n"
        f"CoinXpert: {'🟢 ON' if state['coinxpert'] else '🔴 OFF'}"
    )
    
    buttons = [
        [
            Button.inline(
                "🔴 Stop Monitor" if state['monitoring'] else "🟢 Start Monitor",
                b"toggle_monitor"
            )
        ],
        [
            Button.inline(
                "🔴 CoinXpert OFF" if state['coinxpert'] else "🟢 CoinXpert ON",
                b"toggle_coinxpert"
            )
        ],
        [Button.inline("👥 Show Skipped Users", b"show_skipped")],
        [Button.inline("❌ Close", b"close")]
    ]
    
    await event.edit(status_text, buttons=buttons)
    await event.answer("Monitor status updated!")

@bot.on(events.CallbackQuery(pattern=b"toggle_coinxpert"))
async def toggle_coinxpert(event):
    if event.sender_id not in OWNER_IDS:
        return await event.answer("Not authorized!", alert=True)
    
    state = get_channel_state()
    state['coinxpert'] = not state['coinxpert']
    save_channel_state(state)
    
    stats = state['stats']
    status_text = (
        "📊 Channel Statistics:\n"
        f"• Edited Messages: {stats['edited']}\n"
        f"• CoinXpert Mentions: {stats['coinxpert_mentions']}\n"
        f"• Encrypted Messages: {stats['encrypted']}\n\n"
        f"Status: {'🟢 Monitoring' if state['monitoring'] else '🔴 Stopped'}\n"
        f"CoinXpert: {'🟢 ON' if state['coinxpert'] else '🔴 OFF'}"
    )
    
    buttons = [
        [
            Button.inline(
                "🔴 Stop Monitor" if state['monitoring'] else "🟢 Start Monitor",
                b"toggle_monitor"
            )
        ],
        [
            Button.inline(
                "🔴 CoinXpert OFF" if state['coinxpert'] else "🟢 CoinXpert ON",
                b"toggle_coinxpert"
            )
        ],
        [Button.inline("👥 Show Skipped Users", b"show_skipped")],
        [Button.inline("❌ Close", b"close")]
    ]
    
    await event.edit(status_text, buttons=buttons)
    await event.answer("CoinXpert status updated!")

@bot.on(events.CallbackQuery(pattern=b"show_skipped"))
async def show_skipped_users(event):
    if event.sender_id not in OWNER_IDS:
        return await event.answer("Not authorized!", alert=True)
    
    config = load_config()
    skipped_users = config['skip_user_ids']
    
    if not skipped_users:
        status_text = "No skipped users found."
    else:
        status_text = "📋 Skipped Users List:\n\n"
        for user_id in skipped_users:
            try:
                user = await event.client.get_entity(user_id)
                username = f"@{user.username}" if user.username else "No username"
                name = user.first_name
                if user.last_name:
                    name += f" {user.last_name}"
                status_text += f"• Name: {name}\n  Username: {username}\n  ID: {user_id}\n\n"
            except Exception as e:
                status_text += f"• User ID: {user_id} (Unable to fetch details)\n\n"
    
    buttons = [
        [Button.inline("🔄 Clear All Skipped Users", b"clear_skipped")],
        [Button.inline("🔙 Back", b"back_to_channel")]
    ]
    await event.edit(status_text, buttons=buttons)

@bot.on(events.CallbackQuery(pattern=b"clear_skipped"))
async def clear_skipped_users(event):
    if event.sender_id not in OWNER_IDS:
        return await event.answer("Not authorized!", alert=True)
    
    config = load_config()
    config['skip_user_ids'] = []
    save_config(config)
    global SKIP_USER_IDS
    SKIP_USER_IDS = []
    
    await event.answer("Skipped users list cleared!")
    await show_skipped_users(event)

@bot.on(events.CallbackQuery(pattern=b"back_to_channel"))
async def back_to_channel(event):
    if event.sender_id not in OWNER_IDS:
        return await event.answer("Not authorized!", alert=True)
    
    state = get_channel_state()
    stats = state['stats']
    status_text = (
        "📊 Channel Statistics:\n"
        f"• Edited Messages: {stats['edited']}\n"
        f"• CoinXpert Mentions: {stats['coinxpert_mentions']}\n"
        f"• Encrypted Messages: {stats['encrypted']}\n\n"
        f"Status: {'🟢 Monitoring' if state['monitoring'] else '🔴 Stopped'}\n"
        f"CoinXpert: {'🟢 ON' if state['coinxpert'] else '🔴 OFF'}"
    )
    
    buttons = [
        [
            Button.inline(
                "🔴 Stop Monitor" if state['monitoring'] else "🟢 Start Monitor",
                b"toggle_monitor"
            )
        ],
        [
            Button.inline(
                "🔴 CoinXpert OFF" if state['coinxpert'] else "🟢 CoinXpert ON",
                b"toggle_coinxpert"
            )
        ],
        [Button.inline("👥 Show Skipped Users", b"show_skipped")],
        [Button.inline("❌ Close", b"close")]
    ]
    
    await event.edit(status_text, buttons=buttons)

@bot.on(events.CallbackQuery(pattern=b"toggle_group"))
async def toggle_group(event):
    if event.sender_id not in OWNER_IDS:
        return await event.answer("Not authorized!", alert=True)
    
    config = load_config()
    config['group_settings']['active'] = not config['group_settings']['active']
    save_config(config)
    
    stats = config['group_settings']
    status_text = (
        "📊 Group Statistics:\n"
        f"📱 Group: {group_name}\n"
        f"• Approved Users: {stats['approved_users_count']}\n"
        f"• Deleted Messages: {stats['deleted_count']}\n"
        f"• Skipped Messages: {stats['skipped_count']}\n\n"
        f"Status: {'🟢 Active' if stats['active'] else '🔴 Inactive'}"
    )
    
    buttons = [
        [Button.inline("🔴 Deactivate" if stats['active'] else "🟢 Activate", b"toggle_group")],
        [Button.inline("👥 Approved Users", b"show_approved")],
        [Button.inline("❌ Close", b"close")]
    ]
    
    await event.edit(status_text, buttons=buttons)
    await event.answer("Group status updated!")

@bot.on(events.CallbackQuery(pattern=b"show_approved"))
async def show_approved_users(event):
    if event.sender_id not in OWNER_IDS:
        return await event.answer("Not authorized!", alert=True)
    
    config = load_config()
    approved_users = config['approved_users']
    
    if not approved_users:
        status_text = "No approved users yet."
    else:
        user_list = []
        for user_id in approved_users:
            try:
                user = await bot.get_entity(user_id)
                user_list.append(f"• {user.first_name} (@{user.username}) [{user_id}]")
            except:
                user_list.append(f"• Unknown User [{user_id}]")
        
        status_text = "👥 Approved Users:\n" + "\n".join(user_list)
    
    buttons = [
        [Button.inline("🔄 Clear All Approved Users", b"clear_approved")],
        [Button.inline("⬅️ Back", b"back_to_group")],
        [Button.inline("❌ Close", b"close")]
    ]
    
    await event.edit(status_text, buttons=buttons)

@bot.on(events.CallbackQuery(pattern=b"clear_approved"))
async def clear_approved_users(event):
    if event.sender_id not in OWNER_IDS:
        return await event.answer("Not authorized!", alert=True)
    
    config = load_config()
    config['approved_users'] = []
    config['group_settings']['approved_users_count'] = 0
    save_config(config)
    global APPROVED_USERS
    APPROVED_USERS = []
    
    await event.answer("Approved users list cleared!")
    await show_approved_users(event)

@bot.on(events.NewMessage(pattern='/myid'))
async def my_id_command(event):
    user = await event.get_sender()
    await event.respond(f"Your user ID is: {user.id}")

@bot.on(events.NewMessage(pattern=r'/userid\s+'))
async def userid_command(event):
    try:
        username = event.message.text.split()[1]
        if username.startswith('@'):
            username = username[1:]
        user = await bot.get_entity(username)
        await event.respond(f"User ID for @{username}: {user.id}")
    except Exception as e:
        await event.respond(f"Error: {str(e)}")

@bot.on(events.CallbackQuery(pattern=b"back_to_group"))
async def back_to_group(event):
    if event.sender_id not in OWNER_IDS:
        return await event.answer("Not authorized!", alert=True)
    
    config = load_config()
    stats = config['group_settings']
    status_text = (
        "📊 Group Statistics:\n"
        f"• Approved Users: {stats['approved_users_count']}\n"
        f"• Deleted Messages: {stats['deleted_count']}\n"
        f"• Skipped Messages: {stats['skipped_count']}\n\n"
        f"Status: {'🟢 Active' if stats['active'] else '🔴 Inactive'}"
    )
    
    buttons = [
        [Button.inline("🔴 Deactivate" if stats['active'] else "🟢 Activate", b"toggle_group")],
        [Button.inline("👥 Approved Users", b"show_approved")],
        [Button.inline("❌ Close", b"close")]
    ]
    
    await event.edit(status_text, buttons=buttons)

import json

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def save_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

# Load configuration
config = load_config()
SKIP_USER_IDS = config['skip_user_ids']
APPROVED_USERS = config['approved_users']
GROUP_ID = config['group_id']
GROUP_SETTINGS = config['group_settings']

@bot.on(events.NewMessage(pattern=r'/skip\s+'))
async def skip_command(event):
    if event.sender_id not in OWNER_IDS:
        return await event.respond("You're not authorized to use this command.")
    
    try:
        users = event.message.text.split()[1:]
        config = load_config()
        for user in users:
            if user.startswith('@'):
                try:
                    user_entity = await bot.get_entity(user)
                    if user_entity.id not in config['skip_user_ids']:
                        config['skip_user_ids'].append(user_entity.id)
                except:
                    await event.respond(f"Could not find user {user}")
            else:
                try:
                    user_id = int(user)
                    if user_id not in config['skip_user_ids']:
                        config['skip_user_ids'].append(user_id)
                except:
                    await event.respond(f"Invalid user ID {user}")
        
        save_config(config)
        global SKIP_USER_IDS
        SKIP_USER_IDS = config['skip_user_ids']
        await event.respond("Skip list updated successfully!")
    except Exception as e:
        await event.respond(f"Error updating skip list: {str(e)}")

@bot.on(events.NewMessage(pattern=r'/approve\s+'))
async def approve_command(event):
    if event.sender_id not in OWNER_IDS:
        return await event.respond("You're not authorized to use this command.")
    
    try:
        users = event.message.text.split()[1:]
        config = load_config()
        for user in users:
            if user.startswith('@'):
                try:
                    user_entity = await bot.get_entity(user)
                    if user_entity.id not in config['approved_users']:
                        config['approved_users'].append(user_entity.id)
                        config['group_settings']['approved_users_count'] += 1
                except:
                    await event.respond(f"Could not find user {user}")
            else:
                try:
                    user_id = int(user)
                    if user_id not in config['approved_users']:
                        config['approved_users'].append(user_id)
                        config['group_settings']['approved_users_count'] += 1
                except:
                    await event.respond(f"Invalid user ID {user}")
        
        save_config(config)
        global APPROVED_USERS
        APPROVED_USERS = config['approved_users']
        await event.respond("Approved users list updated successfully!")
    except Exception as e:
        await event.respond(f"Error updating approved users: {str(e)}")

@bot.on(events.NewMessage(pattern='/group'))
async def group_command(event):
    if event.sender_id not in OWNER_IDS:
        return await event.respond("You're not authorized to use this command.")
    
    config = load_config()
    stats = config['group_settings']
    status_text = (
        "📊 Group Statistics:\n"
        f"• Approved Users: {stats['approved_users_count']}\n"
        f"• Deleted Messages: {stats['deleted_count']}\n"
        f"• Skipped Messages: {stats['skipped_count']}\n\n"
        f"Status: {'🟢 Active' if stats['active'] else '🔴 Inactive'}"
    )
    
    buttons = [
        [Button.inline("🔴 Deactivate" if stats['active'] else "🟢 Activate", b"toggle_group")],
        [Button.inline("👥 Approved Users", b"show_approved")],
        [Button.inline("❌ Close", b"close")]
    ]
    
    await event.respond(status_text, buttons=buttons)

# Add group message handler
# Dictionary to track user notification cooldowns
user_notification_cooldowns = {}

@bot.on(events.NewMessage(chats=GROUP_ID))
async def group_message_handler(event):
    config = load_config()
    if not config['group_settings']['active']:
        return
    
    if event.sender_id in config['skip_user_ids']:
        config['group_settings']['skipped_count'] += 1
        save_config(config)
        return
    
    if event.sender_id not in config['approved_users']:
        try:
            # Delete the message regardless
            await event.delete()
            config['group_settings']['deleted_count'] += 1
            save_config(config)
            
            current_time = time.time()
            
            # Check if user is in cooldown
            if event.sender_id in user_notification_cooldowns:
                # If in cooldown, just delete silently
                return
            
            sender = await event.get_sender()
            username = sender.username or str(sender.id)
            
            buttons = [
                [Button.url("Join Chat", "https://t.me/+Ta4bpmajO5BmN2Nh")],
                [Button.url("Wanna get verified?", "https://t.me/vmvr7")]
            ]
            
            # Add user to cooldown
            user_notification_cooldowns[event.sender_id] = current_time
            
            notification = await event.respond(
                f"@{username} this group only for verified vendors to post",
                buttons=buttons
            )
            
            # Delete notification after 1 minute
            await asyncio.sleep(60)
            try:
                await notification.delete()
                # Remove user from cooldown after notification is deleted
                if event.sender_id in user_notification_cooldowns:
                    del user_notification_cooldowns[event.sender_id]
            except Exception as e:
                print(f"Error deleting notification: {e}")
                
        except Exception as e:
            print(f"Error handling message: {e}")
        return

# Modify the channel message handler
@bot.on(events.NewMessage(chats=CHANNEL_ID))
async def channel_message_handler(event):
    config = load_config()
    if not config['channel_settings']['monitoring']:
        return
    
    if not event.message.text:
        return
    
    # Get the actual sender ID from forward info if message is forwarded
    if event.message.forward:
        if event.message.forward.from_id:
            # Check if it's a channel or user
            if hasattr(event.message.forward.from_id, 'channel_id'):
                sender_id = f"channel_{event.message.forward.from_id.channel_id}"
                print(f"Message forwarded from channel: {sender_id}")
            elif hasattr(event.message.forward.from_id, 'user_id'):
                sender_id = event.message.forward.from_id.user_id
            else:
                # If can't determine, use original sender
                sender_id = event.sender_id
        else:
            # If forward info doesn't have ID, use original sender
            sender_id = event.sender_id
    else:
        sender_id = event.sender_id
    
    # Debug log
    print(f"Message from user/channel ID: {sender_id} (forwarded: {bool(event.message.forward)})")
    print(f"Skip list: {config['skip_user_ids']}")
    
    # Convert sender_id to string for comparison if it's a channel
    skip_list_ids = [str(id) for id in config['skip_user_ids']]
    
    # Also add the raw channel/user IDs to the skip check
    if (isinstance(sender_id, int) and sender_id in config['skip_user_ids']) or \
       (isinstance(sender_id, str) and sender_id in skip_list_ids):
        print(f"Skipping message from {sender_id}")
        config['channel_settings']['stats']['skipped'] += 1
        save_config(config)
        return
    
    # Debug log for non-skipped users
    print(f"Processing message from {sender_id}")
    
    text = event.message.text
    
    # Rest of the handler remains the same
    if channel_encryption.is_encrypted(text):
        config['channel_settings']['stats']['encrypted'] += 1
        save_config(config)
        return
    
    # Encrypt the text
    encrypted_text = channel_encryption.encrypt(text)
    
    # Add CoinXpert mention if enabled and not present
    if config['channel_settings']['coinxpert'] and '@CoinXpertBot' not in text:
        encrypted_text += '\n\n@CoinXpertBot'
        config['channel_settings']['stats']['coinxpert_mentions'] += 1
        save_config(config)
    
    # Try to edit the message, if it fails (forwarded message), delete and resend
    try:
        await event.message.edit(encrypted_text)
        config['channel_settings']['stats']['edited'] += 1
        config['channel_settings']['stats']['encrypted'] += 1
        save_config(config)
    except Exception as e:
        print(f"Error editing message: {e}")
        try:
            # Get media from original message
            media = event.message.media
            
            # Store the original message ID before deleting
            original_id = event.message.id
            
            # Delete original message
            await event.message.delete()
            
            # Send new message with the same media and link preview disabled
            new_message = await bot.send_message(
                config['channel_id'],
                encrypted_text,
                file=media,
                link_preview=False
            )
            
            # If this is part of a media group, we need to handle it differently
            # Unfortunately, we can't directly set grouped_id, but we can log it
            if hasattr(event.message, 'grouped_id') and event.message.grouped_id:
                print(f"Message was part of media group: {event.message.grouped_id}")
            
            config['channel_settings']['stats']['edited'] += 1
            config['channel_settings']['stats']['encrypted'] += 1
            save_config(config)
            
            print(f"Successfully resent message: {original_id} → {new_message.id}")
        except Exception as e2:
            print(f"Error resending message: {e2}")
            # Try one more time with just text, no media
            try:
                await bot.send_message(
                    config['channel_id'],
                    encrypted_text,
                    link_preview=False
                )
                config['channel_settings']['stats']['edited'] += 1
                config['channel_settings']['stats']['encrypted'] += 1
                save_config(config)
                print("Sent text-only version as fallback")
            except Exception as e3:
                print(f"Complete failure to send message: {e3}")

print("Bot started...")
bot.run_until_disconnected()
