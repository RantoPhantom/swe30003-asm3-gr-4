import "./App.css";
import { useRef } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from "./pages/home";
import Header from "./components/header";
import Footer from "./components/footer";

const server = "http://127.0.0.1:8000/";

function App() {
  const react_feeling = useRef(false);
  fetch(server)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      react_feeling.current = data;
    });

  return (
    <Router>
      <div className="App mt-5">
        <Header />
        <Routes>
          <Route exact path="/" element={<Home />} />
          {/* Add more routes here as needed */}
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
