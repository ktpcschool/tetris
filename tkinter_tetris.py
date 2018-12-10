"""tkinter_tetris.py - Copyright 2018 Tatsuro Watanabe"""
from tkinter import Tk
from tkinter import Canvas
import numpy as np
import time

#四角形に関するクラス
class Square():
    def __init__(self, cv, color, tag=None):
        self.cv = cv
        self.color = color
        self.tag = tag
        
    def draw(self, x1, y1, x2, y2):
        self.cv.create_rectangle(x1, y1, x2, y2, fill=self.color, width=0, tag=self.tag)

#ブロックに関するクラス
class Block():
    def __init__(self, cv, cell_size, posx, posy, block_type, btype, rot):
        self.cv = cv
        self.cell_size = cell_size
        self.offset = 1
        self.posx = posx #ブロックの左上のx座標
        self.posy = posy #ブロックの左上のy座標
        color_types = {1:'orange', 2:'RoyalBlue1', 3:'magenta', 4:'red', 5:'green2', 6:'yellow', 7:'cyan'}
        self.color = color_types[btype]
        self.block_type = block_type
        tag_types = {1:'one', 2:'two', 3:'three', 4:'four', 5:'five', 6:'six', 7:'seven'}
        self.tag = tag_types[btype]
        self.rotation_number = rot
        self.rot_types = [self.block_type, np.rot90(self.block_type, k=-1), np.rot90(self.block_type, k=2), np.rot90(self.block_type, k=1)]
        self.BLOCK = self.rot_types[rot]
        self.cv.bind_all('<Key-Left>', self.move_left)
        self.cv.bind_all('<Key-Right>', self.move_right)
        self.cv.bind_all('<Key-Down>', self.move_down)
        self.cv.bind_all('<Key-Up>', self.rotate)
        
    #ブロックを描く
    def draw(self):
        index = np.where(self.BLOCK >= 1)
        for i in np.arange(index[0].size):
            x = index[1][i]
            y = index[0][i]
            sq = Square(self.cv, self.color, self.tag)
            x1 = (self.posx + x<<4) + self.offset
            y1 = (self.posy + y<<4) + self.offset
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            sq.draw(x1, y1, x2, y2)
    
    #ブロックが落ちる
    def drop_down(self):
        self.cv.delete(self.tag)
        x = 0
        y = 1
        self.posx += x
        self.posy += y
        self.draw()
    
    #左に動かす
    def move_left(self, event):
        self.cv.delete(self.tag)
        x = -1
        y = 0
        self.posx += x
        self.posy += y
        self.draw()
        if self.is_overlapped():
            self.cv.delete(self.tag)
            x = 1
            y = 0
            self.posx += x
            self.posy += y
            self.draw()
                
    #右に動かす
    def move_right(self, event):
        self.cv.delete(self.tag)
        x = 1
        y = 0
        self.posx += x
        self.posy += y
        self.draw()
        if self.is_overlapped():
            self.cv.delete(self.tag)
            x = -1
            y = 0
            self.posx += x
            self.posy += y
            self.draw()
                
    #下に動かす
    def move_down(self, event):
        self.cv.delete(self.tag)
        x = 0
        y = 1
        self.posx += x
        self.posy += y
        self.draw()
        if self.is_overlapped():
            self.cv.delete(self.tag)
            x = 0
            y = -1
            self.posx += x
            self.posy += y
            self.draw()
            
    #回転させる
    def rotate(self, event):
        self.cv.delete(self.tag)
        rot_num = (self.rotation_number+1) % 4
        self.BLOCK = self.rot_types[rot_num]
        self.draw()
        self.rotation_number += 1
        if self.is_overlapped():
            self.cv.delete(self.tag)
            self.rotation_number -= 1
            rot_num = self.rotation_number % 4
            self.BLOCK = self.rot_types[rot_num]
            self.draw()

    #ブロックが重なったかどうか
    def is_overlapped(self):
        index = np.where(self.BLOCK >= 1)
        for i in np.arange(index[0].size):
            x = index[1][i]
            y = index[0][i]
            
            if self.posy + y >= 0:
                if self.posy + y >= FIELD.shape[0] - 1 \
                or self.posx + x <= 0 \
                or self.posx + x >= FIELD.shape[1] - 1 \
                or FIELD[self.posy + y][self.posx + x] >= 1:
                    return True
            elif self.posx <= 0 \
            or self.posx + x >= FIELD.shape[1] - 1:
                    return True        
        return False

    #ブロックをコピー
    def copy(self):
        cp_block = np.copy(self.BLOCK)
        return cp_block

