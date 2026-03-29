import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { HttpApiUrlInterceptor } from '@core/interceptors/http-api-url.interceptor';

export const AifInterceptors = [
  {
    provide: HTTP_INTERCEPTORS,
    useClass: HttpApiUrlInterceptor,
    multi: true,
  }
];
