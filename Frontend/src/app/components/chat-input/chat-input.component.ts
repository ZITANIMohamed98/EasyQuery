import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../../services/chat/chat.service';
import { GetQueryModel } from '../../data-models/get-query-model';
import { DatabaseSelectorComponent } from '../database-selector/database-selector.component';

@Component({
  selector: 'app-chat-input',
  standalone: true,
  imports: [CommonModule, FormsModule, DatabaseSelectorComponent],
  templateUrl: './chat-input.component.html',
  styleUrls: ['./chat-input.component.css']
})
export class ChatInputComponent {
  inputText = '';
  inputFocused = false;
  messageSent = false; 
  lastQuery: string = '';
  warningMessage: string = 'Please choose a database before sending a question.';
  selectedDatabase: string | null = null;

  onDatabaseSelected(db: string) {
    this.selectedDatabase = db;
    this.warningMessage = ''; // Clear warning when a database is selected
  }

  constructor(private chatService: ChatService) { }

sendMessage() {
  if (!this.selectedDatabase) {
    this.warningMessage = 'Please choose a database before sending a question.';
    return;
  }
  this.warningMessage = '';
  if (this.inputText.trim()) {
    const message = this.inputText;
    this.inputText = '';
    if (!this.messageSent) {
      this.messageSent = true;
    }
    // Add the user's message to the chat
    this.chatService.addMessage({
      sender: 'You',
      text: message,
      type: 'user'
    });

    // Call getQuery from the service with random user_id and activity_id
    const userId = 'db_user1';
    const activityId = 'activity_' + Math.random().toString(36).substring(2, 10);

   this.chatService.getQuery(new GetQueryModel(userId, activityId, this.selectedDatabase, message))
      .subscribe((query: string) => {
        this.chatService.addMessage({
          sender: 'EasyQuery',
          text: query,
          sql: query,
          type: 'sql',
          awaitingExecution: true
        });
        this.lastQuery = query;
      });
  }
}
}