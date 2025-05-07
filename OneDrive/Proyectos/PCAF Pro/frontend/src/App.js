import React from 'react';
import { Switch, Route } from 'react-router-dom';
import LoginForm from './components/Auth/LoginForm';
import Dashboard from './components/Dashboard/Dashboard';

function App() {
  return (
    <div className="app">
      <Switch>
        <Route exact path="/" component={LoginForm} />
        <Route path="/dashboard" component={Dashboard} />
      </Switch>
    </div>
  );
}

export default App;