const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export async function predictPrice(payload) {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || 'Erreur lors de la prédiction');
  }

  return data;
}
