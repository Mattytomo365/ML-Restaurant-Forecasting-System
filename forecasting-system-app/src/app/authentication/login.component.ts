import { Component, inject } from '@angular/core';
import { AuthService } from './auth.service';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
// Angular Material modules
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-login.component',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  private auth = inject(AuthService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  private fb = inject(FormBuilder);

  errorMessage: string | null = null;
  loading = false; // Loading flag prevents double clicks on submit button
  hide = true; 
  private returnUrl = '';

  form = this.fb.group({ // Creates a form group with two form controls
    email: ['', [Validators.required, Validators.email]], // Each form control hold value, status, state, and errors from the validators
    password: ['', [Validators.required, Validators.minLength(6)]],
  });

  onLogin(): void {
    this.errorMessage = null;
    this.loading = true;

    const {email, password} = this.form.value;
    // Grabs the returnUrl (where they wanted to navigate to but couldn't) from the guard, or defaults to /forecast
    this.returnUrl = this.route.snapshot.queryParamMap.get('returnUrl') || '/forecast'; 

    this.auth.login(email!, password!)
      .then(() => this.router.navigateByUrl(this.returnUrl)) // .then returns a new Promise object, allowing for method chaining // user is navigated to forecasting page upon successful login
      .catch((err: any) => {
        this.errorMessage = 'Invalid email or password';
      })
      .finally(() => {
        this.loading = false // Ensures the variable resets even if an error occurs
      })
  }


}
