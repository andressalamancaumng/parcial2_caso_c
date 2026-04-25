import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { AuthService } from '../services/auth.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private auth: AuthService) {}
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // ← VULNERABLE: sin prefijo Bearer
    const token = this.auth.getToken();
    const authReq = token ? req.clone({ setHeaders: { Authorization: token } }) : req;
    return next.handle(authReq).pipe(
      catchError((err: HttpErrorResponse) => {
        // ← VULNERABLE: expone detalle del error
        alert(`Error del servidor: ${JSON.stringify(err.error)}`);
        return throwError(() => err);
      })
    );
  }
}
