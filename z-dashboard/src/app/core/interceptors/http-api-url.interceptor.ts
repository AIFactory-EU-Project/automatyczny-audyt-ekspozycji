import { Injectable } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@environment';

@Injectable()
export class HttpApiUrlInterceptor implements HttpInterceptor {

  public intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const clone: HttpRequest<unknown> = request.clone({
      url: (`${environment.apiURL}/${request.url}`).replace('http://', 'https://')
    });

    return next.handle(clone);
  }
}
