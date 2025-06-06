import { Routes } from "@angular/router";
import { LoginComponent } from "./components/login/login.component";
import { AuthGuard } from "./services/auth/auth.guard";
import { MainChatComponent } from "./components/main-chat/main-chat.component";

export const routes: Routes = [
   { path: 'login', component: LoginComponent },
  { path: '', canActivate: [AuthGuard], component: MainChatComponent },
  { path: '**', redirectTo: 'login' }
];

