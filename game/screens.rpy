## screens.rpy

# This file declares all the screens and styles in DDLC.

## Initialization
################################################################################

init offset = -1

# Thanks RenpyTom! Borrowed from the Ren'Py Launcher
init python:
    def scan_translations():

        languages = renpy.known_languages()

        if not languages:
            return None

        rv = [(i, renpy.translate_string("{#language name and font}", i)) for i in languages ]
        rv.sort(key=lambda a : renpy.filter_text_tags(a[1], allow=[]).lower())

        rv.insert(0, (None, "English"))

        bound = math.ceil(len(rv)/2.)

        return (rv[:bound], rv[bound:2*bound])

default translations = scan_translations()

# Enables the ability to add more settings in the game such as Uncensored Mode.
default extra_settings = True
# If you are using the Extras Menu feature, set this line to True.
default enable_extras_menu = False
# If you are going to use extra languages, set this to True.
default enable_languages = False

## Color Styles
################################################################################

# This controls the color of outlines in the game like
# text, say, navigation, labels and such.
define -2 text_outline_color = "#b59"

## Styles
################################################################################

style button_sounds:
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style default:
    font gui.default_font
    size gui.text_size
    color gui.text_color
    outlines [(2, "#000000aa", 0, 0)]
    line_overlap_split 1
    line_spacing 1

style default_monika is normal:
    slow_cps 30

style edited is default:
    font "gui/font/VerilySerifMono.otf"
    kerning 8
    outlines [(10, "#000", 0, 0)]
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos
    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

style normal is default:
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos

    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

# MARK: sdsds
style input:
    color gui.accent_color

style splash_text:
    size 24
    color "#000"
    font gui.default_font
    text_align 0.5
    outlines []

style gui_text:
    font gui.interface_font
    color gui.interface_text_color
    size gui.interface_text_size


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.button_text_properties("button")
    yalign 0.5


style label_text is gui_text:
    color gui.accent_color
    size gui.label_text_size

style prompt_text is gui_text:
    color gui.text_color
    size gui.interface_text_size

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style bar:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar.png", tile=False)
    thumb Frame("gui/scrollbar/horizontal_poem_thumb.png", top=6, right=6, tile=True)

style scrollbar:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar.png", tile=False)
    thumb Frame("gui/scrollbar/horizontal_poem_thumb.png", top=6, right=6, tile=True)
    unscrollable "hide"
    bar_invert True

style vscrollbar:
    xsize 18
    base_bar Frame("gui/scrollbar/vertical_poem_bar.png", tile=False)
    thumb Frame("gui/scrollbar/vertical_poem_thumb.png", left=6, top=6, tile=True)
    unscrollable "hide"
    bar_invert True

style slider:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar.png", tile=False)
    thumb "gui/slider/horizontal_hover_thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)

################################################################################
## In-game screens
################################################################################


image ctc:
    xalign 0.75 yalign 0.98 alpha 0.0 subpixel True
    "gui/ctc.png"
    block:
        easeout 0.75 alpha 1.0 
        easein 0.75 alpha 0.5
        repeat

################################################################
## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## http://www.renpy.org/doc/html/screen_special.html#input

image input_caret:
    Solid("#b59")
    size (2,25) subpixel True
    block:
        linear 0.35 alpha 0
        linear 0.35 alpha 1
        repeat

# MARK: sdsds
screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xpos gui.text_xpos
            xanchor 0
            ypos gui.text_ypos

            text prompt style "input_prompt"
            input id "input"


style input_prompt is default

style input_prompt:
    xmaximum gui.text_width
    xalign gui.text_xalign
    text_align gui.text_xalign

style input:
    caret "input_caret"
    xmaximum gui.text_width
    text_align 0.5


# MARK: Mod Screens
################################################################
## Main Menu Screen
################################################################
##
## Used to display the new main menu
##


screen say(who, what):
    style_prefix "response"

    window:
        id "window"
        yalign 0.99
        xalign 0.5
        xsize 700
        ysize 200
        xfill True
        padding (10, 10)

        background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)

        text what id "what" xpos 100 ypos 0 xmaximum 550

        if who is not None:
            text who id "who" xpos 0 ypos 0

screen dokis_heads(location):
    $ heads = get_dokis_head(location)

    grid 2 2:
        if len(heads) > 0:
            for ch in heads:
                add ch


