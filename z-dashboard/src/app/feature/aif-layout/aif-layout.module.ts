import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@shared/shared.module';
import { AifRoutingModule } from '@app/feature/aif-layout/aif-routing.module';
import { AifLayoutComponent } from './aif-layout.component';
import { CoreModule } from '@core/core.module';
import { BreadcrumbModule } from 'xng-breadcrumb';

@NgModule({
  declarations: [AifLayoutComponent],
  imports: [
    CommonModule,
    CoreModule,
    SharedModule,
    BreadcrumbModule,
    AifRoutingModule
  ]
})
export class AifLayoutModule { }
