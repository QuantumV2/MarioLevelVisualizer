import levelparser
import sys

if sys.platform != 'emscripten':

    from levelparser import floor_pattern_names
else:
    pass

from PIL import Image, ImageDraw#, ImageFont
import numpy as np
import os
import random

def paste_subarray(arr1, arr2, start_row, start_col, start_row_arr2, start_col_arr2, end_row_arr2, end_col_arr2):
    rows_arr2 = end_row_arr2 - start_row_arr2 + 1
    cols_arr2 = end_col_arr2 - start_col_arr2 + 1

    for i in range(rows_arr2):
        for j in range(cols_arr2):
            if start_row + i < len(arr1) and start_col + j < len(arr1[0]) and start_row_arr2 + i < len(arr2) and start_col_arr2 + j < len(arr2[0]):
                arr1[start_row + i][start_col + j] = arr2[start_row_arr2 + i][start_col_arr2 + j]

    return arr1

#font = ImageFont.truetype("C:\\Users\\\\AppData\\Local\\Microsoft\\Windows\\Fonts\\ARCADECLASSIC.TTF", 16)

if sys.platform != 'emscripten':
    requestedfile = sys.argv[1]
    leveldata = levelparser.parse_binary_file(requestedfile, int(sys.argv[2]) if len(sys.argv) > 2 else 0, int(sys.argv[3]) if len(sys.argv) > 3 else -1)
else:
    leveldata = levelparser.parse_binary_file('_pyodide_arg0_replace_', '_pyodide_arg1_replace_', '_pyodide_arg2_replace_')
print(leveldata[0])
desired_color = (0x92, 0x90, 0xff)
if(leveldata[0]['backdrop'] in ['Snowy Night', 'Fully Gray Night', 'Night Default',]):
    desired_color = (0x00,0x00,0x00)

image = Image.new(mode="RGBA", size=((int(leveldata[-1]['total_pages']) + 2) * 256, 240), color=desired_color)
bg = Image.open(os.path.join("backgrounds", f"{leveldata[0]['background']}.png"))
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
    26: Image.open('chunkids/26.png'),
    27: Image.open('chunkids/27.png'),
    28: Image.open('chunkids/28.png'),
    29: Image.open('chunkids/29.png'),
    30: Image.open('chunkids/30.png'),
    31: Image.open('chunkids/31.png'),
    32: Image.open('chunkids/32.png'),
    33: Image.open('chunkids/33.png'),
    34: Image.open('chunkids/34.png'),
    35: Image.open('chunkids/35.png'),
    36: Image.open('chunkids/36.png'),
    37: Image.open('chunkids/37.png'),
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
    [23,23,23,23,23],
    [21,23,21,23,21],
    [25,23,25,23,25],
]


