## definitions.rpy

# This file defines important stuff for DDLC and your mod!

# This variable declares if the mod is a demo or not.
# Leftover from DDLC.
define persistent.demo = False

# This variable declares whether the mod is in the 'steamapps' folder.
define persistent.steam = ("steamapps" in config.basedir.lower())

# This variable declares whether Developer Mode is on or off in the mod.
define config.developer = False

default monika_agent = None
default persistent.location = None
default persistent.temperature = 0.2
default persistent.current_tokens = 0
define persistent.seed = 0
define executor = None
define monika_agent = None
define nexis = None
default 1 message = ""
default selected_char = ""
define persistent.world_time = [12, 00]
define game_seconds = 2 # Each 1.5 seconds in real time is 2 minutes in game time
default current_place = None
define 1 characters = {
    'monika': m,
    'sayori': s,
    'natsuki': n,
    'yuri': y
}

image bg class_room_day = "mod_assets/bg/class_room_day.jpg"
image bg class_room_afternoon = "mod_assets/bg/class_room_afternoon.jpg"
image bg main_entrance = "mod_assets/bg/main_entrance.jpg"
image bg school = "mod_assets/bg/school.jpg"
image bg left_corridor = "mod_assets/bg/left_corridor.jpg"
image bg right_corridor = "mod_assets/bg/right_corridor.jpg"
image bg man_bathroom = "mod_assets/bg/man_bathroom.jpg"
image bg woman_bathroom = "mod_assets/bg/woman_bathroom.jpg"

image monika_head:
    'mod_assets/heads/monika.png'
    zoom 0.35

image sayori_head:
    'mod_assets/heads/sayori.png'
    zoom 0.35

image natsuki_head:
    'mod_assets/heads/natsuki.png'
    zoom 0.35

image yuri_head:
    'mod_assets/heads/yuri.png'
    zoom 0.35

define character_heads = {
    'monika': "monika_head",
    'sayori': "sayori_head",
    'natsuki': "natsuki_head",
    'yuri': "yuri_head"
}

init python:
    import random
    from concurrent.futures import ThreadPoolExecutor

    if persistent.world_time is not list:
        print("Initializing world time")
        persistent.world_time = [12, 00]
    
    print("Initializing executor")
    executor = ThreadPoolExecutor(max_workers = 25)
    persistent.seed = random.randint(0, 10000)

    schema = os.path.join(renpy.config.gamedir, "schema.json")

    parser = WorldParser(schema)
    nexis = parser.unpack()
    cr = nexis.get_location('Club Room')
    cr.add_character('Monika')
    cr.add_character('Sayori')
    cr.add_character('Natsuki')
    cr.add_character('Yuri')
    


    # if monika_agent is None:
    #     monika_agent = Agent('Monika', monika['bio'], monika['abilities'], monika['memories'], monika['traits'])

    # nexis.get_location(monika_agent.agent_details.location).add_character(monika_agent.agent_details.name)


# This python statement starts singleton to make sure only one copy of the mod
# is running.
python early:
    import singleton
    me = singleton.SingleInstance()

init -3 python:
    ## Dynamic Super Position (DSP)
    # DSP is a feature in where the game upscales the positions of assets 
    # with higher resolutions (1080p).
    # This is just simple division from Adobe, implemented in Python.
    def dsp(orig_val):
        ceil = not isinstance(orig_val, float)
        dsp_scale = config.screen_width / 1280.0 
        if ceil: return math.ceil(orig_val * dsp_scale)
        # since `absolute * float` -> `float`
        # we wanna keep the same type
        return type(orig_val)(orig_val * dsp_scale)
    
    # This makes evaluating the value faster
    renpy.pure(dsp)

    ## Dynamic Super Resolution
    # DSR is a feature in where the game upscales asset sizes to higher
    # resolutions (1080p) and sends back a modified transform.
    # (Recommend that you just make higher res assets than upscale lower res ones)
    def dsr(path):
        img_bounds = renpy.image_size(path)
        return Transform(path, size=(dsp(img_bounds[0]), dsp(img_bounds[1])))

## Android Gestures (provided by Tulkas)
## These gestures allow players to access different settings using the touch screen.
# Swipe Up - Saves
# Swipe Down - Hide Dialogue Box
# Swipe Left - History
# Swipe Right - Skip Dialogue
define config.gestures = { "n" : 'game_menu', "s" : "hide_windows", "e" : 'toggle_skip', "w" : "history" }

