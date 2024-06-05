import levelparser
import sys
from PIL import Image#, ImageFont, ImageDraw
import numpy as np

def paste_subarray(arr1, arr2, start_row, start_col, start_row_arr2, start_col_arr2, end_row_arr2, end_col_arr2):
    rows_arr2 = end_row_arr2 - start_row_arr2 + 1
    cols_arr2 = end_col_arr2 - start_col_arr2 + 1

    for i in range(rows_arr2):
        for j in range(cols_arr2):
            if start_row + i < len(arr1) and start_col + j < len(arr1[0]) and start_row_arr2 + i < len(arr2) and start_col_arr2 + j < len(arr2[0]):
                arr1[start_row + i][start_col + j] = arr2[start_row_arr2 + i][start_col_arr2 + j]

    return arr1

#font = ImageFont.truetype("sans-serif.ttf", 16)
requestedfile = sys.argv[1]
leveldata = levelparser.parse_binary_file(requestedfile)
for obj in leveldata:
    print(obj)
desired_color = (0x92, 0x90, 0xff)
if(leveldata[0]['backdrop'] in ['Snowy Night', 'Fully Gray Night', 'Night Default',]):
    desired_color = (0x00,0x00,0x00)
image = Image.new(mode="RGBA", size=((int(leveldata[-1]['total_pages']) + 1) * 256, 240), color=desired_color)
bg = Image.open(f"backgrounds\\{leveldata[0]['background']}.png")
for i in range(0, image.width, bg.width):
    image.paste(bg, (i, 32), bg)
level_array = []
for i in range(15):

    level_array.append(np.full((1, int(image.width / 16)), leveldata[0]['floor_pattern'][i]).tolist()[0])

tile_size = 16

tile_images = {
    0: Image.open('chunkids/0.png'),
    1: Image.open('chunkids/1.png'),
    2: Image.open('chunkids/2.png'),
    3: Image.open('chunkids/3.png'),
    4: Image.open('chunkids/4.png'),
    5: Image.open('chunkids/5.png'),
    6: Image.open('chunkids/6.png'),
    7: Image.open('chunkids/7.png'),
    8: Image.open('chunkids/8.png'),
    9: Image.open('chunkids/9.png'),
    9: Image.open('chunkids/9.png'),
    10: Image.open('chunkids/10.png'),
    11: Image.open('chunkids/11.png'),
    12: Image.open('chunkids/12.png'),
    13: Image.open('chunkids/13.png'),
    14: Image.open('chunkids/14.png'),
    15: Image.open('chunkids/15.png'),
    16: Image.open('chunkids/16.png'),
    17: Image.open('chunkids/17.png'),
    18: Image.open('chunkids/18.png'),
    19: Image.open('chunkids/19.png'),
    20: Image.open('chunkids/20.png'),
    21: Image.open('chunkids/21.png'),
    22: Image.open('chunkids/22.png'),
    23: Image.open('chunkids/23.png'),
    24: Image.open('chunkids/24.png'),
    25: Image.open('chunkids/25.png'),
}
castle_tiledata = [
    [00,19,19,19,00],
    [00,22,23,24,00],
    [19,20,20,20,19],
    [23,23,21,23,23],
    [23,23,25,23,23],
    [20,20,20,20,20],
    [23,21,23,21,23],
    [23,25,23,25,23],
    [20,20,20,20,20],
    [21,23,21,23,21],
    [25,23,25,23,25],
]