for object in leveldata:

    if object != leveldata[0] and object != leveldata[-1]:
        if object['y_pos'] > 11:
            if object['y_pos'] == 14:
                if (object['obj_type'] >> 2) & 0b001 == 1:
                    if object['obj_size'] & 0b0111 == 0b010:
                        x_start = ((object['x_pos'] + 1) * 16)
                        x_stop = image.width
                        for check_obj in leveldata:
                            if check_obj != leveldata[0] and check_obj != leveldata[-1]:
                                if check_obj['y_pos'] == 14:
                                
                                    if ((check_obj['obj_type'] >> 2) & 0b001 == 1) and check_obj['x_pos'] > object['x_pos'] and check_obj['obj_size'] & 0b0111 != object['obj_size'] & 0b0111 and x_stop == image.width:
                                        x_stop = ((check_obj['x_pos'] + 1) * 16)
                        bg = Image.open(os.path.join("backgrounds", "CastleWalls.png"))
                        for i in range(x_start, x_stop, 16):
                            image.paste(bg, (i, 32), bg)
                else:
                    for i in range(len(level_array[0]) - object['x_pos'] - 1):

                        for j in range(15):
                            if(floor_pattern_names[str(object['obj_size'])][j] == '1'):
                                level_array[j][object['x_pos'] + i + 1] = '1'
                            elif int(level_array[j][object['x_pos'] + i]) <= 1:
                                level_array[j][object['x_pos'] + i + 1] = '0 '
            elif(object['y_pos'] == 0b1100):
                match object['obj_type']:
                    case 0: # HOLE
                        for i in range(object['obj_size'] + 1):
                            if(object['x_pos'] + i < len(level_array[0])):
                                for j in range(5):
                                    if(object['y_pos'] - 2 + j < len(level_array)):
                                        try:
                                            level_array[object['y_pos'] - 2 + j][object['x_pos'] + i] = '0'
                                        except:
                                            pass
                    case 0b101: # HOLE with liquid wip
                        for i in range(object['obj_size'] + 1):
                            if(object['x_pos'] + i < len(level_array[0])):
                                for j in range(5):
                                    if(object['y_pos'] - 2 + j < len(level_array)):
                                        try:
                                            level_array[object['y_pos'] - 2 + j][object['x_pos'] + i] = '0'
                                        except:
                                            pass
                    case 0b110:
                        for i in range(object['obj_size'] + 1):
                            if(object['x_pos'] + i < len(level_array[0])):
                                level_array[3 + 2][object['x_pos'] + i] = '3'
                    case 0b111:
                        for i in range(object['obj_size'] + 1):
                            if(object['x_pos'] + i < len(level_array[0])):
                                level_array[7 + 2][object['x_pos'] + i] = '3'
            elif(object['y_pos'] == 0b1111):
                match object['obj_type']:
                    case 4:
                        values = [
                            ['0', '0', '5', '6'],
                            ['0', '0', '7', '8'],
                            ['11', '13', '14', '8'],
                            ['12', '15', '16', '8']
                        ]

                        paste_subarray(level_array, values, 6, object['x_pos'], 0,0,3,3)
                        for i in range(5):
                            try:
                                level_array[6 - i][object['x_pos'] + 2] = 7
                                level_array[6 - i][object['x_pos'] + 3] = 8
                            except:
                                pass
                    case 3: # Stairs
                        max_height = 8
                        for i in range(object['obj_size'] + 1):
                            for j in range(min(i + 1, max_height)):
                                try:
                                    level_array[12 - j][(object['x_pos']) + i] = '4'
                                except:
                                    pass
                    case 2:
                        paste_subarray(level_array, castle_tiledata, (13 - (len(castle_tiledata) - object['obj_size'])) , object['x_pos'], 0, 0, len(castle_tiledata) - object['obj_size'] - 1, 5)
            elif object['y_pos'] == 0b1101:
                try:
                    subtype = object['obj_type'] >> 2 & 0b001
                    subsubtype = object['obj_size']
                    #print(bin(subtype), bin(subsubtype), bin(object['obj_type']), bin(object['obj_size']))
                    if(subtype == 1):
                        match subsubtype:
                            case 0b0001:
                                level_array[2][object['x_pos']] = '17'
                                for i in range(9):
                                    level_array[3 + i][object['x_pos']] = '18'
                                level_array[3 + 9][object['x_pos']] = '4'
                            case 0:
                                values = [
                                    ['0', '0', '5', '6'],
                                    ['0', '0', '7', '8'],
                                    ['11', '13', '14', '8'],
                                    ['12', '15', '16', '8']
                                ]

                                paste_subarray(level_array, values, 9, object['x_pos'], 0,0,3,3)
                except:
                    pass

        elif(object["obj_type"] == 0):
            object['y_pos'] += 2
            if(object['obj_size'] in [0b0000, 0b0001, 0b0010, 0b011]):
               if object['y_pos']  < len(level_array):
                try:
                    level_array[object['y_pos']][object['x_pos']] = '3'
                except:
                    pass
                
            elif (object['obj_size'] in [0b0100, 0b0101, 0b0110, 0b0111, 0b1000]):
                if object['y_pos']  < len(level_array):
                    try:
                        level_array[object['y_pos']][object['x_pos']] = '2'
                    except:
                        pass
            elif object['obj_size'] == 0b1010:
                try:
                    level_array[object['y_pos']][object['x_pos']] = '10'
                except:
                    pass
            elif object['obj_size'] == 0b1001:
                    try:
                        level_array[object['y_pos']][object['x_pos']] = '11'
                        level_array[object['y_pos'] + 1][object['x_pos']] = '12'
                    except:
                        pass
            

            object['y_pos'] -= 2



        else:
            object['y_pos'] += 2
            try:
                match object['obj_type']:
                    case 1:
                        if(leveldata[0]['tile_and_special_platform'] in ['Normal Block, Green Pipe, Tree', 'Cloud Block, Green Pipe, Tree']):
                            for i in range(object['obj_size'] + 1):
                                if(object['x_pos'] + i < len(level_array[0])):
                                    if(i == 0):
                                        level_array[object['y_pos']][object['x_pos'] + i] = '26'
                                    elif(i == object['obj_size']):
                                        level_array[object['y_pos']][object['x_pos'] + i] = '28'
                                    else:
                                        level_array[object['y_pos']][object['x_pos'] + i] = '27'
                                        for j in range(1, len(level_array) - object['y_pos']):
                                            if(level_array[object['y_pos'] + j][object['x_pos'] + i] not in ['26', '27', '28']):
                                                level_array[object['y_pos'] + j][object['x_pos'] + i] = '29'
                        elif (leveldata[0]['tile_and_special_platform'] == 'Normal Block, Orange Pipe, Mushroom'):
                            for i in range(object['obj_size'] + 1):
                                if(object['x_pos'] + i < len(level_array[0])):
                                    if(i == 0):
                                        level_array[object['y_pos']][object['x_pos'] + i] = '30'
                                    elif(i == object['obj_size']):
                                        level_array[object['y_pos']][object['x_pos'] + i] = '32'
                                    else:
                                        level_array[object['y_pos']][object['x_pos'] + i] = '31'
                                        for j in range(1, len(level_array) - object['y_pos']):
                                            if(level_array[object['y_pos'] + j][object['x_pos'] + i] not in ['30', '31', '32'] and object['obj_size'] / i == 2):
                                                if(j == 1):
                                                    level_array[object['y_pos'] + j][object['x_pos'] + i] = '33' 
                                                else:
                                                    level_array[object['y_pos'] + j][object['x_pos'] + i] = '34' 
                        else: 
                            for i in range(object['obj_size'] + 1):
                                if(object['y_pos'] + i < len(level_array)):
                                    if(i == 0):
                                        level_array[object['y_pos'] + i][object['x_pos']] = '35'
                                    elif(i == 1):
                                        level_array[object['y_pos'] + i][object['x_pos']] = '36'
                                    else:
                                        level_array[object['y_pos'] + i][object['x_pos']] = '37'
                            
                    case 2: # Bricks HOR ROW
                        for i in range(object['obj_size'] + 1):
                            if(object['x_pos'] + i < len(level_array[0])):
                                level_array[object['y_pos']][object['x_pos'] + i] = '2'
                    case 7: # Pipe 
                        if(object['obj_size'] > 10):
                            object['obj_size'] = object['obj_size'] & 0b0111
                        level_array[object['y_pos']][object['x_pos']] = '5'
                        if(object['x_pos'] + 1 < len(level_array[0])):
                            level_array[object['y_pos']][object['x_pos'] + 1] = '6'
                        for i in range(object['obj_size']):
                            if(object['y_pos'] + 1 + i < len(level_array)):
                                if(int(level_array[object['y_pos'] + i + 1][object['x_pos']]) == 0):
                                    level_array[object['y_pos'] + i + 1][object['x_pos']] = '7'
                            if(object['x_pos'] + 1 < len(level_array[0]) and object['y_pos'] + 1 + i < len(level_array)):
                                if(int(level_array[object['y_pos'] + i + 1][object['x_pos'] + 1]) == 0):
                                    level_array[object['y_pos'] + i + 1][object['x_pos'] + 1] = '8'
                    case 4: # Coins HOR ROW
                        for i in range(object['obj_size'] + 1):
                            if(object['x_pos'] + i < len(level_array[0])):
                                level_array[object['y_pos']][object['x_pos'] + i] = '9'
                    case 3: # Square Blocks HOR ROW
                        for i in range(object['obj_size'] + 1):
                            if(object['x_pos'] + i < len(level_array[0])):
                                level_array[object['y_pos']][object['x_pos'] + i] = '4'
                    case 6: # Square Blocks VER COL
                        for i in range(object['obj_size'] + 1):
                            if(object['y_pos'] + i < len(level_array)):
                                level_array[object['y_pos'] + i][object['x_pos']] = '4'
                    case 5: # Bricks VER COL
                        for i in range(object['obj_size'] + 1):
                            if(object['y_pos'] + i < len(level_array)):
                                level_array[object['y_pos'] + i][object['x_pos']] = '2'
            except:
                pass


for row in range(len(level_array)):
    
    for col in range(len(level_array[row])):
        tile_type = level_array[row][col]
        if(int(tile_type) == 0):
            continue
        tile_img = tile_images[int(tile_type)]
        x0 = col * tile_size
        y0 = row * tile_size
        img1 = ImageDraw.Draw(image)
        img1.rectangle((x0, y0, x0 + 15, y0 + 15), fill=desired_color)
        image.paste(tile_img.convert("RGBA"), (x0, y0), tile_img.convert("RGBA"))
        #if object != leveldata[0] and object != leveldata[-1]:
            #img1.text((object['x_pos'] * 16, (object['y_pos'] if object['y_pos'] < 12 else 0) * 16),f"{object['raw_data'][0] + object['raw_data'][1] }",(random.randrange(0, 255),random.randrange(0, 255),random.randrange(0, 255)),font=font)
mario = Image.open('chunkids/mario.png')
image.paste(mario.convert("RGBA"), (24 + 16, (int(leveldata[0]['start_location_y']) * 16) + 16), mario.convert("RGBA"))
    
if sys.platform != 'emscripten':

    image.show()
    image.save('output.png')
else:
    import io
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    img_str