import { useState } from 'react';
import ImageUpload from './components/ImageUpload';
import DiagnosisResults from './components/DiagnosisResults';
import type { DiagnosisResult } from './types';
import './App.css';

const API_URL = 'http://localhost:8000';

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<DiagnosisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleImageSelect = (file: File, preview: string) => {
    setSelectedFile(file);
    setPreviewUrl(preview);
    setResult(null);
    setError(null);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch(`${API_URL}/api/diagnose`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to analyze image');
      }

      const data: DiagnosisResult = await response.json();
      setResult(data);
    } catch (err) {
      console.error('Error analyzing image:', err);
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to analyze image. Please ensure the backend server is running.'
      );
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">
            <span className="title-icon">🦷</span>
            Dental Diagnosis AI!
          </h1>
          <p className="app-subtitle">
            X-ray analysis for cavity and gum disease detection
          </p>
        </div>
      </header>

      <main className="app-main">
        {!result ? (
          <div className="upload-section">
            <ImageUpload
              onImageSelect={handleImageSelect}
              disabled={isAnalyzing}
            />

            {selectedFile && (
              <div className="actions">
                <button
                  className="btn btn-primary"
                  onClick={handleAnalyze}
                  disabled={isAnalyzing}
                >
                  {isAnalyzing ? (
                    <>
                      <span className="spinner" />
                      Analyzing...
                    </>
                  ) : (
                    'Analyze X-ray'
                  )}
                </button>
              </div>
            )}

            {error && (
              <div className="error-box">
                <span className="error-icon">⚠</span>
                <p>{error}</p>
              </div>
            )}
          </div>
        ) : (
          <>
            <DiagnosisResults
              result={result}
              originalImage={previewUrl || ''}
              apiUrl={API_URL}
            />
            <div className="actions">
              <button className="btn btn-secondary" onClick={handleReset}>
                Analyze Another X-ray
              </button>
            </div>
          </>
        )}
      </main>

      <footer className="app-footer">
        <p>
          Made by Ian Roybal
        </p>
      </footer>
    </div>
  );
}

export default App;
