import { Injectable } from '@angular/core';
import { AuthService } from '../auth/auth.service';

@Injectable({
  providedIn: 'root'
})
export class DatabaseService {

  private selectedDatabase: string | null = null;

  constructor(private auth: AuthService) {}

  getDatabases(): string[] {
    return this.auth.getAllowedDatabases();
  }

  setSelectedDatabase(db: string) {
    this.selectedDatabase = db;
  }

  getSelectedDatabase(): string | null {
    return this.selectedDatabase;
  }

  isDatabaseSelected(): boolean {
    return !!this.selectedDatabase;
  }
}
