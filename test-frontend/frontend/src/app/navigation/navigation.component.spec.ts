import { TestBed, inject, ComponentFixture } from '@angular/core/testing';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CommonModule, APP_BASE_HREF } from '@angular/common';

// Load the implementations that should be tested
import { NavigationComponent } from './navigation.component';
import { RouterModule } from '@angular/router';

class MockTranslateService {
  use(lang: string) { }
}

describe('NavigationComponent', () => {

  let fixture: ComponentFixture<NavigationComponent>;
  let component: NavigationComponent;

  // Provide our implementations or mocks to the dependency injector
  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [NavigationComponent],
      imports: [
        CommonModule,
        RouterModule.forRoot([]),
        NgbModule.forRoot()
      ],
      providers: [
        { provide: APP_BASE_HREF, useValue: '/' },
        NavigationComponent
      ]
    });
    fixture = TestBed.createComponent(NavigationComponent);
    component = fixture.componentInstance;
  });


});
