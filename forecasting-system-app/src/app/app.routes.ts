import { Routes } from '@angular/router';
import { LoginComponent } from './authentication/login.component';
import { ForecastComponent } from './forecast/forecast.component';
import { authGuard } from './authentication/auth.guard';

export const routes: Routes = [
    {path: 'login', component: LoginComponent},

    {
        path: 'forecast', // Authenticated route
        component: ForecastComponent,
        canActivate: [authGuard]
    },

    // Fallbacks
    {path: '', redirectTo: 'login', pathMatch: 'full'},
    {path: '**', redirectTo: 'login'}
];
