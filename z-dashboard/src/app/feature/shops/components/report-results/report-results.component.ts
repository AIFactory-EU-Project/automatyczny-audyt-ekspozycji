import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { map, tap } from 'rxjs/operators';
import { BreadcrumbService } from 'xng-breadcrumb';
import { ImageBox, ReportDetails, ReportResult, ReportType } from '@app/feature/shops/types/reports';
import { Order, OrderDirection } from '@shared/types/common-type';
import { ErrorMessage, ShopsService } from '@app/feature/shops/shops.service';
import { ToastService } from '@shared/services/toast.service';

@Component({
  selector: 'aif-report-results',
  templateUrl: './report-results.component.html',
  styleUrls: ['./report-results.component.scss']
})
export class ReportResultsComponent implements OnInit {
  public title: string = 'Wyniki audytu';
  public reportDetails: ReportDetails;
  public reportResults: ReportResult[];
  public error: string;
  public auditType: string;
  public imagePlanogram: ImageBox;

  constructor(
    private shopsService: ShopsService,
    private route: ActivatedRoute,
    private breadcrumbService: BreadcrumbService,
    private toastService: ToastService
  ) {}

  public ngOnInit(): void {
    this.getReportDetails();
    this.getReportResults();
    this.setBreadcrumb();

    this.route.parent.params.subscribe(data => {
      this.auditType = data.type;

      if (data.type === 'quick_snack') {
        this.imagePlanogram = {
          url: '/assets/szybkie-przekaski-planogram.png',
          name: 'planogram szybkie przekąski',
          date: new Date(2019, 11, 20, 8, 0, 0)
        }
      } else if (data.type === 'ready_meal') {
        this.imagePlanogram = {
          url: '/assets/dania-gotowe-planogram.png',
          name: 'planogram dania gotowe',
          date: new Date(2019, 11, 20, 8, 0, 0)
        }
      }
    });
  }

  public sortReportResults(sortParams: Order, data: ReportResult[] = this.reportResults): void {
    const { column, order }: Order = sortParams;
    data.sort((a, b) => {
      switch(order) {
        case 'desc':
          return a[column] < b[column] ? 1 : -1;
        case 'asc':
        default:
          return a[column] > b[column] ? 1 : -1;
      }
    });
  }

  public get totalAccuracy(): string {
    const { count, score }: { count?: number, score?: number } = this.reportDetails;

    if (count >= 0) {
      return count.toString();
    }

    // const totalResult: number = boxes.reduce((total: number, item: ReportResult) => total = total + item.accuracy, 0)/boxes.length;

    return `${score.toFixed(0)} %`;
  }

  public get accuracyInfo(): string {
    const { count }: { count?: number } = this.reportDetails;
    return count ? 'Liczba wykrytych parówek' : 'Poziom zgodności';
  }

  private setBreadcrumb(): void {
    const { type }: Params = this.route.parent.snapshot.params;
    const reportTypeKey: string = type.toUpperCase();
    this.breadcrumbService.set('@reportName', ReportType[reportTypeKey]);
  }

  private getReportDetails(): void {
    const { reportId }: Params = this.route.snapshot.params;
    const timezone = new Date().getTimezoneOffset() * -1;


    this.shopsService.getReportDetails(reportId)
      .pipe(
        map(item => {
          const reportDate: Date = new Date(item.report.date);
          reportDate.setMinutes(reportDate.getMinutes() + timezone);

          return {
            ...item,
            report: {
              ...item.report,
              date: reportDate
            }
          }
        })
      )
      .subscribe(
        ((reportDetails: ReportDetails) => {
          this.reportDetails = reportDetails;
        }),
        ((error: ErrorMessage) => this.displayErrorMessage(error))
      );
  }

  private getReportResults(): void {
    const { reportId }: Params = this.route.snapshot.params;

    // this.shopsService.getReportResultList(reportId)
    //   .pipe(
    //     tap((reportResults: ReportResult[]) => this.sortReportResults({ column: 'shelf', order: OrderDirection.DESC}, reportResults))
    //   )
    //   .subscribe((reportResults: ReportResult[]) => {
    //     this.reportResults = reportResults
    //   });
  }

  private displayErrorMessage(error: ErrorMessage): void {
    this.error = error.message;
    this.toastService.danger(error.errorInfo);
  }
}
