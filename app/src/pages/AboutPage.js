import React from "react";
import { Link } from "react-router-dom";

export default function AboutPage() {
  return (
    <div className="page">
      <header className="header">
        <h1>About This Project</h1>
      </header>

      <main className="app about-page">
        <section className="about-section">
          <p>
            <strong>NBA Magic 8 Ball</strong> was created by <strong>Agrim Jaimini</strong> using <strong>React</strong> on the frontend and a custom <strong>Natural Language Processing (NLP)</strong> model on the backend.
          </p>
          <p>
            The goal is to offer a fun, AI-powered experience for basketball fans — letting users ask any question and receive a predicted NBA player based on the language and semantics of the input.
          </p>
        </section>

        <section className="about-section">
          <h3>
            <span role="img" aria-label="warning">⚠️</span> Limitations & Accuracy
          </h3>
          <p>
            While the app is fun to use, the predictions may occasionally feel inaccurate or unexpected. This is primarily due to:
          </p>
          <ul className="about-list">
            <li>
              <span role="img" aria-label="brain">🧠</span> <strong>Model constraints:</strong> Trained on a small, manually curated dataset — not comprehensive.
            </li>
            <li>
              <span role="img" aria-label="laptop">💻</span> <strong>Limited hardware:</strong> Trained on a personal machine without access to high-performance GPUs or cloud compute.
            </li>
            <li>
              <span role="img" aria-label="calendar">📅</span> <strong>No real-time data:</strong> The model doesn’t reflect live games or stats.
            </li>
          </ul>
          <p>
            Despite these, it highlights what’s possible when creativity meets AI — and serves as a foundation for future, more advanced versions.
          </p>
        </section>

        <section className="about-section">
        <p>
  Want to try it out? Head back to the main app{" "}
  <span role="img" aria-label="down arrow">👇</span>
</p>
          <Link to="/" className="back-link">← Return to Home</Link>
        </section>
      </main>

      <footer>
        <p>
          Made by{" "}
          <a href="https://github.com/agrimjaimini" target="_blank" rel="noopener noreferrer">
            Agrim Jaimini
          </a>
        </p>
      </footer>
    </div>
  );
}
