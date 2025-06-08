import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { of } from 'rxjs'; 

@Injectable({ providedIn: 'root' })
export class AuthService {
  private static userCounter = 0;  
  private loggedIn = false;
  private userId: string = 'db_user1';  
  private baseApi = 'http://localhost:8000';
  private serverIp = 'http://20.121.40.117:80'

  constructor(private router: Router, private http: HttpClient) {}

  login(email: string, password: string): boolean {
    if (email && password) {
      this.loggedIn = true;  
      // Send user id to backend
      this.http.post(`${this.baseApi}/userLogin`, this.userId ).subscribe();

      // Immediately fetch allowed databases for this user
      this.getAllowedDatabases(this.userId).subscribe(dbs => {
        // You can store or process the dbs here as needed
        console.log('Allowed databases:', dbs);
      });

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

  getAllowedDatabases(userId: string) {

        // return of(['trips', 'users', 'orders']);


    // Call the backend endpoint with user_id as a query parameter
    return this.http.get<string[]>(`${this.serverIp}/listAllowedDbs?user_id=${userId}`);
  }
}