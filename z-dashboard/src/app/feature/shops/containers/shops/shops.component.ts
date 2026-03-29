import { Component, OnInit } from '@angular/core';
import { ErrorMessage, ShopsService } from '@app/feature/shops/shops.service';
import { ShopList } from '@app/feature/shops/types/shops';
import { Order } from '@shared/types/common-type';
import { HttpErrorResponse } from '@angular/common/http';
import { ToastService } from '@shared/services/toast.service';
import { map } from 'rxjs/operators';
import { sortBy } from 'lodash';

@Component({
  selector: 'aif-shops',
  templateUrl: './shops.component.html',
  styleUrls: ['./shops.component.scss']
})
export class ShopsComponent implements OnInit {
  public title: string = 'Sklepy';
  public shops: ShopList[] | HttpErrorResponse;
  public error: string;

  constructor(
    private shopsService: ShopsService,
    private toastService: ToastService
  ) { }

  public ngOnInit(): void {
    this.getShopList();
  }

  public sort({ column, order: OrderDirection }: Order): void {
    this.shopsService.orderShopList(column, OrderDirection)
      .subscribe(
        (shops: ShopList[]) => this.shops = shops,
        (error: ErrorMessage) => this.toastService.danger(error.message)
      );
  }

  private getShopList(): void {
    this.shopsService.getShopList()
      .pipe(
        map(shop => sortBy(shop, ['city', 'street'])),
      )
      .subscribe(
        (shops: ShopList[]) => this.shops = shops,
        (error: ErrorMessage) => this.displayErrorMessage(error)
      );
  }

  private displayErrorMessage(error: ErrorMessage): void {
    this.error = error.message;
    this.toastService.danger(error.errorInfo);
  }
}
