import React from 'react';
import './App.css';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Login from './components/Login/Login';
import BeneficiaryDashboard from './pages/BeneficiaryDashboard/BeneficiaryDashboard';
import NotFound from './pages/NotFound/NotFound';
import useToken from './hooks/useToken';
import Home from './pages/Home/Home';


function App() {
  const { token, setToken } = useToken();

  // TODO: handle token expiration
  if(!token) {
    return <Login setToken={setToken} />;
  }

  return (
    <div className="wrapper">
      <BrowserRouter>
        <Switch>
          <Route exact path='/'> 
            <Home />
          </Route>
          <Route exact path="/beneficiaries">
            <BeneficiaryDashboard />
          </Route>
          <Route path='*'>
            <NotFound/>
          </Route>
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;  