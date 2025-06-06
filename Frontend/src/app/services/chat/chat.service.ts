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

  queryReady = new EventEmitter<string>(); // SQL is emitted when ready for execution

  constructor() {}

  /**
   * Called when user sends a query request.
   * Adds user message and emits a SQL query.
   */
  getQuery(userInput: string) {
    // Add user's message
    this.addMessage({ sender: 'You', text: userInput, type: 'user' });

    // Simulate Text-to-SQL (replace this with real API call later)
    const mockSql = `SELECT * FROM Products WHERE Name LIKE '%${userInput}%'`;

    // Add bot message with generated SQL, flagged as awaiting execution
    this.addMessage({
      sender: 'Bot',
      text: `Generated SQL:\n${mockSql}`,
      type: 'sql',
      sql: mockSql,
      awaitingExecution: true
    });

    // Emit the SQL query so UI can ask user for confirmation
    this.queryReady.emit(mockSql);
  }

  /**
   * Called when user confirms SQL execution.
   * Simulates executing SQL and returns a result.
   */
  getQueryResult(sql: string) {
    // Notify user execution is happening
    this.addMessage({ sender: 'Bot', text: 'Executing the query...', type: 'confirm' });

    // Mock data result (replace with backend response)
    const mockResult = `
ID | Name            | Price
---|------------------|-------
1  | Sample Product   | $25.00
2  | Another Item     | $40.00
`;

    this.addMessage({
      sender: 'Bot',
      text: mockResult.trim(),
      type: 'result'
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
