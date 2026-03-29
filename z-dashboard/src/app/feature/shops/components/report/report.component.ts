import { Component, OnInit } from '@angular/core';
import { BreadcrumbService } from 'xng-breadcrumb';
import { ActivatedRoute, Params } from '@angular/router';
import { ShopsService } from '@app/feature/shops/shops.service';

@Component({
  selector: 'aif-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.scss']
})
export class ReportComponent implements OnInit {

  constructor(
    private route: ActivatedRoute,
    private shopsService: ShopsService,
    private breadcrumbService: BreadcrumbService
  ) { }

  public ngOnInit(): void {
    this.setBreadcrumb();
  }

  private setBreadcrumb(): void {
    const { shopId }: Params = this.route.snapshot.params;
    this.shopsService.getShop(shopId).subscribe(({ name, city, street}) => {
      const cityBreadcrumb: string = city ? `,${city}` : '';
      const streetBreadcrumb: string = street ? `,${street}` : '';

      const shopName: string = `${name} ${cityBreadcrumb} ${streetBreadcrumb}`;
      this.breadcrumbService.set('@shopName', shopName);
    });
  }
}
