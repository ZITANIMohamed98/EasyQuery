import { Component } from '@angular/core';
import { DatabaseService } from '../../services/database/database.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-database-selector',
  templateUrl: './database-selector.component.html',
  styleUrls: ['./database-selector.component.css'],
  standalone: true,
  imports: [CommonModule],
})
export class DatabaseSelectorComponent {
  databases: string[] = [];
  selectedDb: string | null = null;

  constructor(private dbService: DatabaseService) {
    this.databases = dbService.getDatabases();
    this.selectedDb = dbService.getSelectedDatabase();
  }

  onDbChange(db: string) {
    this.selectedDb = db;
    this.dbService.setSelectedDatabase(db);
  }
}
