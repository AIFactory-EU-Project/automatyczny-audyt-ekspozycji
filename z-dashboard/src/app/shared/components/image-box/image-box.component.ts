import { AfterViewInit, Component, ElementRef, Input, OnDestroy, ViewChild } from '@angular/core';
import { fromEvent, Subject } from 'rxjs';
import { BoxesCanvas} from '@app/feature/shops/types/canvas-image';
import { ImageBox, ReportResult } from '@app/feature/shops/types/reports';
import { ImageBoxService } from '@shared/components/image-box/image-box.service';
import { takeUntil, tap } from 'rxjs/operators';

@Component({
  selector: 'aif-image-box',
  templateUrl: './image-box.component.html',
  styleUrls: ['./image-box.component.scss'],
  providers: [ImageBoxService]
})
export class ImageBoxComponent implements OnDestroy, AfterViewInit {
  @Input() public image: ImageBox;
  @Input() public products: ReportResult[];
  @Input() public drawCanvas: boolean;

  public imageWidth: number;
  public imageHeight: number;

  @ViewChild('imageBox', { static: false }) public imageBox: ElementRef<HTMLCanvasElement>;

  private destroy: Subject<boolean> = new Subject<boolean>();

  private boxes: BoxesCanvas[];

  constructor(private imageBoxService: ImageBoxService) {}

  public ngOnInit(): void {
    // this.image = {
    //   ...this.image,
    // url: this.image.url.replace('https://', 'http://'),
    // };
  }

  public ngAfterViewInit(): void {
    this.drawImageWithSelectedProducts();
  }

  public ngOnDestroy(): void {
    this.destroy.next();
    this.destroy.complete();
  }

  private drawImageWithSelectedProducts(): void {
    const scale = 1;

    if (!this.products) {
      this.boxes = [];
    } else {
      this.boxes = this.products.filter(product => product['box']).map(product => product['box']).map(cords => {
        const {topLeftX, topLeftY, width, height} = cords;
        return {
          rect: [
            topLeftX / scale,
            topLeftY / scale,
            width / scale,
            height / scale
          ]
        };
      });
    }

    if (!this.drawCanvas) {
      return;
    }

    const image: HTMLImageElement = this.imageBoxService.createCanvasImage(this.image.url, this.imageBox);

    fromEvent(image, 'load')
      .pipe(
        tap(() => {
          this.imageWidth = Math.round(image.width / scale);
          this.imageHeight = Math.round(image.height / scale);
          this.imageBox.nativeElement.width = this.imageWidth;
          this.imageBox.nativeElement.height = this.imageHeight;
        }),
        takeUntil(this.destroy)
      )
      .subscribe(() => {
        this.imageBoxService.ctxBackground.drawImage(image, 0, 0, this.imageWidth, this.imageHeight);
        this.imageBoxService.drawBoxes(this.boxes, this.imageBox);
      });
  }
}
