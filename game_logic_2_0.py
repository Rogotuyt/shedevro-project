import pickle,random

win_pol = [
    ((1,1),(-1,-1)),
    ((1,-1),(-1,1)),
    ((1,0),(-1,0)),
    ((0,1),(0,-1))
    ]

class Game_logic():
    def __init__(self,q_file = 'q_tab.pkl'):
        self.q_file = q_file
        self.q_tab = self.load_q(q_file)
        self.reset()

    def reset(self):
        self.board = [[0]*5 for _ in range(5)]

    def load_q(self,file):
        try:
            with open(file, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}
    
    def svoboda(self, board = None):
        if board == None:
            return [
                (r,c)
                for r in range(1,4)
                for c in range(1,4)
                if self.board[r][c] == 0]
        else:
            return [
                    (r,c)
                    for r in range(1,4)
                    for c in range(1,4)
                    if board[r][c] == 0]
    
    def detect_win(self):
        for r in range(1,4):
            for c in range(1,4):
                for i in win_pol:
                    if self.board[r][c]==self.board[r+i[0][0]][c+i[0][1]] == self.board[r+i[1][0]][c+i[1][1]] != 0:
                        a = [(r,c),(r+i[0][0],c+i[0][1]),(r+i[1][0],c+i[1][1])]
                        #print(a)
                        return a
        return [0,0,0] 

    def create_key(self,pl,board = None  ):
        if board == None:
            b = (tuple(i) for i in self.board)
        else:
            b = (tuple(i) for i in board)
        return (tuple(b),pl)



    def ai_hod(self,pl,eps = 0):
        a = self.create_key(pl=pl)
        all_hd = self.svoboda()
        q = self.q_tab
        if a not in q:
            q[a] = {l:0 for l in all_hd}

        if eps > random.random():
            return random.choice(all_hd)
        else:
            if not all_hd:
                return None
            a = max(all_hd, key= lambda call: q[a][call])
            return a

    def is_game(self):
        if self.detect_win()[0] != 0:
            return False
        elif self.svoboda() == []:
            return False
        #print(self.svoboda())
        return True

    def move(self, row,col,pl):
        if self.board[row][col] == 0:
            self.board[row][col] = pl
            return True
        return False

    def lose_test(self,powtor = 100):
        print('start')
        for _ in range(powtor):
            history = []
            self.reset()
            pl = random.choice([1,-1])
            while self.is_game():       
                if pl == 1:
                    hd = self.ai_hod(pl=pl,eps=0)
                    self.move(hd[0],hd[1],1)
                else:
                    hd = random.choice(self.svoboda())
                    self.move(hd[0],hd[1],-1)
                pl = -pl
                history.append((hd,pl,self.create_key(pl=pl)))
            if  self.detect_win() == -1:
                return history
        print('end game')


    def zero_share(self):
        total = 0
        zeros = 0
        for moves in self.q_tab.values():
            for v in moves.values():
                total += 1
                if v == 0:
                    zeros += 1
        if total == 0:
            return 0.0
        return zeros / total

    def training_ai(self,ep = 0.3,lr = 0.1):
        self.reset()#[[0,0,0,0,0],[0,-1,0,0,0],[0,0,1,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        pl = -1 #random.choice([1,-1])
        history = []
        while self.is_game():
            bor = self.create_key(pl=pl)
            hd = self.ai_hod(pl=pl,eps=ep)
            history.append((pl,hd,bor))
            self.move(hd[0],hd[1],pl)
            pl = -pl
        winer = self.detect_win()
        self.q_lerninig(winer=winer,history=history,)

    def test_ai(self):
        self.reset()
        pl = random.choice([1,-1])
        while self.is_game():
            if pl == 1:
                hd = self.ai_hod(eps=0,pl=pl)
                self.move(hd[0],hd[1],1)
            else:
                hd = random.choice(self.svoboda())
                self.move(hd[0],hd[1],-1)
            pl = -pl
        return self.detect_win()

    def drow_board(self):
        for i in self.board:
            print(i)

    def q_test(self):
        print(self.q_tab[((0,0,0,0,0),(0,0,0,0,0),(0,0,-1,0,0),(0,0,0,0,0),(0,0,0,0,0)),1])
    
    def save_q(self):
        with open(self.q_file, "wb") as f:
            pickle.dump(self.q_tab, f)
            print(f'save:{self.q_file}')

    def q_lerninig(self,winer,gamma = 0.9,history = [],lr = 0.1):
        for i in reversed(range(len(history))):
            pl,hd,bor = history[i]
            if len(history)-1 == i:
                target = winer*pl
            else:
                _,_,bor_next = history[i+1]
                target = -gamma*max(self.q_tab[bor_next].values())
            self.q_tab[bor][hd] += lr*(target-self.q_tab[bor][hd])
            

    
