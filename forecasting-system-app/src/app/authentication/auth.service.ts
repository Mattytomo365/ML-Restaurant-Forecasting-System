import { inject, Injectable } from '@angular/core';
import { Auth, User } from '@angular/fire/auth';
import { createUserWithEmailAndPassword, getIdToken, onAuthStateChanged, onIdTokenChanged, signInWithEmailAndPassword, signOut, UserCredential } from 'firebase/auth';
import { BehaviorSubject, from, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private auth = inject(Auth); // Firebase auth service instance, injecting it into this service

  private userSubject = new BehaviorSubject<User | null>(null); // Behaviour subjects hold the latest value and emits it to new subscribers e.g. navbar, guards, interceptors
  user$ = this.userSubject.asObservable();

  private tokenSubject = new BehaviorSubject<string | null>(null);
  token$ = this.tokenSubject.asObservable();

  constructor(){
    /** Auth status listener, keeps user$ behaviour subject in sync */
    onAuthStateChanged(this.auth, user => this.userSubject.next(user));

    /** Token status listener, keeps tokens fresh */
    onIdTokenChanged(this.auth, async (user) =>{ // Removes the need for getIdToken() method
      this.tokenSubject.next(user ? await getIdToken(user, false) : null); // If u exists (user singed in), get or refresh ID token, otherwise null
    });
  }

  /** Log in with email/password */
  async login(email: string, password: string): Promise<User>{ // Returns promises, objects representing the eventual completion of asynchronous operations, useful for one-off actions
    const cred = await signInWithEmailAndPassword(this.auth, email, password); // Returns UserCredential object
    return cred.user; // user property within the UserCredential (cred) object
  }

  /** Register new user */
  async signUp(email: string, password: string): Promise<User>{
    const cred = await createUserWithEmailAndPassword(this.auth, email, password);
    return cred.user; 
  }

  /** Log out user */
  async logout(): Promise<void>{
    await this.auth.signOut(); // Firebase clears client session
  }
}
