import pandas as pd
import numpy as np
from PIL import Image

df = pd.read_excel('DETAIL.xlsx')

color_map = {
    '/': (0, 255, 0),
    'A': (255, 0, 0), 'B': (0, 128, 128), 'C': (0, 0, 255), 'D': (255, 255, 0), 'E': (255, 0, 255),
    'F': (0, 255, 255), 'G': (128, 0, 0), 'H': (0, 128, 0), 'I': (0, 0, 128), 'J': (128, 128, 0),
    'K': (128, 0, 128), 'L': (0, 128, 128), 'M': (64, 0, 0), 'N': (0, 64, 0), 'O': (0, 0, 64),
    'P': (64, 64, 0), 'Q': (64, 0, 64), 'R': (0, 64, 64), 'S': (192, 0, 0), 'T': (0, 192, 0),
    'U': (0, 0, 192), 'V': (192, 192, 0), 'W': (192, 0, 192), 'X': (0, 192, 192), 'Y': (96, 0, 0),
    'Z': (0, 96, 0),
    '1': (128, 255, 128), '2': (128, 128, 255), '3': (255, 128, 255), '4': (255, 255, 128),
    '5': (128, 255, 255), '6': (192, 128, 128), '7': (128, 128, 64), '8': (128, 128, 192), '9': (192, 128, 192),
}

# WAFER_NO 그룹화
grouped = df.groupby('WAFER_NO')

# WAFER 사이즈에 맞도록 동적으로 설정
max_row_no = df['ROW_NO'].max() + 1  # 최대 ROW_NO -> 세로 길이
max_detail_length = df['DETAIL'].str.len().max()  # DETAIL의 최대 길이 -> 가로 길이

# 전체 캔버스 사이즈 조정
grid_size = 5
canvas_width = grid_size * max_detail_length
canvas_height = grid_size * max_row_no
canvas_size = (canvas_width, canvas_height)
canvas = Image.new('RGB', canvas_size, (0, 0, 0))


# 각 웨이퍼 이미지를 생성 -> 캔버스에 붙이기

# 웨이퍼 수만큼 반복
for wafer_no, wafer_group in grouped:
    if wafer_no > 25:
        break

    # 웨이퍼 이미지 크기 및 배열 설정
    wafer_height = wafer_group['ROW_NO'].max() + 1
    wafer_width = wafer_group['DETAIL'].str.len().max()
    wafer_image = Image.new('RGB', (wafer_width, wafer_height), (255, 255, 255))
    wafer_array = np.zeros((wafer_height, wafer_width, 3), dtype=np.uint8)

    # 하나의 웨이퍼의 ROW_NO만큼 반복
    for index, row in wafer_group.iterrows():
        row_no = row['ROW_NO']
        detail_string = row["DETAIL"]
  
        # 하나의 ROW_NO에 대한 DETAIL만큼 반복하여 색상 배열 생성
        for i, char in enumerate(detail_string[:wafer_width]):
            if row_no < wafer_height and i < wafer_width:
                color = color_map.get(char, (0, 0, 0))
                wafer_array[row_no, i] = color

    # 색상 배열을 이미지로 변환
    wafer_image = Image.fromarray(wafer_array)

    # 그리드 배열에 맞게 위치 설정
    grid_x = (wafer_no - 1) % grid_size
    grid_y = (wafer_no - 1) // grid_size
    pos_x = grid_x * wafer_width
    pos_y = grid_y * wafer_height

    canvas.paste(wafer_image, (pos_x, pos_y))
    
    
canvas.save('wafer_grid.png')
canvas.show('wafer_grid.png')