import { Component, Input, OnInit } from '@angular/core';
import { PercentPipe } from '@angular/common';

@Component({
  selector: 'aif-info-color',
  templateUrl: './info-color.component.html',
  styleUrls: ['./info-color.component.scss']
})
export class InfoColorComponent implements OnInit {
  @Input() public percent: number;
  @Input() public color: string;
  @Input() public info: string;
  @Input() public isHiddenValue: boolean = false;
  @Input() public status: number;
  public infoColor: string;

  constructor(private percentPipe: PercentPipe) {}

  public ngOnInit(): void {
    this.infoColor = this.setColor(this.percent);
  }

  public get value(): string {
    return this.info ? this.info : `${this.percent}%`;
  }

  private setColor(percent: number): string {
    if (this.color) {
      return this.color;
    }

    const HighColor: number = 40;
    const MediumColor: number = 20;

    return percent > HighColor ? 'high' : percent > MediumColor ? 'medium' : 'low';
  }
}
