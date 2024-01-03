// PriceFilter.tsx
import React, { FC, ChangeEvent } from 'react';
import { useNavigate } from 'react-router-dom';

interface PriceFilterProps {
  minValue: number;
  maxValue: number;
}

const PriceFilter: FC<PriceFilterProps> = ({ minValue, maxValue }) => {
  const navigate = useNavigate();

  const handleFilterChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;

    // Валидация значений и обработка ошибок здесь, если необходимо

    navigate(`/products?${name}=${value}`);
  };

  return (
    <div>
      <label>
        Min Price:
        <input
          type="number"
          name="minPrice"
          value={minValue}
          onChange={handleFilterChange}
        />
      </label>
      <label>
        Max Price:
        <input
          type="number"
          name="maxPrice"
          value={maxValue}
          onChange={handleFilterChange}
        />
      </label>
    </div>
  );
};

export default PriceFilter;
