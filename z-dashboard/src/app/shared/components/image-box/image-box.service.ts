import { ElementRef, Injectable } from '@angular/core';
import { BoxesCanvas, colorHex, ProductCanvas } from '@app/feature/shops/types/canvas-image';

@Injectable()
export class ImageBoxService {

  public ctxBackground: CanvasRenderingContext2D;
  private ctx: CanvasRenderingContext2D;

  /**
   * setting image from backend as background Canvas
   */
  public createCanvasImage(url: string, imageBox: ElementRef<HTMLCanvasElement>): HTMLImageElement {
    const image: HTMLImageElement = new Image();
    image.src = url;
    this.ctxBackground = imageBox.nativeElement.getContext('2d');

    return image;
  }

  /**
   * select products over background image (data from Backend - colors and coordinates)
   */
  public drawBoxes(boxes: BoxesCanvas[], imageBox: ElementRef<HTMLCanvasElement>): void {
    boxes.forEach((item) => {
      const { rect: [x, y, w, h]}: BoxesCanvas = item;
      this.drawProduct({
        imageBox,
        cords: { x, y, w, h }
      });
    });
  }

  /**
   * change color from Hex to RGB ex. #FF0000 -> 255,0,0
   */
  private hexToRgb(hexColor: string): string {
    const parseColorToHex: colorHex = (color: string, from: number, to: number): number => parseInt((hexColor).substring(from, to),16);

    const red: number = parseColorToHex(hexColor, 0, 2);
    const green: number = parseColorToHex(hexColor, 2, 4);
    const blue: number = parseColorToHex(hexColor, 4, 6);

    return `${red}, ${green}, ${blue}`;
  }

  /**
   * drawing single selected product on Canvas image
   */
  private drawProduct(obj: ProductCanvas): void {
    const { imageBox, cords: { x, y, w, h } }: ProductCanvas = obj;
    const strokeLineWidth: number = 2;
    this.ctx = imageBox.nativeElement.getContext('2d');
    this.ctx.beginPath();
    this.ctx.rect(x, y, w, h);
    this.ctx.fillStyle = `rgba(0, 125, 198, .5)`;
    this.ctx.fill();
    this.ctx.strokeStyle = `rgba(0, 125, 198, .9)`;
    this.ctx.lineWidth = strokeLineWidth;
    this.ctx.stroke();
  }
}
