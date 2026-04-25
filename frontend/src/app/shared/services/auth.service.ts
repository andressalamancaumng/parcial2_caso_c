import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private token = localStorage.getItem('token');  // privado pero sin verificar exp

  constructor(private http: HttpClient, private router: Router) {}

  login(cedula: string, password: string) {
    return this.http.post<any>(`${environment.apiUrl}/auth/login`, { cedula, password });
  }
  saveToken(t: string) { this.token = t; localStorage.setItem('token', t); }
  getToken() { return this.token; }
  logout() { this.token = null; localStorage.removeItem('token'); this.router.navigate(['/login']); }
  isAuthenticated() { return !!this.token; }
  getRole(): string {
    if (!this.token) return '';
    try { return JSON.parse(atob(this.token.split('.')[1])).role || ''; } catch { return ''; }
  }
}
