# get_colors() and save_palette() by https://gist.github.com/zollinger/1722663

from PIL import Image, ImageDraw
import argparse
import sys


def get_colors(image_file, numcolors=3, resize=150):
    # Resize image to speed up processing
    img = Image.open(image_file)
    img = img.copy()
    img.thumbnail((resize, resize))

    # Reduce to palette
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=numcolors)

    # Find dominant colors
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    colors = list()
    for i in range(numcolors):
        palette_index = color_counts[i][1]
        dominant_color = palette[palette_index*3:palette_index*3+3]
        colors.append(tuple(dominant_color))

    return colors


def save_palette(colors, swatchsize=20, outfile="palette.png" ):
    num_colors = len(colors)
    palette = Image.new('RGB', (swatchsize*num_colors, swatchsize))
    draw = ImageDraw.Draw(palette)

    posx = 0
    for color in colors:
        draw.rectangle([posx, 0, posx+swatchsize, swatchsize], fill=color) 
        posx = posx + swatchsize

    del draw
    palette.save(outfile, "PNG")
    

def get_brightest_color(f) -> tuple:
    colors = get_colors(f)
    # finds color vector with biggest difference between values
    brightest = {"color": (0, 0, 0), "m": 0}
    for c in colors:
        m = max(c)
        for i in c:
            if max([m-c[0], m-c[1], m-c[2]]) > brightest["m"]:
                brightest["color"] = c
                brightest["m"] = m

    return brightest["color"]

            

if __name__ == '__main__':
    color = get_brightest_color("./2.png")
    print(color)

    