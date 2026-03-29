import { InMemoryDbService } from 'angular-in-memory-web-api';
import { Injectable } from '@angular/core';
import { ShopList } from '@app/feature/shops/types/shops';
import { Report, ReportDetails, ReportResult } from '@app/feature/shops/types/reports';

@Injectable({
  providedIn: 'root',
})
export class InMemoryDataService implements InMemoryDbService {
  public createDb(): any {
    const shops: ShopList[] = [
      {
        "id": 1,
        "name": "Żabka",
        "city": "Poznań",
        "street": "Dąbrowskiego 26",
        "zipCode": "80-283",
        "accuracy": "0.75"
      },
      {
        "id": 2,
        "name": "Żabka",
        "city": "Warszawa",
        "street": "Aleje Jerozolimskie 18",
        "zipCode": "23-122",
        "accuracy": "0.25"
      },
      {
        "id": 3,
        "name": "Żabka",
        "city": "Gdańsk",
        "street": "Grunwalldzka 142",
        "zipCode": "12-493",
        "accuracy": "0.47"
      },
      {
        "id": 4,
        "name": "Żabka",
        "city": "Wrocław",
        "street": "Malinowska 35",
        "zipCode": "50-203",
        "accuracy": "0.11"
      },
      {
        "id": 5,
        "name": "Żabka",
        "city": "Kraków",
        "street": "Wileńska 17",
        "zipCode": "90-302",
        "accuracy": "0.31"
      },
      {
        "id": 6,
        "name": "Żabka",
        "city": "Bydgoszcz",
        "street": "Zacisze 7",
        "zipCode": "76-203",
        "accuracy": "0.19"
      }
    ];

    const reports: Report[] = [
      {
        "id": 1,
        "name": "DGWA1231109191200",
        "date":  new Date(2019, 11, 21, 8, 0, 0),
        "accuracy": 0.75,
        "shopId": 1,
        "segmentTypeName": "dg"
      },
      {
        "id": 2,
        "name": "DGWA4711109191200",
        "date":  new Date(2019, 10, 18, 20, 20, 0),
        "accuracy": 0.32,
        "shopId": 2,
        "segmentTypeName": "dg"
      },
      {
        "id": 3,
        "name": "SPWA5621109191200",
        "date":  new Date(2019, 5, 11, 8, 0, 0),
        "accuracy": 0.21,
        "shopId": 1,
        "segmentTypeName": "sp"
      },
      {
        "id": 4,
        "name": "ROWA4711109191200",
        "date":  new Date(2019, 10, 18, 10, 20, 0),
        "accuracy": 0.21,
        "shopId": 1,
        "segmentTypeName": "rollery"
      },
      {
        "id": 5,
        "name": "ROWA5621109191200",
        "date":  new Date(2019, 5, 11, 11, 20, 0),
        "accuracy": 0.67,
        "shopId": 1,
        "segmentTypeName": "rollery"
      },
      {
        "id": 6,
        "name": "ROWA5621109191200",
        "date":  new Date(2019, 10, 18, 20, 20, 0),
        "accuracy": 0.15,
        "shopId": 1,
        "segmentTypeName": "rollery"
      }
    ];

    const reportResult: ReportDetails = {
      "id": 1,
      "shop": {
        "id": 1,
        "name": "Żabka",
        "code": "WA123AAAAAAAA",
        "street": "Myśliwska 33",
        "zipCode": "80-283",
        "city": "Gdańsk"
      },
      "report": {
        "name": "DGWA1231109191200",
        "date": new Date(2019, 10, 21, 8, 30, 0),
        "accuracy": 0.92
      },
      "imageReal": {
        "name": "IMG3023920303AADA",
        "date": new Date(2019, 10, 21, 8, 30, 0),
        "url": "https://testujzzyciem.files.wordpress.com/2018/04/hot1.jpg?w=528&h=312&crop=1"
      },
      // "imagePlanogram": {
      //   "name": "IMG3023920303AADA",
      //   "date": "2019-10-21 08:30:00",
      //   "url": "https://testujzzyciem.files.wordpress.com/2018/04/hot1.jpg?w=528&h=312&crop=1"
      // }
    };

    const ReportResultList: ReportResult[] = [
      {
        shelf: 2,
        position: 13,
        index: '1205893',
        skuName: 'Sok z marchwi i banana 330 ML Delicade',
        faces_count: 2,
        result: 'ok',
        color: '#47C2B1'
      },
      {
        shelf: 1,
        position: 23,
        index: '2930132',
        skuName: 'Sałatka jarzynowa',
        faces_count: 21,
        result: 'za dużo twarzy',
        color: '#FFC76A'
      },
      {
        shelf: 2,
        position: 6,
        index: '1837293',
        skuName: 'Kanapka z grillowanym kurczakiem i pomidorami',
        faces_count: 5,
        result: 'ręczna walidacja',
        color: '#5C5C5C'
      },
      {
        shelf: 5,
        position: 10,
        index: '1294856',
        skuName: 'Sok z marchwi i banana 330 ML Delicade',
        faces_count: 3,
        result: 'brak SKU',
        color: '#FF8576'
      }
    ];

    return {
      shops,
      reports,
      'report-result': reportResult,
      'report-result-list': ReportResultList
    };
  }

}
