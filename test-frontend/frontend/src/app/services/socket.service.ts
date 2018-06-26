import { Injectable } from '@angular/core';
import * as io from 'socket.io-client';
import { Socket } from 'ng-socket-io';
import { Observable } from 'rxjs/Observable'
import 'rxjs/add/operator/map';

@Injectable()
export class SocketService {
  constructor(private socket: Socket) {
  }

  // EMITTER

  sendMessage(msg: any) {
       this.socket.emit("runner", msg);
   }

   sendMessage1(msg: any,endpoint:any)  {
        this.socket.emit(endpoint, msg);
    }
    sendMessage2(msg: any,endpoint:any)  {
         this.socket.emit(endpoint, msg);
     }
     sendNew(endpoint:any)  {
          this.socket.emit(endpoint);
      }
  getMessage() {
        return this.socket
        .fromEvent<any>("balance")
        .map(data => console.log(data))
    }
    getMessage1() {
          return this.socket
              .fromEvent<any>("logs")
              .map( data => data );
      }
      getMessage2() {
            return this.socket
                .fromEvent<any>('prices')
                .map( data => data );
        }
        getM(endpoint:any){
          return this.socket
          .fromEvent<any>(endpoint)
          .map(data =>data)
        }
          // HANDLER
}
