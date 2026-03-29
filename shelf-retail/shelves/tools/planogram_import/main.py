import sys
import pandas as pd
import numpy as np
from logger import configure_logging
from datetime import datetime
import logging
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import csv

#
# TODO: input data in normal form: 2 csv files: planogram_assignment.csv planogram.csv
#

Base = None
Session = None
Planogram = None
Segment = None
Shop = None
Sku = None
PlanogramElement = None
ShopPlanogramAssignment = None
Camera = None
Photo = None


def connect_db(DBURL):
    global Base, Session
    global Planogram, Segment, Shop, Sku, PlanogramElement, ShopPlanogramAssignment, Camera, Photo

    Base = automap_base()
    engine = create_engine(DBURL, echo=0)
    Base.prepare(engine, reflect=1)

    Planogram = Base.classes.planogram
    Segment = Base.classes.segment
    Shop = Base.classes.shop
    Sku = Base.classes.sku
    PlanogramElement = Base.classes.planogram_element
    ShopPlanogramAssignment = Base.classes.shop_planogram_assignment
    Camera = Base.classes.camera
    Photo = Base.classes.photo

    Session = sessionmaker(bind=engine)


planogram_csv_dtype = [
    ('shop_planogram_assignment.shop.codes', str),
    ('shop_planogram_assignment.segment.id', int),
    ('shop_planogram_assignment.start_date_time', str),
    ('shop_planogram_assignment.end_date_time', str),
    ('planogram.name', str),
    ('planogram.version', str),
    ('planogram.description', str),
    ('planogram_element.shelf', int),
    ('planogram_element.position', int),
    ('planogram_element.sku.index', str),
    ('planogram_element.sku.name', str),
    ('planogram_element.faces_count', int),
    ('planogram_element.stack_count', int)]


def pd_type(t):
    if t == str:
        return np.string_
    if t == int:
        return np.int64
    return t


def check_duplicates(df0):
    df = df0[['planogram.name', 'shop_planogram_assignment.segment.id', 'planogram_element.sku.index', 'planogram_element.shelf', 'planogram_element.position']]
    first = {}
    n=0
    for i, row in df.iterrows():
        key = tuple(row)
        if key not in first:
            first[key] = i
        else:
            logging.warning('line {} duplicated at {}'.format(first[key], i))
            n += 1
    return n


def export_planogram_csv(path_csv, planogram_id):
    session = Session()

    #lst = session.query(ShopPlanogramAssignment).join(Planogram).join(PlanogramElement).join(Sku).filter(ShopPlanogramAssignment.id == spa_id).all()
    #import pdb;
    #pdb.set_trace()

    columns, dtype = zip(*planogram_csv_dtype)
    # print(list(map(pd_type, dtype)))
    # df = pd.DataFrame(columns=columns, dtype=list(map(pd_type, dtype)))
    df = pd.DataFrame(columns=columns)


    planogram = session.query(Planogram).filter_by(id=planogram_id).first()
    if planogram is None:
        logging.warning("planogram not found: id: {}".format(planogram_id))
        return

    spas = session.query(ShopPlanogramAssignment).filter_by(planogram=planogram).all()
    #spas = session.query(ShopPlanogramAssignment).all()
    for spa in spas:
        for pe in spa.planogram.planogram_element_collection:
            row = {
                'shop_planogram_assignment.shop.codes': spa.shop.code,
                'shop_planogram_assignment.segment.id': spa.segment.id,
                'shop_planogram_assignment.start_date_time': spa.start_date_time.strftime("%Y-%m-%d %H:%M:%S"),
                'shop_planogram_assignment.end_date_time': spa.end_date_time.strftime("%Y-%m-%d %H:%M:%S"),
                'planogram.name': pe.planogram.name,
                'planogram.version': pe.planogram.version,
                'planogram.description': pe.planogram.description,
                'planogram_element.shelf': pe.shelf,
                'planogram_element.position': pe.position,
                'planogram_element.sku.index': pe.sku.index,
                'planogram_element.sku.name': pe.sku.name,
                'planogram_element.faces_count': pe.faces_count,
                'planogram_element.stack_count': pe.stack_count}
            df = df.append(row, ignore_index=1)

    df.to_csv(path_csv, index=False, quoting=csv.QUOTE_NONNUMERIC, sep=';')



