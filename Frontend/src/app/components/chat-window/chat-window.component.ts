import {
  Component,
  ViewChild,
  ElementRef,
  AfterViewChecked,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatService } from '../../services/chat/chat.service';

import Prism from 'prismjs';
import 'prismjs/components/prism-sql';

@Component({
  selector: 'app-chat-window',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './chat-window.component.html',
  styleUrls: ['./chat-window.component.css'],
})
export class ChatWindowComponent implements AfterViewChecked {
  @ViewChild('chatWindow') private chatWindow!: ElementRef;
  copiedIndex: number | null = null;
  isAtBottom = true;

  constructor(public chatService: ChatService) {}

  onScroll() {
    const el = this.chatWindow.nativeElement;
    // Allow a small threshold for "near the bottom"
    this.isAtBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 50;
  }

  ngAfterViewChecked() {
    Prism.highlightAllUnder(this.chatWindow.nativeElement);

    if (this.isAtBottom) {
      setTimeout(() => this.scrollToBottom(), 0);
    }
  }

  private scrollToBottom() {
    if (this.chatWindow && this.chatWindow.nativeElement) {
      this.chatWindow.nativeElement.scrollTop =
        this.chatWindow.nativeElement.scrollHeight;
    }
  }

  copyMessage(event: MouseEvent, text: string, index: number): void {
    event.stopPropagation();
    navigator.clipboard
      .writeText(text)
      .then(() => {
        this.copiedIndex = index;
        setTimeout(() => {
          this.copiedIndex = null; // revert icon after 1.5 seconds
        }, 1500);
      })
      .catch((err) => {
        console.error('Failed to copy message:', err);
      });
  }

  executeQuery(sql: string, index: number) {
  // Remove the execute button by clearing awaitingExecution flag
  this.chatService.messages[index].awaitingExecution = false;

  // Prepare the data for executeQuery
  const message = this.chatService.messages[index];
  this.chatService
    .executeQuery({
      user_id: message.sender || 'user1',
      activity_id: 'act1',
      database_name: 'mydb',
      input: message.text,
      query: sql,
    })
    .subscribe((response: string) => {
      // Add the result as a new message in the chat
      this.chatService.addMessage({
        sender: 'EasyQuery',
        text: response,
        type: 'result',
      });
    });
}

  private static readonly SQL_KEYWORDS = [
    'SELECT',
    'INSERT',
    'UPDATE',
    'DELETE',
    'CREATE',
    'ALTER',
    'DROP',
    'FROM',
    'WHERE',
  ];

  isSQL(text: string): boolean {
    if (!text) return false;
    const upperText = text.toUpperCase();
    return ChatWindowComponent.SQL_KEYWORDS.some((keyword) =>
      upperText.includes(keyword)
    );
  }
}
