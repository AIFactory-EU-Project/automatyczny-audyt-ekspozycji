import { ElementRef } from '@angular/core';

export interface BoxesCanvas {
  rect: number[];
}

export interface ProductCanvas {
  imageBox: ElementRef<HTMLCanvasElement>;
  cords: {
    x: number;
    y: number;
    w: number;
    h: number;
  }
}

export type colorHex =  (color: string, from: number, to: number) => number;
