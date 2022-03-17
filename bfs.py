import time

def bfs(main, node):
    graf = main.graf

    # definisemo prazan red sa pocetnim cvorom
    red = [node]
    poseceni = [node]
    
    # petlja dok postoji cvorova u redu
    while (len(red)):
        cur = red.pop(0)
        main.izvrsiNaredbu(main.selectCvor, cur)
        time.sleep(1)

        # prolazimo kroz sve komsije
        for ngb in graf.dohvatiVeze(cur):
            main.izvrsiNaredbu(main.selectGranu, ngb, cur)
            time.sleep(1)

            # provera da li je komsija posecen
            if (ngb not in poseceni):
                red.append(ngb)
                poseceni.append(ngb)

            main.izvrsiNaredbu(main.disselectGranu, ngb, cur)

        main.izvrsiNaredbu(main.selectCvor, cur, 'gray75')

