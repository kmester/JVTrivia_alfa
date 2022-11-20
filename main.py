from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.garden.moretransitions import PixelTransition,RippleTransition,BlurTransition,RVBTransition
from kivy.uix.image import Image, AsyncImage
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivy.core.audio import SoundLoader
from kivymd.uix.relativelayout import MDRelativeLayout
import random
import time



Window.size = (360, 640)
WindowSizeWidth = Window.size[0]
WindowSizeHeight = Window.size[1]


# Kérdések osztálya
class Question(object):
    def __init__(self, question, answer, options, chapter):
        self.question = question
        self.answer = answer
        self.options = options
        self.chapter = chapter
############################################################################################################
# Kérdések adatbázisa
questions = [
    Question("Igaz, hogy a labda játékon kívül van, amikor akár a földön, akár a levegőben teljes terjedelmével áthalad a kapuvonalon?", "Igen", ["Bizonyos esetekben igen", "Igen", "Nem", "Soha"], 9),
    Question("Miről szól a Labdarúgás Játékszabályainak 9. szabálya?", "A labda játékban és játékon kívül", ["A mérkőzés időtartama", "A játék kezdése és újraindítása", "A labda játékban és játékon kívül", "A mérkőzés végeredményének \nmeghatározása"], 9),
    Question("Igaz, hogy a labda játékon kívül van, amikor akár a földön, akár a levegőben teljes terjedelmével áthalad az oldalvonalon?", "Igen", ["Bizonyos esetekben igen", "Igen", "Nem", "Soha"], 9),
    Question("Igaz, hogy a labda játékon kívül van, amikor a játékvezető megszakítja a játékot?", "Igen", ["Bizonyos esetekben igen", "Igen", "Nem", "Soha"], 9),
    Question("A labda érint egy játékvezetőt, a játéktéren marad és egy csapat ígéretes támadást indít. Mit kell tennie a játékvezetőnek?", "Szakítsa meg a játékot és \nlabdaejtéssel indítsa újra", ["Szakítsa meg a játékot és \nlabdaejtéssel indítsa újra", "Szakítsa meg a játékot és \nközvetett szabadrúgással indítsa újra", "Engedje tovább a játékot, \namennyiben előnyszabály adható", "Engedje tovább a játékot, amennyiben \na labdát birtokló csapat nem változik"], 9),
    Question("A labda érint egy játékvezetőt, a játéktéren marad és a labdát birtokló csapat megváltozik. Mit kell tennie a játékvezetőnek?", "Szakítsa meg a játékot és \nlabdaejtéssel indítsa újra", ["Szakítsa meg a játékot és \nlabdaejtéssel indítsa újra", "Szakítsa meg a játékot és \nközvetett szabadrúgással indítsa újra", "Engedje tovább a játékot, amennyiben\n előnyszabály adható", "Engedje tovább a játékot, amennyiben \negyik csapat sem vezet ígéretes támafást"], 9),
    Question("A labda érint egy játékvezetőt, a játéktéren marad és a labda közvetlenül a kapuba kerül. Mit kell tennie a játékvezetőnek?", "Szakítsa meg a játékot és \nlabdaejtéssel indítsa újra", ["Szakítsa meg a játékot és \nlabdaejtéssel indítsa újra", "Szakítsa meg a játékot és \nközvetett szabadrúgással indítsa újra", "Adja meg a gólt, amennyiben \nvédő játékost nem akadályozott a játékvezető ", "Adja meg a gólt, amennyiben a labda gólba \ntartott és védő játékost nem akadályozott a játékvezető"], 9),
    Question("A labda érint egy játékvezetőt és a játéktéren marad. Milyen esetekben kerül játékon kívülre a labda?", "Mindegyik válasz helyes", ["Egy csapat ígéretes támadást indít", "Labda közvetlenül a kapuba kerül", "Labdát birtokló csapat megváltozik", "Mindegyik válasz helyes"], 9),
    Question("A labda érinti a sarokzászlót és a játéktéren marad. Hogyan indul újra a játék?", "A labda nem került játékon kívülre, \nnincs szükség a játék újraindítására", ["Szögletrúgással", "Szögletrúgással vagy kirúgással", "Szögletrúgással, kirúgással \nvagy bedobással", "A labda nem került játékon kívülre, \nnincs szükség a játék újraindítására"], 9),
    Question("A labda érinti a sarokzászlót és az oldalvonalon keresztül elhagyja a játékteret. Hogyan indul újra a játék?", "Bedobással", ["Szögletrúgással", "Szögletrúgással vagy kirúgással", "Labdaejtéssel", "Bedobással"], 9),
    Question("A labda megpattan a játékvezetőn és közvetlenül az oldalvonalon keresztül elhagyja a játékteret. Hogyan folytatódik a játék?", "Labdaejtéssel", ["Bedobással", "Labdaejtéssel", "Közvetett szabadrúgással", "Bedobással vagy labdaejtéssel"], 9),
    Question("A labda megpattan a játékvezetőn és közvetlenül a kapuvonalon keresztül elhagyja a játékteret. Hogyan folytatódik a játék?", "Labdaejtéssel", ["Szögletrúgással", "Szögletrúgással vagy kirúgással", "Szögletrúgással, kirúgással \nvagy középkezdéssel", "Labdaejtéssel"], 9),
    #Question("", "", ["", "", "", ""], ),
]
############################################################################################################

# Tematikus játékhoz a kérdések különgyűjtve
new_questions = []
############################################################################################################

# Idézetek
quotes = [
    '"A futballhoz kell szerencse is, de a szerencséért tenni kell."',
    '"A góllövés az egyetlen olyan dolog a labdarúgásban, amit nem lehet megtanítani."',
    '"Kis pénz, kis futball, nagy pénz, nagy futball."',
    '"A kapufa éle mindig igazságos, mert annak lövése pattan be, aki a hétköznapokon többet tett a győzelemért."',
    '"Lecserélhetjük az állásunkat, állampolgárságunkat, még a vallásunkat is. De a csapatunkat soha nem változtathatjuk meg."',
    '"A futballban nincs lehetetlen, csak tehetetlen."',
    '"Ha azzal a tudattal megyünk ki a pályára, hogy a világbajnoki ezüstérmes ellen játszunk, akkor esélyünk sem lesz."',
    '"A fociban néha fel kell tartanod a kezedet, és be kell vallanod, hogy igen, ők jobbak nálunk."',
    '"Egy játékvezetőt nem lehet megtapsolni."',
    '"A futballban nincs előírva, hogy mindig a jobb csapat nyerjen."',
    '"Bárki is találta fel a focit, istenként kellene imádnunk."',
    '"Nem az a fontos, hogy az ember mit csinál a pályán kívül, hanem hogy a zöld gyepen hogyan teljesít."',
    '"Az Aranylabda az egyedüli labda, amit egyetlen védő sem tud elvenni tőlem."',
    '"A futballban a lehetetlen nem létezik."',
    '"A gól olyan, mint a ketchup. Erőltetni kell, és egyszer csak megindul."',
    '"Utánam lehet csinálni, zselés fejű piperkőcök!"',
    '"Ha nem tudsz szurkolni nekünk, amikor döntetlent játszunk vagy vesztünk, ne szurkolj akkor sem, ha győztünk."',
    '"Igyekezzünk végig irányítani a meccset, és ne hagyjuk, hogy az csak úgy megtörténjen velünk!"',
    '"Ebben az országban három dologhoz mindenki ért: a focihoz, a politikához és az irodalomtanításhoz."',
    '"Futni meg lehet tanulni, focizni meg tudni kell!"',
    '"Egy futballbíró legfontosabb dolga: észrevétlennek maradni!"',
    '"Amúgy sem voltam grófi gyerek, nem esik nehezemre téglát pakolni, maltert keverni, sódert, homokot lapátolni vagy betonozni."',
    '"Szőrmegalléros kabátot hordanak a fiaink, és olyanok, mint a nők. Úgy is játszanak."',
    '"Tudja, elnézem én ezeket az ifjú futballistákat, akik sok pénzt keresnek a semmilyen játékukkal, és úgy öltöznek, mint a…"',
    '"A Manchester United ugyanott állna velem, és a Mezőkövesd is egy külföldi topedzővel."',
    '"Gyerekkoromban csak a labda, a foci és a meccsre járás kötött le. Semmi más nem érdekelt."',
    '"Minket az utca nevelt. Megvolt minden telepnek a bandája, és ellenséges területre tévedve könnyen veszélyben találtuk magunkat."',
    '"Ha akkor nem Oroszország mellett döntünk, akkor most nem Abu Dhabiban játszanék."',
    '"A magyar érettségiről érkeztem a díjátadóra, azt hittem, hogy az kettévágta a napomat, de ez az elismerés helyretett."',
    '"Nem akarok kikerülni a műsorból, úgyhogy a Puskást nem mondom…"',
    '"Mindig csak meccsek után piáltunk, általában szombat esténként. Ha nyertünk azért, ha kikaptunk azért, ha pedig döntetlent játszottunk, akkor azért."',
    '"Még nem tudom, ki lesz a szövetségi kapitány, de máris féltem. Attól a több millió szövetségi kapitánytól, aki Magyarországon él."',
    '"Én imádtam a futballt! Imádtam a családomat és mindig a futballpályán jártam, engem több más nem érdekelt."',
    '"Az én kabalám mindig a labda volt. Akkor éreztem magam biztosnak, amikor a labda nálam volt, vagy ha a labdába belerúghattam..."',
    '"A férfiaknak nincsenek céljaik. Így aztán kitalálnak párat, és felállítják azokat egy focipálya két végében."',
    '"A futballban nincs lehetetlen, csak tehetetlen."',
    '"A futballban a "ha" nem játszik."',
    '"Ha meghalok, és újjászületek, megint focista akarok lenni. És ismét Diego Armando Maradona."',
    '"Szomorú, hogy a szurkolók lesüllyedtek a labdarúgás színvonalára."',
    '"A futball megtanított győzni, és megtanított veszíteni is, és megtanított arra is, hogy az öröm úgyis felülkerekedik a bánaton, és hogy a gól maga a boldogság."'
]


quotes_authors = [
    "Wukovics László",
    "Szokolai László",
    "Puskás Ferenc",
    "Kemény Dénes",
    "Elizabeth M. Gilbert",
    "Hajdú B. István",
    "Verebes József",
    "Sir Alex Ferguson",
    "Sir Alex Ferguson",
    "Buzánszky Jenő",
    "Hugo Sánchez",
    "Váczi Zoltán",
    "Albert Flórián",
    "Cristiano Ronaldo",
    "Cristiano Ronaldo",
    "Urbán Flórián",
    "Czibor Zoltán",
    "Jürgen Klopp",
    "Rados Virág",
    "Tóth II. József",
    "Kassai Viktor",
    "Lendvai Miklós",
    "Lendvai Miklós",
    "Lendvai Miklós",
    "Véber György",
    "Nyilasi Tibor",
    "Csank János",
    "Dzsudzsák Balázs",
    "Nagy Ádám",
    "Détári Lajos",
    "Véber György",
    "Puskás Ferenc",
    "Puskás Ferenc",
    "Puskás Ferenc",
    "Hugh Laurie",
    "Hajdú B. István",
    "Puskás Ferenc",
    "Diego Maradona",
    "Hofi Géza",
    "Fehér Miklós"

]

background = None
CHANGE_SCREEN = False

EVENT1 = Clock
EVENT2 = Clock
EVENT3 = Clock
EVENT4 = Clock
EVENT5 = Clock
EVENT6 = Clock
EVENT7 = Clock
EVENT8 = Clock
EVENT9 = Clock
EVENT10 = Clock
EVENT11 = Clock
EVENT12 = Clock
EVENT13 = Clock
EVENT14 = Clock
EVENT15 = Clock
EVENT16 = Clock
EVENT17 = Clock
EVENT18 = Clock
EVENT19 = Clock
EVENT20 = Clock
EVENT21 = Clock
EVENT22 = Clock
EVENT23 = Clock
EVENT24 = Clock
EVENT25 = Clock
EVENT26 = Clock
EVENT27 = Clock
EVENT28 = Clock
EVENT29 = Clock
EVENT30 = Clock
EVENT31 = Clock
EVENT32 = Clock
EVENT33 = Clock
EVENT34 = Clock
EVENT35 = Clock
EVENT36 = Clock
EVENT37 = Clock
EVENT38 = Clock
EVENT39 = Clock
EVENT40 = Clock
EVENT41 = Clock
EVENT42 = Clock
EVENT43 = Clock
EVENT44 = Clock
EVENT45 = Clock
EVENT46 = Clock
EVENT47 = Clock
EVENT48 = Clock
EVENT49 = Clock
EVENT50 = Clock
EVENT51 = Clock
EVENT52 = Clock
EVENT53 = Clock
EVENT54 = Clock
EVENT55 = Clock
EVENT56 = Clock
EVENT57 = Clock
EVENT58 = Clock
EVENT59 = Clock
EVENT60 = Clock
EVENT61 = Clock
EVENT62 = Clock
EVENT63 = Clock
EVENT64 = Clock
EVENT65 = Clock



