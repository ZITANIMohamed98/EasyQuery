import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-database-status',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './database-status.component.html',
  styleUrls: ['./database-status.component.css'],})
export class DatabaseStatusComponent {
  selectedDb: string | null = null;

  constructor() {
  }
}
