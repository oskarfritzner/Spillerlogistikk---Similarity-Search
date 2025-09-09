# Role-specific feature weightings for outfield players
# These are used to guide the similarity search towards relevant attributes

# 🎯 Central Attacking Midfielder (CAM)
cam_profile = {
    'pace': 0.15,
    'shooting': 0.1,
    'passing': 0.3,
    'dribbling': 0.3,
    'defending': 0.05,
    'physic': 0.1
}

# 🦵 Striker / Center Forward (ST/CF)
st_profile = {
    'pace': 0.25,
    'shooting': 0.4,
    'passing': 0.05,
    'dribbling': 0.2,
    'defending': 0.0,
    'physic': 0.1
}

# ⚔️ Central Defensive Midfielder (CDM)
cdm_profile = {
    'pace': 0.1,
    'shooting': 0.05,
    'passing': 0.2,
    'dribbling': 0.1,
    'defending': 0.35,
    'physic': 0.2
}

# 🏃 Winger (LW/RW)
winger_profile = {
    'pace': 0.35,
    'shooting': 0.1,
    'passing': 0.15,
    'dribbling': 0.3,
    'defending': 0.0,
    'physic': 0.1
}

# 🛡️ Center Back (CB)
cb_profile = {
    'pace': 0.05,
    'shooting': 0.0,
    'passing': 0.05,
    'dribbling': 0.0,
    'defending': 0.5,
    'physic': 0.35,
    'height_cm': 0.15
}

# 🏃‍♂️ Full Back / Wing Back (LB/RB/LWB/RWB)
fullback_profile = {
    'pace': 0.25,
    'shooting': 0.0,
    'passing': 0.15,
    'dribbling': 0.15,
    'defending': 0.3,
    'physic': 0.15
}

# 🧠 Box-to-Box Midfielder (CM)
cm_profile = {
    'pace': 0.15,
    'shooting': 0.1,
    'passing': 0.25,
    'dribbling': 0.2,
    'defending': 0.15,
    'physic': 0.15
}

# Dictionary
role_profiles = {
    "cam": cam_profile,
    "cb": cb_profile,
    "st": st_profile,
    "winger": winger_profile,
    "cdm": cdm_profile,
    "cm": cm_profile,
    "fullback": fullback_profile,
    "gk": None  # No weights needed for GK
}