# This init python statement sets up the functions, keymaps and channels
# for the game.
init python:
    ## More Android Gestures
    # This variable makes a keymap for the history screen.
    if renpy.android:
        config.underlay.append(renpy.Keymap(history = ShowMenu("history"))) 

        # These commented variables sets all keybinds from Rollback to History.
        # config.keymap["rollback"] = []
        # config.keymap["history"] = [ 'K_PAGEUP', 'repeat_K_PAGEUP', 'K_AC_BACK', 'mousedown_4' ]

    # These variable declarations adjusts the mapping for certain actions in-game.
    config.keymap['game_menu'].remove('mouseup_3')
    config.keymap['hide_windows'].append('mouseup_3')
    config.keymap['self_voicing'] = []
    config.keymap['clipboard_voicing'] = []
    config.keymap['toggle_skip'] = []

    # This variable declaration registers the music poem channel for the poem sharing music.
    renpy.music.register_channel("music_poem", mixer="music", tight=True)
    
    # This function gets the postition of the music playing in a given channel.
    def get_pos(channel='music'):
        pos = renpy.music.get_pos(channel=channel)
        if pos: return pos
        return 0

    # This function deletes all the saves made in the mod.
    def delete_all_saves():
        for savegame in renpy.list_saved_games(fast=True):
            renpy.unlink_save(savegame)

    # This function deletes a given character name from the characters folder.
    def delete_character(name):
        if renpy.android:
            try: os.remove(os.environ['ANDROID_PUBLIC'] + "/characters/" + name + ".chr")
            except: pass
        else:
            try: os.remove(config.basedir + "/characters/" + name + ".chr")
            except: pass

    # These functions restores all the character CHR files to the characters folder 
    # given the playthrough number in the mod and list of characters to restore.
    def restore_character(names):
        if not isinstance(names, list):
            raise Exception("'names' parameter must be a list. Example: [\"monika\", \"sayori\"].")

        for x in names:
            if renpy.android:
                try: renpy.file(os.environ['ANDROID_PUBLIC'] + "/characters/" + x + ".chr")
                except: open(os.environ['ANDROID_PUBLIC'] + "/characters/" + x + ".chr", "wb").write(renpy.file("chrs/" + x + ".chr").read())
            else:
                try: renpy.file(config.basedir + "/characters/" + x + ".chr")
                except: open(config.basedir + "/characters/" + x + ".chr", "wb").write(renpy.file("chrs/" + x + ".chr").read())

    def restore_all_characters():
        if persistent.playthrough == 0:
            restore_character(["monika", "sayori", "natsuki", "yuri"])
        elif persistent.playthrough == 1 or persistent.playthrough == 2:
            restore_character(["monika", "natsuki", "yuri"])
        elif persistent.playthrough == 3:
            restore_character(["monika"])
        else:
            restore_character(["sayori", "natsuki", "yuri"])
    
    # This function is obsolete as all characters now restores only
    # relevant characters to the characters folder.
    def restore_relevant_characters():
        restore_all_characters()

    # This function pauses the time for a certain amount of time or indefinite.
    def pause(time=None):
        global _windows_hidden

        if not time:
            _windows_hidden = True
            renpy.ui.saybehavior(afm=" ")
            renpy.ui.interact(mouse='pause', type='pause', roll_forward=None)
            _windows_hidden = False
            return
        if time <= 0: return
        _windows_hidden = True
        renpy.pause(time)
        _windows_hidden = False

## Music
# This section declares the music available to be played in the mod.
# Syntax:
#   audio. - This tells Ren'Py this is a audio variable.
#   t1 - This tells Ren'Py the label of the music/sound file being declared.
#   <loop 22.073> - This tells Ren'Py to loop the music/sound to this position when the song completes.
#   "bgm/1.ogg" - This tells Ren'Py the path of the music/sound file to use.
# Example: 
#   define audio.t2 = "bgm/2.ogg"

define audio.t1 = "<loop 22.073>bgm/1.ogg" # Doki Doki Literature Club! - Main Theme
define audio.t2 = "<loop 4.499>bgm/2.ogg" # Ohayou Sayori! - Sayori Theme
define audio.t2g = "bgm/2g.ogg"
define audio.t2g2 = "<from 4.499 loop 4.499>bgm/2.ogg"
define audio.t2g3 = "<loop 4.492>bgm/2g2.ogg"
define audio.t3 = "<loop 4.618>bgm/3.ogg" # Main Theme - In Game 
define audio.t3g = "<to 15.255>bgm/3g.ogg"
define audio.t3g2 = "<from 15.255 loop 4.618>bgm/3.ogg"
define audio.t3g3 = "<loop 4.618>bgm/3g2.ogg"
define audio.t3m = "<loop 4.618>bgm/3.ogg"
define audio.t4 = "<loop 19.451>bgm/4.ogg" # Dreams of Love and Literature - Poem Game Theme
define audio.t4g = "<loop 1.000>bgm/4g.ogg"
define audio.t5 = "<loop 4.444>bgm/5.ogg" # Okay Everyone! - Sharing Poems Theme

