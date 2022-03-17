import time, pq

def dijkstra(main, node):
    graf = main.graf

    # definisemo priority queue
    pred = pq.PriorityQueue()
    pred.insert((0, node, -1))
    poseceni = []

    # petlja dok postoji cvorova u redu
    while (not pred.isEmpty()):
        dist, cur, prev = pred.delete()
        dist = -dist

        # Proveri da li je vec posecen
        if (cur in poseceni):
            continue
        poseceni.append(cur)

        main.izvrsiNaredbu(main.selectCvor, cur)
        if (prev!=-1): main.izvrsiNaredbu(main.selectGranu, prev, cur, "orange")
        time.sleep(1)

        # prolazimo kroz sve komsije (veze je mapa, koja mapira cvorove ka tezini grane )
        veze = graf.dohvatiVeze(cur)
        for ngb in veze:
            if (ngb==prev): continue
            #udaljenost do komsije
            dngb = dist + veze[ngb]

            main.izvrsiNaredbu(main.selectGranu, ngb, cur)
            time.sleep(1)

            # provera da li je komsija posecen
            if (ngb not in poseceni):
                pred.insert( (-dngb, ngb, cur) )

            main.izvrsiNaredbu(main.disselectGranu, ngb, cur)

        main.izvrsiNaredbu(main.selectCvor, cur, 'gray75')

