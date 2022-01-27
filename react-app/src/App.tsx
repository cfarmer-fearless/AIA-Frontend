import React from 'react';
import './App.css';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import NotFound from './pages/NotFound/NotFound';
import Home from './pages/Home/Home';
import { Header } from './components/Header/Header';
import { Footer } from './components/Footer/Footer';

function App() {
  return (
    <div className="wrapper">
      <Header title="AIA Tool" />
      <BrowserRouter>
        <Switch>
          <Route exact path="/">
            <Home />
          </Route>
          <Route path="*">
            <NotFound />
          </Route>
        </Switch>
      </BrowserRouter>
      <Footer text="AIA Tool" />
    </div>
  );
}

export default App;
