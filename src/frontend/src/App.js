import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './App.css';

import MahjongSelection from './components/MahjongSelection';
import YouLose from './components/YouLose';

import Registration from './Registration';
import Login from './Login';

// Компоненты для разных уровней игры
import MahjongRetroCarsEasy1 from './components/mahjong-retroCars-easy-1';
import MahjongRetroCarsEasy2 from './components/mahjong-retroCars-easy-2';
import MahjongRetroCarsEasy3 from './components/mahjong-retroCars-easy-3';
import MahjongRetroCarsMedium1 from './components/mahjong-retroCars-medium-1';
import MahjongRetroCarsMedium2 from './components/mahjong-retroCars-medium-2';
import MahjongRetroCarsMedium3 from './components/mahjong-retroCars-medium-3';
import MahjongRetroCarsHard1 from './components/mahjong-retroCars-hard-1';
import MahjongRetroCarsHard2 from './components/mahjong-retroCars-hard-2';
import MahjongRetroCarsHard3 from './components/mahjong-retroCars-hard-3';

import MahjongElectricCarsEasy1 from './components/mahjong-electricCars-easy-1';
import MahjongElectricCarsEasy2 from './components/mahjong-electricCars-easy-2';
import MahjongElectricCarsEasy3 from './components/mahjong-electricCars-easy-3';
import MahjongElectricCarsMedium1 from './components/mahjong-electricCars-medium-1';
import MahjongElectricCarsMedium2 from './components/mahjong-electricCars-medium-2';
import MahjongElectricCarsMedium3 from './components/mahjong-electricCars-medium-3';
import MahjongElectricCarsHard1 from './components/mahjong-electricCars-hard-1';
import MahjongElectricCarsHard2 from './components/mahjong-electricCars-hard-2';
import MahjongElectricCarsHard3 from './components/mahjong-electricCars-hard-3';

import MahjongRandomCarsEasy1 from './components/mahjong-randomCars-easy-1';
import MahjongRandomCarsEasy2 from './components/mahjong-randomCars-easy-2';
import MahjongRandomCarsEasy3 from './components/mahjong-randomCars-easy-3';
import MahjongRandomCarsMedium1 from './components/mahjong-randomCars-medium-1';
import MahjongRandomCarsMedium2 from './components/mahjong-randomCars-medium-2';
import MahjongRandomCarsMedium3 from './components/mahjong-randomCars-medium-3';
import MahjongRandomCarsHard1 from './components/mahjong-randomCars-hard-1';
import MahjongRandomCarsHard2 from './components/mahjong-randomCars-hard-2';
import MahjongRandomCarsHard3 from './components/mahjong-randomCars-hard-3';

