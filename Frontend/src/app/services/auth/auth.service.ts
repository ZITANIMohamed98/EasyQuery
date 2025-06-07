import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http'; // Add this import

@Injectable({ providedIn: 'root' })
export class AuthService {
  private static userCounter = 0;  
  private loggedIn = false;
private userId: string = 'db_user1';  
private baseApi = 'http://localhost:8000'; // Add your API base URL

  constructor(private router: Router, private http: HttpClient) {} // Inject HttpClient

  login(email: string, password: string): boolean {
    if (email && password) {
      this.loggedIn = true;  

      // Send user id to backend
      this.http.post(`${this.baseApi}/userLogin`, this.userId ).subscribe();

      return true;
    }
    return false;
  }

  logout(): void {
    this.loggedIn = false;
    this.router.navigate(['/login']);
  }

  isAuthenticated(): boolean {
    return this.loggedIn;
  }

  getUserId(): string | null {
    return this.userId;
  }

getAllowedDatabases() {
  // Assumes your backend has an endpoint like /getAllowedDatabases?user_id=...
  return this.http.get<string[]>(`${this.baseApi}/getAllowedDatabases`, {
  });
}
}

