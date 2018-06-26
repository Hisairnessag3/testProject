import { TestBed, inject, ComponentFixture } from '@angular/core/testing';
import { BrowserModule }  from '@angular/platform-browser';
import { APP_BASE_HREF } from '@angular/common';
import { RouterModule } from '@angular/router';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { NavigationComponent } from './navigation';

// Load the implementations that should be tested
import { AppComponent } from './app.component';


describe('AppComponent', () => {

  let fixture: ComponentFixture<AppComponent>;
  let component: AppComponent;

  // Provide our implementations or mocks to the dependency injector
  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [
        AppComponent,
        NavigationComponent
      ],
      imports: [
        BrowserModule,
        NgbModule.forRoot(),
        RouterModule.forRoot([])
      ],
      providers: [
        { provide: APP_BASE_HREF, useValue: '/' },
        AppComponent
      ]
    });
    fixture = TestBed.createComponent(AppComponent);
    component = fixture.componentInstance;
  });

});