# Set location based on the selected location
init python:
    def charge_label(location):
        persistent.location = location

screen main_menu():
    tag menu

    add "menu_bg"
    add "menu_logo"

    use custom_navigation

screen custom_navigation():
    style_prefix "custom_navigation"

    $ RPC.update(state="Thinking")

    vbox:
        hbox:
            textbutton "World" action [
                Function(update_state, state="Selecting location"),
                If(persistent.playername,
                    true=ShowMenu('display_locations'),
                    false=Show(screen="name_input",
                                message="Please enter your name",
                                ok_action=Function(FinishEnterName)))
                ]

            textbutton "Options" action [
                Function(update_state, state="Viewing Options"),
                If(persistent.playername,
                    true=ShowMenu('preferences'), 
                    false=Show(screen="name_input",
                                message="Please enter your name",
                                ok_action=Function(FinishEnterName)))
                ]

            textbutton "About" action [
                If(persistent.playername,
                    true=NullAction(),
                    false=Show(screen="name_input",
                                message="Please enter your name",
                                ok_action=Function(FinishEnterName)))
                ]
        
        hbox:
            textbutton "Exit" action Quit()

style disclaimer_text is gui_text:
    size 20

style custom_navigation_vbox:
    xalign 0.5

style custom_navigation_hbox:
    xalign 0.5
    ypos gui.mid_height + 20
    spacing 10

style custom_navigation_button is button_sounds:
    background None
    

style custom_navigation_button_text is navigation_button_text:
    size 40

screen preferences(goto_main_menu = False):
    tag menu
    add "game_menu_bg"
    style_prefix "preferences"

    python:
        status = "Connected" if RPC.rpc_connected else "Disconnected"
        if not persistent.enable_discord:
            status = "Disabled"

    hbox:
        hbox:
            transclude

        vbox:
            align (0.5, 0.5)
            xsize 250

            vbox:
                align (0.5, 0.5)

                text "Discord RPC"
                text "[status]"
                
                if not renpy.android:
                    textbutton "Toggle" action [
                        ToggleField(persistent, "enable_discord"), 
                        If(persistent.enable_discord,
                            Function(RPC.close),
                            Function(RPC.connect, reset=True))
                    ]

                    if persistent.enable_discord and not RPC.rpc_connected:
                        textbutton _("Reconnect") action Function(RPC.connect, reset=True)

            null height 35

            if config.has_music:
                hbox:
                    label _("Music Volume")
                    
                    null width 5
                
                    text str(round(preferences.get_volume("music") * 100)) style "value_text"

                hbox:
                    bar value Preference("music volume")

            if config.has_sound:
                hbox:
                    label _("Sound Volume")
                    
                    null width 5
                
                    text str(round(preferences.get_volume("sfx") * 100)) style "value_text"

                hbox:
                    bar value Preference("sound volume")

                    if config.sample_sound:
                        textbutton _("Test") action Play("sound", config.sample_sound)
            
            hbox:
                label "Weather Volume"
                null width 5

                text str(round(preferences.get_volume("weather") * 100))
                style "value_text"

            hbox:
                bar value Preference("weather volume")
            
            vbox:
                textbutton "Return" action Return() xalign 0.5
                if goto_main_menu:
                    textbutton "Main Menu" action MainMenu(False, False) xalign 0.5

style preferences_button is button_sounds
style preferences_button_text is navigation_button_text
style preferences_frame is empty

style preferences_vbox:
    align (0.5, 0.5)

style preferences_hbox:
    align (0.5, 0.5)

transform customzoom:
    xzoom 0.78

    on hover:
        easein .2 matrixcolor BrightnessMatrix(0.15)
    on idle:
        easeout .2 matrixcolor BrightnessMatrix(0.0)
    

