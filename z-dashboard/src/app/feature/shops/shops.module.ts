import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ShopsRoutingModule } from '@app/feature/shops/shops-routing.module';
import { SharedModule } from '@shared/shared.module';
import { ShopsComponent } from './containers/shops/shops.component';
import { ShopsListComponent } from './components/shops-list/shops-list.component';
import { ReportsListComponent } from './components/reports-list/reports-list.component';
import { ReportResultsComponent } from './components/report-results/report-results.component';
import { ShopDataComponent } from './components/report-results/shop-data/shop-data.component';
import { AuditDataComponent } from './components/report-results/audit-data/audit-data.component';
import { ReportComponent } from './components/report/report.component';
import { ReportTypeComponent } from './components/report-type/report-type.component';
import { AuditResultListComponent } from './components/report-results/audit-result-list/audit-result-list.component';

@NgModule({
  declarations: [
    ShopsComponent,
    ShopsListComponent,
    ReportsListComponent,
    ReportResultsComponent,
    ShopDataComponent,
    AuditDataComponent,
    ReportComponent,
    ReportTypeComponent,
    AuditResultListComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    ShopsRoutingModule
  ]
})
export class ShopsModule { }
