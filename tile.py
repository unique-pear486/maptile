#!//usr/bin/env python
import argparse
import os
from PIL import Image


def tile_map(mapname, overlayname, min_level, max_level):
    """
    Split a map image (with overlay) into tiles

    Args:
        mapname (str): the prefix for the map file(s). They should be in the
            form mapname_zoomlevel.png. e.g. map_0.png, map_1.png
            If a file does not exist for a given zoom level, it will use the
            previous zoom level instead.
        overlayname (str): prefix for overlay files(s).
        min_level (int): the minimun zoom level to generate. A map and overlay
            file *must* exist for this level
        max_level (int): the maximum level to generate.

    """

    map_ = None
    overlay = None

    # for each zoom level
    for l in range(min_level, max_level):
        # Check if we have a background map_ or overlay for this zoom level, if
        # not we use the one from the last level
        if os.path.isfile("{0}_{1}.png".format(mapname, l)):
            map_ = Image.open("{0}_{1}.png".format(mapname, l)).convert("RGBA")
        if os.path.isfile("{0}_{1}.png".format(overlayname, l)):
            overlay = Image.open("{0}_{1}.png".format(overlayname, l))
        if map_ is None or overlay is None:
            print("image not found")
            return 1

        # create the overall image and scale it to the final size
        out = Image.alpha_composite(map_, overlay)
        out = out.resize((256 * (2**l), 256 * (2**l)), Image.ANTIALIAS)

        # Save each of the tiles
        for x in range(0, 2**l):
            for y in range(0, 2**l):
                # make the directory
                try:
                    os.makedirs("{0}/{1}/".format(l, x))
                except OSError as e:
                    if e.errno != 17:
                        raise
                (out
                    .crop((x * 256, y * 256, (x+1) * 256, (y+1) * 256))
                    .save("{0}/{1}/{2}.png".format(l, x, y), optimize=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Split a map (with overlay) into tiles")
    parser.add_argument("map_prefix",
                        help="The map file prefix i.e. prefix_0.png")
    parser.add_argument("overlay_prefix",
                        help="The overly file prefix i.e. prefix_0.png")
    parser.add_argument("min_zoom",
                        help="The minimum zoom level. Map and overlay must "
                        "exist at this level",
                        type=int)
    parser.add_argument("max_zoom",
                        help="The maximum zoom level",
                        type=int)
    args = parser.parse_args()
    tile_map(args.map_prefix, args.overlay_prefix,
             args.min_zoom, args.max_zoom)
