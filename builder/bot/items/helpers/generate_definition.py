item_name = input("Name of the item? ")
template = """
name: {0}
rarity: Common
price: 100
image: builder/bot/items/images/{0}/normal.svg
colors:
  - white:
    - RGB: !!python/tuple [255, 255, 255]
    - image: builder/bot/items/images/{0}/white.png

  - black:
    - RGB: !!python/tuple [0, 0, 0]
    - image: builder/bot/items/images/{0}/black.png

  - blue:
    - RGB: !!python/tuple []
    - image: builder/bot/items/images/{0}/blue.png

  - pink:
    - RGB: !!python/tuple [237, 163, 255]
    - image: builder/bot/items/images/{0}/pink.png

  - green:
    - RGB: !!python/tuple [97, 176, 18]
    - image: builder/bot/items/images/{0}/green.png
"""

with open(f"builder/bot/items/definitions/{item_name}.yml", "w+") as f:
    f.write(
        template.format(item_name).strip()
    )