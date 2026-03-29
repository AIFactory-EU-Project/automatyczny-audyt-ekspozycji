import json
import sys
import time
from generate_planogram_report import fill_status, El, read_planogram, read_boxes
import subprocess


def sort(es):
    return sorted(es, key=lambda e: (e.shelf, e.position))



def show_shelves(title, es):
    """ Draw shelves with elements """
    print(title)
    shelf = max([e.shelf for e in es])
    while shelf >= 1:
        print("{}:".format(shelf), end=' ')

        shelf_es = sorted([e for e in es if e.shelf == shelf], key=lambda e: e.position)
        for e in shelf_es:
            print(('['+e.index+']')*e.faces_count, end=' ')
        print()
        shelf -= 1
    print()

def print_report(title, es):
    status_name = {1: "OK", 2: "ZA_MALO_TWARZY", 3: "ZLA_POLKA", 4: "BRAK"}
    print(title)
    print('index   ', 'shelf', 'pos', 'faces', 'status')
    for e in es:
        print("{:10s} {:3.0f} {:3.0f} {:5.0f} {}".format(
            e.index, e.shelf, e.position, e.faces_count, status_name.get(e.status, '')))
    print()


def check_int(planogram, detection, ex_report):
    print(json.dumps({
        'planogram': planogram2input(planogram),
        'boxes': boxes2input(report),
    }, indent=2))

        
        
def check_unit(planogram, detection, ex_report=None):
    print('---------------------------------------------------')
    show_shelves('Planogram', planogram)
    show_shelves('Detection', detection)
    score = fill_status(planogram, detection)
    print_report('Report', planogram)
    print('score {:.0f}%'.format(score))
    print()
    
    if ex_report:
        assert planogram == ex_report, planogram
            
def check_test(planogram, boxes, ex_report=None):
    print('---------------------------------------------------')
    
    x = json.dumps({
        'planogram': planogram,
        'boxes': boxes,
    }).encode('utf8')
    

    resp = subprocess.run(['python3', 'generate_planogram_report.py'], stdout=subprocess.PIPE, input=x)
    y = resp.stdout.decode('utf-8')
    #print (y)
    y = json.loads(y)

    
    planogram = read_planogram(planogram)
    boxes = read_boxes(boxes)    
    report = [El(e["index"], e["shelf"], e["position"], e["faces_count"], e["status"]) for e in y['planogram_report']]
    score = y['score']
    
    
    
    show_shelves('Planogram', planogram)
    show_shelves('Boxes', boxes)
    print_report('Report', report)
    print('score {:.0f}%'.format(score))
    print()
    
    if ex_report:
        assert planogram == ex_report, planogram
    


#map_planogram_input
#map_detection_input


def elems2planogram(elems):
    planogram = []
    for e in elems:
        planogram.append({
            "index": e.index,
            "shelf": e.shelf,
            "position": e.position,
            "faces_count": e.faces_count})
    return planogram


def elems2boxes(elems):
    boxes = []
    for e in elems:
        boxes.append({
            "skuIndex": e.index,
            "shelfFromTop": e.shelf,
            "positionFromLeft": e.position
        })
    return boxes
    


def el_dict(e):
    if e.status is None:
        return {"index":e.index, "shelf":e.shelf, "position":e.position, "faces_count":e.faces_count}
    else:
        return {"index":e.index, "shelf":e.shelf, "position":e.position, "faces_count":e.faces_count, "status": e.status}


def test1():
    planogram = elems2planogram([
        El("G",1,1,1),
        El("M",1,2,1),
        El("I",1,3,1),
        El("J",1,4,1),

        El("D",2,1,2),
        El("E",2,2,1),
        El("F",2,3,1),

        El("A",3,1,1),
        El("B",3,2,1),
        El("C",3,3,2),
    ])
    boxes = elems2boxes([
        El("H",1,1,1),
        El("W",1,2,1),
        El("J",1,3,1),
        El("I",1,4,1),

        El("D",2,1,1),
        El("D",2,2,1),
        El("E",2,3,1),
        El("E",2,4,1),
        El("Z",2,5,1),
        El("X",2,6,1),

        El("B",3,1,1),
        El("C",3,2,1),
        El("C",3,3,1),
    ])
    check_test(planogram, boxes)


def test2():
    planogram = elems2planogram([
        El("D",1,1,2),
        El("E",1,2,1),

        El("A",2,1,2),
        El("B",2,2,1),
        El("C",2,3,1),
    ])
    boxes = elems2boxes([
        El("L",1,1,1),
        El("D",1,2,1),
        El("A",1,3,1),
        El("E",1,4,1),

        El("G",2,1,1),
        El("E",2,2,1),
        El("C",2,3,1),
        El("B",2,4,1),
        El("B",2,5,1),
    ])
    check_test(planogram, boxes)

