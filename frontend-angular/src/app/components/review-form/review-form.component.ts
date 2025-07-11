// src/app/components/review-form/review-form.component.ts

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormControl, FormGroup, Validators } from '@angular/forms';
import { ApiService, PredictionResponse } from '../../services/api.service';
import { finalize } from 'rxjs';

// =========================================================================
// === Define a new interface for the component's state (DisplayResult) ===
// This interface includes the 'text' property we need for display.
// =========================================================================
export interface DisplayResult {
  sentiment: 'Positive' | 'Negative' | 'Neutral';
  text: string; // The original text that was predicted
}

@Component({
  selector: 'app-review-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './review-form.component.html',
  styleUrls: ['./review-form.component.css']
})
export class ReviewFormComponent {
  reviewForm = new FormGroup({
    reviewText: new FormControl('', Validators.required)
  });

  isPredicting = false;

  // Use the new DisplayResult interface here
  predictionResult: DisplayResult | null = null;
  errorMessage: string | null = null;

  exampleReviews = [
    { text: "This is the best app for editing videos, I use it all the time and I've never had a problem.", sentiment: 'Positive' },
    { text: "The app is okay, but it's missing some key features that other apps have.", sentiment: 'Neutral' },
    { text: "The latest update made it so slow and it crashes constantly. I can't even open my drafts. Please fix this.", sentiment: 'Negative' },
    { text: "Great fun app so far, lots of potential!", sentiment: 'Positive' },
    { text: "It's not bad, just average. Does the job but nothing special.", sentiment: 'Neutral' },
    { text: "I lost all my work after the recent crash. Unreliable and frustrating.", sentiment: 'Negative' }
  ];

  constructor(private apiService: ApiService) {}

  useExample(text: string) {
    this.reviewForm.get('reviewText')?.setValue(text);
    this.onPredict(); // Automatically predict when an example is chosen
  }

  onPredict() {
    if (this.reviewForm.invalid) {
      // Optionally, add some visual feedback here if the form is invalid
      this.errorMessage = 'Veuillez entrer un avis.';
      this.predictionResult = null;
      return;
    }

    this.isPredicting = true;
    this.predictionResult = null; // Clear previous result
    this.errorMessage = null; // Clear previous error

    const text = this.reviewForm.value.reviewText ?? ''; // Use nullish coalescing for safety
    this.apiService.predictSentiment(text)
      .pipe(finalize(() => this.isPredicting = false)) // Ensure loading state is reset
      .subscribe({
        next: (res: PredictionResponse) => {
          // Create a new DisplayResult object, including the original text
          this.predictionResult = {
            sentiment: res.sentiment,
            text: text
          };
        },
        error: (err) => {
          console.error('API Error:', err);
          this.errorMessage = 'Une erreur est survenue. Le backend est-il lancé ?';
          // Optionally, more specific error messages based on err.status
        }
      });
  }

  getSentimentClass(): string {
    if (!this.predictionResult?.sentiment) {
      return '';
    }
    // Note: Ensure these match the exact string values from your backend
    switch (this.predictionResult.sentiment) {
      case 'Positive': return 'sentiment-positive';
      case 'Negative': return 'sentiment-negative';
      case 'Neutral': return 'sentiment-neutral';
      default: return ''; // Fallback
    }
  }
}