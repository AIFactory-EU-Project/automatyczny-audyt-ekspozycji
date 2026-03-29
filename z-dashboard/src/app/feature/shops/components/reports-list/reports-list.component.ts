import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { ErrorMessage, ParamsOrder, ShopsService } from '@app/feature/shops/shops.service';
import { Report, ReportType } from '@app/feature/shops/types/reports';
import { ToastService } from '@shared/services/toast.service';
import { OrderDirection } from '@shared/types/common-type';
import { sortOrder } from '@shared/helpers/sort';
import { ShopList } from '@app/feature/shops/types/shops';
import { map, tap } from 'rxjs/operators';

@Component({
  selector: 'aif-reports-list',
  templateUrl: './reports-list.component.html',
  styleUrls: ['./reports-list.component.scss']
})
export class ReportsListComponent implements OnInit {
  public title: string;
  public reports: Report[];
  public error: string;
  public isOrder: boolean = false;
  public timezone;

  constructor(
    private route: ActivatedRoute,
    private shopsService: ShopsService,
    private toastService: ToastService
  ) {}

  public ngOnInit(): void {
    this.setTitle();
    this.getReportList();
    this.timezone = new Date().getTimezoneOffset() * -1;
  }

  public sort(column: string): void {
    const { type }: Params = this.route.snapshot.params;
    const { shopId }: Params = this.route.parent.parent.snapshot.params;
    this.isOrder = !this.isOrder;
    const order: OrderDirection = sortOrder(this.isOrder);

    const paramsOrder: ParamsOrder = { reportType: type, shopId, column, order };

    this.shopsService.orderReportList(paramsOrder)
      .subscribe(
        (reports: Report[]) => this.reports = reports,
        (error: ErrorMessage) => this.toastService.danger(error.message)
      );
  }

  private setTitle(): void {
    const { type }: Params = this.route.snapshot.params;
    const reportTypeKey: string = type.toUpperCase();

    if (Object.keys(ReportType).includes(reportTypeKey)) {
      this.title = ReportType[reportTypeKey];

      return;
    }
  }

  private getReportList(): void {
    const { type }: Params = this.route.snapshot.params;
    const { shopId }: Params = this.route.parent.parent.snapshot.params;
    const reportType: string = type.toUpperCase();

    this.shopsService.getReportList(shopId, reportType)
      .pipe(
        map(data => data.map(item => ({ ...item, segmentTypeName: item.segmentTypeName.toLowerCase() }))),
        map(data => data.map(item => {
          const reportDate: Date = new Date(item.date);
          reportDate.setMinutes(reportDate.getMinutes() + this.timezone);
          return {
            ...item,
            date: reportDate
          }
        }))
      )
      .subscribe(
        (reports: Report[]) => this.reports = reports,
        (error: ErrorMessage) => this.displayErrorMessage(error)
      );
  }

  private displayErrorMessage(error: ErrorMessage): void {
    this.error = error.message;
    this.toastService.danger(error.errorInfo);
  }
}
