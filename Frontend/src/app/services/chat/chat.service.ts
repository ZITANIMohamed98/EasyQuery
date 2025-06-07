import { HttpClient } from '@angular/common/http';
import { EventEmitter, Injectable } from '@angular/core';

export interface ChatMessage {
  sender: string;
  text: string;
  type?: 'confirm' | 'sql' | 'result' | 'user' | string;
  sql?: string;
  awaitingExecution?: boolean;
}

@Injectable({ providedIn: 'root' })
export class ChatService {
  messages: ChatMessage[] = [];
  private baseApi = 'http://localhost:8000/';

  queryReady = new EventEmitter<string>(); // SQL is emitted when ready for execution

  constructor(private http: HttpClient) {}

  /**
   * Called when user sends a query request.
   * Adds user message and emits a SQL query.
   */

  getQuery(userInput: string) {
    // Add user's message
    this.addMessage({ sender: 'You', text: userInput, type: 'user' });

    // Use GET request, sending the query as a URL parameter
    this.http
      .get<{ sql: string }>(
        `${this.baseApi}?query=${encodeURIComponent(userInput)}`
      )
      .subscribe({
        next: (response) => {
          const sql = response.sql;

          // Add bot message with generated SQL, flagged as awaiting execution
          this.addMessage({
            sender: 'Bot',
            text: `Generated SQL:\n${sql}`,
            type: 'sql',
            sql: sql,
            awaitingExecution: true,
          });

          // Emit the SQL query so UI can ask user for confirmation
          this.queryReady.emit(sql);
        },
        error: (err) => {
          this.addMessage({
            sender: 'Bot',
            text: 'Sorry, there was an error generating the SQL.',
            type: 'error',
          });
        },
      });
  }

  /**
   * Called when user confirms SQL execution.
   * Simulates executing SQL and returns a result.
   */
  getQueryResult(sql: string) {
    // Notify user execution is happening
    this.addMessage({
      sender: 'Bot',
      text: 'Executing the query...',
      type: 'confirm',
    });

    // Call backend to execute the SQL and get the result
    this.http
      .post<{ result: string }>(`${this.baseApi}/execute-query`, { sql })
      .subscribe({
        next: (response) => {
          this.addMessage({
            sender: 'Bot',
            text: response.result,
            type: 'result',
          });
        },
        error: (err) => {
          this.addMessage({
            sender: 'Bot',
            text: 'Sorry, there was an error executing the SQL.',
            type: 'error',
          });
        },
      });
  }

  /**
   * Adds a message to the chat history
   */
  addMessage(message: ChatMessage) {
    this.messages.push(message);
  }

  /**
   * Clears all messages
   */
  clearMessages() {
    this.messages = [];
  }
}
