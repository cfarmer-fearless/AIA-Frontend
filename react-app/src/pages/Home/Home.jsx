import React from 'react';
import { Redirect } from 'react-router-dom';

export default function Home() {
  return (
    <div>
      <Redirect to='/beneficiaries'/>
      <div>Bank Home Page - redirecting to beneficiary dashboard</div>
    </div>
  );
}
