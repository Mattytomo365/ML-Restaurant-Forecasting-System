import { ApplicationConfig, provideBrowserGlobalErrorListeners, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';

import { firebaseConfig } from './firebase.config';
import { provideFirebaseApp } from '@angular/fire/app';
import { initializeApp } from 'firebase/app';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),

    provideFirebaseApp(() => initializeApp(firebaseConfig)) // Calls Firebase Web SDK to initialise the Firebase App,
    // wrapped within an Angular provider to register the Firebase App instance in Angular's DI container
  ]
};

