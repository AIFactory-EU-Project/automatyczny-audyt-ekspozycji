import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Observable } from 'rxjs';
import { sortOrder } from '@shared/helpers/sort';
import { Order, OrderDirection } from '@shared/types/common-type';
import { ShopList } from '@app/feature/shops/types/shops';

@Component({
  selector: 'aif-shops-list',
  templateUrl: './shops-list.component.html',
  styleUrls: ['./shops-list.component.scss']
})
export class ShopsListComponent {
  @Input() public shops: ShopList[];
  @Input() public error: string;
  @Output() public sortedList: EventEmitter<Order> = new EventEmitter();
  public isOrder: boolean = false;

  // public sort(column: string): void {
  //   this.isOrder = !this.isOrder;
  //   const order: OrderDirection = sortOrder(this.isOrder);
  //   this.sortedList.emit({ column, order });
  // }

}
