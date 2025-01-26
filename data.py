import cv2
IMAGES = "assets/images/"

# Define civilization names and their corresponding images
# civ_data = [
#     ("Abbasid Dynasty", cv2.imread(IMAGES + "abbas.png")),
#     ("Ayyubids", cv2.imread(IMAGES + "ayyu.png")),
#     ("Byzantines", cv2.imread(IMAGES + "byz.png")),
#     ("Chinese", cv2.imread(IMAGES + "ch.png")),
#     ("Delhi Sultanate", cv2.imread(IMAGES + "delhi.png")),
#     ("English", cv2.imread(IMAGES + "eng.png")),
#     ("French", cv2.imread(IMAGES + "fren.png")),
#     ("Holy Roman Empire", cv2.imread(IMAGES + "hre.png")),
#     ("Japanese", cv2.imread(IMAGES + "jap.png")),
#     ("Jeanne d'Arc", cv2.imread(IMAGES + "jean.png")),
#     ("Mali", cv2.imread(IMAGES + "mali.png")),
#     ("Mongols", cv2.imread(IMAGES + "mong.png")),
#     ("Order of the Dragon", cv2.imread(IMAGES + "ootd.png")),
#     ("Ottomans", cv2.imread(IMAGES + "otto.png")),
#     ("Rus", cv2.imread(IMAGES + "rus.png")),
#     ("Zhu Xi's Legacy", cv2.imread(IMAGES + "zhu.png"))
# ]

# # Define villager names and their corresponding images
# vil_data = [
#     ("Abbasid Villager", cv2.imread(IMAGES + "abbas_vil.png")),
#     ("Ayyubid Villager", cv2.imread(IMAGES + "ayyu_vil.png")),
#     ("Byzantine Villager", cv2.imread(IMAGES + "byz_vil.png")),
#     ("Chinese Villager", cv2.imread(IMAGES + "ch_vil.png")),
#     ("Delhi Villager", cv2.imread(IMAGES + "delhi_vil.png")),
#     ("English Villager", cv2.imread(IMAGES + "eng_vil.png")),
#     ("French Villager", cv2.imread(IMAGES + "fren_vil.png")),
#     ("Holy Roman Empire Villager", cv2.imread(IMAGES + "hre_vil.png")),
#     ("Japanese Villager", cv2.imread(IMAGES + "jap_vil.png")),
#     ("Jeanne d'Arc Villager", cv2.imread(IMAGES + "jean_vil.png")),
#     ("Mali Villager", cv2.imread(IMAGES + "mali_vil.png")),
#     ("Mongol Villager", cv2.imread(IMAGES + "mong_vil.png")),
#     ("Order of the Dragon Villager", cv2.imread(IMAGES + "ootd_vil.png")),
#     ("Ottoman Villager", cv2.imread(IMAGES + "otto_vil.png")),
#     ("Rus Villager", cv2.imread(IMAGES + "rus_vil.png")),
#     ("Zhu Xi's Legacy Villager", cv2.imread(IMAGES + "zhu_vil.png"))
# ]


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

    # "gold_worker": {
    #     "x": (136 / 1920) * 100,
    #     "y": (989 / 1080) * 100,
    #     "width": (45 / 1920) * 100,
    #     "height": (26 / 1080) * 100
    # },
    "gold_worker": {
        "x": (136 / 1920) * 100,
        "y": (984 / 1080) * 100,
        "width": (45 / 1920) * 100,
        "height": (30 / 1080) * 100
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


villager_distinct_pixels = [
    (0, 0, (38, 25, 22)),    # Reference point (top-left)
    (20, 1, (81, 61, 47)),   # Relative to reference point
    (27, 3, (59, 43, 34)),   # Relative to reference point
    (35, 31, (36, 24, 21)),  # Relative to reference point
]

sample_build_order = [
    {
        "instructions": "Step 1: Early Food Focus",
        "desired_food_workers": 8,
        "desired_wood_workers": 4,
        "desired_gold_workers": 0,
        "desired_stone_workers": 0
    },
    {
        "instructions": "Step 2: Transition to Wood",
        "desired_food_workers": 6,
        "desired_wood_workers": 8,
        "desired_gold_workers": 0,
        "desired_stone_workers": 0
    },
    {
        "instructions": "Step 3: Gold for Age-Up",
        "desired_food_workers": 6,
        "desired_wood_workers": 6,
        "desired_gold_workers": 4,
        "desired_stone_workers": 0
    }
]