import React, { useState, useEffect } from "react";
import "./App.css";
import { Link } from "react-router-dom";


function HomePage() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("Ask Me Anything");
  const [isPlaceholder, setIsPlaceholder] = useState(true);
  const [isShaking, setIsShaking] = useState(false);
  const [headshot, setHeadshot] = useState("");

  useEffect(() => {
    setAnswer("Ask Me Anything");
    setIsPlaceholder(true);
  }, []);

  const handleShake = () => {
    if (!question.trim()) {
      setAnswer("Please ask a question!");
      setIsPlaceholder(false);
      setHeadshot("");
      return;
    }

    setAnswer("Shaking...");
    setIsPlaceholder(false);
    setIsShaking(true);

    setTimeout(() => {
      setIsShaking(false);
      fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: question }),
      })
        .then((response) => response.json())
        .then((data) => {
          setAnswer(`Player: ${data.name}\nScore: ${data.score}`);
          setHeadshot(data.headshot);
        })
        .catch((error) => {
          console.error("Error:", error);
          setAnswer("Error! Try again.");
        });
    }, 500);
  };

  return (
    <div className="page">
      <header>
        <div className="header">
          <img
            src="https://upload.wikimedia.org/wikipedia/en/thumb/0/03/National_Basketball_Association_logo.svg/800px-National_Basketball_Association_logo.svg.png"
            alt="NBA Logo"
            className="nba-logo"
          />
          <h1>NBA Magic 8 Ball</h1>
        </div>
      </header>

      <main className="app">
        <h2>Consult the Magic 8 Ball of the NBA world, powered by AI</h2>

        <div className={`magic8ball-container ${isShaking ? "shake" : ""}`}>
          <div className="answer-text">
            {isPlaceholder ? (
              <p className="placeholder">{answer}</p>
            ) : (
              answer.split("\n").map((line, index) => (
                <p key={index}>{line}</p>
              ))
            )}
          </div>
        </div>

        {headshot && (
          <div className="player-headshot">
            <img src={headshot} alt="Player Headshot" />
          </div>
        )}

        <div className="input-container">
          <input
            aria-label="Ask your question"
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Enter your question here"
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleShake();
              }
            }}
          />
          <button onClick={handleShake}>Shake</button>
        </div>
      </main>

      {/* 🔗 Social Media Icons directly above footer */}
      <div className="social-icons">
        <a
          href="https://instagram.com/agrimjaimini"
          target="_blank"
          rel="noopener noreferrer"
        >
          <i className="fab fa-instagram"></i>
        </a>
      </div>
      <div className="about-link">
  <Link to="/about">About this project</Link>
</div>

      <footer>
        <p>
          Made by{" "}
          <a
            href="https://github.com/agrimjaimini"
            target="_blank"
            rel="noopener noreferrer"
          >
            Agrim Jaimini
          </a>
        </p>
      </footer>
    </div>
  );
}

export default HomePage;