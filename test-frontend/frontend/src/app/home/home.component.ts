import { Component } from '@angular/core';
import {FormBuilder,FormGroup} from '@angular/forms';
import {FormsModule,ReactiveFormsModule} from '@angular/forms';

import { Observable } from 'rxjs/Rx';
import { Headers, RequestOptions} from '@angular/http';
import { Injectable } from '@angular/core';
import {SocketService} from '../services/socket.service'
import { CookieService } from 'ngx-cookie-service';
@Component({
  selector: 'seed-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
@Injectable()
export class HomeComponent {
  myForm: FormGroup;
  myForm1: FormGroup;
  cancel: boolean = false
  logger: any
  image: any;
  btc: any;
  ltc: any;
  log:any;
  xrp: any;
  auth: any;
  logged_in:any;
  response:any;
  eth: any;
  authForm: FormGroup
  btc_balance: any;
  ltc_balance: any;
  eth_balance: any;
  xrp_balance: any;
  constructor(fb: FormBuilder,
  private socket: SocketService,
  private cookie: CookieService
  ) {
    this.myForm = fb.group({
      'crypto': [''],
      'amount': ['']
    });
    this.myForm1 = fb.group({
      'crypto_sell': [''],
      'amount_sell': ['']
    });
    this.authForm = fb.group({
      'username':[''],
      'password':['']
    })


  }



  ngOnInit() {
    this.socket.getM("connect").subscribe(
      data=> {console.log(data)}
    );
    this.socket.sendMessage1("","connect")
    this.socket.getM("log").subscribe(
      data=>{
        this.log = data;
      }
    );
    this.cryptos();
    this.prices();
   setInterval(() =>{
  this.prices();
  }, 5000)


      this.socket.getMessage().subscribe(
        data=> console.log(data)
      );
      this.socket.getMessage1().subscribe(
    data =>{
      this.logger = data;
    }
  );

    }




  errorHandler(error: any): void {
     console.log(error)
   }

   public prices(){
      this.socket.sendNew('prices')
     this.socket.getMessage2().subscribe(
    data =>{
     console.log(data)
     this.btc = data[0].toString();
     this.eth = data[1].toString();
     this.ltc = data[2].toString();
     this.xrp = data[3].toString();
    }
    );

 console.log('hit')



}


  private extractResponse(res: Response) {
      if (res.status < 200 || res.status >= 300) {
          throw new Error('Bad response status: ' + res.status);
      }

      let body = res.json();

      return body;
  }

  onLogin(value: string): void {
    console.log('hmm')
    let username= value['username']
    let password = value['password']
    let data = {'username':username,'password':password}

    this.socket.sendMessage1(data,'login')
    this.socket.getM('loginreturn').subscribe(
      data=>{
        this.auth = data;
        if (this.auth == 'true'){
          this.logged_in = true
          console.log('true')
          this.cookie.set('username',username)
          console.log(this.cookie.get('username'))
        }else{
          this.response = data;
          console.log(this.response)
        }

      }
    );

  }
  onSignup(value: string): void {
    console.log('hmm')
    let username= value['username']
    let password = value['password']
    let data = {'username':username,'password':password}

    this.socket.sendMessage1(data,'signup')
    this.socket.getM('signupreturn').subscribe(
      data=>{
        this.auth = data;
        if (this.auth == 'true'){
          this.logged_in = true
          console.log('true')
          this.cookie.set('username',username)
          console.log(this.cookie.get('username'))
        }else{
          this.response = data;
          console.log(this.response)
        }

      }
    );



  }


   login(username:string,password:string){


   }



  cryptos(){
    this.socket.getM("crypto_balance").subscribe(
      data =>{
        console.log(data)
        this.btc_balance = data[0].toString();
        this.eth_balance = data[1].toString();
        this.ltc_balance = data[2].toString();
        this.xrp_balance = data[3].toString();
      }
    );
      try{
      let username = this.cookie.get('username')
      this.socket.sendMessage1(username,'cryptos')
    }catch{
      console.log('error')
    }
  }

  onSubmit(value: string): void {
    this.log = ''
    console.log('you submitted value: ', value);

    let currency = value['crypto']
    let amount = value['amount']
    let username = this.cookie.get('username')

        this.socket.getM('balance').subscribe(
          data =>{
            console.log(data)
            this.logger = data
          }
        );
        this.socket.getM('buy').subscribe(
          data =>{

          }
        );
    let d = {'CURRENCY':currency,'AMOUNT':amount,'USERNAME':username}

    this.socket.getM("crypto_balance").subscribe(
      data =>{
        console.log(data)
        this.btc_balance = data[0].toString();
        this.eth_balance = data[1].toString();
        this.ltc_balance = data[2].toString();
        this.xrp_balance = data[3].toString();
      }
    );

      this.socket.sendMessage1(d,'buy');



}

onSubmit1(value: string): void {
  this.log = ''
  console.log('you submitted value: ', value);

  let currency = value['crypto_sell']
  let amount = value['amount_sell']
  let username = this.cookie.get('username')


      this.socket.getM("balance").subscribe(
        data =>{
          console.log(data)
          this.logger = data
        }
      );

  let d = {'CURRENCY':currency,'AMOUNT':amount,"USERNAME":username}
    this.socket.sendMessage1(d,'sell');
  this.socket.getM('sell').subscribe();


}


}
