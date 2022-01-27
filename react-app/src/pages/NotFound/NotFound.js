import React from 'react';
import { Link } from 'react-router-dom';

const NotFound = () => (
  <div>
    <h1>404 - Page Not Found!</h1>
    <p>
      <Link to="/">
        Go Home (Currently redirects to beneficiaries)
      </Link>
    </p>
  </div>
);

export default NotFound;