def test3():
    planogram = elems2planogram([
        El("D",1,1,2),
        El("E",1,2,1),
        
        El("A",2,1,2),
        El("B",2,2,1),
        El("C",2,3,1),
    ])
    boxes = elems2boxes([
        El("A",1,1,1),
        El("L",1,2,1),
        El("E",1,3,1),

        El("A",2,1,1),
        El("B",2,2,1),
        El("A",2,3,1),
        El("C",2,4,1),
        El("B",2,5,1),
        El("E",2,6,1),
        El("D",2,7,1),
    ])
    check_test(planogram, boxes)




def test4():
    planogram = elems2planogram([
        El("D",1,1,2),
        El("E",1,2,1),

        El("A",2,1,2),
        El("B",2,2,1),
        El("C",2,3,1),
        El("A",2,3,1),
    ])
        
    boxes = elems2boxes([
        El("A",1,1,1),
        El("L",1,2,1),
        El("E",1,3,1),

        El("A",2,1,1),
        El("B",2,2,1),
        El("A",2,3,1),
        El("C",2,4,1),
        El("B",2,5,1),
        El("E",2,6,1),
        El("D",2,7,1),
    ])
    check_test(planogram, boxes)

def test5_real():    
    planogram = [
        {"index":"10929954","shelf":1,"position":35,"faces_count":1},
        {"index":"10931554","shelf":1,"position":36,"faces_count":1},
        {"index":"10931553","shelf":1,"position":37,"faces_count":1},
        {"index":"10931545","shelf":1,"position":38,"faces_count":1},
        {"index":"10931546","shelf":1,"position":39,"faces_count":1},
        {"index":"10985242","shelf":1,"position":40,"faces_count":1},
        {"index":"10985243","shelf":1,"position":41,"faces_count":1},
        {"index":"10985876","shelf":1,"position":42,"faces_count":1},
        {"index":"10985877","shelf":1,"position":43,"faces_count":1},
        {"index":"12003574","shelf":1,"position":44,"faces_count":1},
        {"index":"12003581","shelf":1,"position":45,"faces_count":1},
        {"index":"12002262","shelf":1,"position":46,"faces_count":1},
        {"index":"12005005","shelf":2,"position":29,"faces_count":1},
        {"index":"12004987","shelf":2,"position":30,"faces_count":1},
        {"index":"12003572","shelf":2,"position":31,"faces_count":1},
        {"index":"12003601","shelf":2,"position":32,"faces_count":1},
        {"index":"12004471","shelf":2,"position":33,"faces_count":1},
        {"index":"12004968","shelf":2,"position":34,"faces_count":1},
        {"index":"12004979","shelf":3,"position":23,"faces_count":1},
        {"index":"12004988","shelf":3,"position":24,"faces_count":1},
        {"index":"12004980","shelf":3,"position":25,"faces_count":1},
        {"index":"12004708","shelf":3,"position":26,"faces_count":1},
        {"index":"12004954","shelf":3,"position":27,"faces_count":1},
        {"index":"12005007","shelf":3,"position":28,"faces_count":1},
        {"index":"10985950","shelf":4,"position":16,"faces_count":1},
        {"index":"10985949","shelf":4,"position":17,"faces_count":1},
        {"index":"12004496","shelf":4,"position":18,"faces_count":1},
        {"index":"12004480","shelf":4,"position":19,"faces_count":1},
        {"index":"12004221","shelf":4,"position":20,"faces_count":1},
        {"index":"12004612","shelf":4,"position":21,"faces_count":1},
        {"index":"12005461","shelf":4,"position":22,"faces_count":1},
        {"index":"12004562","shelf":5,"position":10,"faces_count":1},
        {"index":"12003987","shelf":5,"position":11,"faces_count":1},
        {"index":"12002243","shelf":5,"position":12,"faces_count":1},
        {"index":"12002232","shelf":5,"position":13,"faces_count":1},
        {"index":"12004669","shelf":5,"position":14,"faces_count":1},
        {"index":"12004241","shelf":5,"position":15,"faces_count":1},
        {"index":"12004982","shelf":6,"position":1,"faces_count":1},
        {"index":"12005006","shelf":6,"position":2,"faces_count":1},
        {"index":"12004981","shelf":6,"position":3,"faces_count":1},
        {"index":"12003593","shelf":6,"position":4,"faces_count":1},
        {"index":"12003614","shelf":6,"position":5,"faces_count":1},
        {"index":"12004574","shelf":6,"position":6,"faces_count":1},
        {"index":"12002252","shelf":6,"position":7,"faces_count":1},
        {"index":"12002242","shelf":6,"position":8,"faces_count":1},
        {"index":"20000008","shelf":6,"position":9,"faces_count":1}
    ]
    
    boxes = [{"accuracy": 99, "shelfFromTop": 1, "positionFromLeft": 1, "skuIndex": "10931545", "box": {"topLeftX": 41, "topLeftY": 706, "width": 103, "height": 108}}, {"accuracy": 99, "shelfFromTop": 1, "positionFromLeft": 2, "skuIndex": "10931545", "box": {"topLeftX": 143, "topLeftY": 713, "width": 114, "height": 115}}, {"accuracy": 99, "shelfFromTop": 1, "positionFromLeft": 3, "skuIndex": "10931545", "box": {"topLeftX": 267, "topLeftY": 709, "width": 110, "height": 117}}, {"accuracy": 99, "shelfFromTop": 1, "positionFromLeft": 4, "skuIndex": "10931545", "box": {"topLeftX": 378, "topLeftY": 716, "width": 107, "height": 109}}, {"accuracy": 99, "shelfFromTop": 1, "positionFromLeft": 5, "skuIndex": "10985242", "box": {"topLeftX": 498, "topLeftY": 720, "width": 117, "height": 106}}, {"accuracy": 99, "shelfFromTop": 1, "positionFromLeft": 6, "skuIndex": "10985242", "box": {"topLeftX": 601, "topLeftY": 719, "width": 123, "height": 107}}, {"accuracy": 99, "shelfFromTop": 1, "positionFromLeft": 7, "skuIndex": "10985242", "box": {"topLeftX": 710, "topLeftY": 714, "width": 122, "height": 106}}, {"accuracy": 99, "shelfFromTop": 2, "positionFromLeft": 1, "skuIndex": "TORTILLA KONSPOL", "box": {"topLeftX": 32, "topLeftY": 579, "width": 112, "height": 65}}, {"accuracy": 99, "shelfFromTop": 2, "positionFromLeft": 2, "skuIndex": "TORTILLA KONSPOL", "box": {"topLeftX": 154, "topLeftY": 578, "width": 110, "height": 66}}, {"accuracy": 99, "shelfFromTop": 2, "positionFromLeft": 3, "skuIndex": "JEDRUS", "box": {"topLeftX": 271, "topLeftY": 578, "width": 125, "height": 95}}, {"accuracy": 99, "shelfFromTop": 2, "positionFromLeft": 4, "skuIndex": "JEDRUS", "box": {"topLeftX": 392, "topLeftY": 587, "width": 109, "height": 80}}, {"accuracy": 99, "shelfFromTop": 2, "positionFromLeft": 5, "skuIndex": "JEDRUS", "box": {"topLeftX": 496, "topLeftY": 585, "width": 120, "height": 57}}, {"accuracy": 99, "shelfFromTop": 2, "positionFromLeft": 6, "skuIndex": "12003573", "box": {"topLeftX": 611, "topLeftY": 583, "width": 114, "height": 72}}, {"accuracy": 99, "shelfFromTop": 2, "positionFromLeft": 7, "skuIndex": "PANIEROWANE", "box": {"topLeftX": 719, "topLeftY": 584, "width": 110, "height": 82}}, {"accuracy": 99, "shelfFromTop": 3, "positionFromLeft": 1, "skuIndex": "12004954", "box": {"topLeftX": 339, "topLeftY": 470, "width": 131, "height": 82}}, {"accuracy": 99, "shelfFromTop": 3, "positionFromLeft": 2, "skuIndex": "12004954", "box": {"topLeftX": 473, "topLeftY": 475, "width": 138, "height": 70}}, {"accuracy": 99, "shelfFromTop": 3, "positionFromLeft": 3, "skuIndex": "12004954", "box": {"topLeftX": 600, "topLeftY": 471, "width": 134, "height": 82}}, {"accuracy": 83, "shelfFromTop": 3, "positionFromLeft": 4, "skuIndex": "12002745", "box": {"topLeftX": 737, "topLeftY": 485, "width": 103, "height": 74}}, {"accuracy": 99, "shelfFromTop": 4, "positionFromLeft": 1, "skuIndex": "SZAMAMM OBIADOWE", "box": {"topLeftX": 186, "topLeftY": 355, "width": 177, "height": 60}}, {"accuracy": 99, "shelfFromTop": 4, "positionFromLeft": 2, "skuIndex": "12004980", "box": {"topLeftX": 368, "topLeftY": 353, "width": 154, "height": 65}}, {"accuracy": 99, "shelfFromTop": 4, "positionFromLeft": 3, "skuIndex": "0", "box": {"topLeftX": 524, "topLeftY": 361, "width": 145, "height": 50}}, {"accuracy": 49, "shelfFromTop": 4, "positionFromLeft": 4, "skuIndex": "0", "box": {"topLeftX": 675, "topLeftY": 362, "width": 158, "height": 53}}, {"accuracy": 99, "shelfFromTop": 5, "positionFromLeft": 1, "skuIndex": "10985949", "box": {"topLeftX": 11, "topLeftY": 227, "width": 116, "height": 97}}, {"accuracy": 99, "shelfFromTop": 5, "positionFromLeft": 2, "skuIndex": "10985950", "box": {"topLeftX": 109, "topLeftY": 219, "width": 149, "height": 110}}, {"accuracy": 99, "shelfFromTop": 5, "positionFromLeft": 3, "skuIndex": "12003572", "box": {"topLeftX": 325, "topLeftY": 221, "width": 178, "height": 94}}, {"accuracy": 99, "shelfFromTop": 5, "positionFromLeft": 4, "skuIndex": "12003572", "box": {"topLeftX": 505, "topLeftY": 216, "width": 164, "height": 124}}, {"accuracy": 99, "shelfFromTop": 6, "positionFromLeft": 1, "skuIndex": "12003987", "box": {"topLeftX": 225, "topLeftY": 99, "width": 120, "height": 89}}, {"accuracy": 99, "shelfFromTop": 6, "positionFromLeft": 2, "skuIndex": "12002232", "box": {"topLeftX": 436, "topLeftY": 82, "width": 130, "height": 114}}, {"accuracy": 99, "shelfFromTop": 6, "positionFromLeft": 3, "skuIndex": "12004669", "box": {"topLeftX": 559, "topLeftY": 86, "width": 109, "height": 114}}, {"accuracy": 99, "shelfFromTop": 6, "positionFromLeft": 4, "skuIndex": "12002243", "box": {"topLeftX": 672, "topLeftY": 78, "width": 157, "height": 124}}, {"accuracy": 99, "shelfFromTop": 7, "positionFromLeft": 1, "skuIndex": "12003593", "box": {"topLeftX": 17, "topLeftY": 0, "width": 78, "height": 49}}, {"accuracy": 99, "shelfFromTop": 7, "positionFromLeft": 2, "skuIndex": "12003593", "box": {"topLeftX": 97, "topLeftY": 1, "width": 77, "height": 53}}, {"accuracy": 99, "shelfFromTop": 7, "positionFromLeft": 3, "skuIndex": "12003593", "box": {"topLeftX": 172, "topLeftY": 0, "width": 84, "height": 57}}, {"accuracy": 99, "shelfFromTop": 7, "positionFromLeft": 4, "skuIndex": "12003614", "box": {"topLeftX": 253, "topLeftY": 0, "width": 85, "height": 58}}, {"accuracy": 99, "shelfFromTop": 7, "positionFromLeft": 5, "skuIndex": "ZUPA", "box": {"topLeftX": 348, "topLeftY": 1, "width": 116, "height": 58}}, {"accuracy": 98, "shelfFromTop": 7, "positionFromLeft": 6, "skuIndex": "0", "box": {"topLeftX": 478, "topLeftY": 0, "width": 76, "height": 27}}, {"accuracy": 99, "shelfFromTop": 7, "positionFromLeft": 7, "skuIndex": "12002252", "box": {"topLeftX": 565, "topLeftY": 0, "width": 145, "height": 62}}, {"accuracy": 99, "shelfFromTop": 7, "positionFromLeft": 8, "skuIndex": "12002242", "box": {"topLeftX": 693, "topLeftY": 0, "width": 138, "height": 63}}]

    check_test(planogram, boxes)


_run_i=0
def run(f):
    global _run_i
    k = int(sys.argv[2]) if len(sys.argv) >= 3 else None    
    print(f.__name__, '[{}]'.format(_run_i))
    if k is None or _run_i == k:
        t0 = time.time()
        f()
        t1 = time.time()
        #print('... runtime_s {:.3f}'.format(t1-t0))
    else:
        print('... skip') 
    _run_i+=1

if __name__ == '__main__':
    run(test1)
    run(test2)
    run(test3)
    run(test4)
    run(test5_real)
