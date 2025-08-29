import { inject, Injectable } from '@angular/core';
import { Auth, User } from '@angular/fire/auth';
import { createUserWithEmailAndPassword, getIdToken, onAuthStateChanged, onIdTokenChanged, signInWithEmailAndPassword, signOut, UserCredential } from 'firebase/auth';
import { BehaviorSubject, from, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private auth = inject(Auth); // Firebase auth service instance, injecting it into this service

  private userSubject = new BehaviorSubject<User | null>(null); // Behaviour subjects hold the latest value and emits it to new subsribers e.g. navbar, guards, interceptors
  user$ = this.userSubject.asObservable();

  private tokenSubject = new BehaviorSubject<string | null>(null);
  token$ = this.tokenSubject.asObservable();

  constructor(){
    onAuthStateChanged(this.auth, async (u) =>{ // Firebase's auth status listener, emits current user and updates on changes
      this.userSubject.next(u); // u is the current Firebase User object
    });

    onIdTokenChanged(this.auth, async (u) =>{ // Another listener used to keep the token fresh
      this.tokenSubject.next(u ? await getIdToken(u, false) : null); // If u exists (user singed in), get or refresh ID token, otherwise null
    });
  }

  login(email: string, password: string): Promise<UserCredential>{
    return (signInWithEmailAndPassword(this.auth, email, password)); // Returns promises, objects representing the eventual completion of asynchronous operations, useful for one-off actions
  }

  logout(): Promise<void>{
    return (signOut(this.auth));
  }

  signUp(email: string, password: string): Promise<UserCredential>{
    return (createUserWithEmailAndPassword(this.auth, email, password));
  }
}
