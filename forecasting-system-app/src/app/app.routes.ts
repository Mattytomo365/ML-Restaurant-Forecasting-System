import { Routes } from '@angular/router';
import { LoginComponent } from './authentication/login.component';
import { ForecastComponent } from './forecast/forecast.component';
import { authGuard } from './authentication/auth.guard-guard';

export const routes: Routes = [
    {path: 'login', component: LoginComponent},

    {
        path: 'forecast', 
        component: ForecastComponent,
        canActivate: [authGuard]
    },

    {path: '', redirectTo: 'login', pathMatch: 'full'},
    {path: '**', redirectTo: 'login'}
];
