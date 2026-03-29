import { Component, Input } from '@angular/core';

@Component({
  selector: 'aif-value-widget',
  templateUrl: './value-widget.component.html',
  styleUrls: ['./value-widget.component.scss']
})
export class ValueWidgetComponent {
  @Input() public title: string;
  @Input() public value: number;

}
