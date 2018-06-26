import { Component } from '@angular/core';
import {FormBuilder,FormGroup} from '@angular/forms';
import {FormsModule,ReactiveFormsModule} from '@angular/forms';
import { HttpClient,HttpHeaders} from '@angular/common/http'
import { Response} from '@angular/http'
import { Observable } from 'rxjs/Rx';
import { Headers, RequestOptions} from '@angular/http';
import { Injectable } from '@angular/core';
import {SocketService} from '../services/socket.service'

@Component({
  selector: 'seed-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.scss']
})
export class AboutComponent {
  myForm: FormGroup;
  logger : any;
constructor(fb: FormBuilder,
private http: HttpClient,
) {
  this.myForm = fb.group({
    'exchanges':[''],
    'key': [''],
    'secret': ['']
  });


}






}
