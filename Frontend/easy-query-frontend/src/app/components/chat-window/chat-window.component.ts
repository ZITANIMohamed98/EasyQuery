import { Component, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatService } from '../../services/chat.service';

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
  copiedIndex: number | null = null;  // tracks which message is copied

  constructor(public chatService: ChatService) {}

  ngAfterViewChecked() {
    this.scrollToBottom();
    Prism.highlightAllUnder(this.chatWindow.nativeElement); // Highlight code blocks
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
    }).catch(err => {
      console.error('Failed to copy message:', err);
    });
  }

  isSQL(text: string): boolean {
    const sqlKeywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP', 'FROM', 'WHERE'];
    const upperText = text.toUpperCase();
    return sqlKeywords.some(keyword => upperText.includes(keyword));
  }
}