#次のブロックに関するクラス
class NextBlock():
    def __init__(self, cv, cell_size, block_type, btype, rot):
        self.cv = cv
        self.cell_size = cell_size
        color_types = {1:'orange', 2:'RoyalBlue1', 3:'magenta', 4:'red', 5:'green2', 6:'yellow', 7:'cyan'}
        self.color = color_types[btype]
        self.block_type = block_type
        tag_types = {1:'n_one', 2:'n_two', 3:'n_three', 4:'n_four', 5:'n_five', 6:'n_six', 7:'n_seven'}
        self.tag = tag_types[btype]
        self.rotation_number = rot
        self.btype = btype
        self.rot = rot
        rot_types = [self.block_type, np.rot90(self.block_type, k=-1), np.rot90(self.block_type, k=2), np.rot90(self.block_type, k=1)]
        self.BLOCK = rot_types[self.rot]
        self.offset = 1
        
    #次のブロックを描く
    def draw(self):
        next_blockx = 13
        next_blocky = 7
        index = np.where(self.BLOCK >= 1)
        for i in np.arange(index[0].size):
            x = index[1][i]
            y = index[0][i]
            sq = Square(self.cv, self.color, self.tag)
            x1 = (next_blockx + x<<4) + self.offset
            y1 = (next_blocky + y<<4) + self.offset
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            sq.draw(x1, y1, x2, y2)
        return self.tag
        
    #次のブロックを削除
    def delete(self, tag):
        self.cv.delete(tag)
        
#フィールドに関するクラス
class Field():
    def __init__(self, cv, cell_size, marginy):
        self.cv = cv
        self.cell_size = cell_size
        self.marginy = marginy
        self.color_types = {1:'orange', 2:'RoyalBlue1', 3:'magenta', 4:'red', 5:'green2', 6:'yellow', 7:'cyan'}
        self.offset = 1
        self.score = 0
        
    #壁と底を描く
    def draw_wall_base(self):
        color = 'white'
        #壁
        for y in np.arange(FIELD.shape[0] - 1):
            for x in [0, FIELD.shape[1] - 1]:
                sq = Square(self.cv, color, tag='wall')
                x1 = (x<<4) + self.offset
                y1 = (y<<4) + self.offset + self.marginy
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                sq.draw(x1, y1, x2, y2)
         
        #底
        y = FIELD.shape[0] - 1
        for x in np.arange(FIELD.shape[1]):
            sq = Square(self.cv, color, tag='wall')
            x1 = (x<<4) + self.offset
            y1 = (y<<4) + self.offset + self.marginy
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            sq.draw(x1, y1, x2, y2)
        
        #SCOREの文字
        scorex = 15
        scorey = 2
        self.cv.create_text(scorex<<4, scorey<<4, text = 'SCORE', font = ('Arial Black', 12), fill='white')
        
        #NEXTの文字
        nextx = 15
        nexty = 6      
        self.cv.create_text(nextx<<4, nexty<<4, text = 'NEXT', font = ('Arial Black', 12), fill='white')
        
    #フィールドを描く
    def draw_field(self, tag):
        self.delete(tag) #積もったブロックを削除

        for y in np.arange(FIELD.shape[0] - 1):
            for x in np.arange(1, FIELD.shape[1] - 1):
                if FIELD[y, x] >= 1:
                    btype = FIELD[y, x]
                    sq = Square(self.cv, color=self.color_types[btype], tag='load')
                    x1 = (x<<4) + self.offset
                    y1 = (y<<4) + self.offset + self.marginy
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    sq.draw(x1, y1, x2, y2)
            
    #積もったブロックをフィールドに反映
    def load_block(self, cp_block, posx, posy):
        index = np.where(cp_block >= 1)
        for i in np.arange(index[0].size):
            x = index[1][i]
            y = index[0][i]
            
            if 0 <= posy + y <= FIELD.shape[0] - 2 \
            and 1 <= posx + x <= FIELD.shape[1] - 2:
                FIELD[posy + y, posx + x] = cp_block[y, x]
        
    #行が全て埋まった段があるかどうか
    def has_filled_line(self):
        field = FIELD[:-1, 1:-1]
        f = field[~np.all(field >= 1, axis=1),:]
        count = field.shape[0] - f.shape[0]
        if count > 0:
            return True
        else:
            return False
        
    #行が全て埋まった段を消す
    def delete_lines(self):
        field1 = FIELD[:-1, 1:-1]
        f = field1[~np.all(field1 >= 1, axis=1),:]
        count = field1.shape[0] - f.shape[0]
        arr = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        arr1 = np.array([arr] * count)
        field2 = np.vstack((arr1, f))
        FIELD[:-1, 1:-1] = field2
        self.score += 2 ** count #スコアを加算
    
    #積もったブロックを削除
    def delete(self, tag):
        tags = [tag, 'load']
        for t in tags:
            self.cv.delete(t)
        
    #スコアを表示
    def show_score(self):
        x = 15
        y = 3
        score_id = self.cv.create_text(x<<4, y<<4, text = str(self.score), font = ('Arial Black', 12), fill='white')
        return score_id
    
    #古いスコアを削除
    def delete_score(self, score_id):
        self.cv.delete(score_id)
        
    #ゲームオーバーかどうか
    def is_game_over(self):
        return np.sum(FIELD[0, 1:-1]>=1) > 0
    
    #GAME OVERの文字を表示
    def show_game_over(self):
        x = 9
        y1 = 9
        y2 = 13
        self.cv.create_text(x<<4, y1<<4, text = 'GAME OVER', font = ('Arial Black', 28), fill= 'LemonChiffon2')
        self.cv.create_text(x<<4, y2<<4, text = 'Produced By\nTatsuro Watanabe\nat KTPC_School', font = ('Arial Black', 12), fill= 'LemonChiffon2')
        
