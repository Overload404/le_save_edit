from os import listdir
from os.path import join,isfile
import getpass
import json
import dearpygui.dearpygui as dpg
import ast
from func import backup_check,backup,backupexists
available_masteries=[]
# functions go below

jaroslave = {"age":31, "lokh":True}
keep_loop = True
backupdone = False
username = getpass.getuser()
current_level = 1
masteries={"0": {"No mastery":"0","Beastmaster":"1","Shaman":"2","Druid":"3"},"1":{"No mastery":"0","Sorcerer":"1","Spellblade":"2","Runemaster":"3"},"2":{"No mastery":"0","Void Knight":"1","Forge Guard":"2","Paladin":"3"},"3":{"No mastery":"0","Necromancer":"1","Lich":"2","Warlock":"3"}, "4":{"No mastery":"0","Bladedancer":"1","Marksman":"2","Falconer":"3"}}

def change_level_value():
    dpg.set_value("level_value", dpg.get_value("level_slider"))

def change_level_slider():
    dpg.set_value("level_slider",int(dpg.get_value("level_value")))

def load_file():
    chosenfile = ast.literal_eval(dpg.get_value("char_list"))
    for f in saves_list:
        if chosenfile[0]==f["name"] and int(chosenfile[1])==f["level"]:
            global savefilepath
            savefilepath=rf"{saves_path}\{f['file']}"
        else:
            pass
    backupfile=backup_check(savefilepath,backupexists)
    backup(savefilepath,backupfile)
    with open(savefilepath) as f:
        f.read(5)
        global read_file
        read_file = json.load(f)
        global name
        name = read_file["characterName"]
        global current_level
        global character_class
        character_class = str(read_file["characterClass"])
        current_level = read_file["level"]
        dpg.set_value("Character Name", f"Character Name: {name}")
        global available_masteries
        available_masteries=list(masteries[character_class].keys())
        dpg.configure_item("mastery_list",items=available_masteries)


# UI Goes Below

saves_path = rf"C:\Users\{username}\AppData\LocalLow\Eleventh Hour Games\Last Epoch\Saves."
all_files = [f for f in listdir(saves_path) if isfile(join(saves_path,f)) and '1CHARACTERSLOT_BETA_' in f and 'BAK' not in f and 'temp'not in f]
saves_list = []

for savefile in all_files:
    with open(rf"{saves_path}\{savefile}") as f:
        f.read(5)
        try:
            read_file = json.load(f)
            unknown=False
        except:
            unknown=True
        if unknown != True:
            name = read_file["characterName"]
            current_level = read_file["level"]
            saves_list.append({"file":savefile, "name":name, "level":current_level})
        current_level=0

char_list = []
for item in saves_list:
    char_list.append([f"{item['name']}", f"{item['level']}"])

dpg.create_context()
        


def level_button_callback():
    read_file['level'] = dpg.get_value("level_slider")

def save_button_callback():
        with open(savefilepath,'w') as file:
            global epochfile
            epochfile='EPOCH'+ json.dumps(read_file)
            file.write(epochfile)

def skip_button_callback():
    with open(r".\files\all_waypoints") as file:
        value=ast.literal_eval(file.read())
        read_file["unlockedWaypointScenes"] = value
    with open(r".\files\all_quests") as file:
        value=ast.literal_eval(file.read())
        read_file["savedQuests"] = value
    read_file["portalUnlocked"] = True
    read_file["reachedTown"] = True

def mastery_button_callback():
    read_file["chosenMastery"] = int(masteries[character_class][dpg.get_value("mastery_list")])
    read_file["savedCharacterTree"] = {"treeID":"","version":0,"nodeIDs":[],"nodePoints":[],"unspentPoints":0,"nodesTaken":[]}

def skill_reset_button_callback():
    read_file["savedCharacterTree"] = {"treeID":"","version":0,"nodeIDs":[],"nodePoints":[],"unspentPoints":0,"nodesTaken":[]}
    

    

with dpg.window(tag="Primary Window"):
    dpg.add_text("Select Savefile:", tag="combo_label")
    dpg.add_combo(items=char_list, tag="char_list")
    dpg.add_button(label="Load", tag="load_button", callback=load_file)
    
    dpg.add_separator()

    dpg.add_text(f"Character Name: ", tag="Character Name")
    dpg.add_slider_int(label="", callback=change_level_value, tag="level_slider", max_value=100, min_value=1)
    dpg.add_input_int(label="Level",callback=change_level_slider, tag="level_value", min_value=1, max_value=100, min_clamped=True, max_clamped=True,default_value=current_level)
    dpg.add_button(label="Set Level", tag="level_button", callback=level_button_callback)
    
    dpg.add_separator()

    dpg.add_button(label="Skip Story", tag="skip_button", callback=skip_button_callback)
    
    dpg.add_separator()

    dpg.add_combo(tag="mastery_list", items=[])
    dpg.add_button(label ="Reset Mastery", tag="mastery_button", callback=mastery_button_callback)
    dpg.add_button(label="Reset Skill Points", tag="skill_reset_button",callback=skill_reset_button_callback)
    
    dpg.add_separator()

    dpg.add_button(label="Save File", tag="save_button", callback=save_button_callback)
    


dpg.create_viewport(title='Le Save Edit', width=500, height=400, resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()