import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth/auth.service';

@Component({
  selector: 'app-database-selector',
  templateUrl: './database-selector.component.html',
  styleUrls: ['./database-selector.component.css'],
  standalone: true,
  imports: [CommonModule],
})
export class DatabaseSelectorComponent implements OnInit {
  databases: string[] = [];
  selectedDb: string | null = null;
  @Output() dbSelected = new EventEmitter<string>();

  constructor(private authService: AuthService) {}

  ngOnInit() {
    const userId = this.authService.getUserId();
    if (userId) {
      this.authService.getAllowedDatabases(userId).subscribe((dbs: string[]) => {
        this.databases = dbs;
      });
    }
  }

  onDbChange(db: string) {
    this.selectedDb = db;
    this.dbSelected.emit(db);
  }
}