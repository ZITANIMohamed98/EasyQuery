import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ChatService {
  messages: { sender: string; text: string }[] = [];

  addMessage(message: { sender: string; text: string }) {
    this.messages.push(message);
  }
}