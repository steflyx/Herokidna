import time
import board
import neopixel
from threading import Thread
import threading

pixel_pin = board.D21
num_pixels = 128
ORDER = neopixel.GRB   #This way (x,y,z) are RGB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.05, auto_write=False, pixel_order=ORDER
)

# With br=0.03, the minimum value visible is 34.
# With br=0.02, the minimum value visible is 50.
#DEFINING COLOURS
ORANGE = (255, 65, 0)
YELLOW = (255, 170, 0)
GREEN =  (0, 255, 0)
VIOLET = (125, 0, 255)
PINK =   (255, 0, 125)
AZURE =  (0, 200, 255)
WHITE =  (200, 200, 200)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)

def idleTh():
        for j in range(255):
            for i in range(64):
                if (i>8 and i!=11 and i!=12 and i!=15 and i!=40 and i!=47 and i!=48
                     and i!=49 and i!=54 and i!=55 and i!=56 and i!=57 and i!=58 and i<61):
                    pixel_index = (i * 256 // num_pixels) + j
                    pixels[i] = wheel(pixel_index & 255)
                else:
                    pixels[i] = 0
                pixels[i+64] = pixels[i]
            pixels.show()
            time.sleep(0.001)

def defenseTh():
   # def run(self):
        k = PINK
        def1 = [0,0,k,k,k,k,0,0,
                0,k,k,k,k,k,k,0,
                k,k,k,k,k,k,k,k,
                k,k,k,0,0,k,k,k,
                k,k,k,0,0,k,k,k,
                k,k,k,k,k,k,k,k,
                0,k,k,k,k,k,k,0,
                0,0,k,k,k,k,0,0]

        def2 = [0,0,k,k,k,k,0,0,
                0,k,k,k,k,k,k,0,
                k,k,k,k,k,k,k,k,
                k,k,k,k,k,k,k,k,
                k,k,k,0,0,k,k,k,
                k,k,k,0,0,k,k,k,
                0,k,k,k,k,k,k,0,
                0,0,k,k,k,k,0,0]

        def3 = [0,0,k,k,k,k,0,0,
                0,k,k,k,k,k,k,0,
                k,k,k,k,k,k,k,k,
                k,k,k,k,k,k,k,k,
                k,k,k,k,0,0,k,k,
                k,k,k,k,0,0,k,k,
                0,k,k,k,k,k,k,0,
                0,0,k,k,k,k,0,0]

        def4 = [0,0,k,k,k,k,0,0,
                0,k,k,k,k,k,k,0,
                k,k,k,k,k,k,k,k,
                k,k,k,k,0,0,k,k,
                k,k,k,k,0,0,k,k,
                k,k,k,k,k,k,k,k,
                0,k,k,k,k,k,k,0,
                0,0,k,k,k,k,0,0]

        def5 = [0,0,k,k,k,k,0,0,
                0,k,k,k,k,k,k,0,
                k,k,k,k,0,0,k,k,
                k,k,k,k,0,0,k,k,
                k,k,k,k,k,k,k,k,
                k,k,k,k,k,k,k,k,
                0,k,k,k,k,k,k,0,
                0,0,k,k,k,k,0,0]

        def6 = [0,0,k,k,k,k,0,0,
                0,k,k,k,k,k,k,0,
                k,k,k,0,0,k,k,k,
                k,k,k,0,0,k,k,k,
                k,k,k,k,k,k,k,k,
                k,k,k,k,k,k,k,k,
                0,k,k,k,k,k,k,0,
                0,0,k,k,k,k,0,0]

        def7 = [0,0,k,k,k,k,0,0,
                0,k,k,k,k,k,k,0,
                k,k,0,0,k,k,k,k,
                k,k,0,0,k,k,k,k,
                k,k,k,k,k,k,k,k,
                k,k,k,k,k,k,k,k,
                0,k,k,k,k,k,k,0,
                0,0,k,k,k,k,0,0]

        def8 = [0,0,k,k,k,k,0,0,
                0,k,k,k,k,k,k,0,
                k,k,k,k,k,k,k,k,
                k,k,0,0,k,k,k,k,
                k,k,0,0,k,k,k,k,
                k,k,k,k,k,k,k,k,
                0,k,k,k,k,k,k,0,
                0,0,k,k,k,k,0,0]

        def9 = [0,0,k,k,k,k,0,0,
                0,k,k,k,k,k,k,0,
                k,k,k,k,k,k,k,k,
                k,k,k,k,k,k,k,k,
                k,k,0,0,k,k,k,k,
                k,k,0,0,k,k,k,k,
                0,k,k,k,k,k,k,0,
                0,0,k,k,k,k,0,0]

        #shrinks
        def10 = [0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,k,k,0,0,0,
                0,0,0,k,k,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0]

        def11 = [0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,k,k,0,0,0,
                0,0,k,0,0,k,0,0,
                0,0,k,0,0,k,0,0,
                0,0,0,k,k,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0]

        def12 = [0,0,0,0,0,0,0,0,
                0,0,0,k,k,0,0,0,
                0,0,k,0,0,k,0,0,
                0,k,0,0,0,0,k,0,
                0,k,0,0,0,0,k,0,
                0,0,k,0,0,k,0,0,
                0,0,0,k,k,0,0,0,
                0,0,0,0,0,0,0,0]

        def13 = [0,0,0,0,0,0,0,0,
                0,0,k,k,k,k,0,0,
                0,k,0,0,0,0,k,0,
                0,k,0,0,0,0,k,0,
                0,k,0,0,0,0,k,0,
                0,k,0,0,0,0,k,0,
                0,0,k,k,k,k,0,0,
                0,0,0,0,0,0,0,0]

        def14 = [0,0,0,k,k,0,0,0,
                0,0,k,k,k,k,0,0,
                0,k,0,0,0,0,k,0,
                k,k,0,0,0,0,k,k,
                k,k,0,0,0,0,k,k,
                0,k,0,0,0,0,k,0,
                0,0,k,k,k,k,0,0,
                0,0,0,k,k,0,0,0]

        def15 = [0,0,k,k,k,k,0,0,
                0,k,k,k,k,k,k,0,
                k,k,0,0,0,0,k,k,
                k,k,0,0,0,0,k,k,
                k,k,0,0,0,0,k,k,
                k,k,0,0,0,0,k,k,
                0,k,k,k,k,k,k,0,
                0,0,k,k,k,k,0,0]

        def16 = [0,0,k,k,k,k,0,0,
                0,k,k,k,k,k,k,0,
                k,0,0,0,0,k,k,k,
                k,0,0,0,0,k,k,k,
                k,0,0,0,0,k,k,k,
                k,0,0,0,0,k,k,k,
                0,k,k,k,k,k,k,0,
                0,0,k,k,k,k,0,0]

        def17 = [0,0,k,k,k,k,0,0,
                0,k,k,k,k,k,k,0,
                k,k,k,0,0,0,0,k,
                k,k,k,0,0,0,0,k,
                k,k,k,0,0,0,0,k,
                k,k,k,0,0,0,0,k,
                0,k,k,k,k,k,k,0,
                0,0,k,k,k,k,0,0]

        def18 = [0,0,k,k,k,k,0,0,
                0,k,0,0,0,0,k,0,
                k,k,0,0,0,0,k,k,
                k,k,0,0,0,0,k,k,
                k,k,0,0,0,0,k,k,
                k,k,k,k,k,k,k,k,
                0,k,k,k,k,k,k,0,
                0,0,k,k,k,k,0,0]

        def19 = [0,0,k,k,k,k,0,0,
                0,k,k,k,k,k,k,0,
                k,k,k,k,k,k,k,k,
                k,k,0,0,0,0,k,k,
                k,k,0,0,0,0,k,k,
                k,k,0,0,0,0,k,k,
                0,k,0,0,0,0,k,0,
                0,0,k,k,k,k,0,0]

        for i in range(128):
            pixels[i] = def1[i%64]
        pixels.show()
        time.sleep(1)
        for rep in range (3):
            for i in range(128):
                pixels[i] = def2[i%64]
            pixels.show()
            time.sleep(0.03)
            for i in range(64):
                pixels[i] = def3[i]
            cnt = 8
            tab = 1
            chk = 0
            for i in range(64):
                pixels[i+64] = def3[cnt-1]
                cnt-=1
                if (cnt == chk):
                    tab+=1
                    cnt=8*tab
                    chk=8*(tab-1)
            pixels.show()
            time.sleep(0.03)
            for i in range(64):
                pixels[i] = def4[i]
            cnt = 8
            tab = 1
            chk = 0
            for i in range(64):
                pixels[i+64] = def4[cnt-1]
                cnt-=1
                if (cnt == chk):
                    tab+=1
                    cnt=8*tab
                    chk=8*(tab-1)
            pixels.show()
            time.sleep(0.03)
            for i in range(64):
                pixels[i] = def5[i]
            cnt = 8
            tab = 1
            chk = 0
            for i in range(64):
                pixels[i+64] = def5[cnt-1]
                cnt-=1
                if (cnt == chk):
                    tab+=1
                    cnt=8*tab
                    chk=8*(tab-1)
            pixels.show()
            time.sleep(0.03)
            for i in range(128):
                pixels[i] = def6[i%64]
            pixels.show()
            time.sleep(0.03)
            for i in range(64):
                pixels[i] = def7[i]
            cnt = 8
            tab = 1
            chk = 0
            for i in range(64):
                pixels[i+64] = def7[cnt-1]
                cnt-=1
                if (cnt == chk):
                    tab+=1
                    cnt=8*tab
                    chk=8*(tab-1)
            pixels.show()
            time.sleep(0.03)
            for i in range(64):
                pixels[i] = def8[i]
            cnt = 8
            tab = 1
            chk = 0
            for i in range(64):
                pixels[i+64] = def8[cnt-1]
                cnt-=1
                if (cnt == chk):
                    tab+=1
                    cnt=8*tab
                    chk=8*(tab-1)
            pixels.show()
            time.sleep(0.03)
            for i in range(64):
                 pixels[i] = def9[i]
            cnt = 8
            tab = 1
            chk = 0
            for i in range(64):
                pixels[i+64] = def9[cnt-1]
                cnt-=1
                if (cnt == chk):
                    tab+=1
                    cnt=8*tab
                    chk=8*(tab-1)
            pixels.show()
            time.sleep(0.03)
        for rep in range (5):
            for i in range(128):
                pixels[i] = def10[i%64]
            pixels.show()
            time.sleep(0.03)
            for i in range(128):
                pixels[i] = def11[i%64]
            pixels.show()
            time.sleep(0.03)
            for i in range(128):
                pixels[i] = def12[i%64]
            pixels.show()
            time.sleep(0.03)
            for i in range(128):
                pixels[i] = def13[i%64]
            pixels.show()
            time.sleep(0.03)
            for i in range(128):
                pixels[i] = def14[i%64]
            pixels.show()
            time.sleep(0.03)
            for i in range(128):
                pixels[i] = def15[i%64]
            pixels.show()
            time.sleep(0.03)
        time.sleep(2)
        for i in range(64):
            pixels[i] = def16[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
            pixels[i+64] = def16[cnt-1]
            cnt-=1
            if (cnt == chk):
                tab+=1
                cnt=8*tab
                chk=8*(tab-1)
        pixels.show()
        time.sleep(1)
        for i in range(64):
            pixels[i] = def17[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
            pixels[i+64] = def17[cnt-1]
            cnt-=1
            if (cnt == chk):
                tab+=1
                cnt=8*tab
                chk=8*(tab-1)
        pixels.show()
        time.sleep(1)
        for i in range(128):
            pixels[i] = def18[i%64]
        pixels.show()
        time.sleep(1)
        for i in range(128):
            pixels[i] = def19[i%64]
        pixels.show()
        time.sleep(1)


def drinkTh():
    #def run(self):
        g = WHITE
        p = AZURE
        drk1 = [0,0,g,g,g,g,0,0,
                0,g,g,g,g,g,g,0,
                g,g,g,g,g,g,g,g,
                g,g,g,0,0,g,g,g,
                g,g,g,0,0,g,g,g,
                g,g,g,g,g,g,g,g,
                0,g,g,g,g,g,g,0,
                0,0,g,g,g,g,0,0]

        drk2 = [0,0,g,g,g,g,0,0,
                0,g,g,g,g,g,g,0,
                g,g,g,g,g,g,g,g,
                g,g,g,g,g,g,g,g,
                g,g,g,0,0,g,g,g,
                g,g,g,0,0,g,g,g,
                0,g,g,g,g,g,g,0,
                0,0,g,g,g,g,0,0]

        drk3 = [0,0,g,g,g,g,0,0,
                0,g,g,g,g,g,g,0,
                g,g,g,g,g,g,g,g,
                g,g,g,g,g,g,g,g,
                g,g,g,g,g,g,g,g,
                g,g,g,0,0,g,g,g,
                0,g,g,0,0,g,g,0,
                0,0,g,g,g,g,0,0]

        drk4 = [0,0,g,g,g,g,0,0,
                0,g,g,g,g,g,g,0,
                g,g,g,g,g,g,g,g,
                g,g,g,g,g,g,g,g,
                g,g,g,g,g,g,g,g,
                g,g,0,0,g,g,g,g,
                0,g,0,0,g,g,g,0,
                0,0,g,g,g,g,0,0]
        #drk3 again
        drk5 = [0,0,g,g,g,g,0,0,
                0,g,g,g,g,g,g,0,
                g,g,g,g,g,g,g,g,
                g,g,g,g,g,g,g,g,
                g,g,g,g,g,g,g,g,
                g,g,g,g,0,0,g,g,
                0,g,g,g,0,0,g,0,
                0,0,g,g,g,g,0,0]

        #start changing color
        drk6 = [0,0,g,g,g,g,0,0,
                0,g,g,g,g,g,g,0,
                g,g,g,g,g,g,g,g,
                g,g,g,g,g,g,g,g,
                g,g,g,g,g,g,g,g,
                g,g,g,g,0,0,g,g,
                0,g,g,g,0,0,g,0,
                0,0,p,p,p,p,0,0]

        drk7 = [0,0,g,g,g,g,0,0,
                0,g,g,g,g,g,g,0,
                g,g,g,g,g,g,g,g,
                g,g,g,g,g,g,g,g,
                g,g,g,g,g,g,g,g,
                g,g,g,g,0,0,g,g,
                0,p,p,p,0,0,p,0,
                0,0,p,p,p,p,0,0]

        drk8 = [0,0,g,g,g,g,0,0,
                0,g,g,g,g,g,g,0,
                g,g,g,g,g,g,g,g,
                g,g,g,g,g,g,g,g,
                g,g,g,g,g,g,g,g,
                p,p,p,p,0,0,p,p,
                0,p,p,p,0,0,p,0,
                0,0,p,p,p,p,0,0]

        drk9 = [0,0,g,g,g,g,0,0,
                0,g,g,g,g,g,g,0,
                g,g,g,g,g,g,g,g,
                g,g,g,g,g,g,g,g,
                p,p,p,p,p,p,p,p,
                p,p,p,p,0,0,p,p,
                0,p,p,p,0,0,p,0,
                0,0,p,p,p,p,0,0]

        drk10 = [0,0,g,g,g,g,0,0,
                0,g,g,g,g,g,g,0,
                g,g,g,g,g,g,g,g,
                p,p,p,p,p,p,p,p,
                p,p,p,p,p,p,p,p,
                p,p,p,p,0,0,p,p,
                0,p,p,p,0,0,p,0,
                0,0,p,p,p,p,0,0]

        drk11 = [0,0,g,g,g,g,0,0,
                0,g,g,g,g,g,g,0,
                p,p,p,p,p,p,p,p,
                p,p,p,p,p,p,p,p,
                p,p,p,p,p,p,p,p,
                p,p,p,p,0,0,p,p,
                0,p,p,p,0,0,p,0,
                0,0,p,p,p,p,0,0]

        drk12 = [0,0,g,g,g,g,0,0,
                0,p,p,p,p,p,p,0,
                p,p,p,p,p,p,p,p,
                p,p,p,p,p,p,p,p,
                p,p,p,p,p,p,p,p,
                p,p,p,p,0,0,p,p,
                0,p,p,p,0,0,p,0,
                0,0,p,p,p,p,0,0]

        drk13 = [0,0,p,p,p,p,0,0,
                0,p,p,p,p,p,p,0,
                p,p,p,p,p,p,p,p,
                p,p,p,p,p,p,p,p,
                p,p,p,p,p,p,p,p,
                p,p,p,p,0,0,p,p,
                0,p,p,p,0,0,p,0,
                0,0,p,p,p,p,0,0]

        #start closing animation
        drk14 = [0,0,p,p,p,p,0,0,
                0,p,p,p,p,p,p,0,
                p,p,p,p,p,p,p,p,
                p,p,p,p,p,p,p,p,
                p,p,p,p,p,p,p,p,
                p,p,p,p,0,0,p,p,
                0,p,p,p,0,0,p,0,
                0,0,0,0,0,0,0,0]

        drk15 = [0,0,p,p,p,p,0,0,
                0,p,p,p,p,p,p,0,
                p,p,p,p,p,p,p,p,
                p,p,p,p,p,p,p,p,
                p,p,p,p,p,p,p,p,
                p,p,p,p,0,0,p,p,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0]

        drk16 = [0,0,0,0,0,0,0,0,
                0,p,p,p,p,p,p,0,
                p,p,p,p,p,p,p,p,
                p,p,p,p,p,p,p,p,
                p,p,p,p,p,p,p,p,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0]

        drk17 = [0,0,0,0,0,0,0,0,
                0,0,p,p,p,p,0,0,
                0,p,p,p,p,p,p,0,
                p,p,0,0,0,0,p,p,
                p,p,0,0,0,0,p,p,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0]

        #change color. start opening

        drk18 = [0,0,0,0,0,0,0,0,
                0,p,p,p,p,p,p,0,
                p,p,p,p,p,p,p,p,
                p,p,p,0,0,p,p,p,
                p,p,p,0,0,p,p,p,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0]

        drk19 = [0,0,p,p,p,p,0,0,
                0,p,p,p,p,p,p,0,
                p,p,p,p,p,p,p,p,
                p,p,p,0,0,p,p,p,
                p,p,p,0,0,p,p,p,
                p,p,p,p,p,p,p,p,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0]

        drk20 = [0,0,p,p,p,p,0,0,
                0,p,p,p,p,p,p,0,
                p,p,p,p,p,p,p,p,
                p,p,p,0,0,p,p,p,
                p,p,p,0,0,p,p,p,
                p,p,p,p,p,p,p,p,
                0,p,p,p,p,p,p,0,
                0,0,0,0,0,0,0,0]
        #drk1

        for i in range(128):
             pixels[i] = drk1[i%64]
        pixels.show()
        time.sleep(1)
        for i in range(128):
             pixels[i] = drk2[i%64]
        pixels.show()
        time.sleep(0.04)
        for i in range(128):
             pixels[i] = drk3[i%64]
        pixels.show()
        time.sleep(0.04)
        for i in range(64):
             pixels[i] = drk4[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = drk4[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(1)
        for i in range(128):
             pixels[i] = drk3[i%64]
        pixels.show()
        time.sleep(0.04)
        for i in range(64):
             pixels[i] = drk5[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = drk5[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(1)
        #start color changing
        for i in range(64):
             pixels[i] = drk6[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = drk6[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.13)
        for i in range(64):
             pixels[i] = drk7[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = drk7[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.13)
        for i in range(64):
             pixels[i] = drk8[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = drk8[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.13)
        for i in range(64):
             pixels[i] = drk9[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = drk9[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.13)
        for i in range(64):
             pixels[i] = drk10[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = drk10[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.13)
        for i in range(64):
             pixels[i] = drk11[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = drk11[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.13)
        for i in range(64):
             pixels[i] = drk12[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = drk12[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.13)
        for i in range(64):
             pixels[i] = drk13[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = drk13[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(1)
        #start closing eye
        for i in range(64):
             pixels[i] = drk14[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = drk14[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.01)
        for i in range(64):
             pixels[i] = drk15[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = drk15[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.01)
        for i in range(128):
             pixels[i] = drk16[i%64]
        pixels.show()
        time.sleep(0.01)
        for i in range(128):
             pixels[i] = drk17[i%64]
        pixels.show()
        time.sleep(0.1)
        #start opening
        for i in range(128):
             pixels[i] = drk18[i%64]
        pixels.show()
        time.sleep(0.01)
        for i in range(128):
             pixels[i] = drk19[i%64]
        pixels.show()
        time.sleep(0.01)
        for i in range(128):
             pixels[i] = drk20[i%64]
        pixels.show()
        time.sleep(0.01)
        for i in range(128):
             pixels[i] = drk1[i%64]
        pixels.show()
        time.sleep(0.08)


def attackTh():
    #def run(self):
        y = YELLOW
        o = ORANGE
        atk1 = [0,y,0,0,0,0,0,0,
                0,y,y,0,0,0,0,0,
                y,y,y,y,y,0,0,0,
                y,y,y,0,0,y,y,0,
                y,y,y,0,0,y,y,y,
                y,y,y,y,y,y,y,y,
                0,y,y,y,y,y,y,0,
                0,0,y,y,y,y,0,0]

        atk2 = [0,o,0,0,0,0,0,0,
                0,o,o,0,0,0,0,0,
                o,o,o,o,o,0,0,0,
                o,o,o,0,0,o,o,0,
                o,o,o,0,0,o,o,o,
                o,o,o,o,o,o,o,o,
                0,o,o,o,o,o,o,0,
                0,0,o,o,o,o,0,0]

        atk3 = [0,o,0,0,0,0,0,0,
                0,o,o,0,0,0,0,0,
                o,o,y,y,y,0,0,0,
                o,o,y,0,0,y,o,0,
                o,o,y,0,0,y,o,o,
                o,o,y,y,y,y,o,o,
                0,o,o,o,o,o,o,0,
                0,0,o,o,o,o,0,0]

        atk4 = [0,o,0,0,0,0,0,0,
                0,o,o,0,0,0,0,0,
                o,y,o,o,o,0,0,0,
                o,y,o,0,0,o,y,0,
                o,y,o,0,0,o,y,o,
                o,y,o,o,o,o,y,o,
                0,y,y,y,y,y,y,0,
                0,0,o,o,o,o,0,0]

        atk5 = [0,o,0,0,0,0,0,0,
                0,o,o,0,0,0,0,0,
                y,o,o,o,o,0,0,0,
                y,o,o,0,0,o,o,0,
                y,o,o,0,0,o,o,y,
                y,o,o,o,o,o,o,y,
                0,o,o,o,o,o,o,0,
                0,0,y,y,y,y,0,0]

        atk6 = [0,o,0,0,0,0,0,0,
                0,o,o,0,0,0,0,0,
                o,o,o,o,o,0,0,0,
                o,o,o,0,0,o,o,0,
                o,o,o,0,0,o,o,o,
                0,o,o,o,o,o,o,o,
                0,0,0,o,o,o,o,0,
                0,0,0,0,0,o,0,0]

        atk7 = [0,o,0,0,0,0,0,0,
                0,o,o,0,0,0,0,0,
                o,o,o,o,o,0,0,0,
                0,o,o,0,0,o,o,0,
                0,0,o,0,0,o,o,o,
                0,0,0,o,o,o,o,o,
                0,0,0,0,0,o,o,0,
                0,0,0,0,0,0,0,0]

        atk8 = [0,o,0,0,0,0,0,0,
                0,o,o,0,0,0,0,0,
                0,0,o,o,o,0,0,0,
                0,0,o,0,0,o,o,0,
                0,0,o,0,0,o,o,o,
                0,0,0,o,o,o,o,o,
                0,0,0,0,0,0,0,o,
                0,0,0,0,0,0,0,0]

        atk9 = [0,o,0,0,0,0,0,0,
                0,o,o,0,0,0,0,0,
                0,0,o,o,0,0,0,0,
                0,0,o,o,o,0,0,0,
                0,0,0,0,o,o,0,0,
                0,0,0,0,o,o,o,0,
                0,0,0,0,0,0,o,o,
                0,0,0,0,0,0,0,0]
        for i in range(64):
             pixels[i] = atk1[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk1[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(1)
        for i in range(64):
             pixels[i] = atk2[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk2[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.1)
        for i in range(64):
             pixels[i] = atk3[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk3[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.09)
        for i in range(64):
             pixels[i] = atk4[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk4[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.09)
        for i in range(64):
             pixels[i] = atk5[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk5[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.09)
        for i in range(64):
             pixels[i] = atk2[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk2[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.12)
        for i in range(64):
             pixels[i] = atk3[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk3[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.09)
        for i in range(64):
             pixels[i] = atk4[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk4[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.09)
        for i in range(64):
             pixels[i] = atk5[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk5[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        for i in range(64):
             pixels[i] = atk2[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk2[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.12)
        for i in range(64):
             pixels[i] = atk3[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk3[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.09)
        for i in range(64):
             pixels[i] = atk4[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk4[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.09)
        for i in range(64):
             pixels[i] = atk5[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk5[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.09)
        for i in range(64):
             pixels[i] = atk2[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk2[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.12)
        for i in range(64):
             pixels[i] = atk6[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk6[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.008)
        for i in range(64):
             pixels[i] = atk7[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk7[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.008)
        for i in range(64):
             pixels[i] = atk8[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk8[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.008)
        for i in range(64):
             pixels[i] = atk9[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk9[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.06)
        for i in range(64):
             pixels[i] = atk8[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk8[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.008)
        for i in range(64):
             pixels[i] = atk7[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk7[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.008)
        for i in range(64):
             pixels[i] = atk6[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk6[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.008)
        for i in range(64):
             pixels[i] = atk2[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = atk2[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.09)


j = 0
stdColors = [AZURE, VIOLET, GREEN]
def standardTh():
    #def run(self):
        global j
        global stdColors
        a = stdColors[j]
        std1 = [0,0,a,a,a,a,0,0,
                0,a,a,a,a,a,a,0,
                a,a,a,a,a,a,a,a,
                a,a,a,0,0,a,a,a,
                a,a,a,0,0,a,a,a,
                a,a,a,a,a,a,a,a,
                0,a,a,a,a,a,a,0,
                0,0,a,a,a,a,0,0]

        std2 = [0,0,a,a,a,a,0,0,
                0,a,a,a,a,a,a,0,
                a,a,a,a,a,a,a,a,
                a,a,0,0,a,a,a,a,
                a,a,0,0,a,a,a,a,
                a,a,a,a,a,a,a,a,
                0,a,a,a,a,a,a,0,
                0,0,a,a,a,a,0,0]

        std3 = [0,0,a,a,a,a,0,0,
                0,a,a,a,a,a,a,0,
                a,a,a,a,a,a,a,a,
                a,0,0,a,a,a,a,a,
                a,0,0,a,a,a,a,a,
                a,a,a,a,a,a,a,a,
                0,a,a,a,a,a,a,0,
                0,0,a,a,a,a,0,0]

        std4 = [0,0,a,a,a,a,0,0,
                0,a,a,a,a,a,a,0,
                a,0,0,a,a,a,a,a,
                a,0,0,a,a,a,a,a,
                a,a,a,a,a,a,a,a,
                a,a,a,a,a,a,a,a,
                0,a,a,a,a,a,a,0,
                0,0,a,a,a,a,0,0]

        std5 = [0,0,a,a,a,a,0,0,
                0,a,0,0,a,a,a,0,
                a,a,0,0,a,a,a,a,
                a,a,a,a,a,a,a,a,
                a,a,a,a,a,a,a,a,
                a,a,a,a,a,a,a,a,
                0,a,a,a,a,a,a,0,
                0,0,a,a,a,a,0,0]

        std6 = [0,0,a,a,a,a,0,0,
                0,a,a,0,0,a,a,0,
                a,a,a,0,0,a,a,a,
                a,a,a,a,a,a,a,a,
                a,a,a,a,a,a,a,a,
                a,a,a,a,a,a,a,a,
                0,a,a,a,a,a,a,0,
                0,0,a,a,a,a,0,0]

        std7 = [0,0,a,a,a,a,0,0,
                0,a,a,a,a,a,a,0,
                a,a,a,0,0,a,a,a,
                a,a,a,0,0,a,a,a,
                a,a,a,a,a,a,a,a,
                a,a,a,a,a,a,a,a,
                0,a,a,a,a,a,a,0,
                0,0,a,a,a,a,0,0]

        std8 = [0,0,a,a,a,a,0,0,
                0,a,a,a,a,a,a,0,
                a,a,a,a,a,a,a,a,
                a,a,a,0,0,a,a,a,
                a,a,a,0,0,a,a,a,
                a,a,a,a,a,a,a,a,
                0,a,a,a,a,a,a,0,
                0,0,a,a,a,a,0,0]

        std9 = [0,0,a,a,a,a,0,0,
                0,a,a,a,a,a,a,0,
                a,a,a,a,a,a,a,a,
                a,a,a,a,a,a,a,a,
                a,a,a,0,0,a,a,a,
                a,a,a,0,0,a,a,a,
                0,a,a,a,a,a,a,0,
                0,0,a,a,a,a,0,0]

        std10 = [0,0,0,0,0,0,0,0,
                0,0,a,a,a,a,0,0,
                0,a,a,a,a,a,a,0,
                a,a,a,a,a,a,a,a,
                a,a,a,0,0,a,a,a,
                a,a,a,0,0,a,a,a,
                0,a,a,a,a,a,a,0,
                0,0,a,a,a,a,0,0]

        std11 = [0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,a,a,a,a,a,a,0,
                a,a,a,a,a,a,a,a,
                a,a,a,0,0,a,a,a,
                a,a,a,0,0,a,a,a,
                0,a,a,a,a,a,a,0,
                0,0,a,a,a,a,0,0]

        std12 = [0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                a,a,a,a,a,a,a,a,
                a,a,a,0,0,a,a,a,
                a,a,a,0,0,a,a,a,
                0,0,a,a,a,a,0,0,
                0,0,0,0,0,0,0,0]

        std13 = [0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                a,a,a,a,a,a,a,a,
                a,a,a,0,0,a,a,a,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0]

        std14 = [0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                a,a,a,a,a,a,a,a,
                0,a,a,a,a,a,a,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0]
        #while True:
        for i in range(128):
             pixels[i] = std1[i%64]
        pixels.show()
        time.sleep(1)
        for i in range(64):
             pixels[i] = std2[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = std2[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.04)
        for i in range(64):
             pixels[i] = std3[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = std3[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(1)
        for i in range(64):
             pixels[i] = std4[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = std4[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.04)
        for i in range(64):
             pixels[i] = std5[i]
        cnt = 8
        tab = 1
        chk = 0
        for i in range(64):
             pixels[i+64] = std5[cnt-1]
             cnt-=1
             if (cnt == chk):
                 tab+=1
                 cnt=8*tab
                 chk=8*(tab-1)
        pixels.show()
        time.sleep(0.04)
        for i in range(128):
             pixels[i] = std6[i%64]
        pixels.show()
        time.sleep(1)
        for i in range(128):
             pixels[i] = std7[i%64]
        pixels.show()
        time.sleep(0.04)
        for i in range(128):
             pixels[i] = std8[i%64]
        pixels.show()
        time.sleep(0.04)
        for i in range(128):
             pixels[i] = std9[i%64]
        pixels.show()
        time.sleep(1)
        for i in range(128):
             pixels[i] = std10[i%64]
        pixels.show()
        time.sleep(0.008)
        for i in range(128):
             pixels[i] = std11[i%64]
        pixels.show()
        time.sleep(0.008)
        for i in range(128):
             pixels[i] = std12[i%64]
        pixels.show()
        time.sleep(0.008)
        for i in range(128):
             pixels[i] = std13[i%64]
        pixels.show()
        time.sleep(0.008)
        for i in range(128):
             pixels[i] = std14[i%64]
        pixels.show()
        time.sleep(0.06)
        for i in range(128):
             pixels[i] = std13[i%64]
        pixels.show()
        time.sleep(0.01)
        for i in range(128):
             pixels[i] = std12[i%64]
        pixels.show()
        time.sleep(0.01)
        for i in range(128):
             pixels[i] = std11[i%64]
        pixels.show()
        time.sleep(0.01)
        for i in range(128):
             pixels[i] = std10[i%64]
        pixels.show()
        time.sleep(0.01)
        for i in range(128):
             pixels[i] = std9[i%64]
        pixels.show()
        time.sleep(0.01)
        if (j == 2):
            j = 0
        else:
            j+=1
        a = stdColors[j]