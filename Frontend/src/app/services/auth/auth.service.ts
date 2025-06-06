import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

@Injectable({ providedIn: 'root' })
export class AuthService {
private static userCounter = 0;  
  private loggedIn = false;
  private userId: number | null = null;
  constructor(private router: Router) {}

login(email: string, password: string): boolean {
    if (email && password) {
      this.loggedIn = true;
      AuthService.userCounter += 1;  
      this.userId = AuthService.userCounter;  
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

  getUserId(): number | null {
    console
    return this.userId;
  }

   getAllowedDatabases(): string[] {
    return ['AdventureWorks2022', 'SalesDB', 'InventoryDB'];
  }
}