#背景を描く
def draw_background(cv, width, height, color):
    x1 = 0
    y1 = 0
    x2 = x1 + width
    y2 = y1 + height
    cv.create_rectangle(x1, y1, x2, y2, fill=color)
    
#ウィンドウの作成
tk = Tk()
tk.title('Tetris')
width = (12<<4) + 1
height = (21<<4) + 1
score_area = 6<<4
marginy = 1<<4
cv = Canvas(tk, width = width + score_area, height = height + marginy, bd=0, highlightthickness=0)
cv.pack()
tk.update()

#背景を描く
bg_color = 'black'
draw_background(cv, width + score_area, height + marginy, bg_color)

global FIELD
FIELD = np.array(
        [[8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], 
         [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], 
         [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], 
         [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], 
         [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], 
         [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])

cell_size = 15

#フィールドを描く
field = Field(cv, cell_size, marginy)
field.draw_wall_base()
score_id = field.show_score()

startx = np.random.randint(2, 7) #ブロックが出る横軸上の位置
starty = -4 #ブロックが出る縦軸上の位置

#ブロックの種類
blocks = {
        1: np.array([[0, 0, 1],
                     [1, 1, 1],
                     [0, 0, 0]]),
        2: np.array([[2, 0, 0], 
                     [2, 2, 2],
                     [0, 0, 0]]),
        3: np.array([[0, 3, 0], 
                     [3, 3, 3],
                     [0, 0, 0]]),
        4: np.array([[4, 4, 0],
                     [0, 4, 4],
                     [0, 0, 0]]),
        5: np.array([[0, 5, 5],
                     [5, 5, 0],
                     [0, 0, 0]]),
        6: np.array([[6, 6],
                     [6, 6]]),
        7: np.array([[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [7, 7, 7, 7],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]])}
          
btype = np.random.randint(1,8)
block_type = blocks[btype]
rot = np.random.randint(4)    
            
block = Block(cv, cell_size, startx, starty, block_type, btype, rot)
block.draw()

count = 0
next_block = None
ntag = None
gameover_count = 0

#ゲームループ
while True:
    if field.is_game_over():
        field.show_game_over()
        gameover_count += 1
        if gameover_count >= 2:
            break    
    
    if block.is_overlapped():
        cp_block = block.copy()
        block.posy -= 1
        field.load_block(cp_block, block.posx, block.posy)
        field.draw_field(block.tag)
            
        if field.has_filled_line():
            field.delete_lines()
            field.draw_field(block.tag)
            field.delete_score(score_id)
            score_id = field.show_score()
            
        if next_block != None:
            startx = np.random.randint(2, 7)
            block = Block(cv, cell_size, startx, starty, next_block.block_type, next_block.btype, next_block.rot)
            block.draw()
            count = 0 #カウントをリセット
            
    if count % 20 == 0:
        block.drop_down()
    if count == 30:    
        btype = np.random.randint(1,8)
        block_type = blocks[btype]
        rot = np.random.randint(4)
        next_block = NextBlock(cv, cell_size, block_type, btype, rot)
        if ntag != None:
            next_block.delete(ntag)
        ntag = next_block.draw() #NEXTブロックを描く
    
    count += 1
    
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
