import { Component, Input } from '@angular/core';

@Component({
  selector: 'aif-heading-title',
  templateUrl: './heading-title.component.html',
  styleUrls: ['./heading-title.component.scss']
})
export class HeadingTitleComponent {
  @Input() public title: string;
}
