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
  private baseApi = 'http://localhost:8000';

  queryReady = new EventEmitter<string>(); // SQL is emitted when ready for execution

  constructor(private http: HttpClient) {}

  /**
   * Called when user sends a query request.
   * Adds user message and emits a SQL query.
   */

  getQuery(inputData: {
  user_id: string;
  activity_id: string;
  database_name: string;
  input: string;
}) {
  return this.http.post<any>(`${this.baseApi}/getQuery`, inputData);
}

  /**
   * Called when user confirms SQL execution.
   * Simulates executing SQL and returns a result.
   */
  executeQuery(data: {
  user_id: string;
  activity_id: string;
  database_name: string;
  input: string;
  query: string;
}) {
  return this.http.post<any>(`${this.baseApi}/executeQuery`, data);
}

  /**
   * Adds a message to the chat history
   */
  addMessage(message: ChatMessage) {
    this.messages.push(message);
  }

}
