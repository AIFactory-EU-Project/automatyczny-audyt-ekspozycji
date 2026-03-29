import { Component, Input } from '@angular/core';
import { ShopDetails } from '@app/feature/shops/types/shops';

@Component({
  selector: 'aif-shop-data',
  templateUrl: './shop-data.component.html',
  styleUrls: ['./shop-data.component.scss']
})
export class ShopDataComponent {
  @Input() public title: string;
  @Input() public shop: ShopDetails;
}
