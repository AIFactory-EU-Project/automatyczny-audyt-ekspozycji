import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Observable } from 'rxjs';
import { ReportResult } from '@app/feature/shops/types/reports';
import { Order, OrderDirection } from '@shared/types/common-type';
import { sortOrder } from '@shared/helpers/sort';

@Component({
  selector: 'aif-audit-result-list',
  templateUrl: './audit-result-list.component.html',
  styleUrls: ['./audit-result-list.component.scss']
})
export class AuditResultListComponent implements OnInit {
  @Input() public reports: ReportResult[];
  @Output() public sortedColumn: EventEmitter<Order> = new EventEmitter();
  public isOrder: boolean = false;
  public reportsList: ReportResult[];

  ngOnInit(): void {
    this.reportsList = this.reports.filter(item => item.index !== '0' && item.skuName !== 'Unknown');
  }

  public sort(column: string): void {
    this.isOrder = !this.isOrder;
    const order: OrderDirection = sortOrder(this.isOrder);
    this.sortedColumn.emit({ column, order });
  }
}
