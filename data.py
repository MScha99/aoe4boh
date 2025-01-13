import cv2
IMAGES = "assets/images/"

# Define civilization names and their corresponding images
civ_data = [
    ("Abbasid Dynasty", cv2.imread(IMAGES + "abbas.png")),
    ("Ayyubids", cv2.imread(IMAGES + "ayyu.png")),
    ("Byzantines", cv2.imread(IMAGES + "byz.png")),
    ("Chinese", cv2.imread(IMAGES + "ch.png")),
    ("Delhi Sultanate", cv2.imread(IMAGES + "delhi.png")),
    ("English", cv2.imread(IMAGES + "eng.png")),
    ("French", cv2.imread(IMAGES + "fren.png")),
    ("Holy Roman Empire", cv2.imread(IMAGES + "hre.png")),
    ("Japanese", cv2.imread(IMAGES + "jap.png")),
    ("Jeanne d'Arc", cv2.imread(IMAGES + "jean.png")),
    ("Mali", cv2.imread(IMAGES + "mali.png")),
    ("Mongols", cv2.imread(IMAGES + "mong.png")),
    ("Order of the Dragon", cv2.imread(IMAGES + "ootd.png")),
    ("Ottomans", cv2.imread(IMAGES + "otto.png")),
    ("Rus", cv2.imread(IMAGES + "rus.png")),
    ("Zhu Xi's Legacy", cv2.imread(IMAGES + "zhu.png"))
]

# Define villager names and their corresponding images
vil_data = [
    ("Abbasid Villager", cv2.imread(IMAGES + "abbas_vil.png")),
    ("Ayyubid Villager", cv2.imread(IMAGES + "ayyu_vil.png")),
    ("Byzantine Villager", cv2.imread(IMAGES + "byz_vil.png")),
    ("Chinese Villager", cv2.imread(IMAGES + "ch_vil.png")),
    ("Delhi Villager", cv2.imread(IMAGES + "delhi_vil.png")),
    ("English Villager", cv2.imread(IMAGES + "eng_vil.png")),
    ("French Villager", cv2.imread(IMAGES + "fren_vil.png")),
    ("Holy Roman Empire Villager", cv2.imread(IMAGES + "hre_vil.png")),
    ("Japanese Villager", cv2.imread(IMAGES + "jap_vil.png")),
    ("Jeanne d'Arc Villager", cv2.imread(IMAGES + "jean_vil.png")),
    ("Mali Villager", cv2.imread(IMAGES + "mali_vil.png")),
    ("Mongol Villager", cv2.imread(IMAGES + "mong_vil.png")),
    ("Order of the Dragon Villager", cv2.imread(IMAGES + "ootd_vil.png")),
    ("Ottoman Villager", cv2.imread(IMAGES + "otto_vil.png")),
    ("Rus Villager", cv2.imread(IMAGES + "rus_vil.png")),
    ("Zhu Xi's Legacy Villager", cv2.imread(IMAGES + "zhu_vil.png"))
]