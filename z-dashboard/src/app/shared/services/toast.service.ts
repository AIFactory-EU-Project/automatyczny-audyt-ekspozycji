import { Injectable } from '@angular/core';
import { NbGlobalLogicalPosition, NbToastrService } from '@nebular/theme';

@Injectable({
  providedIn: 'root'
})
export class ToastService {

  constructor(private toastrService: NbToastrService) { }

  public danger(info: string): void {
    this.toastrService.danger(info, 'Error', {
      position: NbGlobalLogicalPosition.BOTTOM_END,
    });
  }
}