screen display_locations:
    key "K_LEFT" action [SetVariable("idx", (idx - 1) % len(nexis.all_locations)), Play("sound", gui.activate_sound)]
    key "K_RIGHT" action [SetVariable("idx", (idx + 1) % len(nexis.all_locations)),Play("sound", gui.activate_sound)]

    tag menu
    style_prefix "dl"

    python:
        time = get_time()

    window:
        hbox:
            frame:
                padding (10, 10)
                yfill True

                vbox:
                    yfill True

                    vbox:
                        style_prefix "location_data"

                        text "Current state of the world" xalign 0.0
                        text "Day: [persistent.current_day]" xalign 0.0
                        text "Time: [time]" xalign 0.0
                        text "Weather: [persistent.current_weather[0]]" xalign 0.0


                        hbox:
                            textbutton "<":
                                action SetVariable("idx", (idx - 1) % len(nexis.all_locations))
                            textbutton ">":
                                action SetVariable("idx", (idx + 1) % len(nexis.all_locations))

                        text "Dokis in this location"
                        use dokis_heads(nexis.all_locations[idx].name)
                
                    textbutton "Back" action Return() align (0.5, 1.0)

            fixed:
                imagebutton:
                    idle nexis.all_locations[idx].get_background(persistent.world_time)
                    action [Function(init_weather), Function(charge_label, nexis.all_locations[idx].name), Start("charge_location")]
                    at customzoom
                    style "dl_button_image"

                text nexis.all_locations[idx].name:
                    xalign 0.5
                    size 35

style location_data_text:
    xalign 0.5

style location_data_hbox:
    xalign 0.5

style dl_window:
    background  None
    yfill True
    xfill True

                
style dl_button:
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style dl_button_image:
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style arrow_button:
    yalign 0.5
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound 

style arrow_button_text:
    size 100
    xalign 0.5    

screen save():
    style_prefix "preferences"
    
    tag menu
    $ current_weahter_data = persistent.current_weather[1]
    $ clouds_cover = current_weahter_data['clouds']
    $ temp = current_weahter_data['temperature']

    $ temperature = get_two_decimals(temp)
    $ clouds = get_two_decimals(clouds_cover)
    $ time = get_time()

    use preferences(True):
        vbox:
            spacing 35
            hbox:
                spacing 25
                vbox:
                    yalign 0.0
                    text "Temperature: [temperature]°C"
                    text "Weather: [persistent.current_weather[0]]"
                    text "Clouds: [clouds]%"
                vbox:
                    yalign 0.0
                    text "Location: [persistent.location]"
                    text "Time: [time]" 
            hbox:
                xalign 0.0
                spacing 25
                vbox:
                    text "Dokis in this location"
                    use dokis_heads(persistent.location)

