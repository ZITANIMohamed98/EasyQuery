import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../../services/chat.service';

@Component({
  selector: 'app-chat-input',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat-input.component.html',
  styleUrls: ['./chat-input.component.css']
})
export class ChatInputComponent {
  inputText = '';

  constructor(private chatService: ChatService) {}

  sendMessage() {
    if (this.inputText.trim()) {
      this.chatService.addMessage({ sender: 'You', text: this.inputText });
      this.inputText = '';
    }
  }
}