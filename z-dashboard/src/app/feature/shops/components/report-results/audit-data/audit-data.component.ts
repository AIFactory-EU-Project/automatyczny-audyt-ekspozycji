import { Component, Input } from '@angular/core';
import { ReportBase } from '@app/feature/shops/types/reports';

@Component({
  selector: 'aif-audit-data',
  templateUrl: './audit-data.component.html',
  styleUrls: ['./audit-data.component.scss']
})
export class AuditDataComponent {
  @Input() public title: string;
  @Input() public audit: Omit<ReportBase, 'id'>;
}