define audio.tmonika = "<loop 4.444>bgm/5_monika.ogg" # Okay Everyone! (Monika)
define audio.tsayori = "<loop 4.444>bgm/5_sayori.ogg" # Okay Everyone! (Sayori)
define audio.tnatsuki = "<loop 4.444>bgm/5_natsuki.ogg" # Okay Everyone! (Natsuki)
define audio.tyuri = "<loop 4.444>bgm/5_yuri.ogg" # Okay Everyone! (Yuri)

define audio.t5b = "<loop 4.444>bgm/5.ogg"
define audio.t5c = "<loop 4.444>bgm/5.ogg"
define audio.t6 = "<loop 10.893>bgm/6.ogg" # Play With Me - Yuri/Natsuki Theme
define audio.t6g = "<loop 10.893>bgm/6g.ogg"
define audio.t6r = "<to 39.817 loop 0>bgm/6r.ogg"
define audio.t6s = "<loop 43.572>bgm/6s.ogg"
define audio.t7 = "<loop 2.291>bgm/7.ogg" # Poem Panic - Argument Theme
define audio.t7a = "<loop 4.316 to 12.453>bgm/7.ogg"
define audio.t7g = "<loop 31.880>bgm/7g.ogg"
define audio.t8 = "<loop 9.938>bgm/8.ogg" # Daijoubu! - Argument Resolved Theme
define audio.t9 = "<loop 3.172>bgm/9.ogg" # My Feelings - Emotional Theme
define audio.t9g = "<loop 1.532>bgm/9g.ogg" # My Feelings but 207% Speed
define audio.t10 = "<loop 5.861>bgm/10.ogg" # My Confession - Sayori Confession Theme
define audio.t10y = "<loop 0>bgm/10-yuri.ogg"
define audio.td = "<loop 36.782>bgm/d.ogg"

define audio.m1 = "<loop 0>bgm/m1.ogg" # Just Monika. - Just Monika.
define audio.mend = "<loop 6.424>bgm/monika-end.ogg" # I Still Love You - Monika Post-Delete Theme

define audio.ghostmenu = "<loop 0>bgm/ghostmenu.ogg"
define audio.g1 = "<loop 0>bgm/g1.ogg"
define audio.g2 = "<loop 0>bgm/g2.ogg"
define audio.hb = "<loop 0>bgm/heartbeat.ogg"

define audio.closet_open = "sfx/closet-open.ogg"
define audio.closet_close = "sfx/closet-close.ogg"
define audio.page_turn = "sfx/pageflip.ogg"
define audio.fall = "sfx/fall.ogg"

## Backgrounds
# This section declares the backgrounds available to be shown in the mod.
# To define a new color background, declare a new image statement like in this example:
#     image blue = "X" where X is your color hex i.e. '#158353'
# To define a new background, declare a new image statement like this instead:
#     image bg bathroom = "mod_assets/bathroom.png" 

image black = "#000000"
image dark = "#000000e4"
image darkred = "#110000c8"
image white = "#ffffff"
image splash = "bg/splash.png"
image end:
    truecenter
    "gui/end.png"

define fadeIn = Fade(0, 0 , 0.5)

image bg residential_day = "bg/residential.png" # Start of DDLC BG
image bg class_day = "bg/class.png" # The classroom BG
image bg corridor = "bg/corridor.png" # The hallway BG
image bg club_day = "bg/club.png" # The club BG
image bg club_afternoon = "mod_assets/bg/club_afternoon.png" # The club BG
image bg club_day2: # Glitched Club BG
    choice:
        "bg club_day"
    choice:
        "bg club_day"
    choice:
        "bg club_day"
    choice:
        "bg club_day"
    choice:
        "bg club_day"
    choice:
        "bg/club-skill.png"

image bg closet = "bg/closet.png" # The closet BG
image bg bedroom = "bg/bedroom.png" # MC's Room BG
image bg sayori_bedroom = "bg/sayori_bedroom.png" # Sayori's Room BG
image bg house = "bg/house.png" # Sayori's House BG
image bg kitchen = "bg/kitchen.png" # MC's Kitchen BG

image bg trasnparent = "#150DF7" # Blue BG

