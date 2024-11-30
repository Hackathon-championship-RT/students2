import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import useSound from 'use-sound';
import matchSound from './sounds/1.mp3';
import './mahjong.css';

// Generation of cards
const generateCards = (layerIndex, gridSize) => {
  const totalCards = gridSize * gridSize;

  const images = require.context('./retro', false, /\.(jpg|jpeg|png)$/);
  const imageNames = images.keys();

  const selectedImages = imageNames
    .sort(() => Math.random() - 0.5)
    .slice(0, 4);

  const duplicates = totalCards / selectedImages.length;

  const allCards = selectedImages.flatMap(image => Array(duplicates).fill(image));

  const shuffledCards = allCards
    .map((image, index) => ({
      image: images(image),
      id: `${layerIndex}-${index}`,
      matched: false,
    }))
    .sort(() => Math.random() - 0.5);

  return shuffledCards;
};

// Generation of layers
const generateLayers = (numLayers, gridSize) => {
  const layers = [];
  for (let i = 0; i < numLayers; i++) {
    const layerCards = generateCards(i, gridSize);
    layers.push(layerCards);
  }
  return layers;
};

// Main function
const MahjongRetroCarsMedium1 = () => {
  const gridSize = 8;
  const numLayers = 2;
  const [layers, setLayers] = useState([]);
  const [selectedCards, setSelectedCards] = useState([]);
  const [highlightColor, setHighlightColor] = useState(null);
  const [gameStarted, setGameStarted] = useState(false);
  const [coins, setCoins] = useState(0);
  const navigate = useNavigate();

  // Checking if there're any coins in local storage, except 1st level in any difficulty
  useEffect(() => {
    setCoins(0);
  }, []);

  // Save coins to localStorage when they change
  useEffect(() => {
    if (coins > 0) {
      localStorage.setItem('coins', coins);
    }
  }, [coins]);

  // Function to check level completion
  const checkLevelCompletion = useCallback(() => {
    const allMatched = layers.every(layer =>
      layer.every(card => card.matched)
    );

    if (allMatched) {
      console.log('Отправляем монеты: ', coins);
      sendCoinsToServer(coins);
      navigate('/mahjong-retroCars-medium-2');
    }
  }, [layers, coins, navigate]);

  // Request to server
  const sendCoinsToServer = async (coins) => {
    console.log("Отправка монет началась", coins); // Log what it calls
    try {
      const token = localStorage.getItem("jwtToken");
      const response = await fetch('http://localhost:8080/records', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ "level": 1, "score": coins }),
      });
  
  
      if (!response.ok) {
        // If server returned an error
        throw new Error('Ошибка при отправке монет');
      }
  
      console.log('Монеты отправлены успешно');
    } catch (error) {
      console.log("Ошибка: ", error.message); // Logging an error
  
      if (error.message === 'Failed to fetch') {
        console.log("Сервер не найден");
      } else {
        alert('Ошибка');
      }
    }
  };

  useEffect(() => {
    const generatedLayers = generateLayers(numLayers, gridSize);
    setLayers(generatedLayers);
  }, [gridSize, numLayers]);

  // Checking if our card is free to choose (logic of majhong game)
  const isCardFree = (layerIndex, index) => {
    const layer = layers[layerIndex];
    const col = index % gridSize;

    const leftFree = col === 0 || layer[index - 1]?.matched;
    const rightFree = col === gridSize - 1 || layer[index + 1]?.matched;

    return leftFree || rightFree;
  };

  const handleCardClick = (layerIndex, id) => {
    const layer = layers[layerIndex];
    const cardIndex = layer.findIndex((card) => card.id === id);
    const card = layer[cardIndex];

    if (selectedCards.some((c) => c.id === id)) {
      const newSelectedCards = selectedCards.filter((c) => c.id !== id);
      setSelectedCards(newSelectedCards);
      return;
    }

    if (!isCardFree(layerIndex, cardIndex)) {
      console.log("Эта карточка заблокирована!");
      return;
    }

    if (card.matched || selectedCards.some((c) => c.id === id)) {
      console.log("Эта карточка уже выбрана или совпала!");
      return;
    }

    const newSelectedCards = [...selectedCards, card];
    setSelectedCards(newSelectedCards);

    if (!gameStarted) {
      setGameStarted(true);
    }

    if (newSelectedCards.length === 2) {
      checkMatch(newSelectedCards);
    }
  };

  const [palyMatchSound] = useSound(matchSound);

  const checkMatch = ([card1, card2]) => {
    if (card1.image === card2.image) {
      palyMatchSound();

      setHighlightColor('green');
      setLayers((prevLayers) => {
        const newLayers = prevLayers.map((layer) =>
          layer.map((card) =>
            card.id === card1.id || card.id === card2.id
              ? { ...card, matched: true }
              : card
          )
        );
        return newLayers;
      });

      // Increment coins when cards match
      setCoins(prevCoins => prevCoins + 5);
    } else {
      // Decrement coins when cards don't match
      setCoins(prevCoins => {
        const newCoins = prevCoins - 5;
        // Check if coins are less than 0
        if (newCoins < 0) {
          navigate('/YouLose'); // Redirect to YouLose page
        }
        return newCoins;
      });
      setHighlightColor('red');
    }

    setTimeout(() => {
      setSelectedCards([]);
      setHighlightColor(null);
    }, 500);
  };

  // mixing cards with layers
  const mixCards = () => {
    setLayers(prevLayers => prevLayers.map(layer => {
      const shuffledUnmatchedCards = layer.filter(card => !card.matched).sort(() => Math.random() - 0.5);

      const newLayer = [];
      let unmatchedIndex = 0;

      layer.forEach(card => {
        if (card.matched) {
          newLayer.push(card);
        } else {
          newLayer.push(shuffledUnmatchedCards[unmatchedIndex]);
          unmatchedIndex++;
        }
      });

      return newLayer;
    }));
  };

  useEffect(() => {
    if (gameStarted) {
      checkLevelCompletion();
    }
  }, [layers, gameStarted, checkLevelCompletion]);

  // the main calls
  return (
    <div>
      <div className="controls">
        <button className="mix-button" onClick={mixCards}>Mix</button>
        <div className="coins">Счёт: {coins}</div> {/* Display coins */}
      </div>

      <div className="mahjong-board">
        {layers.map((layer, layerIndex) => (
          <div
            key={layerIndex}
            className={`mahjong-layer ${layerIndex % 2 === 0 ? 'even-layer' : 'odd-layer'}`}
            style={{ gridTemplateColumns: `repeat(${gridSize}, 1fr)` }}
          >
            {layer.map((card, index) => (
              <div
                key={card.id}
                className={`card ${card.matched ? 'hidden' : ''} ${isCardFree(layerIndex, index) ? 'free' : ''} ${selectedCards.some((c) => c.id === card.id) ? 'selected' : ''} ${highlightColor ? `highlight-${highlightColor}` : ''}`}
                onClick={() => handleCardClick(layerIndex, card.id)}
              >
                {!card.matched && <img src={card.image} alt="card" />}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};

export default MahjongRetroCarsMedium1;