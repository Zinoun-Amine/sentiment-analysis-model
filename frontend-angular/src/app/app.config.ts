// src/app/app.config.ts
import { ApplicationConfig } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';
// 1. Importer le fournisseur d'animations
import { provideAnimations } from '@angular/platform-browser/animations';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(),
    // 2. Ajouter le fournisseur ici
    provideAnimations() 
  ]
};