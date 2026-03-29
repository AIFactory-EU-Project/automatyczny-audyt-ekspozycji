import { NgModule } from '@angular/core';
import {
  NbAlertModule,
  NbCardModule,
  NbIconModule,
  NbLayoutModule,
  NbSidebarModule,
  NbThemeModule, NbToastrModule
} from '@nebular/theme';
import { NbEvaIconsModule } from '@nebular/eva-icons';

@NgModule({
  declarations: [],
  imports: [
    NbThemeModule.forRoot({ name: 'default' }),
    NbSidebarModule.forRoot(),
    NbToastrModule.forRoot(),
    NbLayoutModule,
    NbEvaIconsModule,
    NbIconModule,
    NbCardModule,
    NbAlertModule,
  ],
  exports: [
    NbThemeModule,
    NbSidebarModule,
    NbLayoutModule,
    NbIconModule,
    NbCardModule,
    NbAlertModule,
    NbToastrModule
  ]
})
export class NebularModule { }
