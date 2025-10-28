/**
 * Diagnosis results display component.
 */

import type { DiagnosisResult } from '../types';
import './DiagnosisResults.css';

interface DiagnosisResultsProps {
  result: DiagnosisResult;
  originalImage: string;
  apiUrl: string;
}

export default function DiagnosisResults({ result, originalImage, apiUrl }: DiagnosisResultsProps) {
  const getStatusColor = (prediction: string): string => {
    switch (prediction) {
      case 'healthy':
        return 'status-healthy';
      case 'cavity':
        return 'status-warning';
      case 'gum_disease':
        return 'status-danger';
      default:
        return 'status-neutral';
    }
  };

  const getStatusIcon = (prediction: string): string => {
    switch (prediction) {
      case 'healthy':
        return '✓';
      case 'cavity':
        return '⚠';
      case 'gum_disease':
        return '⚠';
      default:
        return 'ℹ';
    }
  };

  const formatConfidence = (value: number): string => {
    return `${(value * 100).toFixed(1)}%`;
  };

  const formatPrediction = (prediction: string): string => {
    return prediction
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  return (
    <div className="results-container">
      <div className="results-header">
        <h2 className="results-title">Diagnosis Results</h2>
        <div className={`status-badge ${getStatusColor(result.prediction)}`}>
          <span className="status-icon">{getStatusIcon(result.prediction)}</span>
          <span className="status-text">{formatPrediction(result.prediction)}</span>
        </div>
      </div>

      <div className="confidence-main">
        <div className="confidence-label">Overall Confidence</div>
        <div className="confidence-value">{formatConfidence(result.confidence)}</div>
        <div className="confidence-bar">
          <div
            className="confidence-fill"
            style={{ width: `${result.confidence * 100}%` }}
          />
        </div>
      </div>

      {result.message && (
        <div className="message-box">
          <p>{result.message}</p>
        </div>
      )}

      <div className="confidence-breakdown">
        <h3 className="breakdown-title">Detailed Analysis</h3>
        <div className="confidence-items">
          {Object.entries(result.confidence_scores).map(([key, value]) => (
            <div key={key} className="confidence-item">
              <div className="confidence-item-header">
                <span className="confidence-item-label">{formatPrediction(key)}</span>
                <span className="confidence-item-value">{formatConfidence(value)}</span>
              </div>
              <div className="confidence-item-bar">
                <div
                  className={`confidence-item-fill ${key === result.prediction ? 'primary' : ''}`}
                  style={{ width: `${value * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="images-comparison">
        <h3 className="comparison-title">Visual Analysis</h3>
        <div className="images-grid">
          <div className="image-card">
            <img src={originalImage} alt="Original X-ray" className="result-image" />
            <p className="image-label">Original X-ray</p>
          </div>
          {result.heatmap_url && (
            <div className="image-card">
              <img
                src={`${apiUrl}${result.heatmap_url}`}
                alt="Analysis Heatmap"
                className="result-image"
              />
              <p className="image-label">Analysis Overlay</p>
            </div>
          )}
        </div>
      </div>

      <div className="disclaimer">
        <strong>Disclaimer:</strong> This is an AI-powered tool for educational purposes only.
        Always consult with a qualified dental professional for proper diagnosis and treatment.
      </div>
    </div>
  );
}
