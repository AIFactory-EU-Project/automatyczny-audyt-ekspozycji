import { Component, Input } from '@angular/core';

@Component({
  selector: 'aif-alert-error',
  templateUrl: './alert-error.component.html',
  styleUrls: ['./alert-error.component.scss']
})
export class AlertErrorComponent {
  @Input() public error: string;
}
