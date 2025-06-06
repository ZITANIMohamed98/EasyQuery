import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ChatInputComponent } from '../chat-input/chat-input.component';
import { ChatWindowComponent } from '../chat-window/chat-window.component';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { AuthService } from '../../services/auth/auth.service';
import { DatabaseSelectorComponent } from '../database-selector/database-selector.component';
import { DatabaseStatusComponent } from '../database-status/database-status.component';

@Component({
  selector: 'app-main-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, SidebarComponent, ChatWindowComponent, ChatInputComponent, DatabaseSelectorComponent, DatabaseStatusComponent],
  templateUrl: './main-chat.component.html',
  styleUrl: './main-chat.component.css'
})
export class MainChatComponent {
  constructor(private auth: AuthService) {}

    logout() {
    this.auth.logout(); 
  }
}
