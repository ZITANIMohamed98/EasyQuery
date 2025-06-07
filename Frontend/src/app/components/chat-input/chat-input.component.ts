import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../../services/chat/chat.service';

@Component({
  selector: 'app-chat-input',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat-input.component.html',
  styleUrls: ['./chat-input.component.css']
})
export class ChatInputComponent {
  inputText = '';
  inputFocused = false;
  messageSent = false; // <- Add this
  lastQuery: string = '';


  constructor(private chatService: ChatService) { }

sendMessage() {
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
    // Get the SQL query from the backend
    this.chatService.getQuery({
      user_id: 'user1',
      activity_id: 'act1',
      database_name: 'mydb',
      input: message
    }).subscribe(response => {
      // Add the generated SQL as a new message with copy and execute enabled
      this.chatService.addMessage({
        sender: 'system',
        text: response.query,
        sql: response.query,
        type: 'sql',
        awaitingExecution: true
      });
      this.lastQuery = response.query;
    });
  }
}
}