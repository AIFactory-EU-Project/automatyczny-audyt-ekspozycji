import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AifLayoutComponent } from '@app/feature/aif-layout/aif-layout.component';

const routes: Routes = [
  {
    path: '',
    component: AifLayoutComponent,
    children: [
      {
        path: '',
        loadChildren: () => import('../shops/shops.module').then(m => m.ShopsModule),
        data: {
          breadcrumb: 'Sklepy'
        }
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AifRoutingModule { }
