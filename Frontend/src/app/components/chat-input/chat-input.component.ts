import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../../services/chat/chat.service';
import { GetQueryModel } from '../../data-models/get-query-model';

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

    // Call getQuery from the service with random user_id and activity_id
    const userId = 'user_' + Math.random().toString(36).substring(2, 10);
    const activityId = 'activity_' + Math.random().toString(36).substring(2, 10);

    this.chatService.getQuery(new GetQueryModel(userId, activityId, 'trips', message))
      .subscribe(response => {
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