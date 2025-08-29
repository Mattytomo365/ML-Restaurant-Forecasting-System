import { Component } from '@angular/core';
import { MatCard, MatCardTitle } from "@angular/material/card";

@Component({
  selector: 'app-forecast.component',
  imports: [
    MatCard, 
    MatCardTitle
  ],
  templateUrl: './forecast.component.html',
  styleUrl: './forecast.component.css'
})
export class ForecastComponent {

}
