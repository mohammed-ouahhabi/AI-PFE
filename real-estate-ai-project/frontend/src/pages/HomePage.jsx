import { useState } from 'react';
import PropertyForm from '../components/PropertyForm';
import PredictionResult from '../components/PredictionResult';
import { predictPrice } from '../services/api';

export default function HomePage() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleEstimate(payload) {
    setError('');
    setLoading(true);

    try {
      const response = await predictPrice(payload);
      setResult(response);
    } catch (apiError) {
      setResult(null);
      setError(apiError.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container">
      <header>
        <h1>Estimation intelligente de bien immobilier</h1>
        <p>Saisis les caractéristiques du bien pour obtenir une estimation instantanée.</p>
      </header>

      <PropertyForm onSubmit={handleEstimate} loading={loading} />

      {error && <p className="error">{error}</p>}
      <PredictionResult result={result} />
    </main>
  );
}