################################################################
## Data Screen
################################################################
##
## This screen shows information about the game like time, your position
## in the town, and your AI tokens.
##
screen location_info(characters, rooms, parent_location):
    zorder 10
    style_prefix "data"

    window at slideLeft(.2):
        vbox spacing 10:
            frame:
                vbox:
                    text "Characters in this location" size 18

                    grid 2 2:
                        for char in characters:
                            textbutton char action [SetVariable('selected_char', char.lower()), Call("chat_lobby")] 

            frame:
                # Change the number of columns dynamically based on the current location
                $ columns = (len(rooms) // 5) + 1

                vbox:
                    text "Locations in this area" size 18

                    grid columns 5:
                        if parent_location is not None and nexis.name != parent_location.name:
                            textbutton 'Back' action [SetVariable('persistent.location', parent_location.name), Return()]

                        for place in rooms:
                            textbutton place action [SetVariable('persistent.location', place), Return()]


style data_window:
    background None
    yalign 0
    xalign 0
    ypos 200
    xsize 250
    ysize config.screen_height - 300

style data_vbox:
    xalign .5
    spacing 15

style data_grid:
    spacing 10
    align (0.5, 0)

style data_frame:
    xfill True
    padding (10, 10)
    top_padding 20
    bottom_padding 20


style data_button:  
    # properties gui.button_properties("choice_button")
    xminimum 100
    
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    idle_background Frame("gui/button/choice_idle_background.png", gui.choice_button_borders)
    hover_background Frame("gui/button/choice_hover_background.png", gui.choice_button_borders)
    
style data_button_text:
    size 20
    align (0.5, 0.5)


################################################################
## Info screen
################################################################
##
## This screen shows information about the game like time, your position
## in the town, and your AI tokens.
##
transform appear:
    alpha 0.0
    linear 0.5 alpha 1.0

transform appear_faster:
    alpha 0.0
    linear 0.2 alpha 1.0

transform slideLeft(time=.4):
    parallel:
        xpos -250
        linear time xpos 10
    parallel:
        alpha 0
        linear time/1.6 alpha 1.0

screen game_info():
    zorder 10
    timer 1.5 action update_time repeat True
    timer 0.4 action set_weather_effect repeat True

    $ time = get_time()

    frame at slideLeft:
        yalign 0.025
        xsize 250
        padding (10, 10)

        vbox at appear:
            xfill True
            spacing 5

            hbox:
                xfill True
                spacing 5
                
                text "Time:\n[time]" size 20 xalign 0.0
                text "Location:\n[persistent.location]" size 20 xalign 0.0

            null height 5

            hbox:
                xfill True
                spacing 5

                text "Weather:\n[persistent.current_weather[0]]" size 20 xalign 0.0
                text "Current tokens:\n[persistent.current_tokens]" size 20 xalign 0.0

screen inputma():
    style_prefix "sss"

    key "K_RETURN" action Return()
    key "K_ESCAPE" action Return('exit')

    frame:
        vbox:
            hbox:
                align (0.5, 0.0)
                # textbutton "Back" action Return('exit')
                text "Write Something"
            
            box_wrap True
            input:
                default ""
                size 24
                value VariableInputValue("message")
                multiline True
                copypaste True

style sss_frame:
    yalign 0.99
    xalign 0.5
    xsize 700
    ysize 200
    xfill True
    padding (10, 10)

style sss_vbox:
    yfill True
    xfill True

## When this is true, menu captions will be spoken by the narrator. When false,
## menu captions will be displayed as empty buttons.
define config.narrator_menu = True


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 270
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    idle_background Frame("gui/button/choice_idle_background.png", gui.choice_button_borders)
    hover_background Frame("gui/button/choice_hover_background.png", gui.choice_button_borders)

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")
    outlines []


init python:
    def RigMouse():
        currentpos = renpy.get_mouse_pos()
        targetpos = [640, 345]
        if currentpos[1] < targetpos[1]:
            renpy.display.draw.set_mouse_pos((currentpos[0] * 9 + targetpos[0]) / 10.0, (currentpos[1] * 9 + targetpos[1]) / 10.0)

screen rigged_choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action

    timer 1.0/30.0 repeat True action Function(RigMouse)


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

screen quick_menu():

    # Ensure this appears on top of other screens.
    zorder 100

    if quick_menu:

        # Add an in-game quick menu.
        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 0.995

            textbutton _("History") action ShowMenu('history')
            textbutton _("Settings") action ShowMenu('preferences')


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
#init python:
#    config.overlay_screens.append("quick_menu")

default quick_menu = True

#style quick_button is default
#style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")
    activate_sound gui.activate_sound

style quick_button_text:
    properties gui.button_text_properties("quick_button")
    outlines []


################################################################################
# Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

init python:
    def FinishEnterName():
        if not player: return
        persistent.playername = player
        renpy.save_persistent()
        renpy.hide_screen("name_input")


screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.8

        spacing gui.navigation_spacing

        if not persistent.autoload or not main_menu:

            if main_menu:
                textbutton _("Club Room") action  [Function(charge_label, "Club Room"), If(persistent.playername, true=Start("charge_location"),  false=Show(screen="name_input", message="Please enter your name", ok_action=Function(FinishEnterName)))]
                textbutton _("Class Room") action [Function(charge_label, "Classroom 3"), If(persistent.playername, true=Start("charge_location"),  false=Show(screen="name_input", message="Please enter your name", ok_action=Function(FinishEnterName)))]

            else:

                textbutton _("History") action [ShowMenu("history"), SensitiveIf(renpy.get_screen("history") == None)]

            if enable_extras_menu:
                textbutton _("Extras") action [ShowMenu("extras"), SensitiveIf(renpy.get_screen("extras") == None)]

            if _in_replay:

                textbutton _("End Replay") action EndReplay(confirm=True)

            elif not main_menu:
                if persistent.playthrough != 3:
                    textbutton _("Main Men3") action MainMenu()
                else:
                    textbutton _("Main Menu") action NullAction()

            textbutton _("Settings") action [ShowMenu("preferences2"), SensitiveIf(renpy.get_screen("preferences") == None)]

            if not enable_extras_menu:
                textbutton _("Credits") action ShowMenu("about")

            if renpy.variant("pc"):

                ## Help isn't necessary or relevant to mobile devices.
                textbutton _("Help") action [Help("README.html"), Show(screen="dialog", message="The help file has been opened in your browser.", ok_action=Hide("dialog"))]

                ## The quit button is banned on iOS and unnecessary on Android.
                textbutton _("Quit") action Quit(confirm=not main_menu)
        else:
            timer 1.75 action Start("autoload_yurikill")


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style navigation_button_text:
    properties gui.button_text_properties("navigation_button")
    font "gui/font/RifficFree-Bold.ttf"
    color "#fff"
    outlines [(4, text_outline_color, 0, 0), (2, text_outline_color, 2, 2)]
    #outlines [(4, "#b59", 0, 0), (2, "#b59", 2, 2)]
    hover_outlines [(4, "#fac", 0, 0), (2, "#fac", 2, 2)]
    insensitive_outlines [(4, "#fce", 0, 0), (2, "#fce", 2, 2)]


## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## http://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu2():
    tag menu

    # This ensures that any other menu screen is replaced.

    style_prefix "main_menu"

    if persistent.ghost_menu:
        add "white"
        add "menu_art_y_ghost"
        add "menu_art_n_ghost"
    else:
        add "menu_bg"
        add "menu_art_y"
        add "menu_art_n"
        frame

        ## The use statement includes another screen inside this one. The actual
        ## contents of the main menu are in the navigation screen.
        use navigation

    if not persistent.ghost_menu:
        add "menu_particles"
        add "menu_particles"
        add "menu_particles"
        add "menu_logo"
    if persistent.ghost_menu:
        add "menu_art_s_ghost"
        add "menu_art_m_ghost"
    else:
        if persistent.playthrough == 1 or persistent.playthrough == 2:
            add "menu_art_s_glitch"
        else:
            add "menu_art_s"
        add "menu_particles"
        if persistent.playthrough != 4:
            add "menu_art_m"
        add "menu_fade"

    if gui.show_name:

        vbox:
            text "[config.name!t]":
                style "main_menu_title"

            text "[config.version]":
                style "main_menu_version"

    key "K_ESCAPE" action Quit(confirm=True)

style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text:
    color "#000000"
    size 16
    outlines []

style main_menu_frame:
    xsize 310
    yfill True

    background "menu_nav"

style main_menu_vbox:
    xalign 1.0
    xoffset -20
    xmaximum 800
    yalign 1.0
    yoffset -20

style main_menu_text:
    xalign 1.0

    layout "subtitle"
    text_align 1.0
    color gui.accent_color

style main_menu_title:
    size gui.title_text_size


## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid". When this
## screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu_m():
    $ persistent.menu_bg_m = True
    add "gui/menu_bg_m.png"
    timer 0.3 action Hide("game_menu_m")

screen game_menu(title, scroll=None):

    # Add the backgrounds.
    if main_menu:
        add gui.main_menu_background
    else:
        key "mouseup_3" action Return()
        add gui.game_menu_background

    style_prefix "game_menu"

    frame:
        style "game_menu_outer_frame"

        hbox:

            # Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        yinitial 1.0

                        side_yfill True

                        vbox:
                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial 1.0

                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        side_yfill True

                        transclude

                else:

                    transclude

    use navigation

    if not main_menu and persistent.playthrough == 2 and not persistent.menu_bg_m and renpy.random.randint(0, 49) == 0:
        on "show" action Show("game_menu_m")

    textbutton _("Return"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 30
    top_padding 120

    background "gui/overlay/game_menu.png"
    # background recolorize("gui/overlay/game_menu.png")

style game_menu_navigation_frame:
    xsize 280
    yfill True

style game_menu_content_frame:
    left_margin 40
    right_margin 20
    top_margin 10

style game_menu_viewport:
    xsize 920

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 10

style game_menu_label:
    xpos 50
    ysize 120

style game_menu_label_text:
    font "gui/font/RifficFree-Bold.ttf"
    size gui.title_text_size
    color "#fff"
    outlines [(6, text_outline_color, 0, 0), (3, text_outline_color, 2, 2)]
    #outlines [(6, "#b59", 0, 0), (3, "#b59", 2, 2)]
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -30


## About screen ################################################################
##
## This screen gives credit and copyright information about the game and Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("Credits"), scroll="viewport"):

        style_prefix "about"

        window:
            xoffset 35
            has fixed:
                yfit True

            vbox:
                add Transform("mod_assets/DDLCModTemplateLogo.png", size=(200,200)) xalign .5

                null height 5
                
                label "[config.name!t]" xalign .5
                text _("Version [config.version!t]\n") xalign .5

                ## gui.about is usually set in options.rpy.
                if gui.about:
                    text "[gui.about!t]\n"

                ## Do not touch/remove these unless the © or – symbol isn't available in your font.
                ## You may add things above or below it.
                ## If you are not going with a splashscreen option, this first line MUST stay in the mod.
                text "Made with bronya_rand's {a=https://github.com/GanstaKingofSA/DDLCModTemplate2.0}DDLC Mod Template 2.0{/a}\nCopyright © 2019-" + str(datetime.date.today().year) + " Azariel Del Carmen (bronya_rand). All rights reserved.\n"
                text "Doki Doki Literature Club. Copyright © 2017 Team Salvato. All rights reserved.\n"
                text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n[renpy.license!t]")


## This is redefined in options.rpy to add text to the about screen.
define gui.about = ""

style about_window is empty
style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    color "#000"
    outlines []
    text_align 0.5
    size gui.label_text_size

style about_text:
    color "#000"
    outlines []
    size gui.text_size
    text_align 0.5
    layout "subtitle"

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    idle_color gui.idle_color
    hover_color gui.hover_color
    hover_underline True

## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save
## https://www.renpy.org/doc/html/screen_special.html#load



screen load():

    tag menu


init python:
    def FileActionMod(name, page=None, **kwargs):
        if persistent.playthrough == 1 and not persistent.deleted_saves and renpy.current_screen().screen_name[0] == "load" and FileLoadable(name):
            return Show(screen="dialog", message="File error: \"characters/sayori.chr\"\n\nThe file is missing or corrupt.",
                ok_action=Show(screen="dialog", message="The save file is corrupt. Starting a new game.", ok_action=Function(renpy.full_restart, label="start")))
        elif persistent.playthrough == 3 and renpy.current_screen().screen_name[0] == "save":
            return Show(screen="dialog", message="There's no point in saving anymore.\nDon't worry, I'm not going anywhere.", ok_action=Hide("dialog"))
        else:
            return FileAction(name)


screen file_slots(title):

    default page_name_value = FilePageNameInputValue()

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter event before any of the
            ## buttons do.
            order_reverse True

            # The page name, which can be edited by clicking on a button.

            button:
                style "page_label"

                #key_events True
                xalign 0.5
                #action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileActionMod(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            hbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                spacing gui.page_spacing

                #textbutton _("<") action FilePagePrevious(max=9, wrap=True)

                #textbutton _("{#auto_page}A") action FilePage("auto")

                #textbutton _("{#quick_page}Q") action FilePage("quick")

                # range(1, 10) gives the numbers from 1 to 9.
                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)

                #textbutton _(">") action FilePageNext(max=9, wrap=True)


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 50
    ypadding 3

style page_label_text:
    color "#000"
    outlines []
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.button_text_properties("page_button")
    outlines []

style slot_button:
    properties gui.button_properties("slot_button")
    idle_background Frame("gui/button/slot_idle_background.png", gui.choice_button_borders)
    hover_background Frame("gui/button/slot_hover_background.png", gui.choice_button_borders)

style slot_button_text:
    properties gui.button_text_properties("slot_button")
    color "#666"
    outlines []

screen viewframe_options(title):

    style_prefix "viewframe"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 2

            label title

            null height 10

            transclude

style viewframe_frame is confirm_frame
style viewframe_label is confirm_prompt:
    xalign 0.5
style viewframe_label_text is confirm_prompt_text
style viewframe_button is confirm_button
style viewframe_button_text is confirm_button_text
style viewframe_text is confirm_prompt_text:
    size 20
    yalign 0.7

screen ddlc_preferences():
    hbox:
        box_wrap True

        if renpy.variant("pc"):

            vbox:
                style_prefix "radio"
                label _("Display")
                textbutton _("Windowed") action Preference("display", "window")
                textbutton _("Fullscreen") action Preference("display", "fullscreen")
                # textbutton _("More") action Show("display_options")

        if config.developer:
            vbox:
                style_prefix "radio"
                label _("Rollback Side")
                textbutton _("Disable") action Preference("rollback side", "disable")
                textbutton _("Left") action Preference("rollback side", "left")
                textbutton _("Right") action Preference("rollback side", "right")

        vbox:
            style_prefix "check"
            label _("Skip")
            textbutton _("Unseen Text") action Preference("skip", "toggle")
            textbutton _("After Choices") action Preference("after choices", "toggle")
            # textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))
    
    null height (4 * gui.pref_spacing)

    hbox:
        style_prefix "slider"
        box_wrap True

        vbox:
            
            hbox:
                label _("Text Speed")
                
                null width 5

                text str(preferences.text_cps) style "value_text"

            #bar value Preference("text speed")
            bar value FieldValue(_preferences, "text_cps", range=180, max_is_zero=False, style="slider", offset=20)

            hbox:
                label _("Auto-Forward Time")
                
                null width 5
                
                text str(round(preferences.afm_time)) style "value_text"

            bar value Preference("auto-forward time")

        vbox:
            
            if config.has_music:
                hbox:
                    label _("Music Volume")
                    
                    null width 5
                
                    text str(round(preferences.get_volume("music") * 100)) style "value_text"

                hbox:
                    bar value Preference("music volume")

            if config.has_sound:

                hbox:
                    label _("Sound Volume")
                    
                    null width 5
                
                    text str(round(preferences.get_volume("sfx") * 100)) style "value_text"

                hbox:
                    bar value Preference("sound volume")

                    if config.sample_sound:
                        textbutton _("Test") action Play("sound", config.sample_sound)

            if config.has_voice:
                hbox:
                    label _("Voice Volume")
                    
                    null width 5
                
                    text str(round(preferences.get_volume("voice") * 100)) style "value_text"

                hbox:
                    bar value Preference("voice volume")

                    if config.sample_voice:
                        textbutton _("Test") action Play("voice", config.sample_voice)

            if config.has_music or config.has_sound or config.has_voice:
                null height gui.pref_spacing

                textbutton _("Mute All"):
                    action Preference("all mute", "toggle")
                    style "mute_all_button"

screen template_preferences():
    hbox:
        box_wrap True

        if extra_settings:
            vbox:
                style_prefix "check"
                label _("Game Modes")
                textbutton _("Uncensored Mode") action If(persistent.uncensored_mode, 
                    ToggleField(persistent, "uncensored_mode"), 
                    Show("confirm", message="Are you sure you want to turn on Uncensored Mode?\nDoing so will enable more adult/sensitive\ncontent in your playthrough.\n\nThis setting will be dependent on the modder if\nthey programmed these checks in their story.", 
                        yes_action=[Hide("confirm"), ToggleField(persistent, "uncensored_mode")],
                        no_action=Hide("confirm")
                    ))
                textbutton _("Let's Play Mode") action If(persistent.lets_play, 
                    ToggleField(persistent, "lets_play"),
                    [ToggleField(persistent, "lets_play"), Show("dialog", 
                        message="You have enabled Let's Play Mode.\nThis mode allows you to skip content that\ncontains sensitive information or apply alternative\nstory options.\n\nThis setting will be dependent on the modder\nif they programmed these checks in their story.", 
                        ok_action=Hide("dialog")
                    )])
        
        vbox:
            style_prefix "name"
            label _("Player Name")
            
            null height 3
            
            if player == "":
                text _("No Name Set") xalign 0.5
            else:
                text "[player]" xalign 0.5
            
            textbutton _("Change Name") action Show(screen="name_input", message="Please enter your name", ok_action=Function(FinishEnterName, launchGame=False)):
                text_style "navigation_button_text"
        
        python:
            has_discord_module = True
            try:
                RPC
            except NameError:
                has_discord_module = False

        if not renpy.android and has_discord_module:
            vbox:
                style_prefix "name"
                label _("Discord RPC")

                python:
                    connect_status = _("Disconnected")
                    if not persistent.enable_discord:
                        connect_status = _("Disabled")
                    if RPC.rpc_connected:
                        connect_status = _("Connected")
                
                null height 3

                text "[connect_status]" xalign 0.5

                python:
                    enable_text = _("Enable")
                    if persistent.enable_discord:
                        enable_text = _("Disable")

                textbutton enable_text action [ToggleField(persistent, "enable_discord"), 
                    If(persistent.enable_discord, Function(RPC.close), Function(RPC.connect, reset=True))]:
                        text_style "navigation_button_text"
                if persistent.enable_discord and not RPC.rpc_connected:
                    textbutton _("Reconnect") action Function(RPC.connect, reset=True):
                        text_style "navigation_button_text"

    null height (4 * gui.pref_spacing)

    hbox:
        box_wrap True

        if enable_languages and translations:
            vbox:
                style_prefix "radio"
                label _("Language")
                hbox:
                    viewport:
                        mousewheel True
                        scrollbars "vertical"
                        ysize 120
                        has vbox

                        for tran in translations:
                            vbox:
                                for tlid, tlname in tran:
                                    textbutton tlname:
                                        action Language(tlid)

## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences2():
    tag menu

    if renpy.mobile:
        $ cols = 2
    else:
        $ cols = 4

    default ddlc_settings = True

    use game_menu(_("Settings"), scroll="viewport"):

        vbox:
            xoffset 50

            hbox:
                style_prefix "navigation"
                xoffset 150
                spacing 5
                textbutton _("DDLC Settings") action [SetScreenVariable("ddlc_settings", True), SensitiveIf(not ddlc_settings)]
                textbutton _("Template Settings") action [SetScreenVariable("ddlc_settings", False), SensitiveIf(ddlc_settings)]
            
            null height 10

            if ddlc_settings:
                use ddlc_preferences
            else:
                use template_preferences
                            
    text "v[config.version]":
                xalign 1.0 yalign 1.0
                xoffset -10 yoffset -10
                style "main_menu_version"

style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 2

style pref_label_text:
    font "gui/font/RifficFree-Bold.ttf"
    size 24
    color "#fff"
    outlines [(3, "#b59", 0, 0), (1, "#b59", 1, 1)]
    yalign 1.0

style pref_vbox:
    xsize 225

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style radio_button_text:
    properties gui.button_text_properties("radio_button")
    font "gui/font/Halogen.ttf"
    outlines []

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.button_text_properties("check_button")
    font "gui/font/Halogen.ttf"
    outlines []

style slider_slider:
    xsize 350

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 10

style slider_button_text:
    properties gui.button_text_properties("slider_button")

style slider_vbox:
    xsize 450

style name_label is pref_label
style name_label_text is pref_label_text

style name_text:
    font "gui/font/Halogen.ttf"
    size 24
    color gui.idle_color
    outlines []

style value_text:
    size 18
    color "#000"
    outlines []
    yalign 0.65

## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():
    tag menu
    
    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport")):
        
        style_prefix "history"
       
        for h in _history_list:
            
            window:
                
                ## This lays things out properly if history_height is None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False
                        
                        ## Take the color of the who text from the Character, if
                        ## set.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("The dialogue history is empty.")

define gui.history_allow_tags = set()

style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    text_align gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    text_align gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


################################################################################
## Additional screens
################################################################################

screen name_input(message, ok_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"
    key "K_RETURN" action [Play("sound", gui.activate_sound), ok_action]

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            input default "" value VariableInputValue("player") length 12 allow "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
            #additionally added Cyrillic characters to support Russian names for MC

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("OK") action ok_action

screen dialog(message, ok_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("OK") action ok_action

## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or no
## question.
##
## Edited for handling the ThreadPoolExecutor
##
## http://www.renpy.org/doc/html/screen_special.html#confirm


## This Controls the MultiThreading
init python:
    def Exit():
        print(executor)
        if executor != None:
            print("Shutting down executor")
            executor.shutdown()

screen confirm(message, yes_action, no_action):
    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                ## This evaluates if you want to quit the game or is a different confirmation box
                if isinstance(yes_action, list) and "store.Quit" in str(yes_action[1]):
                    textbutton _("Yes") action [Exit, yes_action]
                else:
                    textbutton _("Yes") action yes_action

                textbutton _("No") action no_action

    ## Right-click and escape answer "no".
    #key "game_menu" action no_action

style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame("gui/frame.png", gui.confirm_frame_borders, tile=gui.frame_tile)
    # background Frame(recolorize("gui/frame.png"), gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    color "#000"
    outlines []
    text_align 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style confirm_button_text is navigation_button_text:
    properties gui.button_text_properties("confirm_button")


## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator
screen fake_skip_indicator():
    use skip_indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 6

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    # We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    # glyph in it.
    font "DejaVuSans.ttf"


## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text message

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    size gui.notify_text_size
