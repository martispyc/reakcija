import time
import random

class SpelesDzinejs:
    def __init__(self):
        self.sakuma_laiks = 0
        self.beigu_laiks = 0
        self.darbojas = False

    def sakt_raundu(self):
        self.sakuma_laiks = time.time()
        self.darbojas = True

    def beigt_raundu(self):
        if not self.darbojas:
            return None
            
        self.beigu_laiks = time.time()
        self.darbojas = False
        
        ilgums_ms = int((self.beigu_laiks - self.sakuma_laiks) * 1000)
        return ilgums_ms

    def iegut_nejausu_poziciju(self, platums, augstums, radiuss):
        atstarpe = radiuss + 5
        
        if platums <= atstarpe * 2 or augstums <= atstarpe * 2:
            return platums // 2, augstums // 2

        x = random.randint(atstarpe, platums - atstarpe)
        y = random.randint(atstarpe, augstums - atstarpe)
        
        return x, y
