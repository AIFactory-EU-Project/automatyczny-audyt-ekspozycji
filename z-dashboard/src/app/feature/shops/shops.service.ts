import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { ShopList } from '@app/feature/shops/types/shops';
import { Report, ReportDetails, ReportResult } from '@app/feature/shops/types/reports';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ShopsService {

  constructor(private http: HttpClient) { }

  public getShopList(): Observable<ShopList[] | HttpErrorResponse> {
    return this.http.get<ShopList[]>('shop')
      .pipe(
        map(response => response['data']),
        catchError(this.handleError)
      );
  }

  public orderShopList(column: string, order: string = 'asc'): Observable<ShopList[]> {
    const params: HttpParams = new HttpParams()
      .set('_sort', column)
      .set('_order', order);

    return this.http.get<ShopList[]>('shop', { params })
      .pipe(
        catchError(this.handleError)
      );
  }

  public getShop(shopId: number): Observable<ShopList> {
    return this.http.get<ShopList>(`shop/${shopId}`)
      .pipe(
        map(response => response['data']),
      );
  }

  public getReportList(shopId: string, reportType: string): Observable<Report[]> {
    return this.http.get<Report[]>(`shop/${shopId}/${reportType}`)
      .pipe(
        map(response => response['data']),
        catchError(this.handleError)
      );
  }

  public orderReportList(paramsOrder: ParamsOrder): Observable<Report[]> {
    const { shopId, reportType, column, order }: ParamsOrder = paramsOrder;
    const params: HttpParams = new HttpParams()
      .set('shopId', shopId)
      .set('reportType', reportType)
      .set('_sort', column)
      .set('_order', order);

    return this.http.get<Report[]>('reports', { params })
      .pipe(
        catchError(this.handleError)
      );
  }

  public getReportDetails(reportId: number): Observable<ReportDetails> {
    return this.http.get<ReportDetails>(`audit/${reportId}`)
      .pipe(
        map(response => response['data']),
        catchError(this.handleError)
      );
  }

  public getReportResultList(reportId: number): Observable<ReportResult[]> {
    return this.http.get<ReportResult[]>(`report-result-list`);
  }

  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorInfo: string;

    errorInfo = error.error instanceof ErrorEvent
      ? `An error occurred:, ${error.error.message}`
      : `Backend returned code ${error.status}, body was: ${error.error}`;

    return throwError({
      message: 'Podczas pobrania danych coś poszło błędnie; spróbuj ponownie później.',
      errorInfo
    });
  };
}

export interface ErrorMessage {
  message: string;
  errorInfo: string;
}

export interface ParamsOrder {
  shopId: string;
  reportType: string;
  column: string;
  order: string;
}