# Főmenü képernyő
class MainMenuScreen(Screen):
    global background
    def set_the_background_music(self):
        global background
        if self.ids.my_icon_volume.icon == 'volume-mute':
            self.ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("free_game_screen").ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("chapter_game_screen").ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("choose_chapters_screen").ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("game_screen").ids.my_icon_volume.icon = 'volume-medium'

            background_randomize_number = random.randint(1,3)
            if background_randomize_number == 1:
                background = SoundLoader.load('background01.ogg')
                background.volume = 0.2
                background.play()
                background.loop = True
            if background_randomize_number == 2:
                background = SoundLoader.load('background02.ogg')
                background.volume = 0.2
                background.play()
                background.loop = True
            if background_randomize_number == 3:
                background = SoundLoader.load('background03.ogg')
                background.volume = 0.2
                background.play()
                background.loop = True

        elif self.ids.my_icon_volume.icon == 'volume-medium':
            self.ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("free_game_screen").ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("chapter_game_screen").ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("choose_chapters_screen").ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("game_screen").ids.my_icon_volume.icon = 'volume-mute'
            background.unload()

    question_number = 0
    dialog = None

    def go_to_main_menu(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos vissza mész a főmenübe?[/color]",
                type="confirmation",
                md_bg_color = "#8D99AE",
                #background_color = '#3B3838',
                auto_dismiss = False,
                radius=[7, 7, 7, 7],

                #text_color = '#EDF2F4',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_main_menu
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_main_menu(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True

        # kattintás letiltások visszaállítása
        self.ids.my_main_menu_button_1.disabled = False
        self.ids.my_main_menu_button_2.disabled = False
        self.ids.my_main_menu_button_3.disabled = False

        self.ids.my_main_menu_button_1.on_active = False
        self.ids.my_main_menu_button_2.on_active = False
        self.ids.my_main_menu_button_3.on_active = False

        # Go to the main menu
        number = random.randint(1,5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None


    def go_to_freegame(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos a szabad játékot választod?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_freegame
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_freegame(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        # belső változók kinullázása

        self.score = 0
        self.wrong = 0
        self.answers_number = 0
        self.question_number = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        self.manager.get_screen("free_game_screen").ids.my_pause_freegame.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_play_freegame.disabled = True

        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None

        global WindowSizeWidth
        global WindowSizeHeight
        self.manager.get_screen("free_game_screen").ids.jvtrivia_icon_freegame.size_hint = (0.3, WindowSizeWidth/WindowSizeHeight*0.3)
        self.manager.get_screen("free_game_screen").ids.jvtrivia_icon_freegame.keep_ratio = True
        self.manager.get_screen("free_game_screen").ids.jvtrivia_icon_freegame.pos_hint = {'x': 0, 'y': 0}

        # Alsó idézet beállítása
        self.set_quotes_free_game()

        # Scoreboard kinullázása
        self.set_scoreboard_freegame()

        # Gombok és kérdés clearing
        self.manager.get_screen("free_game_screen").ids.label_score.text = str(0)
        self.manager.get_screen("free_game_screen").ids.sum_label_questions.text = str(0)
        self.manager.get_screen("free_game_screen").ids.label_question.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_B.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_C.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_D.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_pause_freegame.disabled = True

        self.manager.get_screen("chapter_game_screen").ids.label_score_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.sum_label_questions_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3

        self.manager.get_screen("game_screen").ids.label_score_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.sum_label_questions_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = ""
        self.manager.get_screen("game_screen").ids.my_button_AAA.text = ""
        self.manager.get_screen("game_screen").ids.my_button_BBB.text = ""
        self.manager.get_screen("game_screen").ids.my_button_CCC.text = ""
        self.manager.get_screen("game_screen").ids.my_button_DDD.text = ""
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_AAA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_BBB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_CCC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_DDD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_AAA.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_BBB.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_CCC.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_DDD.elevation = 3

        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)

        # Első kérdés és válasz beállítása
        EVENT49 = Clock.schedule_once(self.set_questions_freegame, 6)
        EVENT50 = Clock.schedule_once(self.set_answers_A_freegame, 10)
        EVENT51 = Clock.schedule_once(self.set_answers_B_freegame, 12)
        EVENT52 = Clock.schedule_once(self.set_answers_C_freegame, 14)
        EVENT53 = Clock.schedule_once(self.set_answers_D_freegame, 16)
        EVENT54 = Clock.schedule_once(self.set_answers_undisabled_freegame, 17)
        EVENT55 = Clock.schedule_once(self.play_sound_question_freegame, 6)
        EVENT56 = Clock.schedule_once(self.play_sound_button_freegame, 10)
        EVENT57 = Clock.schedule_once(self.play_sound_button_freegame, 12)
        EVENT58 = Clock.schedule_once(self.play_sound_button_freegame, 14)
        EVENT59 = Clock.schedule_once(self.play_sound_button_freegame, 16)

    # Kérdés beállítása
    def set_questions_freegame(self, delay=3):
        self.randomize_questions()
        if len(questions[self.question_number].question) > 70:
            self.manager.get_screen("free_game_screen").ids.label_question.font_size = 14
            self.manager.get_screen("free_game_screen").ids.label_question.text = questions[self.question_number].question
        elif len(questions[self.question_number].question) > 140:
            self.manager.get_screen("free_game_screen").ids.label_question.font_size = 13
            self.manager.get_screen("free_game_screen").ids.label_question.text = questions[self.question_number].question
        else:
            self.manager.get_screen("free_game_screen").ids.label_question.font_size = 16
            self.manager.get_screen("free_game_screen").ids.label_question.text = questions[self.question_number].question



    ######################################

    # Kérdések véletlenszerű megkeverése
    def randomize_questions(self):
        random.shuffle(questions)
    #######################################

    def set_scoreboard_freegame(self):
        self.manager.get_screen("free_game_screen").ids.label_score.text = str(0)
        self.manager.get_screen("free_game_screen").ids.sum_label_questions.text = str(0)

    def set_answers_A_freegame(self, delay=4):
        A_length = int(len(questions[self.question_number].options[0]))
        B_length = int(len(questions[self.question_number].options[1]))
        C_length = int(len(questions[self.question_number].options[2]))
        D_length = int(len(questions[self.question_number].options[3]))
        length_list = [A_length, B_length, C_length, D_length]
        max_length = max(length_list)

        if max_length <= 25:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "14"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "14"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "14"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "14"
        if max_length > 25:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "13"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "13"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "13"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "13"

        if max_length > 35:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "12"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "12"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "12"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "12"
        if max_length > 55:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "11"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "11"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "11"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "11"
        if max_length > 65:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "10"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "10"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "10"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "10"
        if max_length > 85:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "9"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "9"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "9"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "9"


        self.manager.get_screen("free_game_screen").ids.my_button_A.text = questions[self.question_number].options[0]
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_A.on_active = False
        self.manager.get_screen("free_game_screen").ids.my_button_A.md_bg_color = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3

    def set_answers_B_freegame(self, delay=4):

        self.manager.get_screen("free_game_screen").ids.my_button_B.text = questions[self.question_number].options[1]
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_B.on_active = False
        self.manager.get_screen("free_game_screen").ids.my_button_B.md_bg_color = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3

    def set_answers_C_freegame(self, delay=4):

        self.manager.get_screen("free_game_screen").ids.my_button_C.text = questions[self.question_number].options[2]
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_C.on_active = False
        self.manager.get_screen("free_game_screen").ids.my_button_C.md_bg_color = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3

    def set_answers_D_freegame(self, delay=4):

        self.manager.get_screen("free_game_screen").ids.my_button_D.text = questions[self.question_number].options[3]
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_D.on_active = False
        self.manager.get_screen("free_game_screen").ids.my_button_D.md_bg_color = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3

    def set_answers_undisabled_freegame(self, delay=8):
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled = False
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled = False
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled = False
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled = False
    #######################################


    def play_sound_button_freegame(self, delay=0):
        sound = SoundLoader.load('buttons01.ogg')
        if CHANGE_SCREEN == False:
            if self.manager.current != "choose_chapters_screen":
                if self.manager.current != "chapter_game_screen":
                    if self.manager.current != "game_screen":
                        if self.manager.current != "main_menu_screen":
                            if sound:
                                sound.volume = 0.5
                                sound.play()

    def play_sound_question_freegame(self, delay=2.5):
        number = random.randint(1,6)
        if number == 1:
            sound = SoundLoader.load('questions01.ogg')
        if number == 2:
            sound = SoundLoader.load('questions02.ogg')
        if number == 3:
            sound = SoundLoader.load('questions03.ogg')
        if number == 4:
            sound = SoundLoader.load('questions04.ogg')
        if number == 5:
            sound = SoundLoader.load('questions05.ogg')
        if number == 6:
            sound = SoundLoader.load('questions06.ogg')
        if CHANGE_SCREEN == False:
            if self.manager.current != "choose_chapters_screen":
                if self.manager.current != "chapter_game_screen":
                    if self.manager.current != "game_screen":
                        if self.manager.current != "main_menu_screen":
                            if sound:
                                sound.volume = 0.3
                                sound.play()

    def go_to_chaptergame(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos a tematikus gyakorlást választod?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_chaptergame
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_chaptergame(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        self.manager.get_screen("chapter_game_screen").ids.my_pause_chaptergame.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_play_chaptergame.disabled = True
        # belső változók kinullázása
        self.score = 0
        self.wrong = 0
        self.answers_number = 0
        self.question_number = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None

        global WindowSizeWidth
        global WindowSizeHeight
        self.manager.get_screen("choose_chapters_screen").ids.jvtrivia_icon_choosechapters.size_hint = (
        0.3, WindowSizeWidth / WindowSizeHeight * 0.3)
        self.manager.get_screen("choose_chapters_screen").ids.jvtrivia_icon_choosechapters.keep_ratio = True
        self.manager.get_screen("choose_chapters_screen").ids.jvtrivia_icon_choosechapters.pos_hint = {'x': 0, 'y': 0}


        # Gombok és kérdés clearing
        self.manager.get_screen("chapter_game_screen").ids.label_score_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.sum_label_questions_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3

        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)

        self.set_quotes_choose_chapter_game()


    def go_to_gamescreen(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos vizsgázni szeretnél?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_gamescreen
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_gamescreen(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        self.manager.get_screen("game_screen").ids.pause_gamescreen.disabled = True
        self.manager.get_screen("game_screen").ids.play_gamescreen.disabled = True

        # belső változók kinullázása
        self.score = 0
        self.wrong = 0
        self.answers_number = 0
        self.question_number = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None

        global WindowSizeWidth
        global WindowSizeHeight
        self.manager.get_screen("game_screen").ids.jvtrivia_icon_gamescreen.size_hint = (
            0.3, WindowSizeWidth / WindowSizeHeight * 0.3)
        self.manager.get_screen("game_screen").ids.jvtrivia_icon_gamescreen.keep_ratio = True
        self.manager.get_screen("game_screen").ids.jvtrivia_icon_gamescreen.pos_hint = {'x': 0, 'y': 0}

        # Alsó idézet beállítása
        self.set_quotes_gamescreen()

        # Scoreboard kinullázása
        self.set_scoreboard_gamescreen()

        # Gombok és kérdés clearing
        self.manager.get_screen("free_game_screen").ids.label_score.text = str(0)
        self.manager.get_screen("free_game_screen").ids.sum_label_questions.text = str(0)
        self.manager.get_screen("free_game_screen").ids.label_question.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_B.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_C.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_D.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3

        self.manager.get_screen("chapter_game_screen").ids.label_score_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.sum_label_questions_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3

        self.manager.get_screen("game_screen").ids.label_score_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.sum_label_questions_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = ""
        self.manager.get_screen("game_screen").ids.my_button_AAA.text = ""
        self.manager.get_screen("game_screen").ids.my_button_BBB.text = ""
        self.manager.get_screen("game_screen").ids.my_button_CCC.text = ""
        self.manager.get_screen("game_screen").ids.my_button_DDD.text = ""
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_AAA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_BBB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_CCC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_DDD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_AAA.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_BBB.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_CCC.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_DDD.elevation = 3


        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)

        # Első kérdés és válasz beállítása
        EVENT49 = Clock.schedule_once(self.set_questions_gamescreen, 6)
        EVENT50 = Clock.schedule_once(self.set_answers_A_gamescreen, 10)
        EVENT51 = Clock.schedule_once(self.set_answers_B_gamescreen, 12)
        EVENT52 = Clock.schedule_once(self.set_answers_C_gamescreen, 14)
        EVENT53 = Clock.schedule_once(self.set_answers_D_gamescreen, 16)
        EVENT54 = Clock.schedule_once(self.set_answers_undisabled_gamescreen, 17)
        EVENT55 = Clock.schedule_once(self.play_sound_question_gamescreen, 6)
        EVENT56 = Clock.schedule_once(self.play_sound_button_gamescreen, 10)
        EVENT57 = Clock.schedule_once(self.play_sound_button_gamescreen, 12)
        EVENT58 = Clock.schedule_once(self.play_sound_button_gamescreen, 14)
        EVENT59 = Clock.schedule_once(self.play_sound_button_gamescreen, 16)

    def play_sound_button_gamescreen(self, delay=0):
        sound = SoundLoader.load('buttons01.ogg')
        if sound:
            sound.volume = 0.5
            sound.play()

    def play_sound_question_gamescreen(self, delay=2.5):
        number = random.randint(1,6)
        if number == 1:
            sound = SoundLoader.load('questions01.ogg')
        if number == 2:
            sound = SoundLoader.load('questions02.ogg')
        if number == 3:
            sound = SoundLoader.load('questions03.ogg')
        if number == 4:
            sound = SoundLoader.load('questions04.ogg')
        if number == 5:
            sound = SoundLoader.load('questions05.ogg')
        if number == 6:
            sound = SoundLoader.load('questions06.ogg')
        if sound:
            sound.volume = 0.3
            sound.play()

    def set_answers_A_gamescreen(self, delay=4):
        A_length = int(len(questions[self.question_number].options[0]))
        B_length = int(len(questions[self.question_number].options[1]))
        C_length = int(len(questions[self.question_number].options[2]))
        D_length = int(len(questions[self.question_number].options[3]))
        length_list = [A_length, B_length, C_length, D_length]
        max_length = max(length_list)

        if max_length <= 25:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "14"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "14"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "14"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "14"
        if max_length > 25:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "13"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "13"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "13"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "13"

        if max_length > 35:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "12"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "12"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "12"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "12"
        if max_length > 55:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "11"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "11"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "11"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "11"
        if max_length > 65:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "10"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "10"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "10"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "10"
        if max_length > 85:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "9"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "9"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "9"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "9"


        self.manager.get_screen("game_screen").ids.my_button_AAA.text = questions[self.question_number].options[0]
        self.manager.get_screen("game_screen").ids.my_button_AAA.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_AAA.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_AAA.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_AAA.elevation = 3

    def set_answers_B_gamescreen(self, delay=5):
        self.manager.get_screen("game_screen").ids.my_button_BBB.text = questions[self.question_number].options[1]
        self.manager.get_screen("game_screen").ids.my_button_BBB.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_BBB.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_BBB.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_BBB.elevation = 3

    def set_answers_C_gamescreen(self, delay=6):
        self.manager.get_screen("game_screen").ids.my_button_CCC.text = questions[self.question_number].options[2]
        self.manager.get_screen("game_screen").ids.my_button_CCC.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_CCC.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_CCC.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_CCC.elevation = 3

    def set_answers_D_gamescreen(self, delay=7):
        self.manager.get_screen("game_screen").ids.my_button_DDD.text = questions[self.question_number].options[3]
        self.manager.get_screen("game_screen").ids.my_button_DDD.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_DDD.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_DDD.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_DDD.elevation = 3

    def set_answers_undisabled_gamescreen(self, delay=8):
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled = False
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled = False
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled = False
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled = False

    # Kérdés beállítása
    def set_questions_gamescreen(self, delay=3):
        self.randomize_questions()
        if len(questions[self.question_number].question) > 70:
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 14
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[
                self.question_number].question
        elif len(questions[self.question_number].question) > 140:
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 13
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[
                self.question_number].question
        else:
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 16
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[
                self.question_number].question
    ######################################

    def set_scoreboard_gamescreen(self):
        self.manager.get_screen("game_screen").ids.label_score_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.sum_label_questions_gamescreen.text = str(0)

    def set_quotes_gamescreen(self, delay=3):
        number = random.randint(0,39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("game_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("game_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("game_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("game_screen").ids.my_quote_author.text = quotes_authors[number]


    def go_to_exit(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos kilépsz a JVTriviából?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_exit
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_exit(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None


    # Click cancel button
    def close_dialog(self, obj):
        # Close alert box
        self.dialog.dismiss(force=True)
        self.dialog = None

    def set_quotes_free_game(self, delay=3):
        number = random.randint(0,39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("free_game_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("free_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("free_game_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("free_game_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("free_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("free_game_screen").ids.my_quote_author.text = quotes_authors[number]

    def set_quotes_choose_chapter_game(self):
        number = random.randint(0, 39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]


class FreeGameScreen(Screen):
    global background

    def set_the_background_music(self):
        global background
        if self.ids.my_icon_volume.icon == 'volume-mute':
            self.ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("main_menu_screen").ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("chapter_game_screen").ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("choose_chapters_screen").ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("game_screen").ids.my_icon_volume.icon = 'volume-medium'

            background_randomize_number = random.randint(1, 3)
            if background_randomize_number == 1:
                background = SoundLoader.load('background01.ogg')
                background.volume = 0.2
                background.play()
                background.loop = True
            if background_randomize_number == 2:
                background = SoundLoader.load('background02.ogg')
                background.volume = 0.2
                background.play()
                background.loop = True
            if background_randomize_number == 3:
                background = SoundLoader.load('background03.ogg')
                background.volume = 0.2
                background.play()
                background.loop = True

        elif self.ids.my_icon_volume.icon == 'volume-medium':
            self.ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("main_menu_screen").ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("chapter_game_screen").ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("choose_chapters_screen").ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("game_screen").ids.my_icon_volume.icon = 'volume-mute'
            background.unload()

    dialog = None

    def go_to_main_menu(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos vissza mész a főmenübe?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_main_menu
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_main_menu(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        # belső változók kinullázása
        self.score = 0
        self.answers_number = 0
        self.question_number = 0
        self.wrong = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        # kattintás letiltások visszaállítása
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_1.disabled = False
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_2.disabled = False
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_3.disabled = False

        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_1.on_active = False
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_2.on_active = False
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_3.on_active = False

        # Gombok és kérdés clearing
        self.manager.get_screen("free_game_screen").ids.label_score.text = str(0)
        self.manager.get_screen("free_game_screen").ids.sum_label_questions.text = str(0)
        self.manager.get_screen("free_game_screen").ids.label_question.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_B.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_C.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_D.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3

        self.manager.get_screen("chapter_game_screen").ids.label_score_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.sum_label_questions_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3

        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)

        # Go to the main menu
        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None

    def go_to_freegame(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos a szabad játékot választod?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_freegame
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_freegame(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True

        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None



    def go_to_chaptergame(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos a tematikus gyakorlást választod?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_chaptergame
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_chaptergame(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        self.manager.get_screen("chapter_game_screen").ids.my_pause_chaptergame.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_play_chaptergame.disabled = True
        # belső változók kinullázása
        self.score = 0
        self.wrong = 0
        self.answers_number = 0
        self.question_number = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None

        global WindowSizeWidth
        global WindowSizeHeight
        self.manager.get_screen("choose_chapters_screen").ids.jvtrivia_icon_choosechapters.size_hint = (
            0.3, WindowSizeWidth / WindowSizeHeight * 0.3)
        self.manager.get_screen("choose_chapters_screen").ids.jvtrivia_icon_choosechapters.keep_ratio = True
        self.manager.get_screen("choose_chapters_screen").ids.jvtrivia_icon_choosechapters.pos_hint = {'x': 0, 'y': 0}

        # Alsó idézet beállítása
        number = random.randint(0, 39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]

        # Gombok és kérdés clearing
        self.manager.get_screen("free_game_screen").ids.label_score.text = str(0)
        self.manager.get_screen("free_game_screen").ids.sum_label_questions.text = str(0)
        self.manager.get_screen("free_game_screen").ids.label_question.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_B.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_C.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_D.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3

        self.manager.get_screen("chapter_game_screen").ids.label_score_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.sum_label_questions_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3

        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)

        self.set_quotes_choose_chapter_game()

    def set_quotes_choose_chapter_game(self):
        number = random.randint(0, 39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]



    def go_to_gamescreen(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos vizsgázni szeretnél?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_gamescreen
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_gamescreen(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        self.manager.get_screen("game_screen").ids.pause_gamescreen.disabled = True
        self.manager.get_screen("game_screen").ids.play_gamescreen.disabled = True
        # belső változók kinullázása
        self.score = 0
        self.wrong = 0
        self.answers_number = 0
        self.question_number = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None

        global WindowSizeWidth
        global WindowSizeHeight
        self.manager.get_screen("game_screen").ids.jvtrivia_icon_gamescreen.size_hint = (
            0.3, WindowSizeWidth / WindowSizeHeight * 0.3)
        self.manager.get_screen("game_screen").ids.jvtrivia_icon_gamescreen.keep_ratio = True
        self.manager.get_screen("game_screen").ids.jvtrivia_icon_gamescreen.pos_hint = {'x': 0, 'y': 0}

        # Alsó idézet beállítása
        self.set_quotes_gamescreen()

        # Scoreboard kinullázása
        self.set_scoreboard_gamescreen()

        # Gombok és kérdés clearing
        self.manager.get_screen("free_game_screen").ids.label_score.text = str(0)
        self.manager.get_screen("free_game_screen").ids.sum_label_questions.text = str(0)
        self.manager.get_screen("free_game_screen").ids.label_question.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_B.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_C.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_D.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3

        self.manager.get_screen("chapter_game_screen").ids.label_score_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.sum_label_questions_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3

        self.manager.get_screen("game_screen").ids.label_score_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.sum_label_questions_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = ""
        self.manager.get_screen("game_screen").ids.my_button_AAA.text = ""
        self.manager.get_screen("game_screen").ids.my_button_BBB.text = ""
        self.manager.get_screen("game_screen").ids.my_button_CCC.text = ""
        self.manager.get_screen("game_screen").ids.my_button_DDD.text = ""
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_AAA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_BBB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_CCC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_DDD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_AAA.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_BBB.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_CCC.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_DDD.elevation = 3

        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)

        # Első kérdés és válasz beállítása
        EVENT49 = Clock.schedule_once(self.set_questions_gamescreen, 6)
        EVENT50 = Clock.schedule_once(self.set_answers_A_gamescreen, 10)
        EVENT51 = Clock.schedule_once(self.set_answers_B_gamescreen, 12)
        EVENT52 = Clock.schedule_once(self.set_answers_C_gamescreen, 14)
        EVENT53 = Clock.schedule_once(self.set_answers_D_gamescreen, 16)
        EVENT54 = Clock.schedule_once(self.set_answers_undisabled_gamescreen, 17)
        EVENT55 = Clock.schedule_once(self.play_sound_question_gamescreen, 6)
        EVENT56 = Clock.schedule_once(self.play_sound_button_gamescreen, 10)
        EVENT57 = Clock.schedule_once(self.play_sound_button_gamescreen, 12)
        EVENT58 = Clock.schedule_once(self.play_sound_button_gamescreen, 14)
        EVENT59 = Clock.schedule_once(self.play_sound_button_gamescreen, 16)

    def play_sound_button_gamescreen(self, delay=0):
        sound = SoundLoader.load('buttons01.ogg')
        if sound:
            sound.volume = 0.5
            sound.play()

    def play_sound_question_gamescreen(self, delay=2.5):
        number = random.randint(1, 6)
        if number == 1:
            sound = SoundLoader.load('questions01.ogg')
        if number == 2:
            sound = SoundLoader.load('questions02.ogg')
        if number == 3:
            sound = SoundLoader.load('questions03.ogg')
        if number == 4:
            sound = SoundLoader.load('questions04.ogg')
        if number == 5:
            sound = SoundLoader.load('questions05.ogg')
        if number == 6:
            sound = SoundLoader.load('questions06.ogg')
        if sound:
            sound.volume = 0.3
            sound.play()

    def set_answers_A_gamescreen(self, delay=4):
        A_length = int(len(questions[self.question_number].options[0]))
        B_length = int(len(questions[self.question_number].options[1]))
        C_length = int(len(questions[self.question_number].options[2]))
        D_length = int(len(questions[self.question_number].options[3]))
        length_list = [A_length, B_length, C_length, D_length]
        max_length = max(length_list)

        if max_length <= 25:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "14"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "14"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "14"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "14"
        if max_length > 25:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "13"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "13"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "13"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "13"

        if max_length > 35:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "12"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "12"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "12"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "12"
        if max_length > 55:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "11"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "11"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "11"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "11"
        if max_length > 65:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "10"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "10"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "10"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "10"
        if max_length > 85:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "9"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "9"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "9"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "9"

        self.manager.get_screen("game_screen").ids.my_button_AAA.text = questions[self.question_number].options[0]
        self.manager.get_screen("game_screen").ids.my_button_AAA.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_AAA.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_AAA.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_AAA.elevation = 3

    def set_answers_B_gamescreen(self, delay=5):
        self.manager.get_screen("game_screen").ids.my_button_BBB.text = questions[self.question_number].options[1]
        self.manager.get_screen("game_screen").ids.my_button_BBB.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_BBB.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_BBB.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_BBB.elevation = 3

    def set_answers_C_gamescreen(self, delay=6):
        self.manager.get_screen("game_screen").ids.my_button_CCC.text = questions[self.question_number].options[2]
        self.manager.get_screen("game_screen").ids.my_button_CCC.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_CCC.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_CCC.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_CCC.elevation = 3

    def set_answers_D_gamescreen(self, delay=7):
        self.manager.get_screen("game_screen").ids.my_button_DDD.text = questions[self.question_number].options[3]
        self.manager.get_screen("game_screen").ids.my_button_DDD.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_DDD.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_DDD.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_DDD.elevation = 3

    def set_answers_undisabled_gamescreen(self, delay=8):
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled = False
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled = False
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled = False
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled = False

        # Kérdés beállítása

    def set_questions_gamescreen(self, delay=3):
        self.randomize_questions()
        if len(questions[self.question_number].question) > 70:
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 14
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[
                self.question_number].question
        elif len(questions[self.question_number].question) > 140:
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 13
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[
                self.question_number].question
        else:
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 16
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[
                self.question_number].question
        ######################################

    def set_scoreboard_gamescreen(self):
        self.manager.get_screen("game_screen").ids.label_score_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.sum_label_questions_gamescreen.text = str(0)

    def set_quotes_gamescreen(self, delay=3):
        number = random.randint(0, 39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("game_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("game_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("game_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("game_screen").ids.my_quote_author.text = quotes_authors[number]


    def go_to_exit(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos kilépsz a JVTriviából?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_exit
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_exit(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        # belső változók kinullázása
        self.score = 0
        self.wrong = 0
        self.answers_number = 0
        self.question_number = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None

    # Click cancel button
    def close_dialog(self, obj):
        # Close alert box
        self.dialog.dismiss(force=True)
        self.dialog = None

    score = 0
    wrong = 0
    answers_number = 0
    question_number = 0

    def on_pre_enter(self, *args):
        self.set_scoreboard()
        global CHANGE_SCREEN
        CHANGE_SCREEN = False
    ####################################

    #Kérdések véletlenszerű megkeverése
    def randomize_questions(self):
        random.shuffle(questions)
    #######################################

    def set_quotes(self, delay=3):
        number = random.randint(0,39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("free_game_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("free_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("free_game_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("free_game_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("free_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("free_game_screen").ids.my_quote_author.text = quotes_authors[number]


    # Kérdés beállítása
    def set_questions(self, delay = 3):
        if self.question_number >= len(questions)-1:
            self.randomize_questions()
            self.question_number = 0
            if len(questions[self.question_number].question) > 70:
                self.manager.get_screen("free_game_screen").ids.label_question.font_size = 14
                self.manager.get_screen("free_game_screen").ids.label_question.text = questions[
                    self.question_number].question
            elif len(questions[self.question_number].question) > 140:
                self.manager.get_screen("free_game_screen").ids.label_question.font_size = 13
                self.manager.get_screen("free_game_screen").ids.label_question.text = questions[
                    self.question_number].question
            else:
                self.manager.get_screen("free_game_screen").ids.label_question.font_size = 16
                self.manager.get_screen("free_game_screen").ids.label_question.text = questions[
                    self.question_number].question
        else:
            self.question_number += 1
            if len(questions[self.question_number].question) > 70:
                self.manager.get_screen("free_game_screen").ids.label_question.font_size = 14
                self.manager.get_screen("free_game_screen").ids.label_question.text = questions[
                    self.question_number].question
            elif len(questions[self.question_number].question) > 140:
                self.manager.get_screen("free_game_screen").ids.label_question.font_size = 13
                self.manager.get_screen("free_game_screen").ids.label_question.text = questions[
                    self.question_number].question
            else:
                self.manager.get_screen("free_game_screen").ids.label_question.font_size = 16
                self.manager.get_screen("free_game_screen").ids.label_question.text = questions[
                    self.question_number].question
    ######################################

    # Üres kérdés beállítása 1 mp nyerése
    def set_questions_blank(self, delay = 2):
        self.ids.label_question.text = ""

    # Válaszok beállítása a gombokra véletlenszerűen
    def set_answers(self, delay = 3):
        # Válaszok szövegének beállítása
        self.ids.my_button_A.text = ""
        self.ids.my_button_B.text = ""
        self.ids.my_button_C.text = ""
        self.ids.my_button_D.text = ""
        self.ids.my_button_A.disabled_color = '#404040'
        self.ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
        self.ids.my_button_B.disabled_color = '#404040'
        self.ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
        self.ids.my_button_C.disabled_color = '#404040'
        self.ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
        self.ids.my_button_D.disabled_color = '#404040'
        self.ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
        random.shuffle(questions[self.question_number].options)

    def set_answers_A(self, delay=4):
        A_length = int(len(questions[self.question_number].options[0]))
        B_length = int(len(questions[self.question_number].options[1]))
        C_length = int(len(questions[self.question_number].options[2]))
        D_length = int(len(questions[self.question_number].options[3]))
        length_list = [A_length, B_length, C_length, D_length]
        max_length = max(length_list)

        if max_length <= 25:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "14"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "14"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "14"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "14"
        if max_length > 25:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "13"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "13"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "13"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "13"

        if max_length > 35:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "12"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "12"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "12"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "12"
        if max_length > 55:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "11"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "11"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "11"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "11"
        if max_length > 65:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "10"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "10"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "10"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "10"
        if max_length > 85:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "9"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "9"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "9"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "9"

        self.ids.my_button_A.text = questions[self.question_number].options[0]
        self.ids.my_button_A.elevation = 3
        self.ids.my_button_A.on_active = False
        self.ids.my_button_A.md_bg_color = '#EDF2F4'
        self.ids.my_button_A.elevation = 3

    def set_answers_B(self, delay=5):
        self.ids.my_button_B.text = questions[self.question_number].options[1]
        self.ids.my_button_B.elevation = 3
        self.ids.my_button_B.on_active = False
        self.ids.my_button_B.md_bg_color = '#EDF2F4'
        self.ids.my_button_B.elevation = 3

    def set_answers_C(self, delay=6):
        self.ids.my_button_C.text = questions[self.question_number].options[2]
        self.ids.my_button_C.elevation = 3
        self.ids.my_button_C.on_active = False
        self.ids.my_button_C.md_bg_color = '#EDF2F4'
        self.ids.my_button_C.elevation = 3

    def set_answers_D(self, delay=7):
        self.ids.my_button_D.text = questions[self.question_number].options[3]
        self.ids.my_button_D.elevation = 3
        self.ids.my_button_D.on_active = False
        self.ids.my_button_D.md_bg_color = '#EDF2F4'
        self.ids.my_button_D.elevation = 3

    def set_answers_undisabled(self, delay=8):
        self.ids.my_button_D.disabled = False
        self.ids.my_button_A.disabled = False
        self.ids.my_button_B.disabled = False
        self.ids.my_button_C.disabled = False
    #######################################

        # Kérdés beállítása a képernyőre
    def set_scoreboard(self, delay = 3):
        self.ids.label_score.text = str(self.score)
        self.ids.sum_label_questions.text = str(self.wrong)
    #######################################

    # Gombnyomásra a kérdés helyességének eldöntése
    def make_decision(self, widget, text, delay, delay_button_color):
        # Ha helyes a válasz
        if text == questions[self.question_number].answer:
            # Új kérdések és válaszok betöltése
            global EVENT1
            EVENT1 = Clock.schedule_once(self.set_questions_blank, delay)
            global EVENT2
            EVENT2 =Clock.schedule_once(self.set_questions, delay + 1)
            global EVENT3
            EVENT3 =Clock.schedule_once(self.play_sound_question, delay + 1)
            global EVENT4
            EVENT4 =Clock.schedule_once(self.set_answers, delay)
            global EVENT5
            EVENT5 =Clock.schedule_once(self.set_quotes, delay)
            global EVENT6
            EVENT6 =Clock.schedule_once(self.set_answers_A, delay + 4)
            global EVENT7
            EVENT7 =Clock.schedule_once(self.play_sound_button, delay + 4)
            global EVENT8
            EVENT8 =Clock.schedule_once(self.set_answers_B, delay + 6)
            global EVENT9
            EVENT9 =Clock.schedule_once(self.play_sound_button, delay + 6)
            global EVENT10
            EVENT10 =Clock.schedule_once(self.set_answers_C, delay + 8)
            global EVENT11
            EVENT11 =Clock.schedule_once(self.play_sound_button, delay + 8)
            global EVENT12
            EVENT12 =Clock.schedule_once(self.set_answers_D, delay + 10)
            global EVENT13
            EVENT13 =Clock.schedule_once(self.play_sound_button, delay + 10)
            global EVENT14
            EVENT14 =Clock.schedule_once(self.set_answers_undisabled, delay + 11)

            self.score += 1
            self.answers_number += 1

            global EVENT15
            EVENT15 =Clock.schedule_once(self.set_scoreboard, delay_button_color + 4.0)
            global EVENT16
            EVENT16 =Clock.schedule_once(self.set_the_button_color_right, delay_button_color)
            global EVENT17
            EVENT17 =Clock.schedule_once(self.animate_the_right_button, delay_button_color + 0.5)
            global EVENT18
            EVENT18 =Clock.schedule_once(self.set_the_button_color_right, delay_button_color + 1.0)
            global EVENT19
            EVENT19 =Clock.schedule_once(self.animate_the_right_button, delay_button_color + 1.50)
            global EVENT20
            EVENT20 =Clock.schedule_once(self.set_the_button_color_right, delay_button_color + 2.0)
            global EVENT21
            EVENT21 =Clock.schedule_once(self.animate_the_right_button, delay_button_color + 2.50)
            global EVENT22
            EVENT22 =Clock.schedule_once(self.set_the_button_color_right, delay_button_color + 3.0)
            global EVENT23
            EVENT23 =Clock.schedule_once(self.play_sound_correct, 2.5)
            global EVENT62
            EVENT62 = Clock.schedule_once(self.set_the_pause_on, delay_button_color + 4.5)
            global EVENT64
            EVENT64 = Clock.schedule_once(self.set_the_pause_off, delay)

        # Ha nem helyes a válasz
        else:
            # Új kérdések és válaszok betöltése
            global EVENT24
            EVENT24 = Clock.schedule_once(self.set_questions_blank, delay)
            global EVENT25
            EVENT25 = Clock.schedule_once(self.set_questions, delay + 1)
            global EVENT26
            EVENT26 = Clock.schedule_once(self.play_sound_question, delay + 1)
            global EVENT27
            EVENT27 = Clock.schedule_once(self.set_answers, delay)
            global EVENT28
            EVENT28 = Clock.schedule_once(self.set_quotes, delay)
            global EVENT29
            EVENT29 = Clock.schedule_once(self.set_answers_A, delay + 4)
            global EVENT30
            EVENT30 = Clock.schedule_once(self.play_sound_button, delay + 4)
            global EVENT31
            EVENT31 = Clock.schedule_once(self.set_answers_B, delay + 6)
            global EVENT32
            EVENT32 = Clock.schedule_once(self.play_sound_button, delay + 6)
            global EVENT33
            EVENT33 = Clock.schedule_once(self.set_answers_C, delay + 8)
            global EVENT34
            EVENT34 = Clock.schedule_once(self.play_sound_button, delay + 8)
            global EVENT35
            EVENT35 = Clock.schedule_once(self.set_answers_D, delay + 10)
            global EVENT36
            EVENT36 = Clock.schedule_once(self.play_sound_button, delay + 10)
            global EVENT37
            EVENT37 = Clock.schedule_once(self.set_answers_undisabled, delay + 11)

            self.answers_number += 1
            self.wrong += 1

            global EVENT38
            EVENT38 = Clock.schedule_once(self.set_scoreboard, delay_button_color + 4.0)
            global EVENT39
            EVENT39 = Clock.schedule_once(self.set_the_button_color_right, delay_button_color)
            global EVENT40
            EVENT40 = Clock.schedule_once(self.animate_the_right_button, delay_button_color + 0.5)
            global EVENT41
            EVENT41 = Clock.schedule_once(self.set_the_button_color_right, delay_button_color + 1.0)
            global EVENT42
            EVENT42 = Clock.schedule_once(self.animate_the_right_button, delay_button_color + 1.50)
            global EVENT43
            EVENT43 = Clock.schedule_once(self.set_the_button_color_right, delay_button_color + 2.0)
            global EVENT44
            EVENT44 = Clock.schedule_once(self.animate_the_right_button, delay_button_color + 2.50)
            global EVENT45
            EVENT45 = Clock.schedule_once(self.set_the_button_color_right, delay_button_color + 3.0)
            global EVENT46
            EVENT46 = Clock.schedule_once(self.play_sound_wrong, 2.5)
            global EVENT63
            EVENT63 = Clock.schedule_once(self.set_the_pause_on, delay_button_color + 4.5)
            global EVENT65
            EVENT65 = Clock.schedule_once(self.set_the_pause_off, delay)

        global CHANGE_SCREEN
        CHANGE_SCREEN = False
    #######################################

    def set_the_button_color_right(self, widget):
        if self.ids.my_button_A.text == questions[self.question_number].answer:
            if self.ids.my_button_B.elevation == 5:
                self.ids.my_button_B.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_C.elevation == 5:
                self.ids.my_button_C.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_D.elevation == 5:
                self.ids.my_button_D.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
            self.ids.my_button_A.md_bg_color_disabled = '#50F263'
            self.ids.my_button_A.disabled_color = '#404040'

        if self.ids.my_button_B.text == questions[self.question_number].answer:
            if self.ids.my_button_A.elevation == 5:
                self.ids.my_button_A.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_C.elevation == 5:
                self.ids.my_button_C.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_D.elevation == 5:
                self.ids.my_button_D.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
            self.ids.my_button_B.md_bg_color_disabled = '#50F263'
            self.ids.my_button_B.disabled_color = '#404040'

        if self.ids.my_button_C.text == questions[self.question_number].answer:
            if self.ids.my_button_A.elevation == 5:
                self.ids.my_button_A.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_B.elevation == 5:
                self.ids.my_button_B.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_D.elevation == 5:
                self.ids.my_button_D.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
            self.ids.my_button_C.md_bg_color_disabled = '#50F263'
            self.ids.my_button_C.disabled_color = '#404040'

        if self.ids.my_button_D.text == questions[self.question_number].answer:
            if self.ids.my_button_A.elevation == 5:
                self.ids.my_button_A.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_B.elevation == 5:
                self.ids.my_button_B.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_C.elevation == 5:
                self.ids.my_button_C.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
            self.ids.my_button_D.md_bg_color_disabled = '#50F263'
            self.ids.my_button_D.disabled_color = '#404040'

    def animate_the_right_button(self, widget):
        if self.ids.my_button_A.text == questions[self.question_number].answer:
            if self.ids.my_button_A.elevation == 5:
                self.ids.my_button_A.md_bg_color_disabled = '#F25063'
            elif self.ids.my_button_B.elevation == 5:
                self.ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_C.elevation == 5:
                self.ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_D.elevation == 5:
                self.ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
        elif self.ids.my_button_B.text == questions[self.question_number].answer:
            if self.ids.my_button_B.elevation == 5:
                self.ids.my_button_B.md_bg_color_disabled = '#F25063'
            elif self.ids.my_button_A.elevation == 5:
                self.ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_C.elevation == 5:
                self.ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_D.elevation == 5:
                self.ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
        elif self.ids.my_button_C.text == questions[self.question_number].answer:
            if self.ids.my_button_C.elevation == 5:
                self.ids.my_button_C.md_bg_color_disabled = '#F25063'
            elif self.ids.my_button_B.elevation == 5:
                self.ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_A.elevation == 5:
                self.ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_D.elevation == 5:
                self.ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
        if self.ids.my_button_D.text == questions[self.question_number].answer:
            if self.ids.my_button_D.elevation == 5:
                self.ids.my_button_D.md_bg_color_disabled = '#F25063'
            elif self.ids.my_button_B.elevation == 5:
                self.ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_C.elevation == 5:
                self.ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_A.elevation == 5:
                self.ids.my_button_D.md_bg_color_disabled = '#EDF2F4'


    def play_sound_correct(self, delay=2.5):
        number = random.randint(1,6)
        if number == 1:
            sound = SoundLoader.load('correct01.ogg')
        if number == 2:
            sound = SoundLoader.load('correct02.ogg')
        if number == 3:
            sound = SoundLoader.load('correct03.ogg')
        if number == 4:
            sound = SoundLoader.load('correct04.ogg')
        if number == 5:
            sound = SoundLoader.load('correct05.ogg')
        if number == 6:
            sound = SoundLoader.load('correct06.ogg')
        if sound:
            sound.volume = 0.5 #from 0-1
            sound.play()

    def play_sound_wrong(self, delay=2.5):
        number = random.randint(1,8)
        if number == 1:
            sound = SoundLoader.load('wrong01.ogg')
        if number == 2:
            sound = SoundLoader.load('wrong02.ogg')
        if number == 3:
            sound = SoundLoader.load('wrong03.ogg')
        if number == 4:
            sound = SoundLoader.load('wrong04.ogg')
        if number == 5:
            sound = SoundLoader.load('wrong05.ogg')
        if number == 6:
            sound = SoundLoader.load('wrong06.ogg')
        if number == 7:
            sound = SoundLoader.load('wrong07.ogg')
        if number == 8:
            sound = SoundLoader.load('wrong08.ogg')
        if sound:
            sound.volume = 0.5 #from 0-1
            sound.play()

    def play_sound_button(self, delay=0):
        sound = SoundLoader.load('buttons01.ogg')
        if sound:
            sound.volume = 0.5
            sound.play()

    def play_sound_question(self, delay=2.5):
        number = random.randint(1,6)
        if number == 1:
            sound = SoundLoader.load('questions01.ogg')
        if number == 2:
            sound = SoundLoader.load('questions02.ogg')
        if number == 3:
            sound = SoundLoader.load('questions03.ogg')
        if number == 4:
            sound = SoundLoader.load('questions04.ogg')
        if number == 5:
            sound = SoundLoader.load('questions05.ogg')
        if number == 6:
            sound = SoundLoader.load('questions06.ogg')
        if sound:
            sound.volume = 0.3
            sound.play()

    def set_the_pause_on(self, widget):
        self.manager.get_screen("free_game_screen").ids.my_pause_freegame.disabled = False

    def set_the_pause_off(self, widget):
        self.manager.get_screen("free_game_screen").ids.my_pause_freegame.disabled = True

    def pause_freegame(self):
        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)

        self.manager.get_screen("free_game_screen").ids.my_pause_freegame.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_play_freegame.disabled = False

    def resume_freegame(self):
        self.manager.get_screen("free_game_screen").ids.my_pause_freegame.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_play_freegame.disabled = True

        self.manager.get_screen("free_game_screen").ids.label_question.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_B.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_C.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_D.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3

        number = random.randint(0, 39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("free_game_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("free_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("free_game_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("free_game_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("free_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("free_game_screen").ids.my_quote_author.text = quotes_authors[number]

        EVENT49 = Clock.schedule_once(self.set_questions, 1)
        EVENT50 = Clock.schedule_once(self.set_answers_A, 5)
        EVENT51 = Clock.schedule_once(self.set_answers_B, 7)
        EVENT52 = Clock.schedule_once(self.set_answers_C, 9)
        EVENT53 = Clock.schedule_once(self.set_answers_D, 11)
        EVENT54 = Clock.schedule_once(self.set_answers_undisabled, 12)
        EVENT55 = Clock.schedule_once(self.play_sound_question, 1)
        EVENT56 = Clock.schedule_once(self.play_sound_button, 5)
        EVENT57 = Clock.schedule_once(self.play_sound_button, 7)
        EVENT58 = Clock.schedule_once(self.play_sound_button, 9)
        EVENT59 = Clock.schedule_once(self.play_sound_button, 11)


class ChooseChapters(Screen):

    global background

    def set_the_background_music(self):
        global background
        if self.ids.my_icon_volume.icon == 'volume-mute':
            self.ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("free_game_screen").ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("chapter_game_screen").ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("main_menu_screen").ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("game_screen").ids.my_icon_volume.icon = 'volume-medium'

            background_randomize_number = random.randint(1, 3)
            if background_randomize_number == 1:
                background = SoundLoader.load('background01.ogg')
                background.volume = 0.2
                background.play()
                background.loop = True
            if background_randomize_number == 2:
                background = SoundLoader.load('background02.ogg')
                background.volume = 0.2
                background.play()
                background.loop = True
            if background_randomize_number == 3:
                background = SoundLoader.load('background03.ogg')
                background.volume = 0.2
                background.play()
                background.loop = True

        elif self.ids.my_icon_volume.icon == 'volume-medium':
            self.ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("free_game_screen").ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("chapter_game_screen").ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("main_menu_screen").ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("game_screen").ids.my_icon_volume.icon = 'volume-mute'
            background.unload()

    dialog = None

    def set_quotes(self):
        number = random.randint(0, 39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]

    def go_to_main_menu(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos vissza mész a főmenübe?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_main_menu
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_main_menu(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True

        # kattintás letiltások visszaállítása
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_1.disabled = False
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_2.disabled = False
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_3.disabled = False

        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_1.on_active = False
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_2.on_active = False
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_3.on_active = False

        # Go to the main menu
        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None

        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)


    def go_to_freegame(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos a szabad játékot választod?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_freegame
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_freegame(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True

        self.manager.get_screen("free_game_screen").ids.my_pause_freegame.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_play_freegame.disabled = True


        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None

        global WindowSizeWidth
        global WindowSizeHeight
        self.manager.get_screen("free_game_screen").ids.jvtrivia_icon_freegame.size_hint = (
        0.3, WindowSizeWidth / WindowSizeHeight * 0.3)
        self.manager.get_screen("free_game_screen").ids.jvtrivia_icon_freegame.keep_ratio = True
        self.manager.get_screen("free_game_screen").ids.jvtrivia_icon_freegame.pos_hint = {'x': 0, 'y': 0}

        # Alsó idézet beállítása
        self.set_quotes_free_game()

        # Scoreboard kinullázása
        self.set_scoreboard_freegame()

        # Gombok és kérdés clearing
        self.manager.get_screen("free_game_screen").ids.label_score.text = str(0)
        self.manager.get_screen("free_game_screen").ids.sum_label_questions.text = str(0)
        self.manager.get_screen("free_game_screen").ids.label_question.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_B.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_C.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_D.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3

        self.manager.get_screen("chapter_game_screen").ids.label_score_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.sum_label_questions_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3

        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)

        # belső változók kinullázása
        self.score = 0
        self.wrong = 0
        self.answers_number = 0
        self.question_number = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        # Első kérdés és válasz beállítása
        EVENT49 = Clock.schedule_once(self.set_questions_freegame, 6)
        EVENT50 = Clock.schedule_once(self.set_answers_A_freegame, 10)
        EVENT51 = Clock.schedule_once(self.set_answers_B_freegame, 12)
        EVENT52 = Clock.schedule_once(self.set_answers_C_freegame, 14)
        EVENT53 = Clock.schedule_once(self.set_answers_D_freegame, 16)
        EVENT54 = Clock.schedule_once(self.set_answers_undisabled_freegame, 17)
        EVENT55 = Clock.schedule_once(self.play_sound_question_freegame, 6)
        EVENT56 = Clock.schedule_once(self.play_sound_button_freegame, 10)
        EVENT57 = Clock.schedule_once(self.play_sound_button_freegame, 12)
        EVENT58 = Clock.schedule_once(self.play_sound_button_freegame, 14)
        EVENT59 = Clock.schedule_once(self.play_sound_button_freegame, 16)

        # Kérdés beállítása
    def set_quotes_free_game(self, delay=3):
        number = random.randint(0,39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("free_game_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("free_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("free_game_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("free_game_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("free_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("free_game_screen").ids.my_quote_author.text = quotes_authors[number]


    def set_quotes_chapter_game(self, delay=3):
        number = random.randint(0,39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("chapter_game_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("chapter_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("chapter_game_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("chapter_game_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("chapter_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("chapter_game_screen").ids.my_quote_author.text = quotes_authors[number]

    def set_questions_freegame(self, delay=3):
        self.randomize_questions()
        if len(questions[self.question_number].question) > 70:
            self.manager.get_screen("free_game_screen").ids.label_question.font_size = 14
            self.manager.get_screen("free_game_screen").ids.label_question.text = questions[
                self.question_number].question
        elif len(questions[self.question_number].question) > 140:
            self.manager.get_screen("free_game_screen").ids.label_question.font_size = 13
            self.manager.get_screen("free_game_screen").ids.label_question.text = questions[
                self.question_number].question
        else:
            self.manager.get_screen("free_game_screen").ids.label_question.font_size = 16
            self.manager.get_screen("free_game_screen").ids.label_question.text = questions[
                self.question_number].question

        # Kérdések véletlenszerű megkeverése

    def randomize_questions(self):
        random.shuffle(questions)
        #######################################

    def set_scoreboard_freegame(self):
        self.manager.get_screen("free_game_screen").ids.label_score.text = str(0)
        self.manager.get_screen("free_game_screen").ids.sum_label_questions.text = str(0)

    def set_answers_A_freegame(self, delay=4):
        A_length = int(len(questions[self.question_number].options[0]))
        B_length = int(len(questions[self.question_number].options[1]))
        C_length = int(len(questions[self.question_number].options[2]))
        D_length = int(len(questions[self.question_number].options[3]))
        length_list = [A_length, B_length, C_length, D_length]
        max_length = max(length_list)

        if max_length <= 25:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "14"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "14"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "14"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "14"
        if max_length > 25:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "13"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "13"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "13"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "13"

        if max_length > 35:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "12"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "12"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "12"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "12"
        if max_length > 55:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "11"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "11"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "11"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "11"
        if max_length > 65:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "10"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "10"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "10"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "10"
        if max_length > 85:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "9"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "9"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "9"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "9"

        self.manager.get_screen("free_game_screen").ids.my_button_A.text = questions[self.question_number].options[0]
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_A.on_active = False
        self.manager.get_screen("free_game_screen").ids.my_button_A.md_bg_color = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3

    def set_answers_B_freegame(self, delay=4):
        self.manager.get_screen("free_game_screen").ids.my_button_B.text = questions[self.question_number].options[1]
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_B.on_active = False
        self.manager.get_screen("free_game_screen").ids.my_button_B.md_bg_color = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3

    def set_answers_C_freegame(self, delay=4):
        self.manager.get_screen("free_game_screen").ids.my_button_C.text = questions[self.question_number].options[2]
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_C.on_active = False
        self.manager.get_screen("free_game_screen").ids.my_button_C.md_bg_color = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3

    def set_answers_D_freegame(self, delay=4):
        self.manager.get_screen("free_game_screen").ids.my_button_D.text = questions[self.question_number].options[3]
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_D.on_active = False
        self.manager.get_screen("free_game_screen").ids.my_button_D.md_bg_color = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3

    def set_answers_undisabled_freegame(self, delay=8):
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled = False
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled = False
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled = False
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled = False
        #######################################

    def play_sound_button_freegame(self, delay=0):
        sound = SoundLoader.load('buttons01.ogg')
        if sound:
            sound.volume = 0.5
            sound.play()

    def play_sound_question_freegame(self, delay=2.5):
        number = random.randint(1, 6)
        if number == 1:
            sound = SoundLoader.load('questions01.ogg')
        if number == 2:
            sound = SoundLoader.load('questions02.ogg')
        if number == 3:
            sound = SoundLoader.load('questions03.ogg')
        if number == 4:
            sound = SoundLoader.load('questions04.ogg')
        if number == 5:
            sound = SoundLoader.load('questions05.ogg')
        if number == 6:
            sound = SoundLoader.load('questions06.ogg')
        if sound:
            sound.volume = 0.3
            sound.play()


    def go_to_chaptergame(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos a tematikus gyakorlást választod?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_chaptergame
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_chaptergame(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True

        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None

        # Alsó idézet beállítása
        number = random.randint(0, 39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]

        global WindowSizeWidth
        global WindowSizeHeight
        self.manager.get_screen("choose_chapters_screen").ids.jvtrivia_icon_choosechapters.size_hint = (
            0.3, WindowSizeWidth / WindowSizeHeight * 0.3)
        self.manager.get_screen("choose_chapters_screen").ids.jvtrivia_icon_choosechapters.keep_ratio = True
        self.manager.get_screen("choose_chapters_screen").ids.jvtrivia_icon_choosechapters.pos_hint = {'x': 0, 'y': 0}



    def go_to_gamescreen(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos vizsgázni szeretnél?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_gamescreen
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_gamescreen(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        self.manager.get_screen("game_screen").ids.pause_gamescreen.disabled = True
        self.manager.get_screen("game_screen").ids.play_gamescreen.disabled = True
        # belső változók kinullázása
        self.score = 0
        self.wrong = 0
        self.answers_number = 0
        self.question_number = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None

        global WindowSizeWidth
        global WindowSizeHeight
        self.manager.get_screen("game_screen").ids.jvtrivia_icon_gamescreen.size_hint = (
            0.3, WindowSizeWidth / WindowSizeHeight * 0.3)
        self.manager.get_screen("game_screen").ids.jvtrivia_icon_gamescreen.keep_ratio = True
        self.manager.get_screen("game_screen").ids.jvtrivia_icon_gamescreen.pos_hint = {'x': 0, 'y': 0}

        # Alsó idézet beállítása
        self.set_quotes_gamescreen()

        # Scoreboard kinullázása
        self.set_scoreboard_gamescreen()

        # Gombok és kérdés clearing
        self.manager.get_screen("free_game_screen").ids.label_score.text = str(0)
        self.manager.get_screen("free_game_screen").ids.sum_label_questions.text = str(0)
        self.manager.get_screen("free_game_screen").ids.label_question.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_B.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_C.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_D.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3

        self.manager.get_screen("chapter_game_screen").ids.label_score_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.sum_label_questions_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3

        self.manager.get_screen("game_screen").ids.label_score_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.sum_label_questions_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = ""
        self.manager.get_screen("game_screen").ids.my_button_AAA.text = ""
        self.manager.get_screen("game_screen").ids.my_button_BBB.text = ""
        self.manager.get_screen("game_screen").ids.my_button_CCC.text = ""
        self.manager.get_screen("game_screen").ids.my_button_DDD.text = ""
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_AAA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_BBB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_CCC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_DDD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_AAA.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_BBB.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_CCC.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_DDD.elevation = 3

        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)

        # Első kérdés és válasz beállítása
        EVENT49 = Clock.schedule_once(self.set_questions_gamescreen, 6)
        EVENT50 = Clock.schedule_once(self.set_answers_A_gamescreen, 10)
        EVENT51 = Clock.schedule_once(self.set_answers_B_gamescreen, 12)
        EVENT52 = Clock.schedule_once(self.set_answers_C_gamescreen, 14)
        EVENT53 = Clock.schedule_once(self.set_answers_D_gamescreen, 16)
        EVENT54 = Clock.schedule_once(self.set_answers_undisabled_gamescreen, 17)
        EVENT55 = Clock.schedule_once(self.play_sound_question_gamescreen, 6)
        EVENT56 = Clock.schedule_once(self.play_sound_button_gamescreen, 10)
        EVENT57 = Clock.schedule_once(self.play_sound_button_gamescreen, 12)
        EVENT58 = Clock.schedule_once(self.play_sound_button_gamescreen, 14)
        EVENT59 = Clock.schedule_once(self.play_sound_button_gamescreen, 16)

    def play_sound_button_gamescreen(self, delay=0):
        sound = SoundLoader.load('buttons01.ogg')
        if sound:
            sound.volume = 0.5
            sound.play()

    def play_sound_question_gamescreen(self, delay=2.5):
        number = random.randint(1, 6)
        if number == 1:
            sound = SoundLoader.load('questions01.ogg')
        if number == 2:
            sound = SoundLoader.load('questions02.ogg')
        if number == 3:
            sound = SoundLoader.load('questions03.ogg')
        if number == 4:
            sound = SoundLoader.load('questions04.ogg')
        if number == 5:
            sound = SoundLoader.load('questions05.ogg')
        if number == 6:
            sound = SoundLoader.load('questions06.ogg')
        if sound:
            sound.volume = 0.3
            sound.play()

    def set_answers_A_gamescreen(self, delay=4):
        A_length = int(len(questions[self.question_number].options[0]))
        B_length = int(len(questions[self.question_number].options[1]))
        C_length = int(len(questions[self.question_number].options[2]))
        D_length = int(len(questions[self.question_number].options[3]))
        length_list = [A_length, B_length, C_length, D_length]
        max_length = max(length_list)

        if max_length <= 25:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "14"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "14"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "14"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "14"
        if max_length > 25:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "13"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "13"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "13"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "13"

        if max_length > 35:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "12"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "12"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "12"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "12"
        if max_length > 55:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "11"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "11"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "11"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "11"
        if max_length > 65:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "10"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "10"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "10"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "10"
        if max_length > 85:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "9"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "9"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "9"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "9"

        self.manager.get_screen("game_screen").ids.my_button_AAA.text = questions[self.question_number].options[0]
        self.manager.get_screen("game_screen").ids.my_button_AAA.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_AAA.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_AAA.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_AAA.elevation = 3

    def set_answers_B_gamescreen(self, delay=5):
        self.manager.get_screen("game_screen").ids.my_button_BBB.text = questions[self.question_number].options[1]
        self.manager.get_screen("game_screen").ids.my_button_BBB.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_BBB.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_BBB.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_BBB.elevation = 3

    def set_answers_C_gamescreen(self, delay=6):
        self.manager.get_screen("game_screen").ids.my_button_CCC.text = questions[self.question_number].options[2]
        self.manager.get_screen("game_screen").ids.my_button_CCC.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_CCC.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_CCC.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_CCC.elevation = 3

    def set_answers_D_gamescreen(self, delay=7):
        self.manager.get_screen("game_screen").ids.my_button_DDD.text = questions[self.question_number].options[3]
        self.manager.get_screen("game_screen").ids.my_button_DDD.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_DDD.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_DDD.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_DDD.elevation = 3

    def set_answers_undisabled_gamescreen(self, delay=8):
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled = False
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled = False
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled = False
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled = False

        # Kérdés beállítása

    def set_questions_gamescreen(self, delay=3):
        self.randomize_questions()
        if len(questions[self.question_number].question) > 70:
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 14
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[
                self.question_number].question
        elif len(questions[self.question_number].question) > 140:
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 13
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[
                self.question_number].question
        else:
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 16
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[
                self.question_number].question
        ######################################

    def set_scoreboard_gamescreen(self):
        self.manager.get_screen("game_screen").ids.label_score_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.sum_label_questions_gamescreen.text = str(0)

    def set_quotes_gamescreen(self, delay=3):
        number = random.randint(0, 39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("game_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("game_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("game_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("game_screen").ids.my_quote_author.text = quotes_authors[number]


    def go_to_the_exit(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None

    # Click cancel button
    def close_dialog(self, obj):
        # Close alert box
        self.dialog.dismiss(force=True)
        self.dialog = None


    def update_questions(self, number):
        selected_chapter = number
        i = 0
        while i < len(questions):
            if questions[i].chapter == selected_chapter:
                new_questions.append(questions[i])
            i = i + 1

    def clearing(self):

        global WindowSizeWidth
        global WindowSizeHeight
        self.manager.get_screen("chapter_game_screen").ids.jvtrivia_icon_chaptergame.size_hint = (
            0.3, WindowSizeWidth / WindowSizeHeight * 0.3)
        self.manager.get_screen("chapter_game_screen").ids.jvtrivia_icon_chaptergame.keep_ratio = True
        self.manager.get_screen("chapter_game_screen").ids.jvtrivia_icon_chaptergame.pos_hint = {'x': 0, 'y': 0}

        self.manager.get_screen("chapter_game_screen").ids.label_score_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.sum_label_questions_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3

        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)

        EVENT49 = Clock.schedule_once(self.set_questions_chaptergame, 6)
        EVENT50 = Clock.schedule_once(self.set_answers_A_chaptergame, 10)
        EVENT51 = Clock.schedule_once(self.set_answers_B_chaptergame, 12)
        EVENT52 = Clock.schedule_once(self.set_answers_C_chaptergame, 14)
        EVENT53 = Clock.schedule_once(self.set_answers_D_chaptergame, 16)
        EVENT54 = Clock.schedule_once(self.set_answers_undisabled_chaptergame, 17)
        EVENT55 = Clock.schedule_once(self.play_sound_question_chaptergame, 6)
        EVENT56 = Clock.schedule_once(self.play_sound_button_chaptergame, 10)
        EVENT57 = Clock.schedule_once(self.play_sound_button_chaptergame, 12)
        EVENT58 = Clock.schedule_once(self.play_sound_button_chaptergame, 14)
        EVENT59 = Clock.schedule_once(self.play_sound_button_chaptergame, 16)

    def set_answers_A_chaptergame(self, delay=4):
        A_length = int(len(new_questions[0].options[0]))
        B_length = int(len(new_questions[0].options[1]))
        C_length = int(len(new_questions[0].options[2]))
        D_length = int(len(new_questions[0].options[3]))
        length_list = [A_length, B_length, C_length, D_length]
        max_length = max(length_list)

        if max_length <= 25:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "14"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "14"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "14"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "14"
        if max_length > 25:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "13"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "13"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "13"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "13"

        if max_length > 35:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "12"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "12"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "12"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "12"
        if max_length > 45:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "11"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "11"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "11"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "11"
        if max_length > 65:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "10"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "10"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "10"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "10"
        if max_length > 85:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "9"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "9"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "9"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "9"

        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.text = new_questions[0].options[0]
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.on_active = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.md_bg_color = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3

    def set_answers_B_chaptergame(self, delay=4):
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.text = new_questions[0].options[1]
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.on_active = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.md_bg_color = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3

    def set_answers_C_chaptergame(self, delay=4):
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.text = new_questions[0].options[2]
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.on_active = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.md_bg_color = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3

    def set_answers_D_chaptergame(self, delay=4):
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.text = new_questions[0].options[3]
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.on_active = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.md_bg_color = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3

    def set_answers_undisabled_chaptergame(self, delay=8):
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled = False
        #######################################

    def play_sound_button_chaptergame(self, delay=0):
        sound = SoundLoader.load('buttons01.ogg')
        if sound:
            sound.volume = 0.5
            sound.play()

    def play_sound_question_chaptergame(self, delay=2.5):
        number = random.randint(1, 6)
        if number == 1:
            sound = SoundLoader.load('questions01.ogg')
        if number == 2:
            sound = SoundLoader.load('questions02.ogg')
        if number == 3:
            sound = SoundLoader.load('questions03.ogg')
        if number == 4:
            sound = SoundLoader.load('questions04.ogg')
        if number == 5:
            sound = SoundLoader.load('questions05.ogg')
        if number == 6:
            sound = SoundLoader.load('questions06.ogg')
        if sound:
            sound.volume = 0.3
            sound.play()

    def set_questions_chaptergame(self, delay=3):
        self.randomize_questions()

        if len(questions[0].question) > 70:
            self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.font_size = 14
            self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = new_questions[
                0].question
        elif len(questions[0].question) > 140:
            self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.font_size = 13
            self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = new_questions[
                0].question
        else:
            self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.font_size = 16
            self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = new_questions[
                0].question







class ChapterGameScreen(Screen):
    global background

    def set_the_background_music(self):
        global background
        if self.ids.my_icon_volume.icon == 'volume-mute':
            self.ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("free_game_screen").ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("main_menu_screen").ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("choose_chapters_screen").ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("game_screen").ids.my_icon_volume.icon = 'volume-medium'

            background_randomize_number = random.randint(1, 3)
            if background_randomize_number == 1:
                background = SoundLoader.load('background01.ogg')
                background.volume = 0.2
                background.play()
                background.loop = True
            if background_randomize_number == 2:
                background = SoundLoader.load('background02.ogg')
                background.volume = 0.2
                background.play()
                background.loop = True
            if background_randomize_number == 3:
                background = SoundLoader.load('background03.ogg')
                background.volume = 0.2
                background.play()
                background.loop = True

        elif self.ids.my_icon_volume.icon == 'volume-medium':
            self.ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("free_game_screen").ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("main_menu_screen").ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("choose_chapters_screen").ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("game_screen").ids.my_icon_volume.icon = 'volume-mute'
            background.unload()

    dialog = None

    def go_to_main_menu(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos vissza mész a főmenübe?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_main_menu
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_main_menu(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True

        # belső változók kinullázása
        self.score = 0
        self.wrong = 0
        self.answers_number = 0
        self.question_number = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        # kattintás letiltások visszaállítása
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_1.disabled = False
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_2.disabled = False
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_3.disabled = False

        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_1.on_active = False
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_2.on_active = False
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_3.on_active = False

        # Gombok és kérdés clearing
        self.manager.get_screen("free_game_screen").ids.label_score.text = str(0)
        self.manager.get_screen("free_game_screen").ids.sum_label_questions.text = str(0)
        self.manager.get_screen("free_game_screen").ids.label_question.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_B.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_C.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_D.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3

        self.manager.get_screen("chapter_game_screen").ids.label_score_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.sum_label_questions_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3

        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)

        # Go to the main menu
        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None


    def go_to_freegame(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos a szabad játékot választod?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_freegame
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_freegame(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        self.manager.get_screen("free_game_screen").ids.my_pause_freegame.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_play_freegame.disabled = True
        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None

        global WindowSizeWidth
        global WindowSizeHeight
        self.manager.get_screen("free_game_screen").ids.jvtrivia_icon_freegame.size_hint = (
        0.3, WindowSizeWidth / WindowSizeHeight * 0.3)
        self.manager.get_screen("free_game_screen").ids.jvtrivia_icon_freegame.keep_ratio = True
        self.manager.get_screen("free_game_screen").ids.jvtrivia_icon_freegame.pos_hint = {'x': 0, 'y': 0}

        # Alsó idézet beállítása
        self.set_quotes_free_game()

        # Scoreboard kinullázása
        self.set_scoreboard_freegame()

        # Gombok és kérdés clearing
        self.manager.get_screen("free_game_screen").ids.label_score.text = str(0)
        self.manager.get_screen("free_game_screen").ids.sum_label_questions.text = str(0)
        self.manager.get_screen("free_game_screen").ids.label_question.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_B.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_C.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_D.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3

        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)


        # belső változók kinullázása
        self.score = 0
        self.wrong = 0
        self.answers_number = 0
        self.question_number = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        # Első kérdés és válasz beállítása
        EVENT49 = Clock.schedule_once(self.set_questions_freegame, 6)
        EVENT50 = Clock.schedule_once(self.set_answers_A_freegame, 10)
        EVENT51 = Clock.schedule_once(self.set_answers_B_freegame, 12)
        EVENT52 = Clock.schedule_once(self.set_answers_C_freegame, 14)
        EVENT53 = Clock.schedule_once(self.set_answers_D_freegame, 16)
        EVENT54 = Clock.schedule_once(self.set_answers_undisabled_freegame, 17)
        EVENT55 = Clock.schedule_once(self.play_sound_question_freegame, 6)
        EVENT56 = Clock.schedule_once(self.play_sound_button_freegame, 10)
        EVENT57 = Clock.schedule_once(self.play_sound_button_freegame, 12)
        EVENT58 = Clock.schedule_once(self.play_sound_button_freegame, 14)
        EVENT59 = Clock.schedule_once(self.play_sound_button_freegame, 16)

    def set_quotes_free_game(self, delay=3):
        number = random.randint(0,39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("free_game_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("free_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("free_game_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("free_game_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("free_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("free_game_screen").ids.my_quote_author.text = quotes_authors[number]

    def set_quotes_free_game(self, delay=3):
        number = random.randint(0,39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("free_game_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("free_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("free_game_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("free_game_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("free_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("free_game_screen").ids.my_quote_author.text = quotes_authors[number]


    def set_quotes_chapter_game(self, delay=3):
        number = random.randint(0,39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("chapter_game_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("chapter_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("chapter_game_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("chapter_game_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("chapter_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("chapter_game_screen").ids.my_quote_author.text = quotes_authors[number]

    def set_questions_freegame(self, delay=3):
        self.randomize_questions()
        if len(questions[self.question_number].question) > 70:
            self.manager.get_screen("free_game_screen").ids.label_question.font_size = 14
            self.manager.get_screen("free_game_screen").ids.label_question.text = questions[
                self.question_number].question
        elif len(questions[self.question_number].question) > 140:
            self.manager.get_screen("free_game_screen").ids.label_question.font_size = 13
            self.manager.get_screen("free_game_screen").ids.label_question.text = questions[
                self.question_number].question
        else:
            self.manager.get_screen("free_game_screen").ids.label_question.font_size = 16
            self.manager.get_screen("free_game_screen").ids.label_question.text = questions[
                self.question_number].question

    def set_questions_chaptergame(self, delay=3):
        self.randomize_questions()
        if len(questions[self.question_number].question) > 70:
            self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.font_size = 14
            self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = new_questions[
                self.question_number].question
        elif len(questions[self.question_number].question) > 140:
            self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.font_size = 13
            self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = new_questions[
                self.question_number].question
        else:
            self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.font_size = 16
            self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = new_questions[
                self.question_number].question
        ######################################

        # Kérdések véletlenszerű megkeverése

    def randomize_questions(self):
        random.shuffle(new_questions)
        #######################################

    def set_scoreboard_freegame(self):
        self.manager.get_screen("free_game_screen").ids.label_score.text = str(0)
        self.manager.get_screen("free_game_screen").ids.sum_label_questions.text = str(0)

    def set_scoreboard_chaptergame(self):
        self.manager.get_screen("chapter_game_screen").ids.label_score_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.sum_label_questions_chaptergame.text = str(0)

    def set_answers_A_chaptergame(self, delay=4):
        A_length = int(len(new_questions[self.question_number].options[0]))
        B_length = int(len(new_questions[self.question_number].options[1]))
        C_length = int(len(new_questions[self.question_number].options[2]))
        D_length = int(len(new_questions[self.question_number].options[3]))
        length_list = [A_length, B_length, C_length, D_length]
        max_length = max(length_list)

        if max_length <= 25:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "14"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "14"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "14"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "14"
        if max_length > 25:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "13"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "13"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "13"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "13"

        if max_length > 35:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "12"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "12"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "12"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "12"
        if max_length > 45:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "11"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "11"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "11"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "11"
        if max_length > 65:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "10"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "10"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "10"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "10"
        if max_length > 85:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "9"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "9"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "9"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "9"

        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.text = new_questions[self.question_number].options[0]
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.on_active = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.md_bg_color = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3

    def set_answers_B_chaptergame(self, delay=4):
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.text = new_questions[self.question_number].options[1]
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.on_active = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.md_bg_color = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3

    def set_answers_C_chaptergame(self, delay=4):
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.text = new_questions[self.question_number].options[2]
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.on_active = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.md_bg_color = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3

    def set_answers_D_chaptergame(self, delay=4):
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.text = new_questions[self.question_number].options[3]
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.on_active = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.md_bg_color = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3

    def set_answers_undisabled_chaptergame(self, delay=8):
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled = False
        #######################################

    def set_answers_A_freegame(self, delay=4):
        A_length = int(len(questions[self.question_number].options[0]))
        B_length = int(len(questions[self.question_number].options[1]))
        C_length = int(len(questions[self.question_number].options[2]))
        D_length = int(len(questions[self.question_number].options[3]))
        length_list = [A_length, B_length, C_length, D_length]
        max_length = max(length_list)

        if max_length <= 25:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "14"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "14"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "14"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "14"
        if max_length > 25:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "13"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "13"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "13"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "13"

        if max_length > 35:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "12"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "12"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "12"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "12"
        if max_length > 55:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "11"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "11"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "11"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "11"
        if max_length > 65:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "10"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "10"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "10"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "10"
        if max_length > 85:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "9"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "9"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "9"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "9"

        self.manager.get_screen("free_game_screen").ids.my_button_A.text = questions[self.question_number].options[0]
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_A.on_active = False
        self.manager.get_screen("free_game_screen").ids.my_button_A.md_bg_color = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3

    def set_answers_B_freegame(self, delay=4):
        self.manager.get_screen("free_game_screen").ids.my_button_B.text = questions[self.question_number].options[1]
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_B.on_active = False
        self.manager.get_screen("free_game_screen").ids.my_button_B.md_bg_color = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3

    def set_answers_C_freegame(self, delay=4):
        self.manager.get_screen("free_game_screen").ids.my_button_C.text = questions[self.question_number].options[2]
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_C.on_active = False
        self.manager.get_screen("free_game_screen").ids.my_button_C.md_bg_color = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3

    def set_answers_D_freegame(self, delay=4):
        self.manager.get_screen("free_game_screen").ids.my_button_D.text = questions[self.question_number].options[3]
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_D.on_active = False
        self.manager.get_screen("free_game_screen").ids.my_button_D.md_bg_color = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3

    def set_answers_undisabled_freegame(self, delay=8):
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled = False
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled = False
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled = False
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled = False

    def play_sound_button_chaptergame(self, delay=0):
        sound = SoundLoader.load('buttons01.ogg')
        if sound:
            sound.volume = 0.5
            sound.play()

    def play_sound_question_chaptergame(self, delay=2.5):
        number = random.randint(1, 6)
        if number == 1:
            sound = SoundLoader.load('questions01.ogg')
        if number == 2:
            sound = SoundLoader.load('questions02.ogg')
        if number == 3:
            sound = SoundLoader.load('questions03.ogg')
        if number == 4:
            sound = SoundLoader.load('questions04.ogg')
        if number == 5:
            sound = SoundLoader.load('questions05.ogg')
        if number == 6:
            sound = SoundLoader.load('questions06.ogg')
        if sound:
            sound.volume = 0.3
            sound.play()

    def play_sound_button_freegame(self, delay=0):
        sound = SoundLoader.load('buttons01.ogg')
        if sound:
            sound.volume = 0.5
            sound.play()

    def play_sound_question_freegame(self, delay=2.5):
        number = random.randint(1, 6)
        if number == 1:
            sound = SoundLoader.load('questions01.ogg')
        if number == 2:
            sound = SoundLoader.load('questions02.ogg')
        if number == 3:
            sound = SoundLoader.load('questions03.ogg')
        if number == 4:
            sound = SoundLoader.load('questions04.ogg')
        if number == 5:
            sound = SoundLoader.load('questions05.ogg')
        if number == 6:
            sound = SoundLoader.load('questions06.ogg')
        if sound:
            sound.volume = 0.3
            sound.play()


    def go_to_chaptergame(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos a tematikus gyakorlást választod?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_chaptergame
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_chaptergame(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        self.manager.get_screen("chapter_game_screen").ids.my_pause_chaptergame.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_play_chaptergame.disabled = True
        # belső változók kinullázása
        self.score = 0
        self.wrong = 0
        self.answers_number = 0
        self.question_number = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None

        global WindowSizeWidth
        global WindowSizeHeight
        self.manager.get_screen("choose_chapters_screen").ids.jvtrivia_icon_choosechapters.size_hint = (
            0.3, WindowSizeWidth / WindowSizeHeight * 0.3)
        self.manager.get_screen("choose_chapters_screen").ids.jvtrivia_icon_choosechapters.keep_ratio = True
        self.manager.get_screen("choose_chapters_screen").ids.jvtrivia_icon_choosechapters.pos_hint = {'x': 0, 'y': 0}

        # Alsó idézet beállítása
        number = random.randint(0, 39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]

        # Gombok és kérdés clearing
        self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3

        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)

        self.set_quotes_choose_chapter_game()

    def set_quotes_choose_chapter_game(self):
        number = random.randint(0, 39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]


    def go_to_gamescreen(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos vizsgázni szeretnél?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_gamescreen
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_gamescreen(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        self.manager.get_screen("game_screen").ids.pause_gamescreen.disabled = True
        self.manager.get_screen("game_screen").ids.play_gamescreen.disabled = True
        # belső változók kinullázása
        self.score = 0
        self.wrong = 0
        self.answers_number = 0
        self.question_number = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None

        global WindowSizeWidth
        global WindowSizeHeight
        self.manager.get_screen("game_screen").ids.jvtrivia_icon_gamescreen.size_hint = (
            0.3, WindowSizeWidth / WindowSizeHeight * 0.3)
        self.manager.get_screen("game_screen").ids.jvtrivia_icon_gamescreen.keep_ratio = True
        self.manager.get_screen("game_screen").ids.jvtrivia_icon_gamescreen.pos_hint = {'x': 0, 'y': 0}

        # Alsó idézet beállítása
        self.set_quotes_gamescreen()

        # Scoreboard kinullázása
        self.set_scoreboard_gamescreen()

        # Gombok és kérdés clearing
        self.manager.get_screen("free_game_screen").ids.label_score.text = str(0)
        self.manager.get_screen("free_game_screen").ids.sum_label_questions.text = str(0)
        self.manager.get_screen("free_game_screen").ids.label_question.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_B.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_C.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_D.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3

        self.manager.get_screen("chapter_game_screen").ids.label_score_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.sum_label_questions_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3

        self.manager.get_screen("game_screen").ids.label_score_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.sum_label_questions_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = ""
        self.manager.get_screen("game_screen").ids.my_button_AAA.text = ""
        self.manager.get_screen("game_screen").ids.my_button_BBB.text = ""
        self.manager.get_screen("game_screen").ids.my_button_CCC.text = ""
        self.manager.get_screen("game_screen").ids.my_button_DDD.text = ""
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_AAA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_BBB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_CCC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_DDD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_AAA.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_BBB.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_CCC.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_DDD.elevation = 3

        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)

        # Első kérdés és válasz beállítása
        EVENT49 = Clock.schedule_once(self.set_questions_gamescreen, 6)
        EVENT50 = Clock.schedule_once(self.set_answers_A_gamescreen, 10)
        EVENT51 = Clock.schedule_once(self.set_answers_B_gamescreen, 12)
        EVENT52 = Clock.schedule_once(self.set_answers_C_gamescreen, 14)
        EVENT53 = Clock.schedule_once(self.set_answers_D_gamescreen, 16)
        EVENT54 = Clock.schedule_once(self.set_answers_undisabled_gamescreen, 17)
        EVENT55 = Clock.schedule_once(self.play_sound_question_gamescreen, 6)
        EVENT56 = Clock.schedule_once(self.play_sound_button_gamescreen, 10)
        EVENT57 = Clock.schedule_once(self.play_sound_button_gamescreen, 12)
        EVENT58 = Clock.schedule_once(self.play_sound_button_gamescreen, 14)
        EVENT59 = Clock.schedule_once(self.play_sound_button_gamescreen, 16)

    def play_sound_button_gamescreen(self, delay=0):
        sound = SoundLoader.load('buttons01.ogg')
        if sound:
            sound.volume = 0.5
            sound.play()

    def play_sound_question_gamescreen(self, delay=2.5):
        number = random.randint(1, 6)
        if number == 1:
            sound = SoundLoader.load('questions01.ogg')
        if number == 2:
            sound = SoundLoader.load('questions02.ogg')
        if number == 3:
            sound = SoundLoader.load('questions03.ogg')
        if number == 4:
            sound = SoundLoader.load('questions04.ogg')
        if number == 5:
            sound = SoundLoader.load('questions05.ogg')
        if number == 6:
            sound = SoundLoader.load('questions06.ogg')
        if sound:
            sound.volume = 0.3
            sound.play()

    def set_answers_A_gamescreen(self, delay=4):
        A_length = int(len(questions[self.question_number].options[0]))
        B_length = int(len(questions[self.question_number].options[1]))
        C_length = int(len(questions[self.question_number].options[2]))
        D_length = int(len(questions[self.question_number].options[3]))
        length_list = [A_length, B_length, C_length, D_length]
        max_length = max(length_list)

        if max_length <= 25:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "14"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "14"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "14"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "14"
        if max_length > 25:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "13"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "13"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "13"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "13"

        if max_length > 35:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "12"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "12"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "12"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "12"
        if max_length > 55:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "11"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "11"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "11"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "11"
        if max_length > 65:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "10"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "10"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "10"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "10"
        if max_length > 85:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "9"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "9"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "9"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "9"

        self.manager.get_screen("game_screen").ids.my_button_AAA.text = questions[self.question_number].options[0]
        self.manager.get_screen("game_screen").ids.my_button_AAA.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_AAA.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_AAA.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_AAA.elevation = 3

    def set_answers_B_gamescreen(self, delay=5):
        self.manager.get_screen("game_screen").ids.my_button_BBB.text = questions[self.question_number].options[1]
        self.manager.get_screen("game_screen").ids.my_button_BBB.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_BBB.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_BBB.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_BBB.elevation = 3

    def set_answers_C_gamescreen(self, delay=6):
        self.manager.get_screen("game_screen").ids.my_button_CCC.text = questions[self.question_number].options[2]
        self.manager.get_screen("game_screen").ids.my_button_CCC.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_CCC.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_CCC.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_CCC.elevation = 3

    def set_answers_D_gamescreen(self, delay=7):
        self.manager.get_screen("game_screen").ids.my_button_DDD.text = questions[self.question_number].options[3]
        self.manager.get_screen("game_screen").ids.my_button_DDD.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_DDD.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_DDD.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_DDD.elevation = 3

    def set_answers_undisabled_gamescreen(self, delay=8):
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled = False
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled = False
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled = False
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled = False

        # Kérdés beállítása

    def set_questions_gamescreen(self, delay=3):
        self.randomize_questions()
        if len(questions[self.question_number].question) > 70:
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 14
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[self.question_number].question
        elif len(questions[self.question_number].question) > 140:
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 13
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[self.question_number].question
        else:
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 16
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[self.question_number].question
        ######################################

    def set_scoreboard_gamescreen(self):
        self.manager.get_screen("game_screen").ids.label_score_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.sum_label_questions_gamescreen.text = str(0)

    def set_quotes_gamescreen(self, delay=3):
        number = random.randint(0, 39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("game_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("game_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("game_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("game_screen").ids.my_quote_author.text = quotes_authors[number]


    def go_to_exit(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos kilépsz a JVTriviából?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_exit
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_exit(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        # belső változók kinullázása
        self.score = 0
        self.wrong = 0
        self.answers_number = 0
        self.question_number = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None

    # Click cancel button
    def close_dialog(self, obj):
        # Close alert box
        self.dialog.dismiss(force=True)
        self.dialog = None

    score = 0
    wrong = 0
    answers_number = 0
    question_number = 0


    # GameScreen képernyő inicializálása
    def on_pre_enter(self, *args):
        self.set_scoreboard()
        global CHANGE_SCREEN
        CHANGE_SCREEN = False
    ####################################

    # Kérdések véletlenszerű megkeverése
    def randomize_questions(self):
        global new_questions
        if new_questions == []:
            new_questions = questions.copy()
        random.shuffle(new_questions)
    #######################################

    def set_quotes(self, delay=3):
        number = random.randint(0, 39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("chapter_game_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("chapter_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("chapter_game_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("chapter_game_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("chapter_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("chapter_game_screen").ids.my_quote_author.text = quotes_authors[number]

    # Kérdés beállítása
    def set_questions(self, delay = 3):
        if self.question_number >= len(new_questions) - 1:
            self.randomize_questions()
            self.question_number = 0
            if len(questions[self.question_number].question) > 70:
                self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.font_size = 14
                self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = new_questions[
                    self.question_number].question
            elif len(questions[self.question_number].question) > 140:
                self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.font_size = 13
                self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = new_questions[
                    self.question_number].question
            else:
                self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.font_size = 16
                self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = new_questions[
                    self.question_number].question
        else:
            self.question_number += 1
            if len(questions[self.question_number].question) > 70:
                self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.font_size = 14
                self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = new_questions[
                    self.question_number].question
            elif len(questions[self.question_number].question) > 140:
                self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.font_size = 13
                self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = new_questions[
                    self.question_number].question
            else:
                self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.font_size = 16
                self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = new_questions[
                    self.question_number].question
    ######################################

    # Üres kérdés beállítása 1 mp nyerése
    def set_questions_blank(self, delay=2):
        self.ids.label_question_chaptergame.text = ""

    # Válaszok beállítása a gombokra véletlenszerűen
    def set_answers(self, delay = 3):
        # Válaszok szövegének beállítása
        self.ids.my_button_AA.text = ""
        self.ids.my_button_BB.text = ""
        self.ids.my_button_CC.text = ""
        self.ids.my_button_DD.text = ""
        self.ids.my_button_AA.disabled_color = '#404040'
        self.ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
        self.ids.my_button_BB.disabled_color = '#404040'
        self.ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
        self.ids.my_button_CC.disabled_color = '#404040'
        self.ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
        self.ids.my_button_DD.disabled_color = '#404040'
        self.ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
        random.shuffle(new_questions[self.question_number].options)

    def set_answers_AA(self, delay=4):
        A_length = int(len(new_questions[self.question_number].options[0]))
        B_length = int(len(new_questions[self.question_number].options[1]))
        C_length = int(len(new_questions[self.question_number].options[2]))
        D_length = int(len(new_questions[self.question_number].options[3]))
        length_list = [A_length, B_length, C_length, D_length]
        max_length = max(length_list)

        if max_length <= 25:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "14"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "14"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "14"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "14"
        if max_length > 25:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "13"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "13"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "13"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "13"

        if max_length > 35:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "12"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "12"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "12"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "12"
        if max_length > 45:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "11"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "11"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "11"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "11"
        if max_length > 65:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "10"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "10"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "10"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "10"
        if max_length > 85:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "9"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "9"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "9"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "9"

        self.ids.my_button_AA.text = new_questions[self.question_number].options[0]
        self.ids.my_button_AA.elevation = 3
        self.ids.my_button_AA.on_active = False
        self.ids.my_button_AA.md_bg_color = '#EDF2F4'
        self.ids.my_button_AA.elevation = 3

    def set_answers_BB(self, delay=5):
        self.ids.my_button_BB.text = new_questions[self.question_number].options[1]
        self.ids.my_button_BB.elevation = 3
        self.ids.my_button_BB.on_active = False
        self.ids.my_button_BB.md_bg_color = '#EDF2F4'
        self.ids.my_button_BB.elevation = 3

    def set_answers_CC(self, delay=6):
        self.ids.my_button_CC.text = new_questions[self.question_number].options[2]
        self.ids.my_button_CC.elevation = 3
        self.ids.my_button_CC.on_active = False
        self.ids.my_button_CC.md_bg_color = '#EDF2F4'
        self.ids.my_button_CC.elevation = 3

    def set_answers_DD(self, delay=7):
        self.ids.my_button_DD.text = new_questions[self.question_number].options[3]
        self.ids.my_button_DD.elevation = 3
        self.ids.my_button_DD.on_active = False
        self.ids.my_button_DD.md_bg_color = '#EDF2F4'
        self.ids.my_button_DD.elevation = 3

    def set_answers_undisabled(self, delay = 8):
        self.ids.my_button_DD.disabled = False
        self.ids.my_button_AA.disabled = False
        self.ids.my_button_BB.disabled = False
        self.ids.my_button_CC.disabled = False
    #######################################

    # Kérdés beállítása a képernyőre
    def set_scoreboard(self, delay = 3):
        self.ids.label_score_chaptergame.text = str(self.score)
        self.ids.sum_label_questions_chaptergame.text = str(self.wrong)
    #######################################

    # Gombnyomásra a kérdés helyességének eldöntése
    def make_decision(self, widget, text, delay, delay_button_color):
        # Ha helyes a válasz
        if text == new_questions[self.question_number].answer:
            # Új kérdések és válaszok betöltése
            global EVENT1
            EVENT1 = Clock.schedule_once(self.set_questions_blank, delay)
            global EVENT2
            EVENT2 = Clock.schedule_once(self.set_questions, delay + 1)
            global EVENT3
            EVENT3 = Clock.schedule_once(self.play_sound_question, delay + 1)
            global EVENT4
            EVENT4 = Clock.schedule_once(self.set_answers, delay)
            global EVENT5
            EVENT5 = Clock.schedule_once(self.set_quotes, delay)
            global EVENT6
            EVENT6 = Clock.schedule_once(self.set_answers_AA, delay + 4)
            global EVENT7
            EVENT7 = Clock.schedule_once(self.play_sound_button, delay + 4)
            global EVENT8
            EVENT8 = Clock.schedule_once(self.set_answers_BB, delay + 6)
            global EVENT9
            EVENT9 = Clock.schedule_once(self.play_sound_button, delay + 6)
            global EVENT10
            EVENT10 = Clock.schedule_once(self.set_answers_CC, delay + 8)
            global EVENT11
            EVENT11 = Clock.schedule_once(self.play_sound_button, delay + 8)
            global EVENT12
            EVENT12 = Clock.schedule_once(self.set_answers_DD, delay + 10)
            global EVENT13
            EVENT13 = Clock.schedule_once(self.play_sound_button, delay + 10)
            global EVENT14
            EVENT14 = Clock.schedule_once(self.set_answers_undisabled, delay + 11)

            self.score += 1
            self.answers_number += 1

            global EVENT15
            EVENT15 = Clock.schedule_once(self.set_scoreboard, delay_button_color + 4.0)
            global EVENT16
            EVENT16 = Clock.schedule_once(self.set_the_button_color_right, delay_button_color)
            global EVENT17
            EVENT17 = Clock.schedule_once(self.animate_the_right_button, delay_button_color + 0.5)
            global EVENT18
            EVENT18 = Clock.schedule_once(self.set_the_button_color_right, delay_button_color + 1.0)
            global EVENT19
            EVENT19 = Clock.schedule_once(self.animate_the_right_button, delay_button_color + 1.50)
            global EVENT20
            EVENT20 = Clock.schedule_once(self.set_the_button_color_right, delay_button_color + 2.0)
            global EVENT21
            EVENT21 = Clock.schedule_once(self.animate_the_right_button, delay_button_color + 2.50)
            global EVENT22
            EVENT22 = Clock.schedule_once(self.set_the_button_color_right, delay_button_color + 3.0)
            global EVENT23
            EVENT23 = Clock.schedule_once(self.play_sound_correct, 2.5)
            global EVENT62
            EVENT62 = Clock.schedule_once(self.set_the_pause_on, delay_button_color + 4.5)
            global EVENT64
            EVENT64 = Clock.schedule_once(self.set_the_pause_off, delay)

        # Ha nem helyes a válasz
        else:
            # Új kérdések és válaszok betöltése
            global EVENT24
            EVENT24 = Clock.schedule_once(self.set_questions_blank, delay)
            global EVENT25
            EVENT25 = Clock.schedule_once(self.set_questions, delay + 1)
            global EVENT26
            EVENT26 = Clock.schedule_once(self.play_sound_question, delay + 1)
            global EVENT27
            EVENT27 = Clock.schedule_once(self.set_answers, delay)
            global EVENT28
            EVENT28 = Clock.schedule_once(self.set_quotes, delay)
            global EVENT29
            EVENT29 = Clock.schedule_once(self.set_answers_AA, delay + 4)
            global EVENT30
            EVENT30 = Clock.schedule_once(self.play_sound_button, delay + 4)
            global EVENT31
            EVENT31 = Clock.schedule_once(self.set_answers_BB, delay + 6)
            global EVENT32
            EVENT32 = Clock.schedule_once(self.play_sound_button, delay + 6)
            global EVENT33
            EVENT33 = Clock.schedule_once(self.set_answers_CC, delay + 8)
            global EVENT34
            EVENT34 = Clock.schedule_once(self.play_sound_button, delay + 8)
            global EVENT35
            EVENT35 = Clock.schedule_once(self.set_answers_DD, delay + 10)
            global EVENT36
            EVENT36 = Clock.schedule_once(self.play_sound_button, delay + 10)
            global EVENT37
            EVENT37 = Clock.schedule_once(self.set_answers_undisabled, delay + 11)

            self.answers_number += 1
            self.wrong += 1

            global EVENT38
            EVENT38 = Clock.schedule_once(self.set_scoreboard, delay_button_color + 4.0)
            global EVENT39
            EVENT39 = Clock.schedule_once(self.set_the_button_color_right, delay_button_color)
            global EVENT40
            EVENT40 = Clock.schedule_once(self.animate_the_right_button, delay_button_color + 0.5)
            global EVENT41
            EVENT41 = Clock.schedule_once(self.set_the_button_color_right, delay_button_color + 1.0)
            global EVENT42
            EVENT42 = Clock.schedule_once(self.animate_the_right_button, delay_button_color + 1.50)
            global EVENT43
            EVENT43 = Clock.schedule_once(self.set_the_button_color_right, delay_button_color + 2.0)
            global EVENT44
            EVENT44 = Clock.schedule_once(self.animate_the_right_button, delay_button_color + 2.50)
            global EVENT45
            EVENT45 = Clock.schedule_once(self.set_the_button_color_right, delay_button_color + 3.0)
            global EVENT46
            EVENT46 = Clock.schedule_once(self.play_sound_wrong, 2.5)
            global EVENT63
            EVENT63 = Clock.schedule_once(self.set_the_pause_on, delay_button_color + 4.5)
            global EVENT65
            EVENT65 = Clock.schedule_once(self.set_the_pause_off, delay)

        global CHANGE_SCREEN
        CHANGE_SCREEN = False
    #######################################

    def set_the_button_color_right(self, widget):
        if self.ids.my_button_AA.text == new_questions[self.question_number].answer:
            if self.ids.my_button_BB.elevation == 5:
                self.ids.my_button_BB.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_CC.elevation == 5:
                self.ids.my_button_CC.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_DD.elevation == 5:
                self.ids.my_button_DD.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
            self.ids.my_button_AA.md_bg_color_disabled = '#50F263'
            self.ids.my_button_AA.disabled_color = '#404040'

        if self.ids.my_button_BB.text == new_questions[self.question_number].answer:
            if self.ids.my_button_AA.elevation == 5:
                self.ids.my_button_AA.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_CC.elevation == 5:
                self.ids.my_button_CC.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_DD.elevation == 5:
                self.ids.my_button_DD.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
            self.ids.my_button_BB.md_bg_color_disabled = '#50F263'
            self.ids.my_button_BB.disabled_color = '#404040'

        if self.ids.my_button_CC.text == new_questions[self.question_number].answer:
            if self.ids.my_button_AA.elevation == 5:
                self.ids.my_button_AA.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_BB.elevation == 5:
                self.ids.my_button_BB.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_DD.elevation == 5:
                self.ids.my_button_DD.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
            self.ids.my_button_CC.md_bg_color_disabled = '#50F263'
            self.ids.my_button_CC.disabled_color = '#404040'

        if self.ids.my_button_DD.text == new_questions[self.question_number].answer:
            if self.ids.my_button_AA.elevation == 5:
                self.ids.my_button_AA.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_BB.elevation == 5:
                self.ids.my_button_BB.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_CC.elevation == 5:
                self.ids.my_button_CC.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
            self.ids.my_button_DD.md_bg_color_disabled = '#50F263'
            self.ids.my_button_DD.disabled_color = '#404040'

    def animate_the_right_button(self, widget):
        if self.ids.my_button_AA.text == new_questions[self.question_number].answer:
            if self.ids.my_button_AA.elevation == 5:
                self.ids.my_button_AA.md_bg_color_disabled = '#F25063'
            elif self.ids.my_button_BB.elevation == 5:
                self.ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_CC.elevation == 5:
                self.ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_DD.elevation == 5:
                self.ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
        elif self.ids.my_button_BB.text == new_questions[self.question_number].answer:
            if self.ids.my_button_BB.elevation == 5:
                self.ids.my_button_BB.md_bg_color_disabled = '#F25063'
            elif self.ids.my_button_AA.elevation == 5:
                self.ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_CC.elevation == 5:
                self.ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_DD.elevation == 5:
                self.ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
        elif self.ids.my_button_CC.text == new_questions[self.question_number].answer:
            if self.ids.my_button_CC.elevation == 5:
                self.ids.my_button_CC.md_bg_color_disabled = '#F25063'
            elif self.ids.my_button_BB.elevation == 5:
                self.ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_AA.elevation == 5:
                self.ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_DD.elevation == 5:
                self.ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
        if self.ids.my_button_DD.text == new_questions[self.question_number].answer:
            if self.ids.my_button_DD.elevation == 5:
                self.ids.my_button_DD.md_bg_color_disabled = '#F25063'
            elif self.ids.my_button_BB.elevation == 5:
                self.ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_CC.elevation == 5:
                self.ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_AA.elevation == 5:
                self.ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'

    def play_sound_correct(self, delay=2.5):
        number = random.randint(1,6)
        if number == 1:
            sound = SoundLoader.load('correct01.ogg')
        if number == 2:
            sound = SoundLoader.load('correct02.ogg')
        if number == 3:
            sound = SoundLoader.load('correct03.ogg')
        if number == 4:
            sound = SoundLoader.load('correct04.ogg')
        if number == 5:
            sound = SoundLoader.load('correct05.ogg')
        if number == 6:
            sound = SoundLoader.load('correct06.ogg')
        if sound:
            sound.volume = 0.5 #from 0-1
            sound.play()

    def play_sound_wrong(self, delay=2.5):
        number = random.randint(1,8)
        if number == 1:
            sound = SoundLoader.load('wrong01.ogg')
        if number == 2:
            sound = SoundLoader.load('wrong02.ogg')
        if number == 3:
            sound = SoundLoader.load('wrong03.ogg')
        if number == 4:
            sound = SoundLoader.load('wrong04.ogg')
        if number == 5:
            sound = SoundLoader.load('wrong05.ogg')
        if number == 6:
            sound = SoundLoader.load('wrong06.ogg')
        if number == 7:
            sound = SoundLoader.load('wrong07.ogg')
        if number == 8:
            sound = SoundLoader.load('wrong08.ogg')
        if sound:
            sound.volume = 0.5 #from 0-1
            sound.play()

    def play_sound_button(self, delay=0):
        sound = SoundLoader.load('buttons01.ogg')
        if sound:
            sound.volume = 0.3
            sound.play()

    def play_sound_question(self, delay=2.5):
        number = random.randint(1,6)
        if number == 1:
            sound = SoundLoader.load('questions01.ogg')
        if number == 2:
            sound = SoundLoader.load('questions02.ogg')
        if number == 3:
            sound = SoundLoader.load('questions03.ogg')
        if number == 4:
            sound = SoundLoader.load('questions04.ogg')
        if number == 5:
            sound = SoundLoader.load('questions05.ogg')
        if number == 6:
            sound = SoundLoader.load('questions06.ogg')
        if sound:
            sound.volume = 0.5
            sound.play()

    def set_the_pause_on(self, widget):
        self.manager.get_screen("chapter_game_screen").ids.my_pause_chaptergame.disabled = False

    def set_the_pause_off(self, widget):
        self.manager.get_screen("chapter_game_screen").ids.my_pause_chaptergame.disabled = True

    def pause_chaptergame(self):
        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)

        self.manager.get_screen("chapter_game_screen").ids.my_pause_chaptergame.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_play_chaptergame.disabled = False

    def resume_chaptergame(self):
        self.manager.get_screen("chapter_game_screen").ids.my_pause_chaptergame.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_play_chaptergame.disabled = True

        self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3

        number = random.randint(0, 39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("chapter_game_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("chapter_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("chapter_game_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("chapter_game_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("chapter_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("chapter_game_screen").ids.my_quote_author.text = quotes_authors[number]

        EVENT49 = Clock.schedule_once(self.set_questions, 1)
        EVENT50 = Clock.schedule_once(self.set_answers_AA, 5)
        EVENT51 = Clock.schedule_once(self.set_answers_BB, 7)
        EVENT52 = Clock.schedule_once(self.set_answers_CC, 9)
        EVENT53 = Clock.schedule_once(self.set_answers_DD, 11)
        EVENT54 = Clock.schedule_once(self.set_answers_undisabled, 12)
        EVENT55 = Clock.schedule_once(self.play_sound_question, 1)
        EVENT56 = Clock.schedule_once(self.play_sound_button, 5)
        EVENT57 = Clock.schedule_once(self.play_sound_button, 7)
        EVENT58 = Clock.schedule_once(self.play_sound_button, 9)
        EVENT59 = Clock.schedule_once(self.play_sound_button, 11)







# Játékmód képernyő
class GameScreen(Screen):
    global background

    def set_the_background_music(self):
        global background
        if self.ids.my_icon_volume.icon == 'volume-mute':
            self.ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("main_menu_screen").ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("chapter_game_screen").ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("choose_chapters_screen").ids.my_icon_volume.icon = 'volume-medium'
            self.manager.get_screen("game_screen").ids.my_icon_volume.icon = 'volume-medium'

            background_randomize_number = random.randint(1, 3)
            if background_randomize_number == 1:
                background = SoundLoader.load('background01.ogg')
                background.volume = 0.2
                background.play()
                background.loop = True
            if background_randomize_number == 2:
                background = SoundLoader.load('background02.ogg')
                background.volume = 0.2
                background.play()
                background.loop = True
            if background_randomize_number == 3:
                background = SoundLoader.load('background03.ogg')
                background.volume = 0.2
                background.play()
                background.loop = True

        elif self.ids.my_icon_volume.icon == 'volume-medium':
            self.ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("main_menu_screen").ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("chapter_game_screen").ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("choose_chapters_screen").ids.my_icon_volume.icon = 'volume-mute'
            self.manager.get_screen("game_screen").ids.my_icon_volume.icon = 'volume-mute'
            background.unload()

    dialog = None

    def go_to_main_menu(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos vissza mész a főmenübe?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_main_menu
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_main_menu(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        # belső változók kinullázása
        self.score = 0
        self.wrong = 0
        self.answers_number = 0
        self.question_number = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        # kattintás letiltások visszaállítása
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_1.disabled = False
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_2.disabled = False
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_3.disabled = False

        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_1.on_active = False
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_2.on_active = False
        self.manager.get_screen("main_menu_screen").ids.my_main_menu_button_3.on_active = False

        # Gombok és kérdés clearing
        self.manager.get_screen("free_game_screen").ids.label_score.text = str(0)
        self.manager.get_screen("free_game_screen").ids.sum_label_questions.text = str(0)
        self.manager.get_screen("free_game_screen").ids.label_question.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_B.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_C.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_D.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3

        self.manager.get_screen("chapter_game_screen").ids.label_score_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.sum_label_questions_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3

        self.manager.get_screen("game_screen").ids.label_score_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.sum_label_questions_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = ""
        self.manager.get_screen("game_screen").ids.my_button_AAA.text = ""
        self.manager.get_screen("game_screen").ids.my_button_BBB.text = ""
        self.manager.get_screen("game_screen").ids.my_button_CCC.text = ""
        self.manager.get_screen("game_screen").ids.my_button_DDD.text = ""
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_AAA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_BBB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_CCC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_DDD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_AAA.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_BBB.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_CCC.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_DDD.elevation = 3

        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)

        # Go to the main menu
        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "main_menu_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None

    def go_to_freegame(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos a szabad játékot választod?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_freegame
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_freegame(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        self.manager.get_screen("free_game_screen").ids.my_pause_freegame.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_play_freegame.disabled = True
        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "free_game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None

        global WindowSizeWidth
        global WindowSizeHeight
        self.manager.get_screen("free_game_screen").ids.jvtrivia_icon_freegame.size_hint = (
        0.3, WindowSizeWidth / WindowSizeHeight * 0.3)
        self.manager.get_screen("free_game_screen").ids.jvtrivia_icon_freegame.keep_ratio = True
        self.manager.get_screen("free_game_screen").ids.jvtrivia_icon_freegame.pos_hint = {'x': 0, 'y': 0}

        # Alsó idézet beállítása
        self.set_quotes_free_game()

        # Scoreboard kinullázása
        self.set_scoreboard_freegame()

        # Gombok és kérdés clearing
        self.manager.get_screen("free_game_screen").ids.label_score.text = str(0)
        self.manager.get_screen("free_game_screen").ids.sum_label_questions.text = str(0)
        self.manager.get_screen("free_game_screen").ids.label_question.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_B.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_C.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_D.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3

        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)


        # belső változók kinullázása
        self.score = 0
        self.wrong = 0
        self.answers_number = 0
        self.question_number = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        # Első kérdés és válasz beállítása
        EVENT49 = Clock.schedule_once(self.set_questions_freegame, 6)
        EVENT50 = Clock.schedule_once(self.set_answers_A_freegame, 10)
        EVENT51 = Clock.schedule_once(self.set_answers_B_freegame, 12)
        EVENT52 = Clock.schedule_once(self.set_answers_C_freegame, 14)
        EVENT53 = Clock.schedule_once(self.set_answers_D_freegame, 16)
        EVENT54 = Clock.schedule_once(self.set_answers_undisabled_freegame, 17)
        EVENT55 = Clock.schedule_once(self.play_sound_question_freegame, 6)
        EVENT56 = Clock.schedule_once(self.play_sound_button_freegame, 10)
        EVENT57 = Clock.schedule_once(self.play_sound_button_freegame, 12)
        EVENT58 = Clock.schedule_once(self.play_sound_button_freegame, 14)
        EVENT59 = Clock.schedule_once(self.play_sound_button_freegame, 16)

    def set_quotes_free_game(self, delay=3):
        number = random.randint(0,39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("free_game_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("free_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("free_game_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("free_game_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("free_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("free_game_screen").ids.my_quote_author.text = quotes_authors[number]

    def set_quotes_chapter_game(self, delay=3):
        number = random.randint(0,39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]

    def set_questions_freegame(self, delay=3):
        self.randomize_questions()
        if len(questions[self.question_number].question) > 70:
            self.manager.get_screen("free_game_screen").ids.label_question.font_size = 14
            self.manager.get_screen("free_game_screen").ids.label_question.text = questions[
                self.question_number].question
        elif len(questions[self.question_number].question) > 140:
            self.manager.get_screen("free_game_screen").ids.label_question.font_size = 13
            self.manager.get_screen("free_game_screen").ids.label_question.text = questions[
                self.question_number].question
        else:
            self.manager.get_screen("free_game_screen").ids.label_question.font_size = 16
            self.manager.get_screen("free_game_screen").ids.label_question.text = questions[
                self.question_number].question

    def randomize_questions(self):
        random.shuffle(new_questions)
        #######################################

    def set_scoreboard_freegame(self):
        self.manager.get_screen("free_game_screen").ids.label_score.text = str(0)
        self.manager.get_screen("free_game_screen").ids.sum_label_questions.text = str(0)

    def set_scoreboard_chaptergame(self):
        self.manager.get_screen("chapter_game_screen").ids.label_score_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.sum_label_questions_chaptergame.text = str(0)

    def set_answers_A_chaptergame(self, delay=4):
        A_length = int(len(new_questions[self.question_number].options[0]))
        B_length = int(len(new_questions[self.question_number].options[1]))
        C_length = int(len(new_questions[self.question_number].options[2]))
        D_length = int(len(new_questions[self.question_number].options[3]))
        length_list = [A_length, B_length, C_length, D_length]
        max_length = max(length_list)

        if max_length <= 25:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "14"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "14"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "14"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "14"
        if max_length > 25:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "13"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "13"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "13"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "13"

        if max_length > 35:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "12"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "12"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "12"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "12"
        if max_length > 45:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "11"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "11"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "11"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "11"
        if max_length > 65:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "10"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "10"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "10"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "10"
        if max_length > 85:
            self.manager.get_screen("chapter_game_screen").ids.my_button_AA.font_size = "9"
            self.manager.get_screen("chapter_game_screen").ids.my_button_BB.font_size = "9"
            self.manager.get_screen("chapter_game_screen").ids.my_button_CC.font_size = "9"
            self.manager.get_screen("chapter_game_screen").ids.my_button_DD.font_size = "9"

        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.text = new_questions[self.question_number].options[0]
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.on_active = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.md_bg_color = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3

    def set_answers_B_chaptergame(self, delay=4):
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.text = new_questions[self.question_number].options[1]
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.on_active = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.md_bg_color = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3

    def set_answers_C_chaptergame(self, delay=4):
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.text = new_questions[self.question_number].options[2]
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.on_active = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.md_bg_color = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3

    def set_answers_D_chaptergame(self, delay=4):
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.text = new_questions[self.question_number].options[3]
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.on_active = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.md_bg_color = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3

    def set_answers_undisabled_chaptergame(self, delay=8):
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled = False
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled = False
        #######################################

    def set_answers_A_freegame(self, delay=4):
        A_length = int(len(questions[self.question_number].options[0]))
        B_length = int(len(questions[self.question_number].options[1]))
        C_length = int(len(questions[self.question_number].options[2]))
        D_length = int(len(questions[self.question_number].options[3]))
        length_list = [A_length, B_length, C_length, D_length]
        max_length = max(length_list)

        if max_length <= 25:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "14"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "14"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "14"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "14"
        if max_length > 25:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "13"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "13"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "13"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "13"

        if max_length > 35:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "12"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "12"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "12"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "12"
        if max_length > 55:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "11"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "11"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "11"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "11"
        if max_length > 65:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "10"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "10"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "10"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "10"
        if max_length > 85:
            self.manager.get_screen("free_game_screen").ids.my_button_A.font_size = "9"
            self.manager.get_screen("free_game_screen").ids.my_button_B.font_size = "9"
            self.manager.get_screen("free_game_screen").ids.my_button_C.font_size = "9"
            self.manager.get_screen("free_game_screen").ids.my_button_D.font_size = "9"

        self.manager.get_screen("free_game_screen").ids.my_button_A.text = questions[self.question_number].options[0]
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_A.on_active = False
        self.manager.get_screen("free_game_screen").ids.my_button_A.md_bg_color = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3

    def set_answers_B_freegame(self, delay=4):
        self.manager.get_screen("free_game_screen").ids.my_button_B.text = questions[self.question_number].options[1]
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_B.on_active = False
        self.manager.get_screen("free_game_screen").ids.my_button_B.md_bg_color = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3

    def set_answers_C_freegame(self, delay=4):
        self.manager.get_screen("free_game_screen").ids.my_button_C.text = questions[self.question_number].options[2]
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_C.on_active = False
        self.manager.get_screen("free_game_screen").ids.my_button_C.md_bg_color = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3

    def set_answers_D_freegame(self, delay=4):
        self.manager.get_screen("free_game_screen").ids.my_button_D.text = questions[self.question_number].options[3]
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_D.on_active = False
        self.manager.get_screen("free_game_screen").ids.my_button_D.md_bg_color = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3

    def set_answers_undisabled_freegame(self, delay=8):
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled = False
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled = False
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled = False
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled = False

    def play_sound_button_chaptergame(self, delay=0):
        sound = SoundLoader.load('buttons01.ogg')
        if sound:
            sound.volume = 0.5
            sound.play()

    def play_sound_question_chaptergame(self, delay=2.5):
        number = random.randint(1, 6)
        if number == 1:
            sound = SoundLoader.load('questions01.ogg')
        if number == 2:
            sound = SoundLoader.load('questions02.ogg')
        if number == 3:
            sound = SoundLoader.load('questions03.ogg')
        if number == 4:
            sound = SoundLoader.load('questions04.ogg')
        if number == 5:
            sound = SoundLoader.load('questions05.ogg')
        if number == 6:
            sound = SoundLoader.load('questions06.ogg')
        if sound:
            sound.volume = 0.3
            sound.play()

    def play_sound_button_freegame(self, delay=0):
        sound = SoundLoader.load('buttons01.ogg')
        if sound:
            sound.volume = 0.5
            sound.play()

    def play_sound_question_freegame(self, delay=2.5):
        number = random.randint(1, 6)
        if number == 1:
            sound = SoundLoader.load('questions01.ogg')
        if number == 2:
            sound = SoundLoader.load('questions02.ogg')
        if number == 3:
            sound = SoundLoader.load('questions03.ogg')
        if number == 4:
            sound = SoundLoader.load('questions04.ogg')
        if number == 5:
            sound = SoundLoader.load('questions05.ogg')
        if number == 6:
            sound = SoundLoader.load('questions06.ogg')
        if sound:
            sound.volume = 0.3
            sound.play()

    def go_to_chaptergame(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos a tematikus gyakorlást választod?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_chaptergame
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_chaptergame(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        self.manager.get_screen("chapter_game_screen").ids.my_pause_chaptergame.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_play_chaptergame.disabled = True
        # belső változók kinullázása
        self.score = 0
        self.wrong = 0
        self.answers_number = 0
        self.question_number = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None

        global WindowSizeWidth
        global WindowSizeHeight
        self.manager.get_screen("choose_chapters_screen").ids.jvtrivia_icon_choosechapters.size_hint = (
            0.3, WindowSizeWidth / WindowSizeHeight * 0.3)
        self.manager.get_screen("choose_chapters_screen").ids.jvtrivia_icon_choosechapters.keep_ratio = True
        self.manager.get_screen("choose_chapters_screen").ids.jvtrivia_icon_choosechapters.pos_hint = {'x': 0, 'y': 0}

        # Alsó idézet beállítása
        number = random.randint(0, 39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]

        # Gombok és kérdés clearing
        self.manager.get_screen("free_game_screen").ids.label_score.text = str(0)
        self.manager.get_screen("free_game_screen").ids.sum_label_questions.text = str(0)
        self.manager.get_screen("free_game_screen").ids.label_question.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_B.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_C.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_D.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3

        self.manager.get_screen("chapter_game_screen").ids.label_score_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.sum_label_questions_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3

        self.manager.get_screen("game_screen").ids.label_score_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.sum_label_questions_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = ""
        self.manager.get_screen("game_screen").ids.my_button_AAA.text = ""
        self.manager.get_screen("game_screen").ids.my_button_BBB.text = ""
        self.manager.get_screen("game_screen").ids.my_button_CCC.text = ""
        self.manager.get_screen("game_screen").ids.my_button_DDD.text = ""
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_AAA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_BBB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_CCC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_DDD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_AAA.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_BBB.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_CCC.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_DDD.elevation = 3

        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)


        def set_quotes_choose_chapter_game(self):
            number = random.randint(0, 39)
            if len(quotes[number]) > 100:
                self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 8
                self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
                self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]
            else:
                self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 9
                self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
                self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]

        self.set_quotes_choose_chapter_game()

    def go_to_gamescreen(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos vizsgázni szeretnél?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_gamescreen
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_gamescreen(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        # belső változók kinullázása
        self.score = 0
        self.wrong = 0
        self.answers_number = 0
        self.question_number = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None


    def set_scoreboard_chaptergame(self):
        self.manager.get_screen("chapter_game_screen").ids.label_score_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.sum_label_questions_chaptergame.text = str(0)

    def set_quotes_choose_chapter_game(self):
        number = random.randint(0, 39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("choose_chapters_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("choose_chapters_screen").ids.my_quote_author.text = quotes_authors[number]

    def go_to_exit(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "[color=404040]Biztos kilépsz a JVTriviából?[/color]",
                type="confirmation",
                md_bg_color="#8D99AE",
                auto_dismiss=False,
                radius=[7, 7, 7, 7],
                # theme_cls= '#3B3838',
                cls='#3B3838',
                content_cls='#3B3838',
                buttons = [
                    MDRaisedButton(
                        text = "Nem",
                        text_color='#404040',
                        elevation= 3,
                        line_color= "#EDF2F4",
                        md_bg_color= '#EDF2F4',
                        font_name= "Arial",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="Igen",
                        text_color='#404040',
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_exit
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_exit(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        # belső változók kinullázása
        self.score = 0
        self.wrong = 0
        self.answers_number = 0
        self.question_number = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "choose_chapters_screen"
            self.window.close()
            self.dialog = None

    # Click cancel button
    def close_dialog(self, obj):
        # Close alert box
        self.dialog.dismiss(force=True)
        self.dialog = None

    score = 0
    wrong = 0
    answers_number = 0
    question_number = 0

    def on_pre_enter(self, *args):
        self.set_scoreboard()
        global CHANGE_SCREEN
        CHANGE_SCREEN = False
    ####################################

    #Kérdések véletlenszerű megkeverése
    def randomize_questions(self):
        random.shuffle(questions)
    #######################################

    def set_quotes(self, delay=3):
        number = random.randint(0,39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("free_game_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("free_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("free_game_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("free_game_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("free_game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("free_game_screen").ids.my_quote_author.text = quotes_authors[number]


    # Kérdés beállítása
    def set_questions(self, delay = 3):
        if self.question_number >= len(questions)-1:
            self.randomize_questions()
            self.question_number = 0
            if len(questions[self.question_number].question) > 70:
                self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 14
                self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[
                    self.question_number].question
            elif len(questions[self.question_number].question) > 140:
                self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 13
                self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[
                    self.question_number].question
            else:
                self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 16
                self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[
                    self.question_number].question
        else:
            self.question_number += 1
            if len(questions[self.question_number].question) > 70:
                self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 14
                self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[
                    self.question_number].question
            elif len(questions[self.question_number].question) > 140:
                self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 13
                self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[
                    self.question_number].question
            else:
                self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 16
                self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[
                    self.question_number].question
    ######################################

    # Üres kérdés beállítása 1 mp nyerése
    def set_questions_blank(self, delay = 2):
        self.ids.label_question_gamescreen.text = ""

    # Válaszok beállítása a gombokra véletlenszerűen
    def set_answers(self, delay = 3):
        # Válaszok szövegének beállítása
        self.ids.my_button_AAA.text = ""
        self.ids.my_button_BBB.text = ""
        self.ids.my_button_CCC.text = ""
        self.ids.my_button_DDD.text = ""
        self.ids.my_button_AAA.disabled_color = '#404040'
        self.ids.my_button_AAA.md_bg_color_disabled = '#EDF2F4'
        self.ids.my_button_BBB.disabled_color = '#404040'
        self.ids.my_button_BBB.md_bg_color_disabled = '#EDF2F4'
        self.ids.my_button_CCC.disabled_color = '#404040'
        self.ids.my_button_CCC.md_bg_color_disabled = '#EDF2F4'
        self.ids.my_button_DDD.disabled_color = '#404040'
        self.ids.my_button_DDD.md_bg_color_disabled = '#EDF2F4'
        random.shuffle(questions[self.question_number].options)

    def set_answers_A(self, delay=4):
        A_length = int(len(questions[self.question_number].options[0]))
        B_length = int(len(questions[self.question_number].options[1]))
        C_length = int(len(questions[self.question_number].options[2]))
        D_length = int(len(questions[self.question_number].options[3]))
        length_list = [A_length, B_length, C_length, D_length]
        max_length = max(length_list)

        if max_length <= 25:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "14"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "14"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "14"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "14"
        if max_length > 25:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "13"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "13"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "13"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "13"

        if max_length > 35:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "12"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "12"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "12"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "12"
        if max_length > 55:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "11"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "11"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "11"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "11"
        if max_length > 65:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "10"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "10"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "10"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "10"
        if max_length > 85:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "9"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "9"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "9"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "9"

        self.ids.my_button_AAA.text = questions[self.question_number].options[0]
        self.ids.my_button_AAA.elevation = 3
        self.ids.my_button_AAA.on_active = False
        self.ids.my_button_AAA.md_bg_color = '#EDF2F4'
        self.ids.my_button_AAA.elevation = 3

    def set_answers_B(self, delay=5):
        self.ids.my_button_BBB.text = questions[self.question_number].options[1]
        self.ids.my_button_BBB.elevation = 3
        self.ids.my_button_BBB.on_active = False
        self.ids.my_button_BBB.md_bg_color = '#EDF2F4'
        self.ids.my_button_BBB.elevation = 3

    def set_answers_C(self, delay=6):
        self.ids.my_button_CCC.text = questions[self.question_number].options[2]
        self.ids.my_button_CCC.elevation = 3
        self.ids.my_button_CCC.on_active = False
        self.ids.my_button_CCC.md_bg_color = '#EDF2F4'
        self.ids.my_button_CCC.elevation = 3

    def set_answers_D(self, delay=7):
        self.ids.my_button_DDD.text = questions[self.question_number].options[3]
        self.ids.my_button_DDD.elevation = 3
        self.ids.my_button_DDD.on_active = False
        self.ids.my_button_DDD.md_bg_color = '#EDF2F4'
        self.ids.my_button_DDD.elevation = 3

    def set_answers_undisabled(self, delay=8):
        self.ids.my_button_DDD.disabled = False
        self.ids.my_button_AAA.disabled = False
        self.ids.my_button_BBB.disabled = False
        self.ids.my_button_CCC.disabled = False
    #######################################

        # Kérdés beállítása a képernyőre
    def set_scoreboard(self, delay = 3):
        self.ids.label_score_gamescreen.text = str(self.score)
        self.ids.sum_label_questions_gamescreen.text = str(self.wrong)
    #######################################

    # Gombnyomásra a kérdés helyességének eldöntése
    def make_decision(self, widget, text, delay, delay_button_color):
        # Ha helyes a válasz
        if text == questions[self.question_number].answer:
            # Új kérdések és válaszok betöltése
            self.score += 1
            self.answers_number += 1
            global EVENT1
            EVENT1 = Clock.schedule_once(self.set_questions_blank, delay)
            global EVENT2
            EVENT2 =Clock.schedule_once(self.set_questions, delay + 1)
            global EVENT3
            EVENT3 =Clock.schedule_once(self.play_sound_question, delay + 1)
            global EVENT4
            EVENT4 =Clock.schedule_once(self.set_answers, delay)
            global EVENT5
            EVENT5 =Clock.schedule_once(self.set_quotes, delay)
            global EVENT6
            EVENT6 =Clock.schedule_once(self.set_answers_A, delay + 4)
            global EVENT7
            EVENT7 =Clock.schedule_once(self.play_sound_button, delay + 4)
            global EVENT8
            EVENT8 =Clock.schedule_once(self.set_answers_B, delay + 6)
            global EVENT9
            EVENT9 =Clock.schedule_once(self.play_sound_button, delay + 6)
            global EVENT10
            EVENT10 =Clock.schedule_once(self.set_answers_C, delay + 8)
            global EVENT11
            EVENT11 =Clock.schedule_once(self.play_sound_button, delay + 8)
            global EVENT12
            EVENT12 =Clock.schedule_once(self.set_answers_D, delay + 10)
            global EVENT13
            EVENT13 =Clock.schedule_once(self.play_sound_button, delay + 10)
            global EVENT14
            EVENT14 =Clock.schedule_once(self.set_answers_undisabled, delay + 11)
            global EVENT15
            EVENT15 =Clock.schedule_once(self.set_scoreboard, delay_button_color + 4.0)
            global EVENT16
            EVENT16 =Clock.schedule_once(self.set_the_button_color_right, delay_button_color)
            global EVENT17
            EVENT17 =Clock.schedule_once(self.animate_the_right_button, delay_button_color + 0.5)
            global EVENT18
            EVENT18 =Clock.schedule_once(self.set_the_button_color_right, delay_button_color + 1.0)
            global EVENT19
            EVENT19 =Clock.schedule_once(self.animate_the_right_button, delay_button_color + 1.50)
            global EVENT20
            EVENT20 =Clock.schedule_once(self.set_the_button_color_right, delay_button_color + 2.0)
            global EVENT21
            EVENT21 =Clock.schedule_once(self.animate_the_right_button, delay_button_color + 2.50)
            global EVENT22
            EVENT22 =Clock.schedule_once(self.set_the_button_color_right, delay_button_color + 3.0)
            global EVENT23
            EVENT23 =Clock.schedule_once(self.play_sound_correct, 2.5)

            if self.answers_number < 25:
                global EVENT62
                EVENT62 = Clock.schedule_once(self.set_the_pause_on, delay_button_color + 4.5)
                global EVENT64
                EVENT64 = Clock.schedule_once(self.set_the_pause_off, delay)

            global EVENT60
            EVENT60 = Clock.schedule_once(self.is_game_over, delay-1)
        # Ha nem helyes a válasz
        else:
            # Új kérdések és válaszok betöltése
            global EVENT24
            EVENT24 = Clock.schedule_once(self.set_questions_blank, delay)
            global EVENT25
            EVENT25 = Clock.schedule_once(self.set_questions, delay + 1)
            global EVENT26
            EVENT26 = Clock.schedule_once(self.play_sound_question, delay + 1)
            global EVENT27
            EVENT27 = Clock.schedule_once(self.set_answers, delay)
            global EVENT28
            EVENT28 = Clock.schedule_once(self.set_quotes, delay)
            global EVENT29
            EVENT29 = Clock.schedule_once(self.set_answers_A, delay + 4)
            global EVENT30
            EVENT30 = Clock.schedule_once(self.play_sound_button, delay + 4)
            global EVENT31
            EVENT31 = Clock.schedule_once(self.set_answers_B, delay + 6)
            global EVENT32
            EVENT32 = Clock.schedule_once(self.play_sound_button, delay + 6)
            global EVENT33
            EVENT33 = Clock.schedule_once(self.set_answers_C, delay + 8)
            global EVENT34
            EVENT34 = Clock.schedule_once(self.play_sound_button, delay + 8)
            global EVENT35
            EVENT35 = Clock.schedule_once(self.set_answers_D, delay + 10)
            global EVENT36
            EVENT36 = Clock.schedule_once(self.play_sound_button, delay + 10)
            global EVENT37
            EVENT37 = Clock.schedule_once(self.set_answers_undisabled, delay + 11)

            self.answers_number += 1
            self.wrong += 1

            global EVENT38
            EVENT38 = Clock.schedule_once(self.set_scoreboard, delay_button_color + 4.0)
            global EVENT39
            EVENT39 = Clock.schedule_once(self.set_the_button_color_right, delay_button_color)
            global EVENT40
            EVENT40 = Clock.schedule_once(self.animate_the_right_button, delay_button_color + 0.5)
            global EVENT41
            EVENT41 = Clock.schedule_once(self.set_the_button_color_right, delay_button_color + 1.0)
            global EVENT42
            EVENT42 = Clock.schedule_once(self.animate_the_right_button, delay_button_color + 1.50)
            global EVENT43
            EVENT43 = Clock.schedule_once(self.set_the_button_color_right, delay_button_color + 2.0)
            global EVENT44
            EVENT44 = Clock.schedule_once(self.animate_the_right_button, delay_button_color + 2.50)
            global EVENT45
            EVENT45 = Clock.schedule_once(self.set_the_button_color_right, delay_button_color + 3.0)
            global EVENT46
            EVENT46 = Clock.schedule_once(self.play_sound_wrong, 2.5)

            if self.answers_number < 25:
                global EVENT63
                EVENT63 = Clock.schedule_once(self.set_the_pause_on, delay_button_color + 4.5)
                global EVENT65
                EVENT65 = Clock.schedule_once(self.set_the_pause_off, delay)

            global EVENT61
            EVENT60 = Clock.schedule_once(self.is_game_over, delay - 1)




        global CHANGE_SCREEN
        CHANGE_SCREEN = False

    def is_game_over(self, delay=15):
        # Ha vége a játéknak
        if self.answers_number == 25:
            Clock.unschedule(EVENT1)
            Clock.unschedule(EVENT2)
            Clock.unschedule(EVENT3)
            Clock.unschedule(EVENT4)
            Clock.unschedule(EVENT5)
            Clock.unschedule(EVENT6)
            Clock.unschedule(EVENT7)
            Clock.unschedule(EVENT8)
            Clock.unschedule(EVENT9)
            Clock.unschedule(EVENT10)
            Clock.unschedule(EVENT11)
            Clock.unschedule(EVENT12)
            Clock.unschedule(EVENT13)
            Clock.unschedule(EVENT14)
            Clock.unschedule(EVENT15)
            Clock.unschedule(EVENT16)
            Clock.unschedule(EVENT17)
            Clock.unschedule(EVENT18)
            Clock.unschedule(EVENT19)
            Clock.unschedule(EVENT20)
            Clock.unschedule(EVENT21)
            Clock.unschedule(EVENT22)
            Clock.unschedule(EVENT23)
            Clock.unschedule(EVENT24)
            Clock.unschedule(EVENT25)
            Clock.unschedule(EVENT26)
            Clock.unschedule(EVENT27)
            Clock.unschedule(EVENT28)
            Clock.unschedule(EVENT29)
            Clock.unschedule(EVENT30)
            Clock.unschedule(EVENT31)
            Clock.unschedule(EVENT32)
            Clock.unschedule(EVENT33)
            Clock.unschedule(EVENT34)
            Clock.unschedule(EVENT35)
            Clock.unschedule(EVENT36)
            Clock.unschedule(EVENT37)
            Clock.unschedule(EVENT38)
            Clock.unschedule(EVENT39)
            Clock.unschedule(EVENT40)
            Clock.unschedule(EVENT41)
            Clock.unschedule(EVENT42)
            Clock.unschedule(EVENT43)
            Clock.unschedule(EVENT44)
            Clock.unschedule(EVENT45)
            Clock.unschedule(EVENT46)
            Clock.unschedule(EVENT47)
            Clock.unschedule(EVENT48)
            Clock.unschedule(EVENT49)
            Clock.unschedule(EVENT50)
            Clock.unschedule(EVENT51)
            Clock.unschedule(EVENT52)
            Clock.unschedule(EVENT53)
            Clock.unschedule(EVENT54)
            Clock.unschedule(EVENT55)
            Clock.unschedule(EVENT56)
            Clock.unschedule(EVENT57)
            Clock.unschedule(EVENT58)
            Clock.unschedule(EVENT59)
            Clock.unschedule(EVENT60)
            Clock.unschedule(EVENT61)
            Clock.unschedule(EVENT62)
            Clock.unschedule(EVENT63)
            Clock.unschedule(EVENT64)
            Clock.unschedule(EVENT65)


            if (self.score / self.answers_number)>=0.8:
                self.test_end_success()
            else:
                self.test_end_unsuccess()




    #######################################

    def set_the_button_color_right(self, widget):
        if self.ids.my_button_AAA.text == questions[self.question_number].answer:
            if self.ids.my_button_BBB.elevation == 5:
                self.ids.my_button_BBB.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_BBB.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_CCC.elevation == 5:
                self.ids.my_button_CCC.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_CCC.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_DDD.elevation == 5:
                self.ids.my_button_DDD.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_DDD.md_bg_color_disabled = '#EDF2F4'
            self.ids.my_button_AAA.md_bg_color_disabled = '#50F263'
            self.ids.my_button_AAA.disabled_color = '#404040'

        if self.ids.my_button_BBB.text == questions[self.question_number].answer:
            if self.ids.my_button_AAA.elevation == 5:
                self.ids.my_button_AAA.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_AAA.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_CCC.elevation == 5:
                self.ids.my_button_CCC.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_CCC.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_DDD.elevation == 5:
                self.ids.my_button_DDD.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_DDD.md_bg_color_disabled = '#EDF2F4'
            self.ids.my_button_BBB.md_bg_color_disabled = '#50F263'
            self.ids.my_button_BBB.disabled_color = '#404040'

        if self.ids.my_button_CCC.text == questions[self.question_number].answer:
            if self.ids.my_button_AAA.elevation == 5:
                self.ids.my_button_AAA.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_AAA.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_BBB.elevation == 5:
                self.ids.my_button_BBB.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_BBB.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_DDD.elevation == 5:
                self.ids.my_button_DDD.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_DDD.md_bg_color_disabled = '#EDF2F4'
            self.ids.my_button_CCC.md_bg_color_disabled = '#50F263'
            self.ids.my_button_CCC.disabled_color = '#404040'

        if self.ids.my_button_DDD.text == questions[self.question_number].answer:
            if self.ids.my_button_AAA.elevation == 5:
                self.ids.my_button_AAA.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_AAA.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_BBB.elevation == 5:
                self.ids.my_button_BBB.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_BBB.md_bg_color_disabled = '#EDF2F4'
            if self.ids.my_button_CCC.elevation == 5:
                self.ids.my_button_CCC.md_bg_color_disabled = '#F25063'
            else:
                self.ids.my_button_CCC.md_bg_color_disabled = '#EDF2F4'
            self.ids.my_button_DDD.md_bg_color_disabled = '#50F263'
            self.ids.my_button_DDD.disabled_color = '#404040'

    def animate_the_right_button(self, widget):
        if self.ids.my_button_AAA.text == questions[self.question_number].answer:
            if self.ids.my_button_AAA.elevation == 5:
                self.ids.my_button_AAA.md_bg_color_disabled = '#F25063'
            elif self.ids.my_button_BBB.elevation == 5:
                self.ids.my_button_AAA.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_CCC.elevation == 5:
                self.ids.my_button_AAA.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_DDD.elevation == 5:
                self.ids.my_button_AAA.md_bg_color_disabled = '#EDF2F4'
        elif self.ids.my_button_BBB.text == questions[self.question_number].answer:
            if self.ids.my_button_BBB.elevation == 5:
                self.ids.my_button_BBB.md_bg_color_disabled = '#F25063'
            elif self.ids.my_button_AAA.elevation == 5:
                self.ids.my_button_BBB.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_CCC.elevation == 5:
                self.ids.my_button_BBB.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_DDD.elevation == 5:
                self.ids.my_button_BBB.md_bg_color_disabled = '#EDF2F4'
        elif self.ids.my_button_CCC.text == questions[self.question_number].answer:
            if self.ids.my_button_CCC.elevation == 5:
                self.ids.my_button_CCC.md_bg_color_disabled = '#F25063'
            elif self.ids.my_button_BBB.elevation == 5:
                self.ids.my_button_CCC.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_AAA.elevation == 5:
                self.ids.my_button_CCC.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_DDD.elevation == 5:
                self.ids.my_button_CCC.md_bg_color_disabled = '#EDF2F4'
        if self.ids.my_button_DDD.text == questions[self.question_number].answer:
            if self.ids.my_button_DDD.elevation == 5:
                self.ids.my_button_DDD.md_bg_color_disabled = '#F25063'
            elif self.ids.my_button_BBB.elevation == 5:
                self.ids.my_button_DDD.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_CCC.elevation == 5:
                self.ids.my_button_DDD.md_bg_color_disabled = '#EDF2F4'
            elif self.ids.my_button_AAA.elevation == 5:
                self.ids.my_button_DDD.md_bg_color_disabled = '#EDF2F4'


    def play_sound_correct(self, delay=2.5):
        number = random.randint(1,6)
        if number == 1:
            sound = SoundLoader.load('correct01.ogg')
        if number == 2:
            sound = SoundLoader.load('correct02.ogg')
        if number == 3:
            sound = SoundLoader.load('correct03.ogg')
        if number == 4:
            sound = SoundLoader.load('correct04.ogg')
        if number == 5:
            sound = SoundLoader.load('correct05.ogg')
        if number == 6:
            sound = SoundLoader.load('correct06.ogg')
        if sound:
            sound.volume = 0.5 #from 0-1
            sound.play()

    def play_sound_wrong(self, delay=2.5):
        number = random.randint(1,8)
        if number == 1:
            sound = SoundLoader.load('wrong01.ogg')
        if number == 2:
            sound = SoundLoader.load('wrong02.ogg')
        if number == 3:
            sound = SoundLoader.load('wrong03.ogg')
        if number == 4:
            sound = SoundLoader.load('wrong04.ogg')
        if number == 5:
            sound = SoundLoader.load('wrong05.ogg')
        if number == 6:
            sound = SoundLoader.load('wrong06.ogg')
        if number == 7:
            sound = SoundLoader.load('wrong07.ogg')
        if number == 8:
            sound = SoundLoader.load('wrong08.ogg')
        if sound:
            sound.volume = 0.5 #from 0-1
            sound.play()

    def play_sound_button(self, delay=0):
        sound = SoundLoader.load('buttons01.ogg')
        if sound:
            sound.volume = 0.5
            sound.play()

    def play_sound_question(self, delay=2.5):
        number = random.randint(1,6)
        if number == 1:
            sound = SoundLoader.load('questions01.ogg')
        if number == 2:
            sound = SoundLoader.load('questions02.ogg')
        if number == 3:
            sound = SoundLoader.load('questions03.ogg')
        if number == 4:
            sound = SoundLoader.load('questions04.ogg')
        if number == 5:
            sound = SoundLoader.load('questions05.ogg')
        if number == 6:
            sound = SoundLoader.load('questions06.ogg')
        if sound:
            sound.volume = 0.3
            sound.play()

    def test_end_success(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="[color=404040]Gratulálunk, sikeres volt a vizsgád![/color]",
                text="[color=404040]Eredményed: " + str(int(self.score / self.answers_number * 100)) + "%[/color]" ,
                type="confirmation",
                md_bg_color="#8D99AE",
                # background_color = '#3B3838',
                auto_dismiss=False,
                radius=[7, 7, 7, 7],

                # text_color = '#EDF2F4',
                buttons=[
                    MDRaisedButton(
                        text="Főmenü",
                        text_color='#404040',
                        text_size= "12",
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_main_menu
                    ),
                    MDRaisedButton(
                        text="Új vizsga",
                        text_color='#404040',
                        elevation=3,
                        text_size= "12",
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_gamescreen_2
                    )
                ]
            )
        self.dialog.open()

    def test_end_unsuccess(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="[color=404040]Ez most nem jött össze, gyakorolj még![/color]",
                text="[color=404040]Eredményed: " + str(int(self.score / self.answers_number * 100)) + "%[/color]" ,
                type="confirmation",
                md_bg_color="#8D99AE",
                # background_color = '#3B3838',
                auto_dismiss=False,
                radius=[7, 7, 7, 7],

                # text_color = '#EDF2F4',
                buttons=[
                    MDRaisedButton(
                        text="Főmenü",
                        text_color='#404040',
                        text_size="12",
                        elevation=3,
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_main_menu
                    ),
                    MDRaisedButton(
                        text="Új vizsga",
                        text_color='#404040',
                        elevation=3,
                        text_size="12",
                        line_color="#EDF2F4",
                        md_bg_color='#EDF2F4',
                        font_name="Arial",
                        on_release=self.go_to_the_gamescreen_2
                    )
                ]
            )
        self.dialog.open()

    def go_to_the_gamescreen_2(self, obj):
        global CHANGE_SCREEN
        CHANGE_SCREEN = True
        self.manager.get_screen("game_screen").ids.pause_gamescreen.disabled = True
        self.manager.get_screen("game_screen").ids.play_gamescreen.disabled = True
        # belső változók kinullázása
        self.score = 0
        self.wrong = 0
        self.answers_number = 0
        self.question_number = 0
        FreeGameScreen.score = 0
        FreeGameScreen.wrong = 0
        FreeGameScreen.answers_number = 0
        FreeGameScreen.question_number = 0
        ChapterGameScreen.score = 0
        ChapterGameScreen.wrong = 0
        ChapterGameScreen.answers_number = 0
        ChapterGameScreen.question_number = 0
        GameScreen.score = 0
        GameScreen.wrong = 0
        GameScreen.answers_number = 0
        GameScreen.question_number = 0

        number = random.randint(1, 5)
        if number == 1:
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 2:
            self.manager.transition = PixelTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 3:
            self.manager.transition = RippleTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 4:
            self.manager.transition = BlurTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None
        if number == 5:
            self.manager.transition = RVBTransition()
            self.manager.transition.duration = 3.0
            Window.clearcolor = "#8D99AE"
            self.manager.current = "game_screen"
            self.dialog.dismiss(force=True)
            self.dialog = None

        global WindowSizeWidth
        global WindowSizeHeight
        self.manager.get_screen("game_screen").ids.jvtrivia_icon_gamescreen.size_hint = (
            0.3, WindowSizeWidth / WindowSizeHeight * 0.3)
        self.manager.get_screen("game_screen").ids.jvtrivia_icon_gamescreen.keep_ratio = True
        self.manager.get_screen("game_screen").ids.jvtrivia_icon_gamescreen.pos_hint = {'x': 0, 'y': 0}

        # Alsó idézet beállítása
        self.set_quotes_gamescreen()

        # Scoreboard kinullázása
        self.set_scoreboard_gamescreen()

        # Gombok és kérdés clearing
        self.manager.get_screen("free_game_screen").ids.label_score.text = str(0)
        self.manager.get_screen("free_game_screen").ids.sum_label_questions.text = str(0)
        self.manager.get_screen("free_game_screen").ids.label_question.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_B.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_C.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_D.text = ""
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled = True
        self.manager.get_screen("free_game_screen").ids.my_button_A.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_B.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_C.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_D.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("free_game_screen").ids.my_button_A.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_B.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_C.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_D.disabled_color = '#404040'
        self.manager.get_screen("free_game_screen").ids.my_button_A.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_B.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_C.elevation = 3
        self.manager.get_screen("free_game_screen").ids.my_button_D.elevation = 3

        self.manager.get_screen("chapter_game_screen").ids.label_score_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.sum_label_questions_chaptergame.text = str(0)
        self.manager.get_screen("chapter_game_screen").ids.label_question_chaptergame.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.text = ""
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled = True
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.disabled_color = '#404040'
        self.manager.get_screen("chapter_game_screen").ids.my_button_AA.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_BB.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_CC.elevation = 3
        self.manager.get_screen("chapter_game_screen").ids.my_button_DD.elevation = 3

        self.manager.get_screen("game_screen").ids.label_score_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.sum_label_questions_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = ""
        self.manager.get_screen("game_screen").ids.my_button_AAA.text = ""
        self.manager.get_screen("game_screen").ids.my_button_BBB.text = ""
        self.manager.get_screen("game_screen").ids.my_button_CCC.text = ""
        self.manager.get_screen("game_screen").ids.my_button_DDD.text = ""
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_AAA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_BBB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_CCC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_DDD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_AAA.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_BBB.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_CCC.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_DDD.elevation = 3


        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)

        # Első kérdés és válasz beállítása
        EVENT49 = Clock.schedule_once(self.set_questions_gamescreen, 6)
        EVENT50 = Clock.schedule_once(self.set_answers_A_gamescreen, 10)
        EVENT51 = Clock.schedule_once(self.set_answers_B_gamescreen, 12)
        EVENT52 = Clock.schedule_once(self.set_answers_C_gamescreen, 14)
        EVENT53 = Clock.schedule_once(self.set_answers_D_gamescreen, 16)
        EVENT54 = Clock.schedule_once(self.set_answers_undisabled_gamescreen, 17)
        EVENT55 = Clock.schedule_once(self.play_sound_question_gamescreen, 6)
        EVENT56 = Clock.schedule_once(self.play_sound_button_gamescreen, 10)
        EVENT57 = Clock.schedule_once(self.play_sound_button_gamescreen, 12)
        EVENT58 = Clock.schedule_once(self.play_sound_button_gamescreen, 14)
        EVENT59 = Clock.schedule_once(self.play_sound_button_gamescreen, 16)

    def play_sound_button_gamescreen(self, delay=0):
        sound = SoundLoader.load('buttons01.ogg')
        if sound:
            sound.volume = 0.5
            sound.play()

    def play_sound_question_gamescreen(self, delay=2.5):
        number = random.randint(1,6)
        if number == 1:
            sound = SoundLoader.load('questions01.ogg')
        if number == 2:
            sound = SoundLoader.load('questions02.ogg')
        if number == 3:
            sound = SoundLoader.load('questions03.ogg')
        if number == 4:
            sound = SoundLoader.load('questions04.ogg')
        if number == 5:
            sound = SoundLoader.load('questions05.ogg')
        if number == 6:
            sound = SoundLoader.load('questions06.ogg')
        if sound:
            sound.volume = 0.3
            sound.play()

    def set_answers_A_gamescreen(self, delay=4):
        A_length = int(len(questions[self.question_number].options[0]))
        B_length = int(len(questions[self.question_number].options[1]))
        C_length = int(len(questions[self.question_number].options[2]))
        D_length = int(len(questions[self.question_number].options[3]))
        length_list = [A_length, B_length, C_length, D_length]
        max_length = max(length_list)

        if max_length <= 25:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "14"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "14"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "14"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "14"
        if max_length > 25:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "13"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "13"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "13"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "13"

        if max_length > 35:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "12"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "12"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "12"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "12"
        if max_length > 55:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "11"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "11"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "11"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "11"
        if max_length > 65:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "10"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "10"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "10"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "10"
        if max_length > 85:
            self.manager.get_screen("game_screen").ids.my_button_AAA.font_size = "9"
            self.manager.get_screen("game_screen").ids.my_button_BBB.font_size = "9"
            self.manager.get_screen("game_screen").ids.my_button_CCC.font_size = "9"
            self.manager.get_screen("game_screen").ids.my_button_DDD.font_size = "9"

        self.manager.get_screen("game_screen").ids.my_button_AAA.text = questions[self.question_number].options[0]
        self.manager.get_screen("game_screen").ids.my_button_AAA.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_AAA.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_AAA.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_AAA.elevation = 3

    def set_answers_B_gamescreen(self, delay=5):
        self.manager.get_screen("game_screen").ids.my_button_BBB.text = questions[self.question_number].options[1]
        self.manager.get_screen("game_screen").ids.my_button_BBB.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_BBB.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_BBB.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_BBB.elevation = 3

    def set_answers_C_gamescreen(self, delay=6):
        self.manager.get_screen("game_screen").ids.my_button_CCC.text = questions[self.question_number].options[2]
        self.manager.get_screen("game_screen").ids.my_button_CCC.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_CCC.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_CCC.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_CCC.elevation = 3

    def set_answers_D_gamescreen(self, delay=7):
        self.manager.get_screen("game_screen").ids.my_button_DDD.text = questions[self.question_number].options[3]
        self.manager.get_screen("game_screen").ids.my_button_DDD.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_DDD.on_active = False
        self.manager.get_screen("game_screen").ids.my_button_DDD.md_bg_color = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_DDD.elevation = 3

    def set_answers_undisabled_gamescreen(self, delay=8):
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled = False
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled = False
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled = False
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled = False

    # Kérdés beállítása
    def set_questions_gamescreen(self, delay=3):
        self.randomize_questions()
        if len(questions[self.question_number].question) > 70:
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 14
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[
                self.question_number].question
        elif len(questions[self.question_number].question) > 140:
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 13
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[
                self.question_number].question
        else:
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.font_size = 16
            self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = questions[
                self.question_number].question
    ######################################

    def set_scoreboard_gamescreen(self):
        self.manager.get_screen("game_screen").ids.label_score_gamescreen.text = str(0)
        self.manager.get_screen("game_screen").ids.sum_label_questions_gamescreen.text = str(0)

    def set_quotes_gamescreen(self, delay=3):
        number = random.randint(0,39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("game_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("game_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("game_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("game_screen").ids.my_quote_author.text = quotes_authors[number]

    def set_the_pause_on(self, delay_button_color):
        self.manager.get_screen("game_screen").ids.pause_gamescreen.disabled = False

    def set_the_pause_off(self, delay):
        self.manager.get_screen("game_screen").ids.pause_gamescreen.disabled = True


    def pause_gamescreen(self):
        global EVENT1
        Clock.unschedule(EVENT1)
        global EVENT2
        Clock.unschedule(EVENT2)
        global EVENT
        Clock.unschedule(EVENT3)
        global EVENT4
        Clock.unschedule(EVENT4)
        global EVENT5
        Clock.unschedule(EVENT5)
        global EVENT6
        Clock.unschedule(EVENT6)
        global EVENT7
        Clock.unschedule(EVENT7)
        global EVENT8
        Clock.unschedule(EVENT8)
        global EVENT9
        Clock.unschedule(EVENT9)
        global EVENT10
        Clock.unschedule(EVENT10)
        global EVENT11
        Clock.unschedule(EVENT11)
        global EVENT12
        Clock.unschedule(EVENT12)
        global EVENT13
        Clock.unschedule(EVENT13)
        global EVENT14
        Clock.unschedule(EVENT14)
        global EVENT15
        Clock.unschedule(EVENT15)
        global EVENT16
        Clock.unschedule(EVENT16)
        global EVENT17
        Clock.unschedule(EVENT17)
        global EVENT18
        Clock.unschedule(EVENT18)
        global EVENT19
        Clock.unschedule(EVENT19)
        global EVENT20
        Clock.unschedule(EVENT20)
        global EVENT21
        Clock.unschedule(EVENT21)
        global EVENT22
        Clock.unschedule(EVENT22)
        global EVENT23
        Clock.unschedule(EVENT23)
        global EVENT24
        Clock.unschedule(EVENT24)
        global EVENT25
        Clock.unschedule(EVENT25)
        global EVENT26
        Clock.unschedule(EVENT26)
        global EVENT27
        Clock.unschedule(EVENT27)
        global EVENT28
        Clock.unschedule(EVENT28)
        global EVENT29
        Clock.unschedule(EVENT29)
        global EVENT30
        Clock.unschedule(EVENT30)
        global EVENT31
        Clock.unschedule(EVENT31)
        global EVENT32
        Clock.unschedule(EVENT32)
        global EVENT33
        Clock.unschedule(EVENT33)
        global EVENT34
        Clock.unschedule(EVENT34)
        global EVENT35
        Clock.unschedule(EVENT35)
        global EVENT36
        Clock.unschedule(EVENT36)
        global EVENT37
        Clock.unschedule(EVENT37)
        global EVENT38
        Clock.unschedule(EVENT38)
        global EVENT39
        Clock.unschedule(EVENT39)
        global EVENT40
        Clock.unschedule(EVENT40)
        global EVENT41
        Clock.unschedule(EVENT41)
        global EVENT42
        Clock.unschedule(EVENT42)
        global EVENT43
        Clock.unschedule(EVENT43)
        global EVENT44
        Clock.unschedule(EVENT44)
        global EVENT45
        Clock.unschedule(EVENT45)
        global EVENT46
        Clock.unschedule(EVENT46)
        global EVENT47
        Clock.unschedule(EVENT47)
        global EVENT48
        Clock.unschedule(EVENT48)
        global EVENT49
        Clock.unschedule(EVENT49)
        global EVENT50
        Clock.unschedule(EVENT50)
        global EVENT51
        Clock.unschedule(EVENT51)
        global EVENT52
        Clock.unschedule(EVENT52)
        global EVENT53
        Clock.unschedule(EVENT53)
        global EVENT54
        Clock.unschedule(EVENT54)
        global EVENT55
        Clock.unschedule(EVENT55)
        global EVENT56
        Clock.unschedule(EVENT56)
        global EVENT57
        Clock.unschedule(EVENT57)
        global EVENT58
        Clock.unschedule(EVENT58)
        global EVENT59
        Clock.unschedule(EVENT59)
        global EVENT60
        Clock.unschedule(EVENT60)
        global EVENT61
        Clock.unschedule(EVENT61)
        global EVENT62
        Clock.unschedule(EVENT62)
        global EVENT63
        Clock.unschedule(EVENT63)
        global EVENT64
        Clock.unschedule(EVENT64)
        global EVENT65
        Clock.unschedule(EVENT65)

        self.manager.get_screen("game_screen").ids.pause_gamescreen.disabled = True
        self.manager.get_screen("game_screen").ids.play_gamescreen.disabled = False

    def resume_gamescreen(self):
        self.manager.get_screen("game_screen").ids.pause_gamescreen.disabled = True
        self.manager.get_screen("game_screen").ids.play_gamescreen.disabled = True

        self.manager.get_screen("game_screen").ids.label_question_gamescreen.text = ""
        self.manager.get_screen("game_screen").ids.my_button_AAA.text = ""
        self.manager.get_screen("game_screen").ids.my_button_BBB.text = ""
        self.manager.get_screen("game_screen").ids.my_button_CCC.text = ""
        self.manager.get_screen("game_screen").ids.my_button_DDD.text = ""
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled = True
        self.manager.get_screen("game_screen").ids.my_button_AAA.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_BBB.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_CCC.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_DDD.md_bg_color_disabled = '#EDF2F4'
        self.manager.get_screen("game_screen").ids.my_button_AAA.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_BBB.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_CCC.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_DDD.disabled_color = '#404040'
        self.manager.get_screen("game_screen").ids.my_button_AAA.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_BBB.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_CCC.elevation = 3
        self.manager.get_screen("game_screen").ids.my_button_DDD.elevation = 3

        number = random.randint(0, 39)
        if len(quotes[number]) > 100:
            self.manager.get_screen("game_screen").ids.my_quote.font_size = 8
            self.manager.get_screen("game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("game_screen").ids.my_quote_author.text = quotes_authors[number]
        else:
            self.manager.get_screen("game_screen").ids.my_quote.font_size = 9
            self.manager.get_screen("game_screen").ids.my_quote.text = quotes[number]
            self.manager.get_screen("game_screen").ids.my_quote_author.text = quotes_authors[number]

        EVENT49 = Clock.schedule_once(self.set_questions_gamescreen, 1)
        EVENT50 = Clock.schedule_once(self.set_answers_A_gamescreen, 5)
        EVENT51 = Clock.schedule_once(self.set_answers_B_gamescreen, 7)
        EVENT52 = Clock.schedule_once(self.set_answers_C_gamescreen, 9)
        EVENT53 = Clock.schedule_once(self.set_answers_D_gamescreen, 11)
        EVENT54 = Clock.schedule_once(self.set_answers_undisabled_gamescreen, 12)
        EVENT55 = Clock.schedule_once(self.play_sound_question_gamescreen, 1)
        EVENT56 = Clock.schedule_once(self.play_sound_button_gamescreen, 5)
        EVENT57 = Clock.schedule_once(self.play_sound_button_gamescreen, 7)
        EVENT58 = Clock.schedule_once(self.play_sound_button_gamescreen, 9)
        EVENT59 = Clock.schedule_once(self.play_sound_button_gamescreen, 11)




class WindowManager(ScreenManager):
    pass




class DesignApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.material_style = "M2"
        self.root = Builder.load_file('JVTrivia_final.kv')



JVTriviaGame = DesignApp()
JVTriviaGame.run()

