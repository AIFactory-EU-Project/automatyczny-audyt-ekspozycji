import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ShopsComponent } from '@app/feature/shops/containers/shops/shops.component';
import { ReportsListComponent } from '@app/feature/shops/components/reports-list/reports-list.component';
import { ReportResultsComponent } from '@app/feature/shops/components/report-results/report-results.component';
import { ReportComponent } from '@app/feature/shops/components/report/report.component';
import { ReportTypeComponent } from '@app/feature/shops/components/report-type/report-type.component';

const routes: Routes = [
  {
    path: '',
    children: [
      {
        path: '',
        component: ShopsComponent,
      },
      {
        path: ':shopId',
        component: ReportComponent,
        data: {
          breadcrumb: {
            skip: true
          }
        },
        children: [
          {
            path: ':type',
            component: ReportTypeComponent,
            data: {
              breadcrumb: {
                alias: 'shopName',
              },
            },
            children: [
              {
                path: '',
                component: ReportsListComponent,
              },
              {
                path: 'result/:reportId',
                component: ReportResultsComponent,
                data: {
                  breadcrumb: {
                    alias: 'reportName'
                  }
                }
              }
            ]
          }
        ]
      },
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ShopsRoutingModule { }