const Leaderboard = ({ data, onClose }) => {
  if (!Array.isArray(data) || data.length === 0) {
    return (
      <div className="leaderboard-popup">
        <div className="leaderboard-content">
          <button onClick={onClose} className="close-btn">x</button>
          <h2>Лидерборд</h2>
          <p>Нет данных для отображения</p>
        </div>
      </div>
    );
  }

  return (
    <div className="leaderboard-popup">
      <div className="leaderboard-content">
        <button onClick={onClose} className="close-btn">x</button>
        <h2>Лидерборд</h2>
        <ul>
          {data.map((player, index) => (
            <li key={player.id}>
              {index + 1}. {player.username} — {player.score} очков
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showLeaderboard, setShowLeaderboard] = useState(false);
  const [leaderboardData, setLeaderboardData] = useState([]);

  // Проверка токена при загрузке компонента
  useEffect(() => {
    const token = localStorage.getItem('jwtToken');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  // Функция для успешной авторизации
  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
  };

  // Функция для выхода (удаляет токен и возвращает пользователя в неавторизованный статус)
  const handleLogout = () => {
    localStorage.removeItem('jwtToken');
    setIsAuthenticated(false);
  };

  // Функция для показа лидерборда
  const handleShowLeaderboard = async () => {
    try {
      const response = await fetch('http://localhost:8080/records?limit=10');
      if (!response.ok) {
        throw new Error(`Ошибка сервера: ${response.statusText}`);
      }
      const result = await response.json();
      console.log('Полученные данные:', result); // Для проверки
      setLeaderboardData(result); // Установить массив данных
      setShowLeaderboard(true);
    } catch (error) {
      console.error('Ошибка при загрузке данных лидерборда:', error);
      setLeaderboardData([]); // Устанавливаем пустой массив в случае ошибки
    }
  };

  // Функция для закрытия лидерборда
  const handleCloseLeaderboard = () => {
    setShowLeaderboard(false);
  };

  const [showRules, setShowRules] = useState(false); // Состояние для показа/скрытия правил

  // Функция для переключения видимости правил
  const toggleRules = () => {
    setShowRules(!showRules);
  };

  return (
    <Router>
      <nav>
        <Link to="/">Home</Link>
        {/* Линк на регистрацию и логин */}
        <Link to="/registration">Регистрация</Link>
        <Link to="/login">Вход</Link>
        <button onClick={handleShowLeaderboard}>Лидерборд</button>
      </nav>
      <div className="container">
        {/* Текст, если пользователь не авторизован */}
        {!isAuthenticated && (
          <div className="progress-prompt">
            Хотите сохранить прогресс? <Link to="/login">Войдите в аккаунт!</Link>
          </div>
        )}

        <button onClick={toggleRules}>Показать правила</button>
        {showRules && (
          <div className="scrolling-rules">
            <p>Правила: соединяй карточки, которые не имеют соседей справа или слева! Избавься от всех карточек на поле!</p>
            <button onClick={toggleRules} className="close-btn">x</button>
          </div>
        )}

        {/* Лидерборд */}
        {showLeaderboard && (
          <Leaderboard data={leaderboardData} onClose={handleCloseLeaderboard} />
        )}

        <Routes>
          {/* Основные маршруты */}
          <Route path="/" element={<MahjongSelection />} />
          
          {/* Маршруты для регистрации и логина */}
          <Route path="/registration" element={<Registration />} />
          <Route path="/login" element={<Login onLoginSuccess={handleLoginSuccess} />} />

          <Route path="/YouLose" element={<YouLose />} />
          
          {/* Ретро автомобили */}
          <Route path="/mahjong-retroCars-easy-1" element={<MahjongRetroCarsEasy1 />} />
          <Route path="/mahjong-retroCars-easy-2" element={<MahjongRetroCarsEasy2 />} />
          <Route path="/mahjong-retroCars-easy-3" element={<MahjongRetroCarsEasy3 />} />
          <Route path="/mahjong-retroCars-medium-1" element={<MahjongRetroCarsMedium1 />} />
          <Route path="/mahjong-retroCars-medium-2" element={<MahjongRetroCarsMedium2 />} />
          <Route path="/mahjong-retroCars-medium-3" element={<MahjongRetroCarsMedium3 />} />
          <Route path="/mahjong-retroCars-hard-1" element={<MahjongRetroCarsHard1 />} />
          <Route path="/mahjong-retroCars-hard-2" element={<MahjongRetroCarsHard2 />} />
          <Route path="/mahjong-retroCars-hard-3" element={<MahjongRetroCarsHard3 />} />
          
          {/* Электрические автомобили */}
          <Route path="/mahjong-electricCars-easy-1" element={<MahjongElectricCarsEasy1 />} />
          <Route path="/mahjong-electricCars-easy-2" element={<MahjongElectricCarsEasy2 />} />
          <Route path="/mahjong-electricCars-easy-3" element={<MahjongElectricCarsEasy3 />} />
          <Route path="/mahjong-electricCars-medium-1" element={<MahjongElectricCarsMedium1 />} />
          <Route path="/mahjong-electricCars-medium-2" element={<MahjongElectricCarsMedium2 />} />
          <Route path="/mahjong-electricCars-medium-3" element={<MahjongElectricCarsMedium3 />} />
          <Route path="/mahjong-electricCars-hard-1" element={<MahjongElectricCarsHard1 />} />
          <Route path="/mahjong-electricCars-hard-2" element={<MahjongElectricCarsHard2 />} />
          <Route path="/mahjong-electricCars-hard-3" element={<MahjongElectricCarsHard3 />} />

          {/* Случайные автомобили */}
          <Route path="/mahjong-randomCars-easy-1" element={<MahjongRandomCarsEasy1 />} />
          <Route path="/mahjong-randomCars-easy-2" element={<MahjongRandomCarsEasy2 />} />
          <Route path="/mahjong-randomCars-easy-3" element={<MahjongRandomCarsEasy3 />} />
          <Route path="/mahjong-randomCars-medium-1" element={<MahjongRandomCarsMedium1 />} />
          <Route path="/mahjong-randomCars-medium-2" element={<MahjongRandomCarsMedium2 />} />
          <Route path="/mahjong-randomCars-medium-3" element={<MahjongRandomCarsMedium3 />} />
          <Route path="/mahjong-randomCars-hard-1" element={<MahjongRandomCarsHard1 />} />
          <Route path="/mahjong-randomCars-hard-2" element={<MahjongRandomCarsHard2 />} />
          <Route path="/mahjong-randomCars-hard-3" element={<MahjongRandomCarsHard3 />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;