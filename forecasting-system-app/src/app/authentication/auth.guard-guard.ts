import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from './auth.service';
import { inject } from '@angular/core';
import { map } from 'rxjs/operators';

// Functional guard of type CanActivateFn, alternative to class-based guards with CanActivate() method
export const authGuard: CanActivateFn = (route, state) => { // Protects navigation to the forecast component based on authentication status
  const auth = inject(AuthService);
  const router = inject(Router);

  return auth.user$.pipe( // Pipe methods allow for transformation of observables through chained operators
    map(user =>{ // Transforms the emitted user into true or false
      if (user){
        return true;
      }
      else{
        router.navigate(['']);
        return false;
      }
    })
  )
};
