import { Component, inject } from '@angular/core';
import { AuthService } from './auth.service';
import { Router } from '@angular/router';
import { FormBuilder, Validators } from '@angular/forms';

@Component({
  selector: 'app-login.component',
  imports: [],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  private auth = inject(AuthService);
  private router = inject(Router);
  private fb = inject(FormBuilder);

  error: string | null = null;

  form = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(6)]],
  });

  onLogin(){
    const {email, password} = this.form.value;
    this.auth.login(email!, password!)
    .then(() => this.router.navigate(['/forecast'])) // .then returns a new Promise object, allowing for method chaining // user is navigated to forecasting page upon successful login
    .catch(err => {
      this.error = err.code;
    })
  }


}
