import { Component, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatService } from '../../services/chat/chat.service';

import Prism from 'prismjs';
import 'prismjs/components/prism-sql';

@Component({
  selector: 'app-chat-window',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './chat-window.component.html',
  styleUrls: ['./chat-window.component.css']
})
export class ChatWindowComponent implements AfterViewChecked {
  @ViewChild('chatWindow') private chatWindow!: ElementRef;
  copiedIndex: number | null = null;

  constructor(public chatService: ChatService) {}

  ngAfterViewChecked() {
    this.scrollToBottom();
    Prism.highlightAllUnder(this.chatWindow.nativeElement);
  }

  private scrollToBottom(): void {
    try {
      this.chatWindow.nativeElement.scrollTop = this.chatWindow.nativeElement.scrollHeight;
    } catch (err) {
      console.error('Could not scroll chat window:', err);
    }
  }

copyMessage(event: MouseEvent, text: string, index: number): void {
  event.stopPropagation();
  navigator.clipboard.writeText(text).then(() => {
    this.copiedIndex = index;
    setTimeout(() => {
      this.copiedIndex = null;  // revert icon after 1.5 seconds
    }, 1500);
  }).catch(err => {
    console.error('Failed to copy message:', err);
  });
}


  executeQuery(sql: string, index: number) {
    // Remove the execute button by clearing awaitingExecution flag
    this.chatService.messages[index].awaitingExecution = false;

    // Execute the SQL (mock or real)
    this.chatService.getQueryResult(sql);
  }

  private static readonly SQL_KEYWORDS = [
    'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP', 'FROM', 'WHERE'
  ];

  isSQL(text: string): boolean {
    if (!text) return false;
    const upperText = text.toUpperCase();
    return ChatWindowComponent.SQL_KEYWORDS.some(keyword => upperText.includes(keyword));
  }
}
