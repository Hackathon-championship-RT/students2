import React from 'react';
import { useNavigate } from 'react-router-dom';

function YouLose() {
  const navigate = useNavigate();

  // Функция для перехода на главную страницу
  const goToHome = () => {
    navigate('/');
  };

  return (
    <div style={styles.container}>
      <div style={styles.content}>
        <h1 style={styles.title}>Вы проиграли!</h1>
        <p style={styles.message}>Не переживайте, попробуйте снова и сохраните свой прогресс!</p>
        <button style={styles.button} onClick={goToHome}>Вернуться на главную</button>
      </div>
    </div>
  );
}

// Стили для компонента
const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
  },
  content: {
    textAlign: 'center',
    backgroundColor: '#ffffff',
    padding: '30px',
    borderRadius: '10px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
  },
  title: {
    fontSize: '36px',
    fontWeight: 'bold',
    color: '#d9534f',
  },
  message: {
    fontSize: '18px',
    color: '#555',
    marginBottom: '20px',
  },
  button: {
    padding: '10px 20px',
    backgroundColor: '#5bc0de',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '16px',
    transition: 'background-color 0.3s',
  },
};

export default YouLose;