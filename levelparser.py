def parse_binary_file(file_path):
    level_data = []
    pagesencountered = 0

    def parse_header(data):

        timertype = (data[0] >> 6) & 0b11
        timer_names = {
            '0': 'No Change',
            '1': '400',
            '2': '300',
            '3': '200'
        }
        timername = timer_names.get(str(timertype), "Unknown" + str(timertype))
        startpos = (data[0] >> 3) & 0b111
        startpos_names = {
            '0': '0',
            '1': '2',
            '2': '11',
            '3': '5',
            '4': '0',
            '5': '0',
            '6': '11',
            '7': '11',

        }
        startposname = startpos_names.get(str(startpos), '0')
        backdrop = data[0] & 0b111
        backdrop_names = {
            '0': 'Default',
            '1': 'Water Waves on Top',
            '2': 'Castle Wall',
            '3': 'Water Waves on The Bottom',
            '4': 'Night Default',
            '5': 'Snowy Default',
            '6': 'Snowy Night',
            '7': 'Fully Gray Night'
        }
        backdropname = backdrop_names.get(str(backdrop), "Unknown")
        tileandplatformtype = data[1] >> 6 & 0b11
        tileandplatform_names = {
            '0': 'Normal Block, Green Pipe, Tree',
            '1': 'Normal Block, Orange Pipe, Mushroom',
            '2': 'Normal Block, Green Pipe, Bullet Bill Cannon',
            '3': 'Cloud Block, Green Pipe, Tree',
        }
        tileandplatform_name = tileandplatform_names.get(str(tileandplatformtype), "Unknown")
        backgroundscenery = data[1] >> 4 & 0b11
        background_names = {
            '0': 'None',
            '2': 'Bushes',
            '1': 'Clouds',
            '3': 'Trees and Fences',
        }
        background_name = background_names.get(str(backgroundscenery), "Unknown")
        floor_pattern = data[1] & 0b1111
        floor_pattern_names = {
            '0': '000000000000000',
            '1': '000000000000011',
            '2': '001000000000011',
            '3': '001110000000011',
            '4': '001111000000011',
            '5': '001111111100011',
            '6': '001000000011111',
            '7': '001110000011111',
            '8': '001111000011111',
            '9': '001000000111111',
            '10':'001000000000000',
            '11':'001111000111111',
            '12':'001000111111111',
            '13':'001001111100011',
            '14':'001000111100011',
            '15':'001111111111111',
        }
        floor_patternname = floor_pattern_names.get(str(floor_pattern), '00000000000000')
        level_data.append({
            'timer': timername,
            'start_location_y': startposname,
            'backdrop': backdropname,
            'tile_and_special_platform': tileandplatform_name,
            'background': background_name,
            'floor_pattern': floor_patternname
        })
    def parse_object(data):
        nonlocal pagesencountered
        x_pos = (data[0] >> 4) & 0x0F
        y_pos = data[0] & 0x0F
        page = (data[1] >> 7) & 0x01
        if(page == 1):
            pagesencountered += 1
        obj_type = (data[1] >> 4) & 0x07
        obj_size = data[1] & 0x0F

        level_data.append({
            'x_page_pos': x_pos,
            'x_pos' : x_pos + pagesencountered * 16,
            'y_pos': y_pos,
            'page': page,
            'obj_type': obj_type,
            'obj_size': obj_size,
            'raw_data': ["{:02x}".format(data[0]), "{:02x}".format(data[1])]
        })

    with open(file_path, 'rb') as f:
        if(len(level_data) <= 0):
            header = f.read(2)
            if len(header) < 2:
                raise ValueError("File is too short to contain a header")
            parse_header(header)
        
        while True:
            data = f.read(2)
            if len(data) < 2: #or data[0] == 0xFD:
                break
            parse_object(data)
        level_data.append({'total_pages': pagesencountered})
    
    return level_data

