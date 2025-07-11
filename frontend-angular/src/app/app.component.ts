import { Component } from '@angular/core';
import { ReviewFormComponent } from './components/review-form/review-form.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ReviewFormComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'frontend-angular';
}