image bg notebook = "bg/notebook.png" # Poem Game Notebook Scene
image bg notebook-glitch = "bg/notebook-glitch.png" # Glitched Poem Game BG

# This image shows a glitched screen during Act 2 poem sharing with Yuri.
image bg glitch = LiveTile("bg/glitch.jpg")

# Default Name Variables
# To define a default name make a character name variable like in this example:
#   default e_name = "Eileen"

default s_name = "Sayori"
default m_name = "Monika"
default n_name = "Natsuki"
default y_name = "Yuri"

## Character Variables
# This is where the characters are declared in the mod.
# To define a new character with assets, declare a character variable like in this example:
#   define e = DynamicCharacter('e_name', image='eileen', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
# To define a new character without assets, declare a character variable like this instead:
#   define en = Character('Eileen & Nat', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")

define narrator = Character(ctc="ctc", ctc_position="fixed")
define mc = DynamicCharacter('player', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define s = DynamicCharacter('s_name', image='sayori', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define m = DynamicCharacter('m_name',  who_color="#8ef78e", image='monika', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define n = DynamicCharacter('n_name', image='natsuki', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define y = DynamicCharacter('y_name', image='yuri', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define ny = Character('Nat & Yuri', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")

# This variable determines whether to allow the player to dismiss pauses.
# By default this is set by config.developer which is normally set to false
# once you packaged your mod.
define _dismiss_pause = config.developer

## Extra Settings Variables
# This section controls whether the mod is censored or is in let's play mode.
default persistent.uncensored_mode = False
default persistent.lets_play = False

## Variables
# This section declares variables when the mod runs for the first time on all saves.
# To make a new persistent variable, make a new variable with the 'persistent.' in it's name
# like in this example:
#   default persistent.monika = 1
# To make a non-persistent variable, make a new variable like this instead:
#   default cookies = False
# To make sure a variable is set to a given condition use 'define' rather than 'default'.

default persistent.playername = ""
default player = persistent.playername
default persistent.playthrough = 0
default persistent.yuri_kill = 0
default persistent.seen_eyes = None
default persistent.seen_sticker = None
default persistent.ghost_menu = None
default persistent.seen_ghost_menu = None
default seen_eyes_this_chapter = False
default persistent.anticheat = 0
default persistent.clear = [False, False, False, False, False, False, False, False, False, False]
default persistent.special_poems = None
default persistent.clearall = None
default persistent.menu_bg_m = None
default persistent.first_load = None
default persistent.first_poem = None
default persistent.seen_colors_poem = None
default persistent.monika_back = None

default in_sayori_kill = None
default in_yuri_kill = None
default anticheat = 0
define config.mouse = None
default allow_skipping = True
default basedir = config.basedir
default chapter = 0
default currentpos = 0
default faint_effect = None

# Poem Variables
# This section records how much each character likes your poem in-game.
# Syntax:
#   -1 - Bad
#   0 - Neutral
#   1 - Good
# To add a new poem person, make a poem array like in this example:
#   default e_poemappeal = [0, 0, 0]

default n_poemappeal = [0, 0, 0]
default s_poemappeal = [0, 0, 0]
default y_poemappeal = [0, 0, 0]
default m_poemappeal = [0, 0, 0]

# This variable keeps tracks on which person won the poem session after each day.
default poemwinner = ['sayori', 'sayori', 'sayori']

# These variables keep track on who has read your poem during poem sharing
default s_readpoem = False
default n_readpoem = False
default y_readpoem = False
default m_readpoem = False

# This variable keeps track on how many people have read your poem.
default poemsread = 0

# These variables control if we have seen Natsuki's or Yuri's exclusive scenes
default n_exclusivewatched = False
default y_exclusivewatched = False

# These variables track whether we gave Yuri our poem in Act 2 and if she
# ran away during Act 2 poem sharing.
default y_gave = False
default y_ranaway = False

# These variables track whether we read Natsuki's or Yuri's 3rd poem in poem sharing.
default n_read3 = False
default y_read3 = False

# This variable tracks which person we sided with in Day 2 of the game.
default ch1_choice = "sayori"

# This variable tracks if we gave Natsuki our poem first during poem sharing.
default n_poemearly = False

# These variables track whether we tried to help Monika or Sayori during Day 3's ending.
default help_sayori = None
default help_monika = None

# These variables track which route Day 4 will play and who is their name.
default ch4_scene = "yuri"
default ch4_name = "Yuri"

# This variable tracks whether we accepted Sayori's confession or not.
default sayori_confess = True

# This variable tracks whether we read Natsuki's 3rd poem in Act 2.
default natsuki_23 = None
