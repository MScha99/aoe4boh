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


worker_location_on_screen = {
    "population": {
        "x": (31 / 1920) * 100,
        "y": (855 / 1080) * 100,
        "width": (70 / 1920) * 100,
        "height": (25 / 1080) * 100
    },
    "idle_worker": {
        "x": (135 / 1920) * 100,
        "y": (852 / 1080) * 100,
        "width": (40 / 1920) * 100,
        "height": (27 / 1080) * 100
    },

    "food_worker": {
        "x": (136 / 1920) * 100,
        "y": (908 / 1080) * 100,
        "width": (45 / 1920) * 100,
        "height": (26 / 1080) * 100
    },

    "wood_worker": {
        "x": (136 / 1920) * 100,
        "y": (949 / 1080) * 100,
        "width": (45 / 1920) * 100,
        "height": (26 / 1080) * 100
    },

    "gold_worker": {
        "x": (136 / 1920) * 100,
        "y": (989 / 1080) * 100,
        "width": (45 / 1920) * 100,
        "height": (26 / 1080) * 100
    },

    "stone_worker": {
        "x": (136 / 1920) * 100,
        "y": (1026 / 1080) * 100,
        "width": (45 / 1920) * 100,
        "height": (26 / 1080) * 100
    }
}

resource_location_on_screen = {

    "food": {
        "x": (33 / 1920) * 100,
        "y": (911 / 1080) * 100,
        "width": (60 / 1920) * 100,
        "height": (30 / 1080) * 100
    },

    "wood": {
        "x": (33 / 1920) * 100,
        "y": (952 / 1080) * 100,
        "width": (60 / 1920) * 100,
        "height": (30 / 1080) * 100
    },

    "gold": {
        "x": (33 / 1920) * 100,
        "y": (993 / 1080) * 100,
        "width": (60 / 1920) * 100,
        "height": (30 / 1080) * 100
    },

    "stone": {
        "x": (33 / 1920) * 100,
        "y": (1031 / 1080) * 100,
        "width": (60 / 1920) * 100,
        "height": (30 / 1080) * 100
    },

}

# worker_location_on_screen = {
#     "population": {
#         "x": 1.0270270270270245,
#         "y": 1.4563106796116916,
#         "width": 42.7837837837838,
#         "height": 12.135922330097086
#     },
#     "idle_worker": {
#         "x": 68.91891891891892,
#         "y": 0.0,
#         "width": 27.027027027027028,
#         "height": 13.106796116504855
#     },
#     "food_worker": {
#         "x": 69.59459459459461,
#         "y": 27.184466019417574,
#         "width": 30.40540540540541,
#         "height": 12.62135922330097
#     },
#     "wood_worker": {
#         "x": 69.59459459459461,
#         "y": 45.08737864077677,
#         "width": 30.40540540540541,
#         "height": 12.62135922330097
#     },
#     "gold_worker": {
#         "x": 69.59459459459461,
#         "y": 64.99029126213595,
#         "width": 30.40540540540541,
#         "height": 12.62135922330097
#     },
#     "stone_worker": {
#         "x": 69.59459459459461,
#         "y": 83.43689320388353,
#         "width": 30.40540540540541,
#         "height": 12.62135922330097
#     }
# }

# resource_location_on_screen = {
#     "food": {
#         "x": 0.0,
#         "y": 27.184466019417574,
#         "width": 40.54054054054055,
#         "height": 14.563106796116504
#     },
#     "wood": {
#         "x": 0.0,
#         "y": 47.08737864077677,
#         "width": 40.54054054054055,
#         "height": 14.563106796116504
#     },
#     "gold": {
#         "x": 0.0,
#         "y": 66.99029126213595,
#         "width": 40.54054054054055,
#         "height": 14.563106796116504
#     },
#     "stone": {
#         "x": 0.0,
#         "y": 85.43689320388353,
#         "width": 40.54054054054055,
#         "height": 14.563106796116504
#     }
# }