def to_string(obj):
    kvs = ((c.name, getattr(obj, c.name)) for c in obj.__class__.__table__.columns)
    args = ', '.join(['{}={}'.format(k,repr(v)) for k,v in kvs])
    return "{}({})".format(obj.__class__.__name__, args)

def import_planogram_csv(path_csv):
    session = Session()

    # sklepy, segmenty, kamery narazie na sztywno
    """
    shops = [
        Shop(id=1, code="Z1891", name="Poznan dabrowskiego 26"),
        Shop(id=2, code="Z0810", name="Poznan strzelecka 13"),
        Shop(id=3, code="Z1790", name="Poznan opolska 29"),
        Shop(id=4, code="Z6730", name="Warszawa przeworska 3"),
        Shop(id=5, code="Z6311", name="Warszawa gagarina 33"),
        Shop(id=6, code="Z6688", name="Warszawa faworytki 2"),
        Shop(id=7, code="Z8008", name="Warszawa targowa 80"),
        Shop(id=8, code="Z6436", name="Warszawa gen r abrahama 18"),
        Shop(id=9, code="Z6742", name="Warszawa odkryta 51A"),
        Shop(id=10, code="Z7510", name="Warszawa zamiany 12"),
        Shop(id=11, code="Z5928", name="Warszawa jana kazimierza 33"),
        Shop(id=12, code="Z5433", name="Warszawa rzeczypospolitej 33"),
        Shop(id=13, code="Z8508", name="Warszawa modlińska 61"),
        Shop(id=14, code="Z0435", name="Poznan uminskiego 12"),
        Shop(id=15, code="Z2680", name="Poznan kutrzeby 14"),
        Shop(id=16, code="Z5606", name="Poznan dabrowskiego 7"),
        Shop(id=17, code="Z2520", name="Poznan malwowa 128 Daliowa 1A"),
        Shop(id=18, code="Z8788", name="Poznan swierzawska 14"),
        Shop(id=19, code="Z8607", name="Poznan jeleniogorska 7"),
        Shop(id=20, code="Z2957", name="Poznan falista 4a 2N")]
    """
    shops = [
        Shop(id=1, code="Z1891", name="Poznan_dabrowskiego_26"),
        Shop(id=2, code="Z0810", name="Poznan_strzelecka_13"),
        Shop(id=3, code="Z1790", name="Poznan_opolska_29"),
        Shop(id=4, code="Z6730", name="Warszawa_przeworska_3"),
        Shop(id=5, code="Z6311", name="Warszawa_gagarina_33"),
        Shop(id=6, code="Z6688", name="Warszawa_faworytki_2"),
        Shop(id=7, code="Z8008", name="Warszawa_targowa_80"),
        Shop(id=8, code="Z6436", name="Warszawa_gen_r_abrahama_18"),
        Shop(id=9, code="Z6742", name="Warszawa_odkryta_51A"),
        Shop(id=10, code="Z7510", name="Warszawa_zamiany_12"),
        Shop(id=11, code="Z5928", name="Warszawa_jana_kazimierza_33"),
        Shop(id=12, code="Z5433", name="Warszawa_rzeczypospolitej_33"),
        Shop(id=13, code="Z8508", name="Warszawa_modlińska_61"),
        Shop(id=14, code="Z0435", name="Poznan_uminskiego_12"),
        Shop(id=15, code="Z2680", name="Poznan_kutrzeby_14"),
        Shop(id=16, code="Z5606", name="Poznan_dabrowskiego_7"),
        Shop(id=17, code="Z2520", name="Poznan_malwowa_128_Daliowa_1A"),
        Shop(id=18, code="Z8788", name="Poznan_swierzawska_14"),
        Shop(id=19, code="Z8607", name="Poznan_jeleniogorska_7"),
        Shop(id=20, code="Z2957", name="Poznan_falista_4a_2N")]



    segments = [
        Segment(id=2, name="dania_gotowe", type='READY_MEAL'),
        Segment(id=3, name="szybkie_przekaski", type='QUICK_SNACK'),
        Segment(id=1, name="grille_rollery", type='GRILL')]

    cameras = [
        Camera(id=41, type="dahua", ip="172.16.1.251", manipulation_settings='{"rotate_angle": 0, "crop_x": 769, "crop_y": 132, "crop_width": 427, "crop_height": 385}'),
        Camera(id=42, type="dahua", ip="172.16.2.251", manipulation_settings='{"rotate_angle": 8, "crop_x": 746, "crop_y": 370, "crop_width": 384, "crop_height": 329}'),
        Camera(id=43, type="hikvision", ip="172.16.3.251", manipulation_settings='{"rotate_angle": 0, "crop_x": 744, "crop_y": 327, "crop_width": 394, "crop_height": 364}'),
        Camera(id=44, type="dahua", ip="172.16.4.251", manipulation_settings='{"rotate_angle": -4, "crop_x": 638, "crop_y": 446, "crop_width": 527, "crop_height": 491}'),
        Camera(id=45, type="hikvision", ip="172.16.5.251", manipulation_settings='{"rotate_angle": 80, "crop_x": 479, "crop_y": 272, "crop_width": 448, "crop_height": 401}'),
        Camera(id=46, type="hikvision", ip="172.16.6.251", manipulation_settings='{"rotate_angle": 0, "crop_x": 817, "crop_y": 439, "crop_width": 343, "crop_height": 268}'),
        Camera(id=47, type="hikvision", ip="172.16.7.251", manipulation_settings='{"rotate_angle": -85, "crop_x": 882, "crop_y": 587, "crop_width": 344, "crop_height": 351}'),
        Camera(id=48, type="dahua", ip="172.16.8.251", manipulation_settings='{"rotate_angle": 39, "crop_x": 677, "crop_y": 357, "crop_width": 389, "crop_height": 371}'),
        Camera(id=49, type="dahua", ip="172.16.9.251", manipulation_settings='{"rotate_angle": -90, "crop_x": 826, "crop_y": 287, "crop_width": 303, "crop_height": 269}'),
        Camera(id=50, type="dahua", ip="172.16.10.251", manipulation_settings='{"rotate_angle": -78, "crop_x": 935, "crop_y": 314, "crop_width": 266, "crop_height": 293}'),
        Camera(id=51, type="dahua", ip="172.16.11.251", manipulation_settings='{"rotate_angle": 0, "crop_x": 900, "crop_y": 324, "crop_width": 348, "crop_height": 363}'),
        Camera(id=52, type="dahua", ip="172.16.12.251", manipulation_settings='{"rotate_angle": 0, "crop_x": 788, "crop_y": 355, "crop_width": 380, "crop_height": 341}'),
        Camera(id=53, type="dahua", ip="172.16.13.251", manipulation_settings='{"rotate_angle": -90, "crop_x": 873, "crop_y": 336, "crop_width": 334, "crop_height": 386}'),
        Camera(id=54, type="dahua", ip="172.16.14.251", manipulation_settings='{"rotate_angle": 0, "crop_x": 781, "crop_y": 379, "crop_width": 334, "crop_height": 249}'),
        Camera(id=55, type="dahua", ip="172.16.15.251", manipulation_settings='{"rotate_angle": 0, "crop_x": 881, "crop_y": 381, "crop_width": 316, "crop_height": 319}'),
        Camera(id=56, type="dahua", ip="172.16.16.251", manipulation_settings='{"rotate_angle": 0, "crop_x": 768, "crop_y": 475, "crop_width": 308, "crop_height": 339}'),
        Camera(id=57, type="dahua", ip="172.16.17.251", manipulation_settings='{"rotate_angle": 0, "crop_x": 701, "crop_y": 350, "crop_width": 551, "crop_height": 473}'),
        Camera(id=58, type="dahua", ip="172.16.18.251", manipulation_settings='{"rotate_angle": 0, "crop_x": 815, "crop_y": 362, "crop_width": 396, "crop_height": 358}'),
        Camera(id=59, type="dahua", ip="172.16.19.251", manipulation_settings='{"rotate_angle": 0, "crop_x": 692, "crop_y": 269, "crop_width": 403, "crop_height": 358}'),
        Camera(id=60, type="dahua", ip="172.16.20.251", manipulation_settings='{"rotate_angle": 0, "crop_x": 733, "crop_y": 414, "crop_width": 464, "crop_height": 404}'),
        Camera(id=1, type="dahua", ip="172.16.1.252", manipulation_settings='{"rotate_angle": 90}'),
        Camera(id=2, type="dahua", ip="172.16.2.252", manipulation_settings='{"rotate_angle": 90}'),
        Camera(id=3, type="dahua", ip="172.16.3.252", manipulation_settings='{"rotate_angle": -90}'),
        Camera(id=4, type="dahua", ip="172.16.4.252", manipulation_settings='{}'),
        Camera(id=5, type="hikvision", ip="172.16.5.252", manipulation_settings='{"rotate_angle": -90}'),
        Camera(id=6, type="hikvision", ip="172.16.6.252", manipulation_settings='{"rotate_angle": 90}'),
        Camera(id=7, type="dahua", ip="172.16.7.252", manipulation_settings='{"rotate_angle": 90}'),
        Camera(id=8, type="dahua", ip="172.16.8.252", manipulation_settings='{"rotate_angle": 90, "crop_x": 27, "crop_y": 0, "crop_width": 601, "crop_height": 698}'),
        Camera(id=9, type="dahua", ip="172.16.9.252", manipulation_settings='{"rotate_angle": 90}'),
        Camera(id=10, type="dahua", ip="172.16.10.252", manipulation_settings='{"rotate_angle": 90}'),
        Camera(id=11, type="dahua", ip="172.16.11.252", manipulation_settings='{"rotate_angle": 90}'),
        Camera(id=12, type="dahua", ip="172.16.12.252", manipulation_settings='{"rotate_angle": 90}'),
        Camera(id=13, type="dahua", ip="172.16.13.252", manipulation_settings='{"rotate_angle": 90}'),
        Camera(id=14, type="dahua", ip="172.16.14.252", manipulation_settings='{"rotate_angle": 90}'),
        Camera(id=15, type="hikvision", ip="172.16.15.252", manipulation_settings='{"rotate_angle": -90}'),
        Camera(id=16, type="hikvision", ip="172.16.16.252", manipulation_settings='{"rotate_angle": -90}'),
        Camera(id=17, type="hikvision", ip="172.16.17.252", manipulation_settings='{"rotate_angle": -90}'),
        Camera(id=18, type="hikvision", ip="172.16.18.252", manipulation_settings='{"rotate_angle": -90}'),
        Camera(id=19, type="hikvision", ip="172.16.19.252", manipulation_settings='{"rotate_angle": -90}'),
        Camera(id=20, type="hikvision", ip="172.16.20.252", manipulation_settings='{"rotate_angle": -90}'),
        Camera(id=21, type="hikvision", ip="172.16.1.253", manipulation_settings='{"rotate_angle": 90}'),
        Camera(id=22, type="hikvision", ip="172.16.2.253", manipulation_settings='{"rotate_angle": 90}'),
        Camera(id=23, type="hikvision", ip="172.16.3.253", manipulation_settings='{"rotate_angle": 90}'),
        Camera(id=24, type="dahua", ip="172.16.4.253", manipulation_settings='{}'),
        Camera(id=25, type="hikvision", ip="172.16.5.253", manipulation_settings='{"rotate_angle": -90}'),
        Camera(id=26, type="hikvision", ip="172.16.6.253", manipulation_settings='{"rotate_angle": 90}'),
        Camera(id=27, type="hikvision", ip="172.16.7.253", manipulation_settings='{"rotate_angle": -90}'),
        Camera(id=28, type="dahua", ip="172.16.8.253", manipulation_settings='{"rotate_angle": 90, "crop_x": 54, "crop_y": 0, "crop_width": 624, "crop_height": 668}'),
        Camera(id=29, type="dahua", ip="172.16.9.253", manipulation_settings='{"rotate_angle": 90}'),
        Camera(id=30, type="dahua", ip="172.16.10.253", manipulation_settings='{"rotate_angle": 90}'),
        Camera(id=31, type="dahua", ip="172.16.11.253", manipulation_settings='{"rotate_angle": 90}'),
        Camera(id=32, type="dahua", ip="172.16.12.253", manipulation_settings='{"rotate_angle": 90}'),
        Camera(id=33, type="dahua", ip="172.16.13.253", manipulation_settings='{"rotate_angle": 90}'),
        Camera(id=34, type="dahua", ip="172.16.14.253", manipulation_settings='{"rotate_angle": 90, "crop_x": 4, "crop_y": 0, "crop_width": 565, "crop_height": 697}'),
        Camera(id=35, type="hikvision", ip="172.16.15.253", manipulation_settings='{"rotate_angle": -90, "crop_x": 9, "crop_y": 0, "crop_width": 946, "crop_height": 944}'),
        Camera(id=36, type="hikvision", ip="172.16.16.253", manipulation_settings='{"rotate_angle": -90}'),
        Camera(id=37, type="hikvision", ip="172.16.17.253", manipulation_settings='{"rotate_angle": -90}'),
        Camera(id=38, type="hikvision", ip="172.16.18.253", manipulation_settings='{"rotate_angle": -90}'),
        Camera(id=39, type="hikvision", ip="172.16.19.253", manipulation_settings='{"rotate_angle": -90}'),
        Camera(id=40, type="hikvision", ip="172.16.20.253", manipulation_settings='{"rotate_angle": -90}'),
    ]

    sku_classes = [
        Sku(index="0", name="Unknown"),
        Sku(index="FOODINI", name="FOODINI"),
        Sku(index="DELICADE", name="DELICADE"),
        Sku(index="MUS GOOD MOOD", name="MUS GOOD MOOD"),
        Sku(index="OWOCE KAWALKI", name="OWOCE KAWALKI"),
        Sku(index="WYCISK", name="WYCISK"),
        Sku(index="OWSIANKA", name="OWSIANKA"),
        Sku(index="KANAPKA TROJKAT", name="KANAPKA TROJKAT"),
        Sku(index="KAZJERKA", name="KAZJERKA"),
        Sku(index="BAGIETKA", name="BAGIETKA"),
        Sku(index="SALATKA LUNCHBOX", name="SALATKA LUNCHBOX"),
        Sku(index="SALATKA POKEBOWL", name="SALATKA POKEBOWL"),
        Sku(index="PANINI", name="PANINI"),
        Sku(index="PIZZINA", name="PIZZINA"),
        Sku(index="TOST", name="TOST"),
        Sku(index="SALATKA SHAKER", name="SALATKA SHAKER"),
        Sku(index="ONIGIRI", name="ONIGIRI"),
        Sku(index="SUSHI", name="SUSHI"),
        Sku(index="OLIWKI", name="OLIWKI"),
        Sku(index="SALATKA Z HUMMUSEM", name="SALATKA Z HUMMUSEM"),
        Sku(index="SALATKA AL DENTE", name="SALATKA AL DENTE"),
        Sku(index="GRZESKOWIAK", name="GRZESKOWIAK"),
        Sku(index="MIESO W GALARECIE", name="MIESO W GALARECIE"),
        Sku(index="SALATKA DEGA", name="SALATKA DEGA"),
        Sku(index="SOTI", name="SOTI"),
        Sku(index="BRACIA SADOWNICY", name="BRACIA SADOWNICY"),
        Sku(index="ZUPA", name="ZUPA"),
        Sku(index="PIEROGI W KUBKU", name="PIEROGI W KUBKU"),
        Sku(index="SZAMAMM BIALE TACKI", name="SZAMAMM BIALE TACKI"),
        Sku(index="KURCZAK AZJATYCKI", name="KURCZAK AZJATYCKI"),
        Sku(index="SPAGHETTI", name="SPAGHETTI"),
        Sku(index="SZAMAMM OBIADOWE", name="SZAMAMM OBIADOWE"),
        Sku(index="TORTILLA KONSPOL", name="TORTILLA KONSPOL"),
        Sku(index="ZAPIEKANKA VIRTU", name="ZAPIEKANKA VIRTU"),
        Sku(index="JEDRUS", name="JEDRUS"),
        Sku(index="PANIEROWANE", name="PANIEROWANE"),
        Sku(index="DANIE OBIADOWE", name="DANIE OBIADOWE"),
        Sku(index="PIZZA", name="PIZZA"),
        Sku(index="SPORTFOOD", name="SPORTFOOD"),
    ]

    def add_obj(session, obj, key):
        db_obj = session.query(obj.__class__).filter_by(**{key: getattr(obj, key)}).first()
        if db_obj is None:
            logging.info('insert {}'.format(to_string(obj)))
            session.add(obj)
        else:
            obj = db_obj
        #assert obj.id is not None
        return obj

    def add_all_obj(session, objs, key='id'):
        for i in range(len(objs)):
            objs[i] = add_obj(session, objs[i], key)

    def add_planogram(session, row):
        planogram = session.query(Planogram).filter_by(
            name=row['planogram.name'],
            version=row['planogram.version']).first()
        if planogram is None:
            planogram = Planogram(
                name=row['planogram.name'],
                version=row['planogram.version'],
                description=row['planogram.description'],
                neural_network_id=-1)
            logging.info('insert {}'.format(to_string(planogram)))
            session.add(planogram)
        #assert planogram.id is not None
        return planogram

    def add_shop_planogram_assigments(session, row, shops, segment, planogram):
        spas = []
        for shop in shops:
            spa = session.query(ShopPlanogramAssignment).filter_by(shop=shop, segment=segment, planogram=planogram).first()
            if spa is None:
                spa = ShopPlanogramAssignment(
                    shop=shop,
                    segment=segment,
                    planogram=planogram,
                    start_date_time=row['shop_planogram_assignment.start_date_time'],
                    end_date_time=row['shop_planogram_assignment.end_date_time'])
                logging.info('insert {}'.format(to_string(spa)))
                session.add(spa)
            spas.append(spa)
        return spas

    def add_sku(session, row):
        sku = session.query(Sku).filter_by(index=row['planogram_element.sku.index']).first()
        if sku is None:
            sku = Sku(index=row['planogram_element.sku.index'], name=row['planogram_element.sku.name'])
            logging.info('insert {}'.format(to_string(sku)))
            session.add(sku)
        #assert sku.id is not None
        return sku

    def add_planogram_element(session, row, planogram, sku):
        pe = session.query(PlanogramElement).filter_by(
            planogram=planogram,
            shelf=row['planogram_element.shelf'],
            position=row['planogram_element.position']).first()
        if pe is None:
            pe = PlanogramElement(
                planogram=planogram,
                sku=sku,
                shelf=row['planogram_element.shelf'],
                position=row['planogram_element.position'],
                faces_count=row['planogram_element.faces_count'],
                stack_count=row['planogram_element.stack_count'])
            logging.info('insert {}'.format(to_string(pe)))
            session.add(pe)
        return pe


    logging.info('assert static data present')
    add_all_obj(session, shops)
    add_all_obj(session, segments)
    add_all_obj(session, cameras)
    add_all_obj(session, sku_classes, key='index')


    session.commit()

    #assert len(session.query(Shop).all()) == len(shops)
    assert len(session.query(Segment).all()) == len(segments)
    assert len(session.query(Camera).all()) == len(cameras)

    if path_csv is None:
        logging.info('no input file: only static data imported')
        return

    planogram_ids = []
    logging.info('read planogram csv: {}'.format(path_csv))
    df = pd.read_csv(path_csv, skiprows=2, dtype=dict(planogram_csv_dtype), sep=';')

    # duplicated are handled gracefully but we can check anyways
    ndup = check_duplicates(df)

    for (i, row) in df.iterrows():
        logging.info("row {}".format(i))

        shop_codes = [field.strip() for field in row['shop_planogram_assignment.shop.codes'].split(',')]
        shops = session.query(Shop).filter(Shop.code.in_(shop_codes)).all()
        if len(shops) != len(shop_codes):
            e = Exception("at least one shop not found: {}".format(' '.join(shop_codes)))
            logging.error(e)
            raise e
        del shop_codes

        segment_id = row['shop_planogram_assignment.segment.id']
        segment = session.query(Segment).filter_by(id=segment_id).first()
        if segment is None:
            e = Exception("no segment with id: {}".format(segment_id))
            logging.error(e)
            raise e
        del segment_id

        planogram = add_planogram(session, row)
        sku = add_sku(session, row)
        spas = add_shop_planogram_assigments(session, row, shops, segment, planogram)
        pe = add_planogram_element(session, row, planogram, sku)

        session.commit()

        planogram_ids.append(planogram.id)
        logging.info('planogram.id {}'.format(planogram.id))

    if ndup:
        logging.warning('duplicates_found {}'.format(ndup))


    session.commit()
    return list(set(planogram_ids))

    #session.rollback()


if __name__ == '__main__':
    configure_logging(None)

    if sys.argv[1] == 'test':
        connect_db("postgres://planogram_test:planogram_test@127.0.0.1:5432/planogram_test")
    elif sys.argv[1] == 'prod':
        connect_db("postgres://planogram_import:planogram_import@127.0.0.1:5432/planogram")
    else:
        print('usage: python3 main.py <test|prod> <planogram.csv>')
        sys.exit(1)

    try:
        if len(sys.argv) < 3:
            # import only static data
            import_planogram_csv(None)
        else:
            import_planogram_csv(sys.argv[2])
    except:
        Session().rollback()
        raise

