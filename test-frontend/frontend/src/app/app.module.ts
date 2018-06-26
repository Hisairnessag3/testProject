import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import {SocketService} from './services/socket.service'
import { AppComponent } from './app.component';
import { routing } from './app.routing';
import { HomeComponent } from './home';
import { AboutComponent } from './about';
import { NavigationComponent } from './navigation';
import { CookieService } from 'ngx-cookie-service';
import {FormBuilder,FormGroup,ReactiveFormsModule} from '@angular/forms';
import { SocketIoModule, SocketIoConfig } from 'ng-socket-io';

const config: SocketIoConfig = { url: 'http://127.0.0.1:5000/trade', options: {} };

@NgModule({
  bootstrap: [AppComponent],
  declarations: [
    AppComponent,
    NavigationComponent,
    HomeComponent,
    AboutComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    NgbModule.forRoot(),
    SocketIoModule.forRoot(config),
    routing
  ],
  providers:[SocketService,CookieService]
})
export class AppModule { }
