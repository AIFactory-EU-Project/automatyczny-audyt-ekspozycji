import { NgModule } from '@angular/core';
import { CommonModule, PercentPipe } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NebularModule } from '@shared/modules/nebular.module';
import { InfoColorComponent } from './components/info-color/info-color.component';
import { HeadingTitleComponent } from './components/heading-title/heading-title.component';
import { CardComponent } from './components/card/card.component';
import { ValueWidgetComponent } from './components/value-widget/value-widget.component';
import { ImageBoxComponent } from './components/image-box/image-box.component';
import { AlertErrorComponent } from './components/alert-error/alert-error.component';

const SHARED_COMPONENTS: unknown[] = [
  InfoColorComponent,
  HeadingTitleComponent,
  CardComponent,
  ValueWidgetComponent,
  ImageBoxComponent,
  AlertErrorComponent
];

const SHARED_MODULES: unknown[] = [
  CommonModule,
  FormsModule,
  ReactiveFormsModule,
  NebularModule,
];

@NgModule({
  declarations: [
    SHARED_COMPONENTS,
  ],
  imports: [
    SHARED_MODULES
  ],
  exports: [
    SHARED_MODULES,
    SHARED_COMPONENTS
  ],
  providers: [
    PercentPipe
  ]
})
export class SharedModule { }
