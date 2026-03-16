export default function PredictionResult({ result }) {
  if (!result) return null;

  const price = new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: result.currency || 'EUR',
    maximumFractionDigits: 0
  }).format(result.estimated_price);

  return (
    <section className="result-card">
      <h2>Prix estimé</h2>
      <p className="result-price">{price}</p>
      <small>Modèle: {result.model_version}</small>
    </section>
  );
}
