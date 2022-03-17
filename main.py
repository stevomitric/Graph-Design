
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from ctypes import windll
from threading import Thread

from bfs import bfs
from dijkstra import dijkstra

import mat, time

class Graf:
    def __init__(self):
        self.veze = {}

    def __slobodanIndex(self):
        for i in range(100):
            if i not in self.veze:
                return i

    def dohvatiCvorove(self):
        return list(self.veze.keys())

    def dohvatiVeze(self, node):
        if node not in self.veze: return []
        return self.veze[node]

    def dodajGranu(self, node1, node2, tezina):
        self.veze[node1][node2] = tezina
        self.veze[node2][node1] = tezina

    def izbrisiGranu(self, node1, node2):
        if node1 in self.veze[node2]:
            self.veze[node2].pop(node1)
        if node2 in self.veze[node1]:
            self.veze[node1].pop(node2)

    def izbrisiCvor(self, node):
        if node in self.veze:
            self.veze.pop(node)
        
        # izbrisi sve veze drugih cvorova u taj
        for k in self.veze:
            if node in self.veze[k]:
                self.veze[k].pop(node)

    def dodajCvor(self):
        inx = self.__slobodanIndex()
        self.veze[inx] = {}
        return inx

class GUI:
    def __init__(self, g):
        self.graf = g
        self.cvorovi = {}

        self.selektovanCvor = None
        self.selektovanOffset = (0,0)
        self.tempLine = None
        self.tempDuzina = ''
        self.selektovanaDuzina = None

        windll.shcore.SetProcessDpiAwareness(1)

    def mainProzor(self):
        self.root = Tk()
        self.root.geometry("700x500")
        self.root.title("Grafovi")

        self.lf1 = LabelFrame(self.root, width = 495, height=495, text = "Graf")
        self.canv = Canvas(self.lf1, width = 485, height=445)

        self.lf2 = LabelFrame(self.root, width = 190, height=495, text = "Algoritmi")
        Button(self.lf2, text = 'Upustvo', width=19, command = self.prikaziUpustvo).place(x=10,y=430)
        Button(self.lf2, text = 'BFS pretraga', width=16, command = lambda : self.pokreniAlgo(bfs, self.eBFS) ).place(x=10,y=30)
        Button(self.lf2, text = 'Dijkstra', width=16, command = lambda : self.pokreniAlgo(dijkstra, self.eDJKS) ).place(x=10,y=70)
        self.eBFS = Entry(self.lf2, width=3)
        self.eBFS.place(x=152,y=32)
        self.eDJKS = Entry(self.lf2, width=3)
        self.eDJKS.place(x=152,y=72)

        self.lf1.place(x=4,y=2)
        self.canv.place(x=0,y=0)

        self.lf2.place(x=505,y=2)

        self.canv.bind("<Button-1>", self.leviKlikCanvas)
        self.canv.bind("<ButtonRelease-1>", self.leviReleaseCanvas)
        self.canv.bind("<B1-Motion>", self.leviPomeraCanvas)

        self.canv.bind("<Button-3>", self.desniKlikCanvas)
        self.canv.bind("<ButtonRelease-3>", self.desniReleaseCanvas)
        self.canv.bind("<B3-Motion>", self.desniPomeraCanvas)

        self.canv.bind("<Motion>", self.pomeraMis)
        self.root.bind("<Key>", self.pritisnuoTaster)

        self.root.mainloop()

    def pokreniAlgo(self,fun, ent = None, msg = 'Za Ovaj algoritam je potrebno uneti pocetni cvor.'):
        if (ent):
            try:
                num = int(ent.get())
            except:
                messagebox.showerror("Greska pri pokretanju", msg)
                return

            self.blokirajIzmene()
            Thread(target = lambda : fun(self, num) ).start()

        else:
            self.blokirajIzmene()
            Thread(target = lambda : fun(self) ).start()

    def prikaziUpustvo(self):
        pass

    def pomeraMis(self, event):
        prev = self.selektovanaDuzina

        najblizi = self.najblizaTezina(event.x,event.y)
        if (najblizi[0] > 50):
            self.selektovanaDuzina = None
            return
        self.selektovanaDuzina = najblizi[1]

        # promenio granu
        if (prev != self.selektovanaDuzina):
            self.tempDuzina = ''
        

    def pritisnuoTaster(self, event):
        num = event.keycode -48
        if (num < 0 or num > 9): return
        if (self.tempDuzina != None and self.selektovanaDuzina != None and self.selektovanaDuzina != -1):
            self.tempDuzina += str(num)

            self.canv.itemconfigure(self.selektovanaDuzina[1], text = self.tempDuzina)
            self.updateTezinu(self.selektovanaDuzina[1], int(self.tempDuzina))
            
    
    def updateTezinu(self, elem, tezina):
        for node1 in self.cvorovi:
            for node2 in self.cvorovi[node1]['veze']:
                if (self.cvorovi[node1]['veze'][node2][1] == elem):
                    self.cvorovi[node1]['veze'][node2][2] = tezina
                    self.graf.dodajGranu( self.pronadjiInxCvora(node1), self.pronadjiInxCvora(node2), tezina )

    def napraviCvor(self, x, y):
        ''' Kreira novi cvor u strukturi Graf i poziva crtanje kruga na poziciji x,y '''
        inx = self.graf.dodajCvor()
        elem1 = self.nacrtajKrug(x, y, 20, fill='snow',width=1)
        elem2 = self.canv.create_text(x,y,text = str(inx))
        self.cvorovi[elem1] = {'text': elem2, 'veze': {} }

    def updateGrane(self, node):
        ''' Updejtuje sve veze koje idu ili ulaze u cvor node '''
        if node not in self.cvorovi:
            return
        for node2 in list(self.cvorovi[node]['veze'].keys()):
            grana = self.cvorovi[node]['veze'][node2][0]
            tezina = self.cvorovi[node]['veze'][node2][1]
            num_tezina = self.cvorovi[node]['veze'][node2][2]
            self.cvorovi[node]['veze'].pop(node2)
            self.cvorovi[node2]['veze'].pop(node)
            self.canv.delete(grana)
            self.canv.delete(tezina)

            self.dodajGranu(node, node2, num_tezina)

    def dodajGranu(self, node1, node2, num_tezina = 1):
        ''' i crta liniju na canvasu '''
        if node1 not in self.cvorovi or node2 not in self.cvorovi or node1 in self.cvorovi[node2]['veze']:
            return
        A = self.koordinatiCvora(node1)
        B = self.koordinatiCvora(node2)
        if (A[0] < B[0]):
            A,B = B,A
            node1, node2=node2,node1
        X = mat.nadjiNormalu( mat.nadjiCentar(A,B), B, 10)
        A = self.izracunajDuz(A,B)
        B = self.izracunajDuz(B,A)
        veza = self.canv.create_line(A[0], A[1], B[0], B[1], width=1)
        tezina = self.canv.create_text(X[0],X[1],text = str(num_tezina))
        self.cvorovi[node1]['veze'][node2] = [veza, tezina, num_tezina]
        self.cvorovi[node2]['veze'][node1] = [veza, tezina, num_tezina]

        self.graf.dodajGranu( self.pronadjiInxCvora(node1), self.pronadjiInxCvora(node2), num_tezina )

    def najblizaTezina(self, x, y):
        ''' Vraca element teksta od tezine koja je najbliza koordinatama '''
        rez, relem = -1, -1
        for node1 in self.cvorovi:
            for node2 in self.cvorovi[node1]['veze']:
                pos = self.canv.coords(self.cvorovi[node1]['veze'][node2][1])
                pos = (pos[0], pos[1])
                if rez == -1 or ((pos[0]-x)**2 + (pos[1]-y)**2)**0.5 < rez:
                    rez = ((pos[0]-x)**2 + (pos[1]-y)**2)**0.5
                    relem = self.cvorovi[node1]['veze'][node2]
        # povratna vrednost je oblika (12.2, [linija, text, num_tezina] )
        return (rez, relem)


    def najbliziCvor(self, x, y, ignore = []):
        ''' Vraca canvas elem cvora koji je najblizi koordinatama x,y '''
        rez, relem = -1, -1
        for elem in self.cvorovi:
            if (elem in ignore):
                continue

            pos = self.canv.coords(elem)
            pos = (pos[0]+20, pos[1]+20)
            if rez == -1 or ((pos[0]-x)**2 + (pos[1]-y)**2)**0.5 < rez:
                rez = ((pos[0]-x)**2 + (pos[1]-y)**2)**0.5
                relem = elem
        return (rez, relem)

    def izracunajDuz(self, A, B):
        C = mat.pomeriTacku(A, B, 20)
        return (C[0], C[1], B[0], B[1])

    def koordinatiCvora(self, node):
        if node not in self.cvorovi:
            return (0,0)
        A = self.canv.coords(node)
        return (A[0]+20, A[1]+20)
        

    def desniKlikCanvas(self, event):
        najblizi = self.najbliziCvor(event.x, event.y)
        if (najblizi[0] != -1 and najblizi[0] < 20 ):
            self.selektovanCvor = najblizi[1]
            A = self.canv.coords(self.selektovanCvor)
            A = (A[0]+20, A[1]+20)
            rez = self.izracunajDuz(A, (event.x, event.y) )
            self.tempLine = self.canv.create_line( rez[0], rez[1], rez[2], rez[3])

    def desniPomeraCanvas(self, event):
        if (self.selektovanCvor and self.selektovanCvor in self.cvorovi and self.tempLine):
            A = self.canv.coords(self.selektovanCvor)
            A = (A[0]+20, A[1]+20)
            rez = self.izracunajDuz(A, (event.x, event.y) )
            self.canv.coords(self.tempLine,  rez[0], rez[1], rez[2], rez[3])

    def desniReleaseCanvas(self, event):
        if (self.tempLine):
            najblizi = self.najbliziCvor(event.x, event.y)
            if (najblizi[0] != -1 and najblizi[0] <= 20 and najblizi[1] != self.selektovanCvor ):
                self.dodajGranu(self.selektovanCvor, najblizi[1])
            
            self.canv.delete(self.tempLine)
            self.tempLine = None
        self.selektovanCvor = None

    def leviKlikCanvas(self, event):
        najblizi = self.najbliziCvor(event.x, event.y)
        if (najblizi[0] == -1 or najblizi[0] > 50 ):
            self.napraviCvor(event.x, event.y)
        elif (najblizi[0] != -1):
            self.selektovanCvor = najblizi[1]
            pos = self.canv.coords(najblizi[1])
            self.selektovanOffset = (event.x-pos[0]-20, event.y-pos[1]-20)

    def leviPomeraCanvas(self, event):
        if (self.selektovanCvor and self.selektovanCvor in self.cvorovi):
            addx =  event.x - self.canv.coords(self.selektovanCvor)[0]-20 - self.selektovanOffset[0]
            addy =  event.y - self.canv.coords(self.selektovanCvor)[1]-20 - self.selektovanOffset[1]
            self.canv.move(self.selektovanCvor, addx, addy)
            self.canv.move(self.cvorovi[self.selektovanCvor]['text'], addx, addy)
            self.updateGrane(self.selektovanCvor)

    def leviReleaseCanvas(self, event):
        self.selektovanCvor = None

    def nacrtajKrug(self, x, y, r, **kwargs):
        return self.canv.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def pronadjiElemCvora(self, inx):
        for node in self.cvorovi:
            cvor = self.canv.itemcget(self.cvorovi[node]['text'], 'text')
            if (str(inx) == cvor):
                return node
    
    def pronadjiInxCvora(self, elem):
        if (elem not in self.cvorovi):
            return -1

        return int(self.canv.itemcget(self.cvorovi[elem]['text'], 'text'))

    ###
    ### Manipulacija sa grafom
    ###
    def selectCvor(self, node, col = 'pink'):
        elem = self.pronadjiElemCvora(node)
        if (elem == None):
            return

        self.canv.itemconfigure(elem, fill=col)
    
    def disselectCvor(self, node):
        return self.selectCvor(node, 'snow')

    def selectGranu(self, inx1, inx2, col = 'red'):
        elem1 = self.pronadjiElemCvora(inx1)
        elem2 = self.pronadjiElemCvora(inx2)
        if (not elem1 or not elem2):
            return

        for ngb in self.cvorovi[elem1]['veze']:
            if elem2 == ngb:
                self.canv.itemconfigure( self.cvorovi[elem1]['veze'][ngb][0], fill = col )
                if (col != 'black'): self.canv.itemconfigure( self.cvorovi[elem1]['veze'][ngb][0], width=2 )
                else: self.canv.itemconfigure( self.cvorovi[elem1]['veze'][ngb][0], width=1 )

    def disselectGranu(self, node1, node2):
        return self.selectGranu(node1, node2, 'black')

    def blokirajIzmene(self):
        pass

    def oslobodiIzmene(self):
        pass

    def izvrsiNaredbu(self,fun,*arg):
        self.root.after(5, lambda : fun(*arg) )

    ###
    ###
    ###


if __name__ == "__main__":
    G = Graf()
    app = GUI(G)
    app.mainProzor()