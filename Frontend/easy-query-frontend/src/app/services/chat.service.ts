import { EventEmitter, Injectable } from '@angular/core';

interface ChatMessage {
  sender: string;
  text: string;
  type?: 'confirm' | 'sql' | 'result' | string;
  sql?: string;
    awaitingExecution?: boolean; // new flag
}

@Injectable({ providedIn: 'root' })
export class ChatService {
  messages: ChatMessage[] = [];

  queryReady = new EventEmitter<string>(); // Emits SQL string when ready

  constructor() {}

  // Simulate generating SQL from user input
  getQuery(userInput: string) {
    // Clear previous system/bot messages if needed or keep history
    // Add user message
    this.addMessage({ sender: 'You', text: userInput });

    // Mock SQL generation logic (simplified)
    const mockSql = `SELECT * FROM Products WHERE Name LIKE '%${userInput}%'`;

    // Add bot message with generated SQL
  this.addMessage({ sender: 'Bot', text: mockSql, type: 'sql', sql: mockSql, awaitingExecution: true });

    // Add system message asking for confirmation to execute
    this.queryReady.emit(mockSql);
  }

  // Simulate executing SQL query and returning results
  getQueryResult(sql: string) {
    // Add system message that query execution is starting
    this.addMessage({ sender: 'Bot', text: 'Executing the query...' });

    // Mock result for demonstration
    const mockResult = `
ID | Name          | Price
---|---------------|-------
1  | Sample Product| $25.00
2  | Another Item  | $40.00
`;

    // Add bot message with mock result
    this.addMessage({ sender: 'Bot', text: mockResult, type: 'result' });
  }

  // Simple method to add a message to chat history
  addMessage(message: ChatMessage) {
    this.messages.push(message);
  }
}
