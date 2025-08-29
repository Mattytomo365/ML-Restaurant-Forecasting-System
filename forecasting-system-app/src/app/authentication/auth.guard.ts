import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from './auth.service';
import { inject } from '@angular/core';
import { map, take } from 'rxjs/operators';

/** Functional guard of type CanActivateFn, alternative to class-based guards with CanActivate() method */ 
export const authGuard: CanActivateFn = (route, state) => { // Protects navigation to the forecast component based on authentication status
  const auth = inject(AuthService);
  const router = inject(Router);

  return auth.user$.pipe(
    take(1),
    map(user =>
      user ? true : router.createUrlTree( // Returns either true or a UrlTree redirecting back to /login
            ['/login'], { queryParams: { returnUrl: state.url } } // Includes the page the user tried to open so user can be sent back after login (UX)
          )
    )
  )
};
