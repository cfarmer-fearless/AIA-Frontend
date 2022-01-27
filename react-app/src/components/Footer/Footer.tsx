import React from 'react';

import './footer.css';

interface FooterProps {
  text: string;
}

export const Footer: React.FC<FooterProps> = ({ text }) => (
  <footer className="footer-container">
    <div className="footer-container">
      {text}
    </div>
  </footer>
);
