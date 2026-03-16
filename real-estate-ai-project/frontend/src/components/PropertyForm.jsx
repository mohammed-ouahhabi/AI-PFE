import { useState } from 'react';

const initialValues = {
  surface: '',
  rooms: '',
  bedrooms: '',
  city: '',
  construction_year: '',
  has_garage: false,
  has_garden: false,
  has_balcony: false
};

export default function PropertyForm({ onSubmit, loading }) {
  const [formValues, setFormValues] = useState(initialValues);

  function handleChange(event) {
    const { name, value, type, checked } = event.target;
    setFormValues((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  }

  function handleSubmit(event) {
    event.preventDefault();
    onSubmit({
      ...formValues,
      surface: Number(formValues.surface),
      rooms: Number(formValues.rooms),
      bedrooms: Number(formValues.bedrooms),
      construction_year: Number(formValues.construction_year)
    });
  }

  return (
    <form className="property-form" onSubmit={handleSubmit}>
      <div className="grid">
        <label>
          Surface (m²)
          <input name="surface" type="number" min="1" required value={formValues.surface} onChange={handleChange} />
        </label>
        <label>
          Pièces
          <input name="rooms" type="number" min="1" required value={formValues.rooms} onChange={handleChange} />
        </label>
        <label>
          Chambres
          <input name="bedrooms" type="number" min="0" required value={formValues.bedrooms} onChange={handleChange} />
        </label>
        <label>
          Ville
          <input name="city" type="text" required value={formValues.city} onChange={handleChange} />
        </label>
        <label>
          Année de construction
          <input
            name="construction_year"
            type="number"
            min="1700"
            max="2100"
            required
            value={formValues.construction_year}
            onChange={handleChange}
          />
        </label>
      </div>

      <fieldset>
        <legend>Équipements</legend>
        <label><input name="has_garage" type="checkbox" checked={formValues.has_garage} onChange={handleChange} /> Garage</label>
        <label><input name="has_garden" type="checkbox" checked={formValues.has_garden} onChange={handleChange} /> Jardin</label>
        <label><input name="has_balcony" type="checkbox" checked={formValues.has_balcony} onChange={handleChange} /> Balcon</label>
      </fieldset>

      <button type="submit" disabled={loading}>{loading ? 'Estimation en cours...' : 'Estimer le prix'}</button>
    </form>
  );
}
