// src/app/services/api.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// --- UPDATED RESPONSE TYPE ---
// This now matches the capitalized sentiment from the final FastAPI backend
export interface PredictionResponse {
  sentiment: 'Positive' | 'Negative' | 'Neutral';
  // You can add other fields here if your API sends them
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  // Use the correct endpoint from your FastAPI server
  private predictUrl = 'http://localhost:8000/predict'; // Default for FastAPI is 8000

  constructor(private http: HttpClient) { }

  predictSentiment(text: string): Observable<PredictionResponse> {
    const requestBody = { text: text };
    return this.http.post<PredictionResponse>(this.predictUrl, requestBody);
  }
}