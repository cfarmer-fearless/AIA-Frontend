import React from "react";
import PropTypes from "prop-types";

import "./footer.css";

export const Footer = ({ text }) => (
  <footer className="footer-container">
    <div className="footer-container">
      {text}
    </div>
  </footer>
);

Footer.propTypes = {
  text: PropTypes.string,
};

Footer.defaultProps = {
  text: null,
};
