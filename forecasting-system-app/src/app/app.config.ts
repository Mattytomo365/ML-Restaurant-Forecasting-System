import { ApplicationConfig, provideBrowserGlobalErrorListeners, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';

import { firebaseConfig } from './firebase.config';
import { provideFirebaseApp } from '@angular/fire/app';
import { initializeApp } from 'firebase/app';
import { getAuth, provideAuth } from '@angular/fire/auth';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { authInterceptor } from './authentication/auth.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [ // Providers are collections of tokens facilitating object creation and ensure singleton instances. They are injected into constructors, defining how dependencies are resolved, registration recipe
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),

    provideFirebaseApp(() => initializeApp(firebaseConfig)), // Calls Firebase Web SDK to initialise the Firebase App
    provideAuth(() => getAuth()), // Returns the Firebase Authentication service tied to the initialised app

    provideHttpClient(withInterceptors([authInterceptor])), // Registers HttpClient and the interceptor function its requests will flow through
  ]
};

