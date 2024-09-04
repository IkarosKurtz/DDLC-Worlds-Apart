# Rain Effect

image small_raindrop:
  subpixel True
  "mod_assets/effects/rain/raindrop.png"
  zoom .5

image normal_raindrop:
  subpixel True
  "mod_assets/effects/rain/raindrop.png"
  zoom .65

image large_raindrop:
  subpixel True
  "mod_assets/effects/rain/raindrop.png"
  zoom .80

image eff_rain:
  truecenter
  subpixel True
  yzoom 1.6
  xzoom 1.2

  contains:
    SnowBlossom("large_raindrop", 20, 60, (30, 100), (1400, 1600))
  contains:
    SnowBlossom("normal_raindrop", 50, 60, (50, 100), (1200, 1400))
    alpha .8
  contains:
    SnowBlossom("small_raindrop", 120, 60, (25, 50), (1000, 1200))
    alpha .5
  
  rotate 20.0

screen rain:
  add "eff_rain"

screen stormy:
  add "eff_rain"
  add "eff_rain"

# Snow Effect

image snow_particle:
  subpixel True
  "mod_assets/effects/snowflake/snowflake.png"
  zoom .35

image eff_snow:
  truecenter
  subpixel True

  contains:
    SnowBlossom("snow_particle", 80, 60, (10, 100), (100, 200))
    alpha .8
  contains:
    SnowBlossom("snow_particle", 150, 60, (-10, -100), (200, 300))

screen snow:
  add "eff_snow"

# Thunder Effect

image thunder:
  # A white background
  '#fff'

  alpha .8

  linear 1.0 alpha 0.0
