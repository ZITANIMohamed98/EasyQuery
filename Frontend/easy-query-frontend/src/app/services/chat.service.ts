import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ChatService {
  messages: { sender: string; text: string }[] = [];

  addMessage(message: { sender: string; text: string }) {
    this.messages.push(message);

    // Add bot response with a delay
    setTimeout(() => {
      const responseText = this.generateResponse(message.text);
      this.messages.push({ sender: 'EasyQuery', text: responseText });
    }, 1000); 
  }

   private generateResponse(userMessage: string): string {
    // Basic response logic; replace with AI call or custom logic later
    return `USE AdventureWorks2022;
GO

IF OBJECT_ID('dbo.NewProducts', 'U') IS NOT NULL
DROP TABLE dbo.NewProducts;
GO

ALTER DATABASE AdventureWorks2022 SET RECOVERY BULK_LOGGED;
GO

SELECT *
INTO dbo.NewProducts
FROM Production.Product
WHERE ListPrice > $25
    AND ListPrice < $100;
GO

ALTER DATABASE AdventureWorks2022 SET RECOVERY FULL;
GO`;
  }
}