import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function MahjongSelection() {
  const [theme, setTheme] = useState('');
  const navigate = useNavigate();

  const handleStartGame = (difficulty) => {
    if (theme && difficulty) {
      const path = `/mahjong-${theme}-${difficulty}-1`;
      navigate(path); // Перенаправление сразу
    }
  };

  return (
    <div>
      <h1>Добро пожаловать в игру Маджонг!</h1>
      <p>Выберите тематику карточек:</p>
      <div>
        <button onClick={() => setTheme('retroCars')}>Ретро автомобили</button>
        <button onClick={() => setTheme('electricCars')}>Электрокары</button>
        <button onClick={() => setTheme('randomCars')}>Рандом</button>
      </div>

      {theme && (
        <>
          <p>Вы выбрали: {theme === 'retroCars' ? 'Ретро автомобили' : theme === 'electricCars' ? 'Электрокары' : 'Рандом'}</p>
          <p>Выберите уровень сложности:</p>
          <div>
            <button onClick={() => handleStartGame('easy')}>Легкий</button>
            <button onClick={() => handleStartGame('medium')}>Средний</button>
            <button onClick={() => handleStartGame('hard')}>Сложный</button>
          </div>
        </>
      )}
    </div>
  );
}

export default MahjongSelection;