/**
 * Type definitions for the dental diagnosis application.
 */

export interface ConfidenceScores {
  healthy: number;
  cavity: number;
  gum_disease: number;
}

export interface DiagnosisResult {
  success: boolean;
  prediction: string;
  confidence: number;
  confidence_scores: ConfidenceScores;
  image_id: string;
  message?: string;
  heatmap_url?: string;
}

export interface HealthStatus {
  status: string;
  message: string;
  model_loaded: boolean;
}