for object in leveldata:

    if object != leveldata[0] and object != leveldata[-1]:
        #draw = ImageDraw.Draw(image)
        #draw.text((object['x_pos'] * 16, (object['y_pos']) * 16),f"{object['raw_data'][0] + object['raw_data'][1] }",(255,255,255),font=font)
        if(object["obj_type"] == 0):
            object['y_pos'] += 2
            if(object['obj_size'] in [0b0000, 0b0001, 0b0010, 0b011]):
                level_array[object['y_pos']][object['x_pos']] = 3
            elif (object['obj_size'] in [0b0100, 0b0101, 0b0110, 0b0111, 0b1000]):
                level_array[object['y_pos']][object['x_pos']] = 2
            elif object['obj_size'] == 0b1010:
                try:
                    level_array[object['y_pos']][object['x_pos']] = 10
                except:
                    break
            elif object['obj_size'] == 0b1100:
                try:
                    #im not sure if this is accurate i did it by memory
                    values = [
                        [5, 6],
                        [7, 8],
                        [14, 8],
                        [16, 8]
                    ]

                    for dy, row in enumerate(values):
                        for dx, val in enumerate(row):
                            level_array[object['y_pos'] + dy][object['x_pos'] + 2 + dx] = val

                    level_array[object['y_pos'] + 2][object['x_pos']] = 11
                    level_array[object['y_pos'] + 3][object['x_pos']] = 12
                    level_array[object['y_pos'] + 2][object['x_pos'] + 1] = 12
                    level_array[object['y_pos'] + 3][object['x_pos'] + 1] = 15
                except:
                    break
            elif object['obj_size'] == 0b1001:
                    try:
                        level_array[object['y_pos']][object['x_pos']] = 11
                        level_array[object['y_pos'] + 1][object['x_pos']] = 12
                    except:
                        break
            

            object['y_pos'] -= 2
        if(object['y_pos'] > 11):
            if(object['y_pos'] == 0b1100):
                match object['obj_type']:
                    case 0: # HOLE
                        for i in range(object['obj_size'] + 1):
                            if(object['x_pos'] + i < len(level_array[0])):
                                for j in range(5):
                                    if(object['y_pos'] + j < len(level_array)):
                                        try:
                                            level_array[object['y_pos'] + j][object['x_pos'] + i] = 0
                                        except:
                                            continue
                    case 0b110:
                        for i in range(object['obj_size'] + 1):
                            if(object['x_pos'] + i < len(level_array[0])):
                                level_array[3 + 2][object['x_pos'] + i] = 3
                    case 0b111:
                        for i in range(object['obj_size'] + 1):
                            if(object['x_pos'] + i < len(level_array[0])):
                                level_array[7 + 2][object['x_pos'] + i] = 3
            elif(object['y_pos'] == 0b1111):
                match object['obj_type']:
                    case 3: # Stairs
                        max_height = 8
                        for i in range(object['obj_size'] + 1):
                            for j in range(min(i + 1, max_height)):
                                try:
                                    level_array[12 - j][object['x_pos'] + i] = 4
                                except:
                                    continue
                    case 2:
                        paste_subarray(level_array, castle_tiledata, (object['obj_size'] - 2) + 4, object['x_pos'], 0, 0, object['obj_size'] - 2, 5)
            elif object['y_pos'] == 0b1101:
                level_array[2][object['x_pos']] = 17
                for i in range(9):
                    level_array[3 + i][object['x_pos']] = 18
                level_array[3 + 9][object['x_pos']] = 4
        else:
            object['y_pos'] += 2
            match object['obj_type']:
                case 2: # Bricks HOR ROW
                    for i in range(object['obj_size'] + 1):
                        if(object['x_pos'] + i < len(level_array[0])):
                            level_array[object['y_pos']][object['x_pos'] + i] = 2
                case 7: # Pipe 
                    if(object['obj_size'] > 10):
                        object['obj_size'] = object['obj_size'] & 0b0111
                    level_array[object['y_pos']][object['x_pos']] = 5
                    if(object['x_pos'] + 1 < len(level_array[0])):
                        level_array[object['y_pos']][object['x_pos'] + 1] = 6
                    for i in range(object['obj_size']):
                        if(object['y_pos'] + 1 + i < len(level_array)):
                            level_array[object['y_pos'] + i + 1][object['x_pos']] = 7
                        if(object['x_pos'] + 1 < len(level_array[0]) and object['y_pos'] + 1 + i < len(level_array)):
                            level_array[object['y_pos'] + i + 1][object['x_pos'] + 1] = 8
                case 4: # Coins HOR ROW
                    for i in range(object['obj_size'] + 1):
                        if(object['x_pos'] + i < len(level_array[0])):
                            level_array[object['y_pos']][object['x_pos'] + i] = 9
                case 3: # Square Blocks HOR ROW
                    for i in range(object['obj_size'] + 1):
                        if(object['x_pos'] + i < len(level_array[0])):
                            level_array[object['y_pos']][object['x_pos'] + i] = 4
                case 6: # Square Blocks VER COL
                    for i in range(object['obj_size'] + 1):
                        if(object['y_pos'] + i < len(level_array)):
                            level_array[object['y_pos'] + i][object['x_pos']] = 4
                case 5: # Bricks VER COL
                    for i in range(object['obj_size'] + 1):
                        if(object['y_pos'] + i < len(level_array)):
                            level_array[object['y_pos'] + i][object['x_pos']] = 2


for row in range(len(level_array)):
    for col in range(len(level_array[row])):
        tile_type = level_array[row][col]
        if(int(tile_type) == 0):
            continue
        tile_img = tile_images[int(tile_type)]
        x0 = col * tile_size
        y0 = row * tile_size
        image.paste(tile_img.convert("RGBA"), (x0, y0), tile_img.convert("RGBA"))

image.show()
image.save('output.png')