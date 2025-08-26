import { Routes } from '@angular/router';
import { LoginComponent } from './authentication/login.component';
import { ForecastComponent } from './forecast/forecast.component';

export const routes: Routes = [
    {path: 'login', component: LoginComponent},
    {path: 'forecast', component: ForecastComponent},
    {path: '', redirectTo: 'login', pathMatch: 'full'},
    {path: '**', redirectTo: 'login'}
];
