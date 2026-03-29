import { Component, Input } from '@angular/core';

@Component({
  selector: 'aif-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.scss']
})
export class CardComponent {
  @Input() public title: string;
  @Input() public paddingBodyLeftRight: number;
}
