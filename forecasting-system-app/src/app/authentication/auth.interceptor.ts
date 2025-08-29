import { HttpEvent, HttpHandlerFn, HttpInterceptorFn, HttpRequest } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from './auth.service';
import { Observable, switchMap, take } from 'rxjs';

// Functional interceptor recieving the outgoing request (req) and a function to pass the request onward (next), returns an observable
export const authInterceptor: HttpInterceptorFn = (req: HttpRequest<any>, next: HttpHandlerFn): Observable<HttpEvent<any>> => { 
  const auth = inject(AuthService);

  // Returns the transformed observable to the HttpClient pipeline
  return auth.token$.pipe( 
    take(1), // Limits how many times the outer observable (token$) can emit
    switchMap(token => // Switches to a new observable which handles the HTTP request (Observable<HttpEvent>)
      next(token ? req.clone({setHeaders: {Authorization: `Bearer ${token}`}}) : req) // Requests are immutable, clone is required
      // next() continues the request after intercepting it
    )
  );
};
