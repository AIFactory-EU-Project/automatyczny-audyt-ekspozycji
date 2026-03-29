"""" Version: 3
Format danych wejścia/wyjścia skryptu do generowania raportu:

Na stdin przyjmuje json postaci (dane planogramu z bazy):
```
{
  "planogram": [
    {
      "index": <index_sku:string>,
      "shelf": <shelf:int> ,
      "position": <pos:int>,
      "faces_count": <faces:int>
    },
    ...
  ],
  "boxes": <lista "boxes" zwrocona z ai service>
}
```

Na stdout zwraca json postaci (dane do wyświetlenia w raporcie):
```
{
  "score": <zgodnosc%:int>,
  "abundance": <obfitosc%:int>,
  "availability": <dostepnosc%:int>,
  "planogram_report": [
    {
      "index": <index_sku:string>,
      "shelf": <shelf:int> ,
      "position": <pos:int>,
      "faces_count": <faces:int>,
      "status": <int>
    },
    ...
  ]
}
```

gdzie status oznacza:
1 -> "OK"
2 -> "ZA MAŁO TWARZY"
3 -> "ZŁA PÓŁKA"
4 -> "BRAK"

"""
import sys
import logging
import json


g_status_name = {0: "ERROR", 1: "OK", 2: "ZA_MALO_TWARZY", 3: "ZLA_POLKA", 4: "BRAK"}


class El:
    def __init__(self, index, shelf, position, faces_count, status=None):
        self.index, self.shelf, self.position, self.faces_count, self.status = index, shelf, position, faces_count, status

    def __str__(self):
        return "{:7s} {:3.0f} {:3.0f} {:5.0f} {}".format(self.index, self.shelf, self.position, self.faces_count, g_status_name.get(self.status, ''))


def read_planogram(planogram_input):
    planogram = []
    for p in planogram_input:
        planogram.append(El(p["index"], p["shelf"], p["position"], p["faces_count"]))
    return planogram


def read_boxes(boxes_input):
    boxes = []
    for b in boxes_input:
        boxes.append(El(b["skuIndex"], b["shelfFromTop"], b["positionFromLeft"], 1))
    return boxes


def write_report(planogram):
    planogram_input = []
    for p in planogram:
        planogram_input.append({
            "index": p.index,
            "shelf": p.shelf,
            "position": p.position,
            "faces_count": p.faces_count,
            "status": p.status})
    return planogram_input



def main():
    input_json = sys.stdin.read()
    input = json.loads(input_json)
    
    planogram = read_planogram(input["planogram"])
    boxes = read_boxes(input["boxes"])

    score, abundance, availability = fill_status(planogram, boxes)
    
    sys.stdout.write(json.dumps({
        "planogram_report": write_report(planogram),
        "score": int(score),
        "abundance": int(abundance),
        "availability": int(availability),
    })+'\n')








def report_aggregate_faces(report):
    report_by_shelf_pos = sorted(report, key=lambda e: (e.shelf, e.position))
    cs = []
    c = El(None, None, None, None)
    for r in report_by_shelf_pos:
        if r.index == c.index and r.shelf == c.shelf:
            c.faces_count += 1
        else:
            cs.append(c)
            c = El(r.index, r.shelf, r.position, 1)
    cs.append(c)
    cs = cs[1:]
    return cs

# OK
def is_status1(p, report):
    for r in report:
        if p.index == r.index and p.shelf == r.shelf:
            if p.faces_count <= r.faces_count:
                return True
    return False

# ZA MALO TWARZY
def is_status2(p, report):
    for r in report:
        if p.index == r.index and p.shelf == r.shelf:
            if p.faces_count > r.faces_count:
                return True
    return False

# ZLA POLKA
def is_status3(p, report):
    for r in report:
        if p.index == r.index and p.shelf != r.shelf:
            return True
    return False



def get_indexes(xs):
    return set(x.index for x in xs)

def get_availability(boxes, planogram):    
    pi = get_indexes(planogram)
    bi = get_indexes(boxes)
    if len(pi) == 0:
        return 100
    availability01 = len(pi.intersection(bi))/len(pi)
    availability = min(100*availability01, 100)
    return availability
    



def fill_status(planogram, report):
    """ Return score% """
    report2 = report_aggregate_faces(report)
    boxes = report2
    
    #print('report2')
    #for r in report2:
    #    print(r)
    #print()
    
    
    #  Zgodność z planogramem = Liczba produktów umieszczonych na półce zgodnie z planogramem zaakceptowanym przez centralę
    score = 0
    max_score = 0
    p_count_ok_faces = 0
    for p in planogram:
        if   is_status1(p, report2):
            p.status = 1            
            score += 1                        
        elif is_status2(p, report2):
            p.status = 2            
        elif is_status3(p, report2):
            p.status = 3            
        else:
            p.status = 4
        
        max_score += 1

    
    # Obfitość = Puste miejsca na półce vs. maksymalna ilość face’ów produktów wg. planogramu
    # abundance
    p_total_faces = sum(p.faces_count for p in planogram)
    b_total_faces = sum(b.faces_count for b in boxes)
    if p_total_faces == 0:
        return 100    
    abundance = min(100*b_total_faces/p_total_faces, 100)

    # Dostępność liczona jako: ilość produktów rozpoznanych z planogramu  vs. ilość produktów na półce    
    # availability
    availability = get_availability(boxes, planogram)
    
    # zgodnosc
    if max_score == 0:
        max_score = 1
    return (score/max_score)*100, abundance, availability



if __name__ == '__main__':
    main()



